"""
CityLink - Power Distribution Infrastructure Module
Simulates:
- 66kV/11kV Substation and 4 Radial Feeders
- Dynamic Load Aggregation: Base Load + EV Fast Charging + Streetlights/Signals + Traffic Idling Grid Coupling
- Overload Timing & Circuit Breaker Tripping
- Telemetry vs True Physical State (Enabling FDI cyberattack modeling)
"""

import time
from typing import Dict, Any, List, Optional


class DistributionFeeder:
    """Represents an 11kV Radial Distribution Feeder feeding a city zone."""

    def __init__(self, feeder_id: str, zone_id: str, zone_name: str, capacity_mw: float, base_load_mw: float):
        self.feeder_id = feeder_id
        self.zone_id = zone_id
        self.zone_name = zone_name
        self.capacity_mw = capacity_mw
        self.base_load_mw = base_load_mw

        # Dynamic load additions
        self.ev_charging_mw = 0.8
        self.auxiliary_load_mw = 0.5
        self.traffic_idling_stress_mw = 0.0

        # Physical status
        self.physical_load_mw = base_load_mw + self.ev_charging_mw + self.auxiliary_load_mw
        self.status = "NORMAL"  # "NORMAL", "WARNING", "OVERLOADED", "TRIPPED"
        self.breaker_closed = True
        self.overload_start_time: float | None = None
        self.trip_delay_seconds = 6.0  # Tripping threshold under sustained overload

        # Cyber Telemetry (can be compromised via FDI attack)
        self.telemetry_load_mw = self.physical_load_mw
        self.telemetry_status = self.status
        self.fdi_attacked = False

    def update_load(self, active_evs: int, congestion_density: float, dt: float, current_sim_time: float):
        """
        Calculates dynamic feeder load based on physical traffic conditions and EV queue.
        TRAFFIC -> POWER coupling:
        - Higher congestion -> higher idle energy, emergency lighting, HVAC draw
        - Queued EVs at charging hub consume 60kW to 150kW each
        """
        if not self.breaker_closed:
            self.physical_load_mw = 0.0
            self.status = "TRIPPED"
            if not self.fdi_attacked:
                self.telemetry_load_mw = 0.0
                self.telemetry_status = "TRIPPED"
            return

        # EV Fast Charging load: base EV load + 0.12 MW per actively charging vehicle
        ev_mw = (active_evs * 0.12)
        self.ev_charging_mw = max(0.4, min(ev_mw, 6.0))

        # Congestion stress coupling: idling vehicles in commercial zones cause local grid HVAC/cooling load spikes
        # (models real urban heat island & commercial cooling draw correlated with massive gridlock)
        self.traffic_idling_stress_mw = congestion_density * 3.5

        # Total Physical Load
        self.physical_load_mw = round(
            self.base_load_mw + self.ev_charging_mw + self.auxiliary_load_mw + self.traffic_idling_stress_mw, 2
        )

        # Check overload limits
        loading_pct = (self.physical_load_mw / self.capacity_mw) * 100.0

        if loading_pct >= 100.0:
            self.status = "OVERLOADED"
            if self.overload_start_time is None:
                self.overload_start_time = current_sim_time
            elif (current_sim_time - self.overload_start_time) >= self.trip_delay_seconds:
                # Protective breaker trip!
                self.breaker_closed = False
                self.status = "TRIPPED"
                self.physical_load_mw = 0.0
        elif loading_pct >= 85.0:
            self.status = "WARNING"
            self.overload_start_time = None
        else:
            self.status = "NORMAL"
            self.overload_start_time = None

        # Telemetry update
        if not self.fdi_attacked:
            self.telemetry_load_mw = self.physical_load_mw
            self.telemetry_status = self.status

    def inject_fdi_attack(self, spoofed_load_mw: float):
        """Attacker overrides SCADA telemetry to report safe reading while physical feeder is overloaded."""
        self.fdi_attacked = True
        self.telemetry_load_mw = spoofed_load_mw
        self.telemetry_status = "NORMAL"

    def clear_fdi_attack(self):
        self.fdi_attacked = False
        self.telemetry_load_mw = self.physical_load_mw
        self.telemetry_status = self.status

    def reset_breaker(self):
        """Restores breaker after fault clearance."""
        self.breaker_closed = True
        self.overload_start_time = None
        self.status = "NORMAL"
        self.physical_load_mw = self.base_load_mw + 0.8
        self.telemetry_load_mw = self.physical_load_mw
        self.telemetry_status = "NORMAL"
        self.fdi_attacked = False

    def to_dict(self) -> Dict[str, Any]:
        loading_pct = 0.0 if not self.breaker_closed else round((self.physical_load_mw / self.capacity_mw) * 100.0, 1)
        overload_countdown = 0.0
        if self.overload_start_time is not None and self.status == "OVERLOADED":
            overload_countdown = max(0.0, round(self.trip_delay_seconds - (time.time() - self.overload_start_time), 1))

        return {
            "feeder_id": self.feeder_id,
            "zone_id": self.zone_id,
            "zone_name": self.zone_name,
            "capacity_mw": self.capacity_mw,
            "physical_load_mw": self.physical_load_mw,
            "telemetry_load_mw": self.telemetry_load_mw,
            "loading_percentage": loading_pct,
            "status": self.status,
            "telemetry_status": self.telemetry_status,
            "breaker_closed": self.breaker_closed,
            "fdi_attacked": self.fdi_attacked,
            "ev_charging_mw": round(self.ev_charging_mw, 2),
            "traffic_stress_mw": round(self.traffic_idling_stress_mw, 2),
            "trip_countdown_sec": overload_countdown
        }


class PowerGridManager:
    """Manages the municipal substation and 4 zonal feeders."""

    def __init__(self):
        self.substation_name = "Substation Central 66/11kV"
        self.feeders: Dict[str, DistributionFeeder] = {
            "FEEDER_KOR": DistributionFeeder("FEEDER_KOR", "Zone_A", "Koramangala", capacity_mw=15.0, base_load_mw=8.5),
            "FEEDER_HSR": DistributionFeeder("FEEDER_HSR", "Zone_B", "HSR Layout", capacity_mw=12.5, base_load_mw=7.2),
            "FEEDER_BEL": DistributionFeeder("FEEDER_BEL", "Zone_C", "Bellandur", capacity_mw=18.0, base_load_mw=11.5),
            "FEEDER_SLK": DistributionFeeder("FEEDER_SLK", "Zone_D", "Silk Board", capacity_mw=14.0, base_load_mw=9.0)
        }

    def update_grid(self, zone_metrics: Dict[str, Dict[str, Any]], dt: float, current_sim_time: float):
        for feeder in self.feeders.values():
            z_data = zone_metrics.get(feeder.zone_id, {})
            active_evs = z_data.get("ev_count", 8)
            congestion_density = z_data.get("density", 0.3)
            feeder.update_load(active_evs, congestion_density, dt, current_sim_time)

    def get_feeder(self, fid: str) -> Optional[DistributionFeeder]:
        """Resolves feeder by ID or alias (e.g. BESCOM_F_SLK, FEEDER_SLK, Zone_D)."""
        if not fid:
            return None
        clean = fid.strip().upper()
        norm = clean.replace("BESCOM_F_", "FEEDER_").replace("BESCOM_", "")
        if norm in self.feeders:
            return self.feeders[norm]
        if clean in self.feeders:
            return self.feeders[clean]
        for f in self.feeders.values():
            if f.zone_id.upper() == clean or f.zone_name.upper() == clean or f.feeder_id.upper() == clean:
                return f
        return None

    def toggle_breaker(self, fid: str) -> Dict[str, Any]:
        """Physically toggles feeder circuit breaker and returns updated state."""
        f = self.get_feeder(fid)
        if not f:
            return {"status": "ERROR", "message": f"Feeder {fid} not found"}

        if f.breaker_closed:
            # Trip the breaker!
            f.breaker_closed = False
            f.status = "TRIPPED"
            f.physical_load_mw = 0.0
            f.telemetry_load_mw = 0.0
            action = "TRIPPED"
        else:
            # Re-close and energize the breaker!
            f.reset_breaker()
            action = "CLOSED"

        return {
            "status": "SUCCESS",
            "action": action,
            "feeder_id": f.feeder_id,
            "zone_id": f.zone_id,
            "zone_name": f.zone_name,
            "breaker_closed": f.breaker_closed,
            "physical_load_mw": f.physical_load_mw,
            "feeder_status": f.status
        }

    def trigger_power_overload_scenario(self, target_feeder: str = "FEEDER_SLK", immediate_trip: bool = False):
        """Forces an extreme EV and industrial load spike in a specific feeder."""
        if target_feeder in self.feeders:
            f = self.feeders[target_feeder]
            f.base_load_mw = f.capacity_mw * 1.25  # 125% severe overload
            f.status = "OVERLOADED"
            if immediate_trip:
                f.breaker_closed = False
                f.status = "TRIPPED"
                f.physical_load_mw = 0.0
            else:
                f.overload_start_time = -10.0  # Expire trip delay so it trips on next step cycle

    def reset_all_feeders(self):
        base_loads = {
            "FEEDER_KOR": 8.5,
            "FEEDER_HSR": 7.2,
            "FEEDER_BEL": 11.5,
            "FEEDER_SLK": 9.0
        }
        for fid, f in self.feeders.items():
            f.base_load_mw = base_loads[fid]
            f.reset_breaker()

    def get_summary(self) -> Dict[str, Any]:
        total_physical_mw = sum(f.physical_load_mw for f in self.feeders.values())
        total_telemetry_mw = sum(f.telemetry_load_mw for f in self.feeders.values())
        total_capacity = sum(f.capacity_mw for f in self.feeders.values())
        tripped_count = sum(1 for f in self.feeders.values() if not f.breaker_closed)

        return {
            "substation": self.substation_name,
            "total_physical_mw": round(total_physical_mw, 2),
            "total_telemetry_mw": round(total_telemetry_mw, 2),
            "total_capacity_mw": round(total_capacity, 2),
            "tripped_feeders_count": tripped_count,
            "feeders": {fid: f.to_dict() for fid, f in self.feeders.items()}
        }
