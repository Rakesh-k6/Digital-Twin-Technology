"""
CityLink - Master Cyber-Physical Simulation Coordinator
Orchestrates the Tri-Infrastructure Nexus:
1. Traffic Management (Vehicles, Signals, Flyovers, Queues)
2. BESCOM Electrical Grid (Substation, 4 Feeders, Breaker Trips, FDI)
3. BWSSB Water Supply Network (Pumps, Pressurized Pipelines, Burst Flooding)
Cross-Domain Cascade Feedback Loops:
- Power -> Water: Feeder trip kills pump house power -> line pressure collapses
- Water -> Traffic: Pipe burst causes street flash flooding -> lane closures & gridlock
- Traffic -> Power: Severe congestion & EV queues trigger feeder overload
- Power -> Traffic: Feeder trip switches traffic lights to fail-safe flashing amber
"""

import time
import threading
from typing import Dict, Any, List, Optional

from .graph import InfrastructureTopology
from .power import PowerGridManager
from .traffic import TrafficSimulationManager
from .water import WaterSupplyManager
from .security import CyberSecurityEngine
from .prediction import CascadePredictor
from .optimizer import ResilienceOptimizer
from .tomtom import tomtom_service
from .ai_model import cascade_ml_predictor


class CityLinkSimulation:
    """Master simulation runtime."""

    def __init__(self):
        self.lock = threading.Lock()
        self.topology = InfrastructureTopology()
        self.power = PowerGridManager()
        self.traffic = TrafficSimulationManager()
        self.water = WaterSupplyManager()
        self.security = CyberSecurityEngine()
        self.predictor = CascadePredictor(horizon_minutes=20)
        self.optimizer = ResilienceOptimizer()

        self.running = True
        self.is_paused = False
        self.sim_speed = 1.0
        self.current_scenario = "NORMAL_CITY"
        self.sim_time = 0.0
        self.step_dt = 0.1

        # Real-time weather & atmospheric sensor integration
        self.weather = {
            "rainfall_mm_hr": 4.0,
            "zone_id": "ALL",
            "storm_active": False,
            "temperature_c": 24.5,
            "humidity_pct": 72.0
        }

        # Central SCADA & Physical Critical Condition / Emergency Alarm state
        self.emergency_alarm = {
            "active": False,
            "alarm_type": "NONE",  # UNAUTHORIZED_CYBER_ATTACK, FEEDER_BREAKER_TRIP, WATER_MAIN_RUPTURE, HEAVY_RAIN_CHAMBER_SURGE
            "severity": "NORMAL",  # NORMAL, WARNING, CRITICAL
            "headline": "All Systems Nominal",
            "affected_zone": "None",
            "timestamp": time.time()
        }

        self.worker_thread = threading.Thread(target=self._run_loop, daemon=True)
        self.worker_thread.start()

    def _run_loop(self):
        last_t = time.time()
        while self.running:
            now = time.time()
            elapsed = now - last_t
            target_interval = 0.1 / max(0.1, self.sim_speed)

            if elapsed >= target_interval:
                last_t = now
                if not self.is_paused:
                    self.step(self.step_dt)
            else:
                time.sleep(max(0.005, target_interval - elapsed))

    def step(self, dt: float):
        with self.lock:
            self.sim_time += dt

            # 1. Update Power Grid using Traffic Densities & EV loads
            zone_metrics = {
                zid: {
                    "density": dens,
                    "ev_count": sum(1 for v in self.traffic.vehicles.values() if v.origin_zone == zid and v.veh_type == "car")
                }
                for zid, dens in self.traffic.zone_densities.items()
            }
            self.power.update_grid(zone_metrics, dt, self.sim_time)

            # 2. Extract Feeder Statuses for Traffic Signals AND Water Pumps
            feeder_statuses = {fid: f.breaker_closed for fid, f in self.power.feeders.items()}

            # 3. Step Water Network (Power -> Water coupling & Heavy Rain Chamber Dynamics)
            self.water.update(dt, feeder_statuses, ambient_rain_mm=self.weather.get("rainfall_mm_hr", 4.0))

            # 4. Check Water Burst Flooding -> Traffic lane blockage (Water -> Traffic coupling)
            for zid, wz in self.water.zones.items():
                if wz.pipe_ruptured and wz.flood_severity_meters > 0.2:
                    self.traffic.create_road_blockage(f"FLOOD_{zid}_PIPELINE_BURST")
                    # Slow down vehicles in flooded zone
                    for veh in self.traffic.vehicles.values():
                        if veh.current_zone == zid:
                            veh.speed = min(veh.speed, 2.0)
                            veh.in_queue = True

            # 5. Step Traffic Engine (Power -> Traffic coupling)
            self.traffic.update(dt, feeder_statuses)

            # 6. Cybersecurity Telemetry Evaluation
            feeders_dict = {fid: f.to_dict() for fid, f in self.power.feeders.items()}
            signals_dict = {sid: s.to_dict() for sid, s in self.traffic.signals.items()}
            traffic_summary = self.traffic.get_summary()
            self.security.evaluate_telemetry(feeders_dict, traffic_summary, signals_dict)

            # 7. Step Predictive Engine
            feeder_loads = {fid: f.physical_load_mw for fid, f in self.power.feeders.items()}
            self.predictor.record_step(self.sim_time, feeder_loads, self.traffic.zone_densities)

            # 8. Real-time SCADA Physical Safety & Unauthorized Intrusion Alarm Engine
            has_cyber = (len(self.security.active_attacks) > 0) or any(f.fdi_attacked for f in self.power.feeders.values())
            tripped_feeders = [fid for fid, f in self.power.feeders.items() if not f.breaker_closed]
            burst_zones = [zid for zid, z in self.water.zones.items() if z.pipe_ruptured]
            surge_zones = [zid for zid, z in self.water.zones.items() if z.chamber_surge_warning or z.chamber_level_pct > 75.0]
            rain_mm = self.weather.get("rainfall_mm_hr", 4.0)

            if has_cyber:
                self.emergency_alarm = {
                    "active": True,
                    "alarm_type": "UNAUTHORIZED_CYBER_ATTACK",
                    "severity": "CRITICAL",
                    "headline": "UNAUTHORIZED SCADA INTRUSION DETECTED (FDI / TELEMETRY SPOOFING)",
                    "affected_zone": "Silk Board Substation 66kV",
                    "timestamp": time.time()
                }
            elif surge_zones or (rain_mm >= 50.0 and burst_zones):
                self.emergency_alarm = {
                    "active": True,
                    "alarm_type": "HEAVY_RAIN_CHAMBER_SURGE",
                    "severity": "CRITICAL",
                    "headline": f"TORRENTIAL RAIN ({rain_mm:.1f} mm/h) - DRAINAGE CHAMBER SURCHARGE & RUPTURE RISK",
                    "affected_zone": ", ".join(surge_zones or burst_zones or ["Silk Board"]),
                    "timestamp": time.time()
                }
            elif tripped_feeders:
                self.emergency_alarm = {
                    "active": True,
                    "alarm_type": "FEEDER_BREAKER_TRIP",
                    "severity": "CRITICAL",
                    "headline": f"GRID CRITICAL: FEEDER CIRCUIT BREAKER OPEN ({', '.join(tripped_feeders)})",
                    "affected_zone": ", ".join(tripped_feeders),
                    "timestamp": time.time()
                }
            elif burst_zones:
                self.emergency_alarm = {
                    "active": True,
                    "alarm_type": "WATER_MAIN_RUPTURE",
                    "severity": "CRITICAL",
                    "headline": f"HYDRAULIC FAILURE: 800mm WATER MAIN RUPTURED ({', '.join(burst_zones)})",
                    "affected_zone": ", ".join(burst_zones),
                    "timestamp": time.time()
                }
            else:
                self.emergency_alarm = {
                    "active": False,
                    "alarm_type": "NONE",
                    "severity": "NORMAL",
                    "headline": "All Municipal Infrastructure Systems Nominal",
                    "affected_zone": "None",
                    "timestamp": time.time()
                }

    def set_scenario(self, scenario_name: str) -> Dict[str, Any]:
        """Switches between the official hackathon scenarios."""
        with self.lock:
            name = scenario_name.upper().strip()
            self.current_scenario = name

            if name == "NORMAL_CITY" or name == "SCENARIO_1":
                self.current_scenario = "NORMAL_CITY"
                self.power.reset_all_feeders()
                self.water.repair_all_pipes()
                self.traffic.clear_road_blockages()
                self.traffic.spillover_active = False
                self.traffic.zone_densities = {"Zone_A": 0.24, "Zone_B": 0.22, "Zone_C": 0.32, "Zone_D": 0.35}
                self.security.clear_attacks()
                self.weather = {
                    "rainfall_mm_hr": 4.0,
                    "zone_id": "ALL",
                    "storm_active": False,
                    "temperature_c": 24.5,
                    "humidity_pct": 72.0
                }
                self.water.set_rainfall(4.0)

            elif name == "TRAFFIC_CONGESTION" or name == "SCENARIO_2":
                self.current_scenario = "TRAFFIC_CONGESTION"
                self.traffic.spawn_congestion_vehicles(target_zone="Zone_D", count=24)
                self.traffic.create_road_blockage("INT_SLK_2_TO_INT_BEL_1")
                for veh in self.traffic.vehicles.values():
                    if veh.origin_zone == "Zone_D":
                        veh.speed = 0.0
                        veh.in_queue = True
                self.traffic.zone_densities["Zone_D"] = 0.88
                self.traffic.spillover_active = True

            elif name == "POWER_FAILURE" or name == "SCENARIO_3":
                self.current_scenario = "POWER_FAILURE"
                # Overload Silk Board Feeder causing breaker trip -> Traffic blackout & Water pump stall
                self.power.trigger_power_overload_scenario("FEEDER_SLK", immediate_trip=True)

            elif name == "WATER_BURST" or name == "WATER_MAIN_BURST":
                self.current_scenario = "WATER_BURST"
                # 800mm Water Main bursts under Silk Board / Outer Ring Road -> Flash flood & lane closures
                self.water.trigger_pipe_burst("Zone_D")
                self.traffic.create_road_blockage("FLOOD_Zone_D_PIPELINE_BURST")
                self.traffic.zone_densities["Zone_D"] = 0.82

            elif name == "CYBERATTACK" or name == "SCENARIO_4":
                self.current_scenario = "CYBERATTACK"
                f = self.power.feeders["FEEDER_SLK"]
                f.breaker_closed = True
                f.status = "OVERLOADED"
                f.base_load_mw = 16.5
                f.physical_load_mw = 16.5
                f.inject_fdi_attack(spoofed_load_mw=5.8)
                self.security.inject_attack("fdi_power", "FEEDER_SLK", spoof_value=5.8)

            elif name == "AUTOMATIC_RECOVERY" or name == "SCENARIO_5":
                self.current_scenario = "AUTOMATIC_RECOVERY"
                self.water.repair_all_pipes()
                return self.optimizer.apply_mitigation(self.traffic, self.power, self.security)

            elif name == "HEAVY_RAIN_STORM" or name == "TORRENTIAL_RAIN" or name == "SCENARIO_6":
                self.current_scenario = "HEAVY_RAIN_STORM"
                self.weather = {
                    "rainfall_mm_hr": 86.0,
                    "zone_id": "Zone_D",
                    "storm_active": True,
                    "temperature_c": 19.8,
                    "humidity_pct": 98.0
                }
                # Severe downpour causes chamber backpressure surcharge & structural pipe blowout
                self.water.set_rainfall(86.0, "Zone_D")
                z = self.water.get_zone("Zone_D")
                if z:
                    z.chamber_level_pct = 96.0
                    z.chamber_surge_warning = True
                    z.trigger_pipe_burst()
                self.traffic.create_road_blockage("FLOOD_Zone_D_PIPELINE_BURST")
                self.traffic.zone_densities["Zone_D"] = 0.92
                for veh in self.traffic.vehicles.values():
                    if veh.current_zone == "Zone_D":
                        veh.speed = 1.0
                        veh.in_queue = True

            return {"scenario": self.current_scenario, "status": "ACTIVATED"}

    def toggle_feeder(self, feeder_id: str) -> Dict[str, Any]:
        """Toggles feeder breaker state physically (Trip / Close)."""
        with self.lock:
            res = self.power.toggle_breaker(feeder_id)
            # If feeder was tripped, switch connected traffic signals and cut pump
            f = self.power.get_feeder(feeder_id)
            if f and not f.breaker_closed:
                for sig in self.traffic.signals.values():
                    if sig.zone_id == f.zone_id:
                        sig.power_active = False
            elif f and f.breaker_closed:
                for sig in self.traffic.signals.values():
                    if sig.zone_id == f.zone_id:
                        sig.power_active = True
            return res

    def toggle_water_pump(self, zone_id: str) -> Dict[str, Any]:
        with self.lock:
            return self.water.toggle_pump(zone_id)

    def set_water_valve(self, zone_id: str, open_pct: float) -> Dict[str, Any]:
        with self.lock:
            return self.water.set_valve(zone_id, open_pct)

    def set_rainfall(self, rainfall_mm_hr: float, zone_id: Optional[str] = None) -> Dict[str, Any]:
        with self.lock:
            self.weather["rainfall_mm_hr"] = rainfall_mm_hr
            self.weather["storm_active"] = rainfall_mm_hr > 40.0
            if zone_id:
                self.weather["zone_id"] = zone_id
            return self.water.set_rainfall(rainfall_mm_hr, zone_id)

    def apply_mitigation(self) -> Dict[str, Any]:
        with self.lock:
            self.water.repair_all_pipes()
            self.weather = {
                "rainfall_mm_hr": 4.0,
                "zone_id": "ALL",
                "storm_active": False,
                "temperature_c": 24.5,
                "humidity_pct": 72.0
            }
            self.water.set_rainfall(4.0)
            return self.optimizer.apply_mitigation(self.traffic, self.power, self.security)

    def reset(self):
        with self.lock:
            self.power.reset_all_feeders()
            self.water.repair_all_pipes()
            self.traffic = TrafficSimulationManager()
            self.security = CyberSecurityEngine()
            self.predictor = CascadePredictor(horizon_minutes=20)
            self.optimizer = ResilienceOptimizer()
            self.weather = {
                "rainfall_mm_hr": 4.0,
                "zone_id": "ALL",
                "storm_active": False,
                "temperature_c": 24.5,
                "humidity_pct": 72.0
            }
            self.water.set_rainfall(4.0)
            self.current_scenario = "NORMAL_CITY"
            self.sim_time = 0.0

    def get_full_state(self) -> Dict[str, Any]:
        with self.lock:
            power_summary = self.power.get_summary()
            traffic_summary = self.traffic.get_summary()
            water_summary = self.water.get_summary()
            security_summary = self.security.get_status()

            # Ingest live TomTom traffic flow, incidents, and routing
            tomtom_flow = tomtom_service.get_traffic_flow()
            tomtom_incidents = tomtom_service.get_traffic_incidents()
            tomtom_routing = tomtom_service.get_alternative_route()
            tomtom_data = {
                "flow": tomtom_flow,
                "incidents": tomtom_incidents,
                "routing": tomtom_routing,
                "service_status": tomtom_service.get_status_summary()
            }

            predictions = self.predictor.predict_cascade(
                power_summary["feeders"],
                traffic_summary,
                security_summary,
                tomtom_live_data=tomtom_data
            )
            optimizer_summary = self.optimizer.get_summary()

            # Automatic real-time AI ML inference directly on live TomTom API data & weather
            ai_prediction = cascade_ml_predictor.predict_from_tomtom(
                tomtom_data=tomtom_data,
                feeders_state=power_summary.get("feeders", {}),
                water_state=water_summary,
                rainfall_mm=self.weather.get("rainfall_mm_hr", 4.0)
            )

            vehicles_payload = [v.to_dict() for v in self.traffic.vehicles.values()]
            pedestrians_payload = [p.to_dict() for p in self.traffic.pedestrians.values()]

            return {
                "sim_time": round(self.sim_time, 1),
                "is_paused": self.is_paused,
                "sim_speed": self.sim_speed,
                "current_scenario": self.current_scenario,
                "weather": self.weather,
                "emergency_alarm": self.emergency_alarm,
                "power": power_summary,
                "traffic": traffic_summary,
                "water": water_summary,
                "security": security_summary,
                "tomtom": tomtom_data,
                "predictions": predictions,
                "ai_prediction": ai_prediction,
                "optimizer": optimizer_summary,
                "entities": {
                    "vehicle_count": len(vehicles_payload),
                    "pedestrian_count": len(pedestrians_payload),
                    "vehicles": vehicles_payload,
                    "pedestrians": pedestrians_payload
                }
            }


citylink_sim = CityLinkSimulation()
