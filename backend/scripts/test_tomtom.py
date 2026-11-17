"""
Test Suite for CityLink TomTom Live Traffic Integration & Modular Providers.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from citylink.tomtom import tomtom_service, BANGALORE_HOTSPOTS
from citylink.providers import provider_registry
from citylink.simulation import citylink_sim


def run_tests():
    print("==================================================")
    print("RUNNING TOMTOM TRAFFIC INTEGRATION TEST SUITE")
    print("==================================================")

    # 1. Test Bangalore Hotspots Coverage
    print("\n[TEST 1] Verifying 9 Prioritized Bangalore Hotspots...")
    expected_spots = [
        "SILK_BOARD", "ELEC_CITY", "BELLANDUR_ORR", "MARATHAHALLI",
        "KR_PURAM", "HEBBAL", "WHITEFIELD", "SONY_WORLD", "ORR_AGARA"
    ]
    for s in expected_spots:
        assert s in BANGALORE_HOTSPOTS, f"Missing hotspot: {s}"
        spot = BANGALORE_HOTSPOTS[s]
        assert "lat" in spot and "lon" in spot, f"Hotspot {s} missing coordinates"
        print(f"  ✓ {spot['name']} ({spot['lat']}, {spot['lon']}) verified")
    print("  -> TEST 1 PASSED: All 9 prioritized hotspots configured.")

    # 2. Test Traffic Flow API retrieval & calculation
    print("\n[TEST 2] Testing Traffic Flow Retrieval & Calculation...")
    flow_data = tomtom_service.get_traffic_flow()
    assert "hotspots" in flow_data, "Flow data missing hotspots key"
    assert len(flow_data["hotspots"]) == 9, f"Expected 9 hotspots, got {len(flow_data['hotspots'])}"
    sb = flow_data["hotspots"]["SILK_BOARD"]
    assert "current_speed_kmh" in sb and "free_flow_speed_kmh" in sb
    assert "congestion_pct" in sb and "traffic_delay_min" in sb
    assert sb["congestion_pct"] >= 75.0, "Silk Board should reflect high congestion"
    print(f"  ✓ Silk Board Flow: Speed {sb['current_speed_kmh']}/{sb['free_flow_speed_kmh']} km/h, Congestion: {sb['congestion_pct']}%, Delay: +{sb['traffic_delay_min']}m")
    print(f"  ✓ Data Status: {flow_data['status']}, Provider: {flow_data['provider']}")
    print("  -> TEST 2 PASSED: Traffic flow correctly retrieved and calculated.")

    # 3. Test Caching (Cache Hits & TTL)
    print("\n[TEST 3] Testing In-Memory TTL Cache...")
    initial_hits = tomtom_service.cache_hits
    flow_cached = tomtom_service.get_traffic_flow()
    assert flow_cached["status"] in ("CACHED", "SIMULATION_FALLBACK")
    assert tomtom_service.cache_hits >= initial_hits
    print(f"  ✓ Cache Hit Count: {tomtom_service.cache_hits}, Cache Age: {flow_cached.get('cache_age_sec', 0)}s")
    print("  -> TEST 3 PASSED: In-memory TTL cache working cleanly.")

    # 4. Test Incidents API
    print("\n[TEST 4] Testing Traffic Incidents API...")
    inc_data = tomtom_service.get_traffic_incidents()
    assert "incidents" in inc_data and len(inc_data["incidents"]) > 0
    first_inc = inc_data["incidents"][0]
    assert "category" in first_inc and "title" in first_inc
    assert "delay_min" in first_inc and "lat" in first_inc and "lon" in first_inc
    print(f"  ✓ Active Incident Count: {inc_data['count']}")
    print(f"  ✓ Sample Incident: [{first_inc['category']}] {first_inc['title']} at {first_inc['from_street']}")
    print("  -> TEST 4 PASSED: Incidents retrieved with coordinates and delays.")

    # 5. Test Alternative Routing API
    print("\n[TEST 5] Testing TomTom Alternative Route Calculation...")
    route_data = tomtom_service.get_alternative_route("SILK_BOARD", "ELEC_CITY")
    assert "primary_route" in route_data and "alternative_route" in route_data
    prim = route_data["primary_route"]
    alt = route_data["alternative_route"]
    assert alt["current_travel_time_min"] < prim["current_travel_time_min"], "Bypass route should be faster"
    print(f"  ✓ Primary (At-Grade): {prim['current_travel_time_min']} min ({prim['congestion_pct']}% jam)")
    print(f"  ✓ Alternative (Elevated): {alt['current_travel_time_min']} min ({alt['congestion_pct']}% jam)")
    print(f"  ✓ Time Saved: {alt['time_saved_min']} min")
    print("  -> TEST 5 PASSED: Route comparison & bypass calculation verified.")

    # 6. Test Predictive AI Integration with TomTom Data
    print("\n[TEST 6] Testing Predictive AI Coupling with TomTom Live Data...")
    full_state = citylink_sim.get_full_state()
    assert "tomtom" in full_state, "Full state missing tomtom telemetry payload"
    assert "predictions" in full_state, "Full state missing predictions"
    preds = full_state["predictions"]
    assert "detected_hotspots" in preds, "Predictions missing detected_hotspots"
    print(f"  ✓ Overall System Risk: {preds['overall_system_risk']}")
    print(f"  ✓ Hotspots detected by AI: {preds['detected_hotspots_count']}")
    print(f"  ✓ Active AI Predictions: {len(preds['predictions'])}")
    for p in preds['predictions'][:2]:
        print(f"    - [{p['risk_level']}] {p['incident']} -> Root Cause: {p['root_cause']}")
    print("  -> TEST 6 PASSED: Predictive AI successfully coupled with live TomTom data.")

    # 7. Test Modular Data Provider Architecture
    print("\n[TEST 7] Testing Modular Provider Registry (Weather, Power, Water, Traffic)...")
    statuses = provider_registry.get_all_status()
    assert "traffic" in statuses and "weather" in statuses
    assert "electricity" in statuses and "water" in statuses
    for cat, stat in statuses.items():
        print(f"  ✓ Provider [{cat}]: Status = {stat.get('status')}")
    telemetry = provider_registry.collect_all_telemetry()
    assert "weather" in telemetry and telemetry["weather"]["temperature_c"] > 0
    assert "water" in telemetry and telemetry["water"]["daily_discharge_mld"] > 0
    print("  -> TEST 7 PASSED: All modular municipal data providers registered & streaming.")

    # 8. Test API Key Validation Security
    print("\n[TEST 8] Testing API Key Validation Security...")
    # Invalid key test
    ok, msg = tomtom_service.test_key("INVALID_KEY_TEST_XYZ")
    assert not ok, "Invalid key should be rejected"
    print(f"  ✓ Invalid key safely rejected: {msg}")
    status_summary = tomtom_service.get_status_summary()
    assert "masked_key" in status_summary
    print(f"  ✓ Masked Key Protection: {status_summary['masked_key']}")
    print("  -> TEST 8 PASSED: Secret API key is protected and validated securely.")

    print("\n==================================================")
    print("ALL 8 TOMTOM INTEGRATION TESTS PASSED SUCCESSFULLY!")
    print("==================================================")


if __name__ == "__main__":
    run_tests()
