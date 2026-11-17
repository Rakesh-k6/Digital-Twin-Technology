# CityLink Hackathon Live Demonstration Script

Use this 5-minute presentation script when demonstrating CityLink to the hackathon judging panel.

---

## 0:00 - 0:45 | Introduction & Problem Statement
> *"Respected judges, modern smart cities are deeply interdependent cyber-physical systems. A traffic jam is no longer just a traffic problem—it creates localized EV charging surges and grid stress. Conversely, an electrical feeder failure blinds traffic signals, turning high-throughput intersections into gridlocked choke points.
>
> We present **CityLink: Cyber-Physical Cascade Predictor for Interdependent Urban Infrastructure**. It couples microscopic traffic physics with electrical distribution grid dynamics, simulates adversarial cyberattacks such as False Data Injection (FDI), and predicts cascading failures 15–30 minutes in advance with automated mitigation."*

---

## 0:45 - 1:45 | Scenario 1: Normal City Equilibrium
1. In the Dashboard or Unity, click **"1. Normal City"**.
2. Point out:
   - 4 Interconnected Zones: **Koramangala, HSR Layout, Bellandur, Silk Board**.
   - Vehicles (Cars, Bikes, Buses, Trucks, Ambulances) moving autonomously with collision avoidance and lane discipline.
   - Pedestrians walking on sidewalks and crossing safely at zebra crossings.
   - Traffic lights cycling through Red, Yellow, Green, and Pedestrian Walk phases.
   - 4 Electrical Feeders (F-KOR, F-HSR, F-BEL, F-SLK) operating in the **Green (< 85%)** zone.

---

## 1:45 - 2:45 | Scenario 2 & 3: The Bidirectional Traffic-Power Cascade
1. Click **"2. Traffic Congestion"**:
   - A roadblock and vehicle surge occur at **Silk Board (Zone D)**.
   - Show how congestion builds vehicle queues and spillovers begin bleeding into **Bellandur (Zone C)**.
2. Click **"3. Power Failure"**:
   - Silk Board Feeder (F-SLK) enters **OVERLOAD (> 100%)** due to EV charging concentration and commercial cooling draw.
   - Watch the protective circuit breaker trip after the configured delay.
   - **Crucial Cascade Demonstration**: The moment Feeder F-SLK trips, all 4 connected traffic signals at Silk Board lose normal power and enter **Flashing Amber / Fail-Safe**.
   - Show the judges: Intersection throughput collapses by 70%, vehicle queues surge, and traffic completely stagnates.

---

## 2:45 - 3:45 | Scenario 4: Cybersecurity FDI Attack & Physics Residual Detection
1. Click **"4. Cyberattack"** or click **"Inject FDI (Feeder F-SLK)"**:
   - Explain to the Cyber Security judges:
     > *"An adversary has compromised the SCADA gateway. They are injecting False Data into the telemetry stream, making the operator see a calm 5.8 MW reading while the physical transformer is actually burning at 16.5 MW!"*
   - Show the CSOC panel:
     > *"Our Physics-Informed State Estimator detects that $|y_{telemetry} - \hat{y}_{physics}| > \tau$ (residual exceeds 2.5 MW threshold). It immediately flags a **CRITICAL FALSE DATA INJECTION** alert before catastrophic transformer destruction occurs."*

---

## 3:45 - 4:30 | Scenario 5: AI Cascade Prediction & Automatic Mitigation
1. Point to the **AI Cascade Predictive Engine**:
   - Show the 20-minute forward forecast predicting imminent breaker trips and secondary corridor spillovers with identified root causes.
2. Click **"⚡ Apply Recommended Mitigation"** (or hotkey **F5**):
   - Watch the Before vs After Modal appear:
     * Traffic signal green splits automatically extended to 38s on the choked corridor.
     * Dynamic vehicle rerouting around Silk Board onto bypass lanes.
     * Smart EV charging curtailment shedding 3.5 MW of non-critical load.
     * Tripped distribution breaker safely re-closed under protected margins.
     * CSOC telemetry resynchronized with cryptographic trust anchor.
   - Show the live city recovering in real-time.

---

## 4:30 - 5:00 | Conclusion & Q&A
> *"CityLink demonstrates that true smart city resilience requires co-simulating transportation, power, and cybersecurity as a single unified digital twin. Thank you, and we welcome your questions!"*
