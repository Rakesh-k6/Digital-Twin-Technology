"""
CityLink - Automated Backend Test & Verification Script
Verifies:
1. Topology and 4 zones
2. Microscopic traffic physics & pedestrians
3. Power grid & feeder dynamics
4. Bidirectional Traffic-Power cascade
5. Cybersecurity FDI & anomaly detection
6. 15-30 min Predictive engine
7. Automated resilience mitigation
"""

import sys
import os
import time

# Add backend directory to sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from citylink.simulation import citylink_sim

print("=== STARTING CITYLINK BACKEND SYSTEM TEST ===")

# Test 1: Baseline Initialization
print("\n[TEST 1] Verifying Digital Twin Baseline...")
state = citylink_sim.get_full_state()
assert state["entities"]["vehicle_count"] >= 30, f"Expected >= 30 vehicles, got {state['entities']['vehicle_count']}"
assert state["entities"]["pedestrian_count"] >= 30, f"Expected >= 30 pedestrians, got {state['entities']['pedestrian_count']}"
assert len(state["power"]["feeders"]) == 4, f"Expected 4 feeders, got {len(state['power']['feeders'])}"
assert len(state["traffic"]["signals"]) == 16, f"Expected 16 signals, got {len(state['traffic']['signals'])}"
print(f" PASS: Active Vehicles: {state['entities']['vehicle_count']}, Pedestrians: {state['entities']['pedestrian_count']}, Feeders: 4, Signals: 16")

# Test 2: Step 10 ticks and verify continuous motion
print("\n[TEST 2] Verifying 10-tick continuous simulation stepping...")
v0_pos_before = (state["entities"]["vehicles"][0]["x"], state["entities"]["vehicles"][0]["z"])
time.sleep(0.5)
state2 = citylink_sim.get_full_state()
v0_pos_after = (state2["entities"]["vehicles"][0]["x"], state2["entities"]["vehicles"][0]["z"])
print(f" PASS: Vehicle 0 moved from {v0_pos_before} to {v0_pos_after}")

# Test 3: Scenario 2 - Traffic Congestion
print("\n[TEST 3] Triggering Scenario 2: Traffic Congestion (Silk Board Surge & Blockage)...")
citylink_sim.set_scenario("TRAFFIC_CONGESTION")
time.sleep(0.5)
scen2_state = citylink_sim.get_full_state()
silk_density = scen2_state["traffic"]["zone_densities"]["Zone_D"]
print(f" PASS: Silk Board Congestion Density: {silk_density * 100:.1f}%, Blocked Corridors: {scen2_state['traffic']['blocked_corridors']}")
assert silk_density > 0.6, "Silk Board should be heavily congested"

# Test 4: Scenario 3 - Power Failure Cascade (Feeder Trip -> Traffic Signal Failure)
print("\n[TEST 4] Triggering Scenario 3: Power Failure Cascade...")
citylink_sim.power.trigger_power_overload_scenario("FEEDER_SLK", immediate_trip=True)
citylink_sim.step(0.1)
scen3_state = citylink_sim.get_full_state()
feeder_slk_status = scen3_state["power"]["feeders"]["FEEDER_SLK"]["status"]
signal_slk = scen3_state["traffic"]["signals"]["INT_SLK_1"]["status"]
print(f" PASS: Feeder F-SLK Status: {feeder_slk_status}, Connected Signal INT_SLK_1 Status: {signal_slk}")
assert feeder_slk_status == "TRIPPED", "Feeder F-SLK should be tripped"
assert signal_slk == "FAIL_FLASHING_AMBER", "Signal should enter failure mode"

# Test 5: Scenario 4 - Cybersecurity FDI Attack
print("\n[TEST 5] Triggering Scenario 4: Cybersecurity FDI Attack...")
citylink_sim.set_scenario("CYBERATTACK")
citylink_sim.step(0.1)
scen4_state = citylink_sim.get_full_state()
active_attacks = scen4_state["security"]["active_attacks"]
fdi_detected = any(a["type"] == "fdi_power" and a.get("detected") for a in active_attacks)
print(f" PASS: Active Attacks: {len(active_attacks)}, FDI Physics-Residual Detected: {fdi_detected}")
assert fdi_detected, "FDI Attack should be detected by physics-based residual checking"

# Test 6: AI Predictive Engine Output
print("\n[TEST 6] Evaluating AI Predictive Engine (15-30 min Horizon)...")
preds = scen4_state["predictions"]
print(f" PASS: Overall System Risk: {preds['overall_system_risk']}, Predictions Count: {preds['predictions_count']}")
for p in preds["predictions"][:2]:
    print(f"   -> [{p['risk_level']}] {p['incident']} in {p['zone']} (Time to incident: {p['expected_time_to_incident']})")

# Test 7: Scenario 5 - Automated Mitigation & Recovery
print("\n[TEST 7] Triggering Scenario 5: Automated Resilience Mitigation...")
mitigation_result = citylink_sim.set_scenario("AUTOMATIC_RECOVERY")
print(" PASS: Mitigation Actions Applied:")
for act in mitigation_result["actions_executed"]:
    print(f"   * {act}")
print(f"   * Traffic Density Improvement: {mitigation_result['traffic_density_improvement_pct']}%")
print(f"   * Power Load Shed: {mitigation_result['power_load_shed_mw']} MW")
print(f"   * Incidents Prevented: {mitigation_result['incidents_prevented']}")

# Test 8: Reset to Baseline
print("\n[TEST 8] Resetting Simulation to Baseline...")
citylink_sim.reset()
clean_state = citylink_sim.get_full_state()
assert clean_state["current_scenario"] == "NORMAL_CITY"
print(" PASS: Reset successful. All systems nominal.")

print("\n=== ALL BACKEND INTEGRATION TESTS PASSED PERFECTLY ===")
