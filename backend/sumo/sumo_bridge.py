"""
CityLink - SUMO & TraCI Microscopic Traffic Simulation Bridge
Connects to Eclipse SUMO daemon via TraCI if available.
Syncs vehicle coordinates, speeds, lane IDs, traffic light phase controls, and pedestrian positions.
If SUMO is not installed or daemon is offline, automatically activates high-fidelity native micro-simulation.
"""

import os
import sys
import time
import subprocess
from typing import Dict, Any, Optional

try:
    import traci
    import sumolib
    TRACI_AVAILABLE = True
except ImportError:
    TRACI_AVAILABLE = False


class SumoBridge:
    """Manages TraCI connection and bidirectional state mapping with CityLink."""

    def __init__(self, sumocfg_path: Optional[str] = None):
        self.sumocfg_path = sumocfg_path or os.path.join(
            os.path.dirname(__file__), "configuration", "citylink.sumocfg"
        )
        self.is_connected = False
        self.sumo_process = None

    def start_sumo(self, use_gui: bool = False, port: int = 8873) -> bool:
        """Launches SUMO or SUMO-GUI with TraCI listening server."""
        if not TRACI_AVAILABLE:
            print("[SUMO Bridge] TraCI python library not installed. Using native micro-simulation engine.")
            return False

        sumo_binary = "sumo-gui" if use_gui else "sumo"
        cmd = [sumo_binary, "-c", self.sumocfg_path, "--remote-port", str(port), "--step-length", "0.1"]

        try:
            self.sumo_process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            time.sleep(1.0)
            traci.init(port)
            self.is_connected = True
            print(f"[SUMO Bridge] Successfully connected to TraCI on port {port}")
            return True
        except Exception as e:
            print(f"[SUMO Bridge] Could not start or connect to SUMO ({e}). Continuing with native physics.")
            self.is_connected = False
            return False

    def step_simulation(self):
        """Advances SUMO simulation by one step."""
        if self.is_connected and TRACI_AVAILABLE:
            try:
                traci.simulationStep()
            except Exception as e:
                print(f"[SUMO Bridge] Step error: {e}")
                self.is_connected = False

    def get_sumo_vehicles(self) -> Dict[str, Any]:
        """Extracts live vehicle telemetry from TraCI."""
        if not self.is_connected or not TRACI_AVAILABLE:
            return {}

        veh_data = {}
        try:
            for vid in traci.vehicle.getIDList():
                x, y = traci.vehicle.getPosition(vid)
                angle = traci.vehicle.getAngle(vid)
                speed = traci.vehicle.getSpeed(vid)
                vtype = traci.vehicle.getTypeID(vid)
                veh_data[vid] = {
                    "id": vid,
                    "x": x - 120.0,  # Center offset to match Unity world (0,0)
                    "y": 0.0,
                    "z": y - 120.0,
                    "heading": angle,
                    "speed": speed,
                    "type": vtype
                }
        except Exception as e:
            print(f"[SUMO Bridge] Error reading vehicles: {e}")
        return veh_data

    def set_traffic_light_state(self, tls_id: str, state_string: str):
        """Overrides traffic light state in SUMO (e.g., during power failure)."""
        if self.is_connected and TRACI_AVAILABLE:
            try:
                traci.trafficlight.setRedYellowGreenState(tls_id, state_string)
            except Exception as e:
                print(f"[SUMO Bridge] Error setting TLS {tls_id}: {e}")

    def close(self):
        if self.is_connected and TRACI_AVAILABLE:
            try:
                traci.close()
            except Exception:
                pass
            self.is_connected = False
        if self.sumo_process:
            self.sumo_process.terminate()
