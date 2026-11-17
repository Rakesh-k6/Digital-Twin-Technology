"""
CityLink - REST API Routes
Provides endpoints for Traffic, Electricity (BESCOM), Water Supply (BWSSB),
Cybersecurity, Scenarios, and Mitigation.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional

from citylink.simulation import citylink_sim
from citylink.tomtom import tomtom_service, BANGALORE_HOTSPOTS
from citylink.providers import provider_registry
from citylink.ai_model import cascade_ml_predictor
from citylink.auth import auth_manager, LoginCredentials

router = APIRouter()


class SpeedRequest(BaseModel):
    speed: float


class CyberAttackRequest(BaseModel):
    attack_type: str  # "fdi_power", "traffic_sensor_spoof", "signal_tampering"
    target_id: str
    spoof_value: Optional[float] = None


class WaterBurstRequest(BaseModel):
    zone_id: str = "Zone_D"


class ValveRequest(BaseModel):
    open_pct: float


class RainfallRequest(BaseModel):
    rainfall_mm_hr: float
    zone_id: Optional[str] = None


class TomTomConfigRequest(BaseModel):
    api_key: str
    persist: bool = True


@router.get("/status")
def get_status() -> Dict[str, Any]:
    return citylink_sim.get_full_state()


@router.post("/scenario/{scenario_name}")
def set_scenario(scenario_name: str) -> Dict[str, Any]:
    return citylink_sim.set_scenario(scenario_name)


@router.post("/mitigation/apply")
def apply_mitigation() -> Dict[str, Any]:
    return citylink_sim.apply_mitigation()


@router.post("/water/burst")
def trigger_water_burst(req: WaterBurstRequest) -> Dict[str, Any]:
    """Simulates a major pressurized pipeline burst creating road flooding & low line pressure."""
    citylink_sim.water.trigger_pipe_burst(req.zone_id)
    citylink_sim.traffic.create_road_blockage(f"FLOOD_{req.zone_id}_PIPELINE_BURST")
    return {"status": "PIPE_BURST_TRIGGERED", "zone": req.zone_id, "details": "800mm main ruptured, road flooded"}


@router.post("/water/repair")
def repair_water_pipes() -> Dict[str, Any]:
    citylink_sim.water.repair_all_pipes()
    citylink_sim.traffic.clear_road_blockages()
    return {"status": "PIPES_REPAIRED", "message": "Line pressure restored to 4.2 bar"}


# ==============================================================================
# ELECTRICAL GRID (BESCOM) BREAKER ON / OFF HARDWARE TELEMETRY CONTROLS
# ==============================================================================

@router.post("/power/feeder/{feeder_id}/toggle")
def toggle_feeder_breaker(feeder_id: str) -> Dict[str, Any]:
    """Physically toggles the high-voltage distribution feeder circuit breaker."""
    res = citylink_sim.toggle_feeder(feeder_id)
    if res.get("status") == "ERROR":
        raise HTTPException(status_code=404, detail=res.get("message"))
    return res


@router.post("/power/feeder/{feeder_id}/trip")
def trip_feeder_breaker(feeder_id: str) -> Dict[str, Any]:
    """Manually trips the circuit breaker open, dropping feeder load to 0 MW."""
    f = citylink_sim.power.get_feeder(feeder_id)
    if not f:
        raise HTTPException(status_code=404, detail=f"Feeder {feeder_id} not found")
    f.breaker_closed = False
    f.status = "TRIPPED"
    f.physical_load_mw = 0.0
    f.telemetry_load_mw = 0.0
    for sig in citylink_sim.traffic.signals.values():
        if sig.zone_id == f.zone_id:
            sig.power_active = False
    return {"status": "SUCCESS", "action": "TRIPPED", "feeder_id": f.feeder_id, "breaker_closed": False}


@router.post("/power/feeder/{feeder_id}/close")
def close_feeder_breaker(feeder_id: str) -> Dict[str, Any]:
    """Closes and energizes the circuit breaker, restoring electrical service."""
    f = citylink_sim.power.get_feeder(feeder_id)
    if not f:
        raise HTTPException(status_code=404, detail=f"Feeder {feeder_id} not found")
    f.reset_breaker()
    for sig in citylink_sim.traffic.signals.values():
        if sig.zone_id == f.zone_id:
            sig.power_active = True
    return {"status": "SUCCESS", "action": "CLOSED", "feeder_id": f.feeder_id, "breaker_closed": True}


# ==============================================================================
# WATER UTILITY (BWSSB) PUMP, SLUICE VALVE & CHAMBER CONTROLS
# ==============================================================================

@router.post("/water/pump/{zone_id}/toggle")
def toggle_water_pump(zone_id: str) -> Dict[str, Any]:
    """Toggles water pumping station motor ON or OFF."""
    res = citylink_sim.toggle_water_pump(zone_id)
    if res.get("status") == "ERROR":
        raise HTTPException(status_code=404, detail=res.get("message"))
    return res


@router.post("/water/valve/{zone_id}")
def set_water_valve(zone_id: str, req: ValveRequest) -> Dict[str, Any]:
    """Adjusts motorized sluice valve aperture percentage (0% closed to 100% full open)."""
    res = citylink_sim.set_water_valve(zone_id, req.open_pct)
    if res.get("status") == "ERROR":
        raise HTTPException(status_code=404, detail=res.get("message"))
    return res


# ==============================================================================
# WEATHER SENSING & HEAVY RAIN CHAMBER CONTROLS
# ==============================================================================

@router.post("/weather/rain")
def set_weather_rain(req: RainfallRequest) -> Dict[str, Any]:
    """
    Sets real-time rainfall rate (mm/h).
    If rainfall > 45 mm/h: Stormwater chambers surge and backpressure warning triggers.
    If rainfall >= 70 mm/h: Causes structural pipeline failure & street flash flooding.
    """
    res = citylink_sim.set_rainfall(req.rainfall_mm_hr, req.zone_id)
    return {
        "status": "SUCCESS",
        "rainfall_mm_hr": req.rainfall_mm_hr,
        "zone_id": req.zone_id or "ALL",
        "storm_active": citylink_sim.weather.get("storm_active", False),
        "emergency_alarm": citylink_sim.emergency_alarm
    }


@router.get("/weather/status")
def get_weather_status() -> Dict[str, Any]:
    return citylink_sim.weather


@router.get("/alarm/status")
def get_alarm_status() -> Dict[str, Any]:
    """Returns central SCADA high-sound emergency alarm state."""
    return citylink_sim.emergency_alarm


@router.post("/cyber/inject")
def inject_cyberattack(req: CyberAttackRequest) -> Dict[str, Any]:
    if req.attack_type == "fdi_power":
        if req.target_id in citylink_sim.power.feeders:
            val = req.spoof_value if req.spoof_value is not None else 5.2
            citylink_sim.power.feeders[req.target_id].inject_fdi_attack(val)
            citylink_sim.security.inject_attack("fdi_power", req.target_id, val)
            return {"status": "INJECTED", "details": f"FDI injected on {req.target_id} reporting {val} MW"}
    elif req.attack_type == "traffic_sensor_spoof":
        val = req.spoof_value if req.spoof_value is not None else 0.12
        citylink_sim.security.inject_attack("traffic_sensor_spoof", req.target_id, val)
        return {"status": "INJECTED", "details": f"Sensor spoof injected on {req.target_id} reporting {val*100}%"}
    elif req.attack_type == "signal_tampering":
        if req.target_id in citylink_sim.traffic.signals:
            citylink_sim.traffic.signals[req.target_id].cyber_tampered = True
            citylink_sim.security.inject_attack("signal_tampering", req.target_id)
            return {"status": "INJECTED", "details": f"Signal tampering injected on {req.target_id}"}

    raise HTTPException(status_code=400, detail="Invalid attack type or target asset")


@router.post("/cyber/clear")
def clear_cyberattacks() -> Dict[str, Any]:
    citylink_sim.security.clear_attacks()
    for f in citylink_sim.power.feeders.values():
        f.clear_fdi_attack()
    for s in citylink_sim.traffic.signals.values():
        s.cyber_tampered = False
    return {"status": "CLEARED", "message": "All cyberattacks neutralized and telemetry resynchronized."}


@router.post("/control/pause")
def pause_sim() -> Dict[str, Any]:
    citylink_sim.is_paused = True
    return {"status": "PAUSED"}


@router.post("/control/resume")
def resume_sim() -> Dict[str, Any]:
    citylink_sim.is_paused = False
    return {"status": "RESUMED"}


@router.post("/control/speed")
def set_speed(req: SpeedRequest) -> Dict[str, Any]:
    if req.speed < 0.1 or req.speed > 10.0:
        raise HTTPException(status_code=400, detail="Speed must be between 0.1 and 10.0")
    citylink_sim.sim_speed = req.speed
    return {"status": "SPEED_UPDATED", "speed": citylink_sim.sim_speed}


@router.post("/reset")
def reset_sim() -> Dict[str, Any]:
    citylink_sim.reset()
    return {"status": "RESET", "message": "Simulation restored to baseline initialization"}


@router.get("/unity/config")
def get_unity_config() -> Dict[str, Any]:
    return {
        "world_size": 360.0,
        "zones": [
            {"id": "Zone_A", "name": "Koramangala", "center": [-90.0, 0.0, 90.0], "feeder": "BESCOM_F_KOR"},
            {"id": "Zone_B", "name": "HSR Layout", "center": [90.0, 0.0, 90.0], "feeder": "BESCOM_F_HSR"},
            {"id": "Zone_C", "name": "Bellandur", "center": [90.0, 0.0, -90.0], "feeder": "BESCOM_F_BEL"},
            {"id": "Zone_D", "name": "Silk Board", "center": [-90.0, 0.0, -90.0], "feeder": "BESCOM_F_SLK"},
        ],
        "water_pumps": [z.to_dict() for z in citylink_sim.water.zones.values()],
        "intersections": [s.to_dict() for s in citylink_sim.traffic.signals.values()],
        "feeders": [f.to_dict() for f in citylink_sim.power.feeders.values()]
    }


# ==============================================================================
# TOMTOM LIVE TRAFFIC API & MODULAR PROVIDER ROUTES
# ==============================================================================

@router.get("/tomtom/live")
def get_tomtom_live() -> Dict[str, Any]:
    """Retrieves full TomTom traffic flow, incidents, and routing for Bangalore."""
    flow = tomtom_service.get_traffic_flow()
    incidents = tomtom_service.get_traffic_incidents()
    routing = tomtom_service.get_alternative_route()
    status = tomtom_service.get_status_summary()

    return {
        "status": status.get("status", "SIMULATION_FALLBACK"),
        "service_summary": status,
        "flow": flow,
        "incidents": incidents,
        "routing": routing
    }


@router.get("/tomtom/incidents")
def get_tomtom_incidents() -> Dict[str, Any]:
    """Retrieves real-time accidents, road closures, and traffic incidents in Bangalore."""
    return tomtom_service.get_traffic_incidents()


@router.get("/tomtom/flow/{hotspot_id}")
def get_tomtom_hotspot_flow(hotspot_id: str) -> Dict[str, Any]:
    """Retrieves flow segment data for a specific Bangalore hotspot."""
    hid = hotspot_id.upper()
    if hid not in BANGALORE_HOTSPOTS:
        raise HTTPException(
            status_code=404,
            detail=f"Hotspot {hotspot_id} not found. Available: {list(BANGALORE_HOTSPOTS.keys())}"
        )
    return tomtom_service.get_traffic_flow(hotspot_id=hid)


@router.get("/tomtom/route")
def get_tomtom_route(origin: str = "SILK_BOARD", dest: str = "ELEC_CITY") -> Dict[str, Any]:
    """Calculates primary and alternative bypass routes with travel times and delays."""
    return tomtom_service.get_alternative_route(origin=origin, dest=dest)


@router.post("/tomtom/config")
def configure_tomtom_key(req: TomTomConfigRequest) -> Dict[str, Any]:
    """
    Securely validates and configures the TomTom API key in the backend.
    The key is tested against TomTom before saving, and is never returned in frontend logs.
    """
    success, msg = tomtom_service.set_api_key(req.api_key, persist_to_env=req.persist)
    if not success:
        raise HTTPException(status_code=400, detail=msg)
    return {
        "status": "CONFIGURED",
        "message": msg,
        "summary": tomtom_service.get_status_summary()
    }


@router.get("/tomtom/status")
def get_tomtom_status() -> Dict[str, Any]:
    """Returns connectivity, rate-limit, and cache status of TomTom service."""
    return tomtom_service.get_status_summary()


@router.get("/providers/status")
def get_all_providers_status() -> Dict[str, Any]:
    """Returns data lineage, source types, and connectivity of all infrastructure providers."""
    return provider_registry.get_all_status()


@router.get("/providers/telemetry")
def get_all_providers_telemetry() -> Dict[str, Any]:
    """Aggregates telemetry across traffic, weather, electricity, and water providers."""
    return provider_registry.collect_all_telemetry()


# ==============================================================================
# AUTHENTICATION & RBAC OPERATOR GATEWAY
# ==============================================================================

class QuickLoginRequest(BaseModel):
    role: str  # "operator", "csoc_sec", "admin"


@router.post("/auth/login")
def login(creds: LoginCredentials) -> Dict[str, Any]:
    session = auth_manager.authenticate(creds.username, creds.password)
    if not session:
        raise HTTPException(status_code=401, detail="Invalid username or password. Check demo credentials.")
    return {"status": "AUTHENTICATED", "session": session}


@router.post("/auth/quick-login")
def quick_login(req: QuickLoginRequest) -> Dict[str, Any]:
    session = auth_manager.quick_login(req.role)
    if not session:
        raise HTTPException(status_code=400, detail=f"Role '{req.role}' not recognized. Use 'operator', 'csoc_sec', or 'admin'.")
    return {"status": "AUTHENTICATED", "session": session}


@router.get("/auth/me")
def get_current_user(token: Optional[str] = None) -> Dict[str, Any]:
    if not token:
        # Default fallback to operator for convenience
        default_session = auth_manager.quick_login("operator")
        return {"authenticated": True, "user": default_session["user"], "token": default_session["token"]}
    user = auth_manager.verify_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Session expired or invalid")
    return {"authenticated": True, "user": user}


@router.post("/auth/logout")
def logout(token: Optional[str] = None) -> Dict[str, Any]:
    if token:
        auth_manager.revoke_session(token)
    return {"status": "LOGGED_OUT", "message": "Operator session terminated."}


# ==============================================================================
# REAL AI MACHINE LEARNING MODEL PREDICTION ENDPOINTS
# ==============================================================================

class AIInferenceRequest(BaseModel):
    traffic_density: float = 0.55
    avg_speed_kmh: float = 25.0
    rainfall_mm: float = 5.0
    ev_charging_demand_mw: float = 4.5
    pipeline_burst_active: bool = False
    fdi_residual_mw: float = 0.0


@router.post("/ai/predict")
def run_ai_prediction(req: AIInferenceRequest) -> Dict[str, Any]:
    """Runs inference through the trained Deep Ensemble Neural Multi-Head Regressor."""
    return cascade_ml_predictor.predict(
        traffic_density=req.traffic_density,
        avg_speed_kmh=req.avg_speed_kmh,
        rainfall_mm=req.rainfall_mm,
        ev_charging_demand_mw=req.ev_charging_demand_mw,
        pipeline_burst_active=req.pipeline_burst_active,
        fdi_residual_mw=req.fdi_residual_mw
    )


@router.get("/ai/live-inference")
def get_live_ai_inference() -> Dict[str, Any]:
    """
    Ingests real-world live data automatically from TomTom Traffic API (speed, congestion %,
    delays, and incidents across Bangalore hotspots) and executes live AI inference.
    """
    state = citylink_sim.get_full_state()
    # Check if simulation already computed it
    if "ai_prediction" in state:
        return state["ai_prediction"]

    tomtom_data = state.get("tomtom", {})
    power = state.get("power", {})
    water = state.get("water", {})

    return cascade_ml_predictor.predict_from_tomtom(
        tomtom_data=tomtom_data,
        feeders_state=power.get("feeders", {}),
        water_state=water,
        rainfall_mm=6.5
    )


@router.get("/ai/model-info")
def get_ai_model_info() -> Dict[str, Any]:
    """Returns AI model architecture, metrics, and Gini feature importances."""
    return {
        "status": "ONLINE",
        "model_version": cascade_ml_predictor.model_version,
        "algorithm": "Deep Ensemble Neural Multi-Head Regressor (NumPy-Vectorized)",
        "training_samples": cascade_ml_predictor.training_samples,
        "r2_score": cascade_ml_predictor.r2_score,
        "mean_squared_error": cascade_ml_predictor.mean_squared_error,
        "feature_names": cascade_ml_predictor.feature_names,
        "base_feature_importances": cascade_ml_predictor.base_feature_importances
    }


# ==============================================================================
# CYBER SECURITY OPERATIONS CENTER (CSOC) COMMAND ROUTES
# ==============================================================================

@router.get("/security/status")
def get_security_status() -> Dict[str, Any]:
    """Returns CSOC threat level, residual checks, and incident logs."""
    return citylink_sim.security.get_status()


@router.post("/security/purge-attack")
def purge_cyber_attack() -> Dict[str, Any]:
    """Neutralizes active cyberattacks, rolls keys, and restores verified telemetry."""
    citylink_sim.security.clear_attacks()
    for f in citylink_sim.power.feeders.values():
        f.clear_fdi_attack()
    for s in citylink_sim.traffic.signals.values():
        s.cyber_tampered = False
    return {
        "status": "NEUTRALIZED",
        "threat_level": "NOMINAL",
        "message": "FDI and spoofing vectors eliminated. SCADA telemetry resynchronized with hardware physics estimator."
    }


