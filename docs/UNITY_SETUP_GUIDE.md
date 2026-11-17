# CityLink Unity 3D Setup & Execution Guide

This guide explains step-by-step how to open, build, and run the realistic 3D virtual smart city inside Unity.

---

## 1. Prerequisites
- **Unity Hub**: Installed on your Windows PC (`winget install Unity.UnityHub`).
- **Unity Editor Version**: Unity 2022.3 LTS (recommended) or Unity 2023 / Unity 6.
- **Visual Studio / VS Code**: Installed with C# tools.

---

## 2. Opening the Project in Unity
1. Open **Unity Hub**.
2. Click the **Add** button (or **Add project from disk**).
3. Browse to and select:
   ```
   D:\Anti gravity llm\CityLink\unity\CityLinkUnity
   ```
4. Click **Open**.
5. Select your installed Unity Editor version (e.g. `2022.3.x LTS`) and click **Open Project**.
6. Unity will import packages and compile the C# scripts.

---

## 3. Creating the 3D City Scene (1-Click Procedural Generation)
1. In the **Project** window, go to `Assets/Scenes/`.
2. Right-click -> **Create** -> **Scene**, and name it `CityLinkScene`. Double-click to open it.
3. In the **Hierarchy** window, delete the default `Main Camera` and `Directional Light` (or keep them).
4. Create an empty GameObject:
   - In Hierarchy: Right-click -> **Create Empty**. Name it `CityManager`.
5. Attach the following scripts to `CityManager`:
   - Click **Add Component** in Inspector.
   - Search and add `CityBuilder` (Builds roads, buildings, intersections, streetlights, trees, EV hubs, and substations).
   - Search and add `CityLinkManager` (Connects to `http://localhost:8000/api` and streams vehicles, pedestrians, signals, and feeders).
6. Create the Camera:
   - In Hierarchy: Right-click -> **Camera**. Name it `CityLinkCamera`.
   - Add Component -> `CameraController` (Provides WASD, mouse look, scroll zoom, and Top-View modes).
   - Tag the camera as `MainCamera`.
7. Add a Directional Light:
   - In Hierarchy: Right-click -> **Light** -> **Directional Light**.
   - Rotation: `(50, -30, 0)`.
   - Color: Warm Sunlight (`#FFF8EE`).
   - Intensity: `1.2`.

---

## 4. Running the Simulation
1. Ensure the Python backend is running:
   ```powershell
   python "d:\Anti gravity llm\CityLink\backend\main.py"
   ```
2. In Unity, press the **Play** button (`Ctrl + P`).
3. You will immediately see:
   - The complete 4-zone 3D smart city generated with multi-lane roads, asphalt markings, buildings, and parks.
   - Moving vehicles (cars, buses, trucks, bikes, and ambulances with flashing sirens).
   - Pedestrians walking on footpaths and crossing at zebra crossings.
   - Traffic lights cycling red, yellow, green, and pedestrian walk glyphs.
   - Electrical feeders and central substation conduits glowing with real-time load colors.

---

## 5. Keyboard Controls & Shortcuts

### Camera Modes:
- **`1`**: Free-Roam Camera (WASD to move, Right-click to rotate, Q/E for height, Scroll to zoom).
- **`2`**: Top-View Satellite / Orthographic Camera.
- **`3`**: Follow-Vehicle Camera (locks onto lead or emergency vehicle).

### Hackathon Scenario Hotkeys:
- **`F1`**: Activate **Scenario 1: Normal City**.
- **`F2`**: Activate **Scenario 2: Traffic Congestion** (Silk Board surge & blockage).
- **`F3`**: Activate **Scenario 3: Power Failure** (Feeder overload trip -> flashing amber signals).
- **`F4`**: Activate **Scenario 4: Cyberattack** (FDI on SCADA telemetry).
- **`F5`**: Activate **Scenario 5: Automatic Resilience Recovery** (Reroute, signal split, shed load).
- **`R`**: Reset simulation to baseline.
