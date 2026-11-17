"""
CityLink - Bangalore Water Supply & Sewerage Board (BWSSB) Utility Module
Simulates:
- Central Water Pumping Station (Cauvery Scheme 600 MLD)
- 4 Zonal Pump Houses & Reservoirs (Koramangala, HSR, Bellandur, Silk Board)
- Pressurized Transmission Mains (running alongside road networks)
- Water-Power-Traffic Interdependent Cascades:
  1. POWER -> WATER: Feeder trip kills pump house power, collapsing line pressure
  2. WATER -> TRAFFIC: Main pipe burst floods roadway, blocking lanes and stalling traffic
  3. TRAFFIC -> WATER/POWER: Gridlock delays utility emergency repair crews
"""

import time
from typing import Dict, Any, List, Optional


class WaterDistributionZone:
    """Represents a zonal water reservoir, pump house, pipeline network, and drainage chamber."""

    def __init__(self, zone_id: str, zone_name: str, pump_id: str, feeder_id: str,
                 nominal_pressure_bar: float, nominal_flow_mld: float):
        self.zone_id = zone_id
        self.zone_name = zone_name
        self.pump_id = pump_id
        self.feeder_id = feeder_id

        # Physical hydraulics
        self.nominal_pressure_bar = nominal_pressure_bar
        self.nominal_flow_mld = nominal_flow_mld
        self.current_pressure_bar = nominal_pressure_bar
        self.current_flow_mld = nominal_flow_mld
        self.reservoir_level_pct = 78.5  # Reservoir percentage
        self.pump_power_active = True
        self.pump_manual_enabled = True  # Manual operator pump switch
        self.pump_speed_rpm = 1450.0
        self.valve_open_pct = 100.0  # Sluice control valve (0 - 100%)

        # Stormwater drainage chamber & pipeline integrity
        self.chamber_level_pct = 28.0  # Stormwater/sewer chamber water level (0-100%)
        self.chamber_capacity_m3 = 1250.0
        self.chamber_surge_warning = False
        self.rainfall_mm_hr = 4.0  # Local rainfall rate in mm/h
        self.pipe_ruptured = False
        self.flood_severity_meters = 0.0  # Road flood depth (0 to 0.9m)
        self.water_quality_ph = 7.4
        self.status = "NORMAL"  # "NORMAL", "LOW_PRESSURE", "PIPE_BURST", "OUTAGE", "CHAMBER_SURGE", "CHAMBER_BURST"

    def set_valve(self, pct: float):
        """Sets sluice valve aperture percentage (0-100%)."""
        self.valve_open_pct = max(0.0, min(100.0, pct))

    def toggle_pump(self) -> bool:
        """Toggles manual pump state (ON/OFF)."""
        self.pump_manual_enabled = not self.pump_manual_enabled
        return self.pump_manual_enabled

    def update(self, dt: float, feeder_powered: bool, ambient_rain_mm: float = 0.0):
        self.pump_power_active = feeder_powered and self.pump_manual_enabled
        effective_rain = max(self.rainfall_mm_hr, ambient_rain_mm)

        # 1. Stormwater Chamber Dynamics
        if effective_rain > 45.0:
            # Heavy torrential rain rapidly fills drainage chamber
            fill_rate = (effective_rain - 30.0) * 0.45 * dt
            self.chamber_level_pct = min(100.0, self.chamber_level_pct + fill_rate)
            self.chamber_surge_warning = self.chamber_level_pct > 75.0

            # If chamber overflows (>92%) or rain >= 70 mm/hr, structural rupture occurs!
            if (self.chamber_level_pct >= 90.0 or effective_rain >= 70.0) and not self.pipe_ruptured:
                self.trigger_pipe_burst()
                self.status = "CHAMBER_BURST"
        else:
            # Gravity discharge / drainage pumps slowly drain chamber towards nominal (25-35%)
            if self.chamber_level_pct > 28.0:
                self.chamber_level_pct = max(28.0, self.chamber_level_pct - 2.5 * dt)
            self.chamber_surge_warning = False

        # 2. Pump & Feeder Power Failure
        if not feeder_powered or not self.pump_manual_enabled:
            # Power failure or manual pump shutoff -> pressure collapses
            self.pump_speed_rpm = max(0.0, self.pump_speed_rpm - 350.0 * dt)
            self.current_pressure_bar = max(0.2, self.current_pressure_bar - 0.8 * dt)
            self.current_flow_mld = max(0.0, self.current_flow_mld - 18.0 * dt)
            if self.status not in ("PIPE_BURST", "CHAMBER_BURST"):
                self.status = "OUTAGE" if self.current_pressure_bar < 1.0 else "LOW_PRESSURE"
            return

        # 3. Pipe Ruptured or Chamber Burst Condition
        if self.pipe_ruptured:
            self.current_pressure_bar = max(0.8, 1.2 * (self.valve_open_pct / 100.0))
            self.current_flow_mld = self.nominal_flow_mld * 1.5 * (self.valve_open_pct / 100.0)
            self.flood_severity_meters = min(0.75, self.flood_severity_meters + 0.04 * dt)
            self.reservoir_level_pct = max(10.0, self.reservoir_level_pct - 0.5 * dt)
            self.status = "CHAMBER_BURST" if self.chamber_level_pct > 80.0 else "PIPE_BURST"
            return

        # 4. Normal Hydrologic Equilibrium modulated by Sluice Valve
        target_pressure = self.nominal_pressure_bar * (self.valve_open_pct / 100.0)
        target_flow = self.nominal_flow_mld * (self.valve_open_pct / 100.0)

        if self.current_pressure_bar < target_pressure:
            self.current_pressure_bar = min(target_pressure, self.current_pressure_bar + 0.4 * dt)
        elif self.current_pressure_bar > target_pressure:
            self.current_pressure_bar = max(target_pressure, self.current_pressure_bar - 0.5 * dt)

        if self.current_flow_mld < target_flow:
            self.current_flow_mld = min(target_flow, self.current_flow_mld + 8.0 * dt)
        elif self.current_flow_mld > target_flow:
            self.current_flow_mld = max(target_flow, self.current_flow_mld - 10.0 * dt)

        if self.flood_severity_meters > 0.0:
            self.flood_severity_meters = max(0.0, self.flood_severity_meters - 0.08 * dt)

        self.pump_speed_rpm = 1450.0 * (self.valve_open_pct / 100.0)
        if self.valve_open_pct < 15.0:
            self.status = "VALVE_CLOSED"
        elif self.chamber_surge_warning:
            self.status = "CHAMBER_SURGE"
        else:
            self.status = "NORMAL"

    def trigger_pipe_burst(self):
        self.pipe_ruptured = True
        self.flood_severity_meters = max(self.flood_severity_meters, 0.48)
        self.status = "CHAMBER_BURST" if self.chamber_level_pct > 80.0 else "PIPE_BURST"

    def repair_pipe(self):
        self.pipe_ruptured = False
        self.flood_severity_meters = 0.0
        self.chamber_level_pct = 30.0
        self.chamber_surge_warning = False
        self.rainfall_mm_hr = 4.0
        self.status = "NORMAL"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "zone_id": self.zone_id,
            "zone_name": self.zone_name,
            "pump_id": self.pump_id,
            "feeder_id": self.feeder_id,
            "pressure_bar": round(self.current_pressure_bar, 2),
            "nominal_pressure_bar": self.nominal_pressure_bar,
            "flow_mld": round(self.current_flow_mld, 1),
            "valve_open_pct": round(self.valve_open_pct, 1),
            "reservoir_level_pct": round(self.reservoir_level_pct, 1),
            "chamber_level_pct": round(self.chamber_level_pct, 1),
            "chamber_surge_warning": self.chamber_surge_warning,
            "rainfall_mm_hr": round(self.rainfall_mm_hr, 1),
            "pump_powered": self.pump_power_active,
            "pump_manual_enabled": self.pump_manual_enabled,
            "pump_rpm": round(self.pump_speed_rpm, 0),
            "pipe_ruptured": self.pipe_ruptured,
            "flood_depth_m": round(self.flood_severity_meters, 2),
            "water_ph": self.water_quality_ph,
            "status": self.status
        }


class WaterSupplyManager:
    """Manages the municipal Cauvery water supply network for South Bangalore."""

    def __init__(self):
        self.central_treatment_plant = "BWSSB Cauvery Stage IV Treatment Plant (600 MLD)"
        self.ambient_rainfall_mm_hr = 4.0
        self.zones: Dict[str, WaterDistributionZone] = {
            "Zone_A": WaterDistributionZone("Zone_A", "Koramangala", "PUMP_KOR_GLR", "FEEDER_KOR", 4.2, 120.0),
            "Zone_B": WaterDistributionZone("Zone_B", "HSR Layout", "PUMP_HSR_SEC4", "FEEDER_HSR", 3.8, 95.0),
            "Zone_C": WaterDistributionZone("Zone_C", "Bellandur Ecospace", "PUMP_BEL_BOOSTER", "FEEDER_BEL", 4.5, 140.0),
            "Zone_D": WaterDistributionZone("Zone_D", "Silk Board Main", "PUMP_SLK_VALVE", "FEEDER_SLK", 4.0, 110.0)
        }

    def get_zone(self, zid: str) -> Optional[WaterDistributionZone]:
        """Resolves zone by ID, name, or pump ID."""
        if not zid:
            return None
        clean = zid.strip().upper()
        if clean in self.zones:
            return self.zones[clean]
        for z in self.zones.values():
            if z.zone_id.upper() == clean or z.zone_name.upper() == clean or z.pump_id.upper() == clean:
                return z
            # Check partial match like 'SILK BOARD' or 'KORAMANGALA'
            if clean in z.zone_name.upper() or clean in z.zone_id.upper():
                return z
        return None

    def update(self, dt: float, feeder_statuses: Dict[str, bool], ambient_rain_mm: float = 0.0):
        self.ambient_rainfall_mm_hr = ambient_rain_mm
        for z in self.zones.values():
            powered = feeder_statuses.get(z.feeder_id, True)
            z.update(dt, powered, ambient_rain_mm)

    def trigger_pipe_burst(self, zone_id: str = "Zone_D"):
        z = self.get_zone(zone_id)
        if z:
            z.trigger_pipe_burst()
        elif zone_id in self.zones:
            self.zones[zone_id].trigger_pipe_burst()

    def repair_pipe(self, zone_id: str):
        z = self.get_zone(zone_id)
        if z:
            z.repair_pipe()

    def repair_all_pipes(self):
        for z in self.zones.values():
            z.repair_pipe()

    def toggle_pump(self, zone_id: str) -> Dict[str, Any]:
        z = self.get_zone(zone_id)
        if not z:
            return {"status": "ERROR", "message": f"Zone or pump '{zone_id}' not found"}
        is_on = z.toggle_pump()
        return {
            "status": "SUCCESS",
            "zone_id": z.zone_id,
            "pump_id": z.pump_id,
            "pump_manual_enabled": is_on,
            "pump_powered": z.pump_power_active,
            "message": f"Pump {z.pump_id} turned {'ON' if is_on else 'OFF'}"
        }

    def set_valve(self, zone_id: str, open_pct: float) -> Dict[str, Any]:
        z = self.get_zone(zone_id)
        if not z:
            return {"status": "ERROR", "message": f"Zone '{zone_id}' not found"}
        z.set_valve(open_pct)
        return {
            "status": "SUCCESS",
            "zone_id": z.zone_id,
            "valve_open_pct": z.valve_open_pct,
            "message": f"Sluice valve for {z.zone_name} set to {z.valve_open_pct}%"
        }

    def set_rainfall(self, rainfall_mm_hr: float, zone_id: Optional[str] = None) -> Dict[str, Any]:
        self.ambient_rainfall_mm_hr = rainfall_mm_hr
        if zone_id:
            z = self.get_zone(zone_id)
            if z:
                z.rainfall_mm_hr = rainfall_mm_hr
        else:
            for z in self.zones.values():
                z.rainfall_mm_hr = rainfall_mm_hr
        return {
            "status": "SUCCESS",
            "rainfall_mm_hr": rainfall_mm_hr,
            "affected_zone": zone_id or "ALL"
        }

    def get_summary(self) -> Dict[str, Any]:
        total_flow = sum(z.current_flow_mld for z in self.zones.values())
        avg_pressure = sum(z.current_pressure_bar for z in self.zones.values()) / len(self.zones)
        active_bursts = sum(1 for z in self.zones.values() if z.pipe_ruptured)
        active_outages = sum(1 for z in self.zones.values() if z.status in ("OUTAGE", "LOW_PRESSURE"))
        chamber_surges = sum(1 for z in self.zones.values() if z.chamber_surge_warning or z.chamber_level_pct > 75.0)
        max_flood = max((z.flood_severity_meters for z in self.zones.values()), default=0.0)

        # Critical alert evaluation for high-sound alarm
        critical_condition = active_bursts > 0 or chamber_surges > 0 or max_flood > 0.25

        return {
            "treatment_plant": self.central_treatment_plant,
            "ambient_rainfall_mm_hr": round(self.ambient_rainfall_mm_hr, 1),
            "total_flow_mld": round(total_flow, 1),
            "average_pressure_bar": round(avg_pressure, 2),
            "active_bursts_count": active_bursts,
            "outage_count": active_outages,
            "chamber_surges_count": chamber_surges,
            "max_flood_depth_m": round(max_flood, 2),
            "critical_condition": critical_condition,
            "zones": {zid: z.to_dict() for zid, z in self.zones.items()}
        }
