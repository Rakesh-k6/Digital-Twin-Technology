"""
CityLink - Cybersecurity & Cyber-Physical Anomaly Detection Engine
Implements:
1. False Data Injection (FDI) on Electrical Feeder SCADA Telemetry
2. Traffic Loop Detector / Camera Density Spoofing
3. Unauthorized Traffic Signal Timing Tampering
4. Physics-Based State Estimation & Residual Anomaly Detector:
   |y_telemetry - y_physics_estimated| > threshold
5. Cyber Security Operations Center (CSOC) Incident Logging & Metrics
"""

import time
import math
from typing import Dict, List, Any


class CyberSecurityEngine:
    """Detects FDI, sensor spoofing, and actuation tampering in smart city infrastructure."""

    def __init__(self):
        # Attack States
        self.active_attacks: Dict[str, Dict[str, Any]] = {}
        self.incident_log: List[Dict[str, Any]] = []

        # Physics-based detector thresholds
        self.fdi_power_residual_threshold = 2.5  # MW deviation threshold
        self.sensor_density_residual_threshold = 0.25  # 25% discrepancy
        self.signal_timing_deviation_threshold = 12.0  # seconds

        # Detection metrics
        self.alerts_generated = 0
        self.mitigated_incidents = 0

    def inject_attack(self, attack_type: str, target_id: str, spoof_value: float | None = None) -> Dict[str, Any]:
        """
        attack_type: 'fdi_power', 'traffic_sensor_spoof', 'signal_tampering'
        """
        attack_meta = {
            "attack_id": f"ATK_{int(time.time() * 1000) % 100000}",
            "type": attack_type,
            "target": target_id,
            "timestamp": time.time(),
            "spoof_value": spoof_value,
            "detected": False,
            "status": "ACTIVE"
        }
        self.active_attacks[attack_type] = attack_meta

        # Add event to incident log
        self._log_event(
            severity="HIGH" if attack_type == "fdi_power" else "CRITICAL",
            title=f"Hostile Anomaly Injected: {attack_type.upper()}",
            target=target_id,
            details=f"Adversary injected manipulated payload into asset '{target_id}' with spoof parameter {spoof_value}."
        )
        return attack_meta

    def clear_attacks(self):
        self.active_attacks.clear()
        self._log_event(
            severity="INFO",
            title="Cyber Defenses Applied: Attacks Neutralized",
            target="ALL_SYSTEMS",
            details="All sensor streams resynchronized with cryptographic trust anchor and verified ground truth."
        )

    def evaluate_telemetry(
        self,
        feeder_dict: Dict[str, Any],
        traffic_summary: Dict[str, Any],
        signals_dict: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Evaluates physical consistency against cyber telemetry at 10Hz.
        Generates security alerts when physics conservation is breached.
        """
        detected_alerts = []

        # 1. Evaluate Power Grid FDI (Physical Load vs SCADA Telemetry)
        for fid, f in feeder_dict.items():
            physical_mw = f.get("physical_load_mw", 0.0)
            telemetry_mw = f.get("telemetry_load_mw", 0.0)
            residual = abs(physical_mw - telemetry_mw)

            if residual > self.fdi_power_residual_threshold and f.get("status") != "TRIPPED":
                alert = {
                    "alert_id": f"ALT_FDI_{fid}",
                    "type": "FALSE_DATA_INJECTION",
                    "severity": "CRITICAL",
                    "asset": fid,
                    "zone": f.get("zone_name"),
                    "physical_ground_truth": f"{physical_mw} MW",
                    "manipulated_telemetry": f"{telemetry_mw} MW",
                    "residual_mw": round(residual, 2),
                    "message": (
                        f"CRITICAL FDI DETECTED on {fid}: SCADA telemetry reports {telemetry_mw} MW "
                        f"while physical transformer state is {physical_mw} MW! Possible blinding attack before breaker trip."
                    ),
                    "recommended_action": "Switch SCADA to Fallback Physics State Estimator and isolate telemetry gateway."
                }
                detected_alerts.append(alert)

                if "fdi_power" in self.active_attacks:
                    self.active_attacks["fdi_power"]["detected"] = True

        # 2. Evaluate Traffic Sensor Spoofing (Reported vs True Vehicle Counts)
        if "traffic_sensor_spoof" in self.active_attacks:
            target_zone = self.active_attacks["traffic_sensor_spoof"]["target"]
            reported_density = self.active_attacks["traffic_sensor_spoof"].get("spoof_value", 0.1)
            actual_density = traffic_summary.get("zone_densities", {}).get(target_zone, 0.4)
            density_diff = abs(actual_density - reported_density)

            if density_diff > self.sensor_density_residual_threshold:
                alert = {
                    "alert_id": f"ALT_SPOOF_{target_zone}",
                    "type": "TRAFFIC_SENSOR_SPOOFING",
                    "severity": "HIGH",
                    "asset": f"CAMERA_RADAR_{target_zone}",
                    "zone": target_zone,
                    "physical_ground_truth": f"{round(actual_density * 100, 1)}% density",
                    "manipulated_telemetry": f"{round(reported_density * 100, 1)}% density",
                    "residual": round(density_diff, 3),
                    "message": (
                        f"Sensor spoofing detected in {target_zone}: Video/loop sensors report low density "
                        f"({round(reported_density * 100, 1)}%) while camera flow conservation indicates severe queue buildup ({round(actual_density * 100, 1)}%)."
                    ),
                    "recommended_action": "Verify with connected emergency vehicle GPS and override signal plans."
                }
                detected_alerts.append(alert)
                self.active_attacks["traffic_sensor_spoof"]["detected"] = True

        # 3. Evaluate Signal Timing Manipulation
        for sid, s in signals_dict.items():
            if s.get("cyber_tampered"):
                alert = {
                    "alert_id": f"ALT_SIG_{sid}",
                    "type": "SIGNAL_ACTUATION_TAMPERING",
                    "severity": "CRITICAL",
                    "asset": sid,
                    "zone": s.get("zone_id"),
                    "message": f"Unauthorized signal plan override detected on intersection {sid}. Forced red phase inducing artificial bottleneck.",
                    "recommended_action": "Force local fail-safe flashing amber and revert to local edge schedule."
                }
                detected_alerts.append(alert)
                if "signal_tampering" in self.active_attacks:
                    self.active_attacks["signal_tampering"]["detected"] = True

        # Update log if newly detected
        for a in detected_alerts:
            # Avoid spamming duplicates in incident log
            existing = any(item.get("alert_id") == a["alert_id"] for item in self.incident_log[-10:])
            if not existing:
                self.alerts_generated += 1
                self._log_event(
                    severity=a["severity"],
                    title=f"SECURITY ALERT: {a['type']}",
                    target=a["asset"],
                    details=a["message"]
                )

        return detected_alerts

    def _log_event(self, severity: str, title: str, target: str, details: str):
        self.incident_log.append({
            "timestamp": time.strftime("%H:%M:%S"),
            "severity": severity,
            "title": title,
            "target": target,
            "details": details
        })
        # Keep log bounded
        if len(self.incident_log) > 60:
            self.incident_log.pop(0)

    def get_status(self) -> Dict[str, Any]:
        return {
            "active_attacks_count": len(self.active_attacks),
            "active_attacks": list(self.active_attacks.values()),
            "total_alerts_generated": self.alerts_generated,
            "system_threat_level": "ELEVATED" if len(self.active_attacks) > 0 else "NOMINAL",
            "incident_log": self.incident_log[-20:]  # Return most recent 20
        }
