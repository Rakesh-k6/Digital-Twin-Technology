# CityLink – Cyber-Physical Digital Twin of Interdependent Urban Infrastructure

> **Realistic 3D Cyber-Physical Digital Twin of Bangalore** co-simulating microscopic transportation physics, TomTom Traffic Live API streams, BESCOM power distribution, BWSSB Cauvery water networks, stormwater drainage chamber surge dynamics, cybersecurity FDI anomaly detection, and AI cascade prediction with automated mitigation.

---

## 🏙️ Architecture Overview

```
                         [ 3D Bangalore Digital Twin & Glassmorphic Dashboard ] (Port 8000)
                                      ▲
                                      │ WebSocket / REST (10Hz Stream)
                                      ▼
[ TomTom Traffic Live API ] ◄───► [ FastAPI Coordinator ] ◄───► [ Web Audio Siren Synthesizer ]
  (Flow & Incidents Radar)              (Port 8000)                   (880Hz / 660Hz Industrial Klaxon)
                                      ▲
           ┌──────────────────────────┼──────────────────────────┬──────────────────────────┐
           ▼                          ▼                          ▼                          ▼
   [ Power Grid (BESCOM) ]     [ Traffic Engine ]        [ Water Utility (BWSSB) ]  [ Cybersecurity SOC ]
(66kV/11kV Feeders & Breakers) (Vehicles, Pedestrians)   (Pumps, Sluice Valves,      (Physics Residual FDI
                                                          Stormwater Chambers)        Anomaly Detection)
           │                          │                          │                          │
           └──────────────────────────┴──────────────────────────┴──────────────────────────┘
                                      ▼
                      [ AI Cascade Predictive Engine ]
                    (NumPy-Vectorized Deep ML Regressor)
                                      ▼
                     [ Resilience Optimizer Mitigation ]
                       (Signal Split, EV Curtailment)
```

---

## ⚡ Quick Start Instructions

### Prerequisites
- Python 3.10+
- Modern Web Browser (Chrome, Edge, Firefox)

### Step 1: Install Python Dependencies
```bash
pip install fastapi uvicorn websockets pydantic numpy requests
```

### Step 2: Configure Environment
Copy `.env.example` to `.env` and set your TomTom API key (optional — includes robust built-in cached and fallback telemetry):
```bash
cp .env.example .env
```

### Step 3: Run the Complete Digital Twin
```bash
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```
Open **[http://localhost:8000/](http://localhost:8000/)** in your browser to experience the live 3D Digital Twin of Bangalore.

---

## 🎮 6 Real-Time Crisis Scenarios

| Scenario | Name | Trigger | Physical & Cyber Behaviour |
|---|---|---|---|
| **Scenario 1** | Normal City | Dashboard Button 1 | Equilibrium flow, pedestrians crossing, normal green feeder loads (<85%), nominal water pressure (4.2 Bar). |
| **Scenario 2** | Traffic Congestion | Dashboard Button 2 | Road blockage at Silk Board, queue buildup, spillover into Bellandur ORR. |
| **Scenario 3** | Power Failure Cascade | Dashboard Button 3 | Feeder F-SLK overloads (>100%), breaker trips, connected traffic signals lose power, water pumps stall, and high-sound alarm triggers. |
| **Scenario 4** | Water Main Burst | Dashboard Button 4 | 800mm Cauvery transmission pipe ruptures under Sony World / 100ft road, street flash floods to 0.48m depth, lanes impassable. |
| **Scenario 5** | Cybersecurity FDI Attack | Dashboard Button 5 | Attacker injects false low-power reading on SCADA telemetry; Physics-informed residual detector exposes discrepancy ($>2.5$ MW) and alerts CSOC. |
| **Scenario 6** | Torrential Rain & Chamber Burst | Dashboard Button 6 | Downpour ($86\text{ mm/h}$) overflows underground drainage chambers, triggers structural pipeline rupture, flash floods roadways, and sounds the industrial emergency siren. |

---

## 📂 Project Structure

```
CityLink/
│
├── backend/
│   ├── main.py                  # FastAPI application entry point
│   ├── requirements.txt         # Python package dependencies
│   ├── citylink/
│   │   ├── simulation.py        # Master 10Hz cyber-physical coordinator
│   │   ├── traffic.py           # Microscopic vehicles & pedestrians engine
│   │   ├── power.py             # 66kV/11kV power distribution & breaker trip
│   │   ├── security.py          # FDI attack & physics-residual anomaly detector
│   │   ├── prediction.py        # 15-30 min cascade forecasting engine
│   │   ├── optimizer.py         # Automated resilience mitigation optimizer
│   │   └── graph.py             # NetworkX 4-zone infrastructure topology
│   ├── api/
│   │   ├── routes.py            # REST endpoints for scenarios & control
│   │   └── websocket.py         # 10Hz live streaming WebSocket manager
│   └── sumo/
│       ├── configuration/       # citylink.sumocfg
│       ├── network/             # citylink.net.xml (16 junctions, multi-lane)
│       ├── routes/              # citylink.rou.xml (cars, bikes, buses, emergency)
│       ├── pedestrians/         # citylink.ped.xml (sidewalks & zebra crossings)
│       ├── build_sumo_network.py # SUMO network generator script
│       └── sumo_bridge.py       # TraCI bidirectional bridge
│
├── unity/
│   └── CityLinkUnity/
│       ├── Packages/manifest.json
│       └── Assets/
│           └── Scripts/
│               ├── CityBuilder.cs            # Procedural 4-zone 3D city generator
│               ├── CityLinkManager.cs        # Master networking & entity spawner
│               ├── CameraController.cs       # WASD, Orbit, Top-View & Follow modes
│               ├── VehicleController.cs      # Wheels, brake lights & emergency siren
│               ├── PedestrianController.cs   # Procedural walking animation
│               ├── TrafficLightController.cs # 3-aspect heads & power fail flash
│               ├── PowerFeederVisualizer.cs  # Glowing feeder load conduits
│               └── ZoneManager.cs            # 4-zone labels & congestion heat
│
├── dashboard/
│   ├── package.json             # Vite React configuration
│   ├── vite.config.js
│   ├── index.html
│   └── src/
│       ├── main.jsx
│       ├── App.jsx              # Main Dashboard HUD layout
│       ├── index.css            # Cyber-physical glassmorphism styling
│       └── components/
│           ├── CityTwinCanvas.jsx    # Real-time 2D/3D digital twin viewport
│           ├── FeederPanel.jsx       # 4 Feeders, MW loads & breaker trips
│           ├── CyberSecurityPanel.jsx# CSOC FDI injection & incident log
│           ├── PredictorPanel.jsx    # 15-30 min horizon cascade prediction
│           ├── MitigationModal.jsx   # Before vs After analytics comparison
│           └── ControlToolbar.jsx    # Scenario 1-5 selector & playback
│
├── docs/
│   ├── ARCHITECTURE.md          # Full mathematical & technical specification
│   ├── UNITY_SETUP_GUIDE.md     # Step-by-step Unity setup instructions
│   └── HACKATHON_DEMO_SCRIPT.md # 5-minute judges presentation script
│
├── scripts/
│   ├── test_backend.py          # Automated integration test suite
│   ├── start_backend.ps1        # PowerShell backend runner
│   ├── start_dashboard.ps1      # PowerShell dashboard runner
│   └── run_all.ps1              # Unified single-command launcher
└── README.md
```

---

## ⚡ Quick Start Instructions (Windows PowerShell)

### Step 1: Install Missing Dependencies
Open Windows PowerShell as Administrator and run:
```powershell
# 1. Install Eclipse SUMO (Micro-traffic simulator)
winget install Eclipse.SUMO

# 2. Install Unity Hub (for 3D Unity Environment)
winget install Unity.UnityHub

# 3. Install Python dependencies
python -m pip install fastapi uvicorn websockets pydantic numpy pandas networkx
```

### Step 2: Verify Backend Simulation
```powershell
python "d:\Anti gravity llm\CityLink\scripts\test_backend.py"
```
*(All 8 test suites pass: Baseline, Motion, Congestion, Power Cascade, FDI Detection, AI Prediction, Mitigation, Reset).*

### Step 3: Run the Complete System
In PowerShell:
```powershell
powershell -ExecutionPolicy Bypass -File "d:\Anti gravity llm\CityLink\scripts\run_all.ps1"
```
This automatically launches:
- **FastAPI Backend**: `http://localhost:8000` (API docs at `/docs`)
- **React Monitoring Dashboard**: `http://localhost:3000`

---

## 🎮 5 Hackathon Scenarios

| Scenario | Name | Trigger | Physical & Cyber Behaviour |
|---|---|---|---|
| **Scenario 1** | Normal City | `F1` or Dashboard Button | Equilibrium flow, pedestrians crossing, normal green feeder loads (<85%). |
| **Scenario 2** | Traffic Congestion | `F2` or Dashboard Button | Road blockage at Silk Board, queue buildup, spillover into Bellandur. |
| **Scenario 3** | Power Failure Cascade | `F3` or Dashboard Button | Feeder F-SLK overloads (>100%), breaker trips, connected traffic signals lose power and enter flashing amber failure mode, intersection throughput collapses by 70%. |
| **Scenario 4** | Cybersecurity FDI Attack | `F4` or Dashboard Button | Attacker injects false low-power reading on SCADA telemetry; Physics-informed residual detector exposes discrepancy ($>2.5$ MW) and alerts CSOC. |
| **Scenario 5** | Automatic Resilience Recovery | `F5` or Dashboard Button | Adaptive green wave signal timing (+38s), vehicle rerouting, EV charging curtailment (-3.5 MW load shed), breaker re-closure, and before/after verification. |

---

## 📊 Evaluation & Verification Summary
- **4 Interconnected Zones**: Koramangala, HSR Layout, Bellandur, Silk Board.
- **Microscopic Traffic Physics**: Continuous vehicle routing, speed adaptation, safe gap keeping, traffic light obedience, pedestrian crossing safety.
- **Power Grid Modeling**: 66kV substation, 4 feeders, dynamic EV charging load coupling, sustained overload breaker trip logic.
- **Bidirectional Cascade**: Congestion -> EV draw -> Overload -> Feeder Trip -> Traffic Signal Blackout -> Stagnation.
- **Cybersecurity Module**: False Data Injection (FDI), Traffic Sensor Spoofing, Signal Tampering, Physics Residual Anomaly Detection.
- **Predictive Engine**: 15–30 minute forward cascade horizon with root-cause identification.
- **Resilience Mitigation**: Measurable before vs after state changes (density reduction, load shed, incident prevention).
