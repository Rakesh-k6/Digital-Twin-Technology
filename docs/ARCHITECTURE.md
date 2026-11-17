# CityLink Technical & Mathematical Architecture Specification

## 1. Mathematical Modeling of the Bidirectional Traffic-Power Cascade

CityLink models urban infrastructure as a tightly-coupled bidirectional dynamical system:

$$\mathcal{S} = \langle \mathcal{G}_{\text{traffic}}, \mathcal{G}_{\text{power}}, \mathcal{C}_{\text{cyber}}, \mathcal{M}_{\text{interdep}} \rangle$$

### 1.1 Traffic Layer Dynamics (Intelligent Driver Model - IDM)
Each vehicle $i$ calculates instantaneous acceleration $\dot{v}_i$ based on leading distance $s_i$ and velocity difference $\Delta v_i$:

$$\dot{v}_i = a_{\max} \left[ 1 - \left(\frac{v_i}{v_0}\right)^\delta - \left(\frac{s^*(v_i, \Delta v_i)}{s_i}\right)^2 \right]$$

Where the desired minimum dynamic headway $s^*$ is given by:

$$s^*(v_i, \Delta v_i) = s_0 + v_i T + \frac{v_i \Delta v_i}{2\sqrt{a_{\max} b_{\text{safe}}}}$$

When an intersection signal state $S_j \in \{\text{RED}, \text{FAIL\_FLASHING\_AMBER}\}$, a virtual stationary obstacle is inserted at distance $d_{\text{stop}}$, forcing vehicles to decelerate smoothly to zero velocity.

---

### 1.2 Power Layer Dynamics & Overload Tripping
The physical active power demand $P_{k}(t)$ on radial feeder $k$ serving zone $z_k$ is the sum of baseline municipal draw $P_{\text{base}}$, dynamic EV fast charging $P_{\text{ev}}$, and traffic congestion coupling stress $P_{\text{stress}}$:

$$P_{k}(t) = P_{\text{base}, k} + \sum_{m \in \mathcal{EV}_k} p_m(t) + \alpha \cdot \rho_{z_k}(t) + P_{\text{aux}}$$

Where:
- $\rho_{z_k}(t) \in [0, 1]$ is the vehicle congestion density in zone $z_k$.
- $\alpha = 3.5 \text{ MW}$ is the empirical urban idling stress coefficient (HVAC load, emergency ventilation, and auxiliary municipal load).
- $p_m(t) \in [60 \text{ kW}, 150 \text{ kW}]$ is active DC fast charging demand per vehicle.

**Circuit Breaker Tripping Function:**
A protective trip timer triggers when physical loading exceeds nominal thermal capacity $C_k$:

$$T_{\text{overload}}(t) = \int_{t_0}^t \mathbb{I}\left(P_k(\tau) \ge C_k\right) d\tau$$

$$\text{Breaker State} = \begin{cases} \text{TRIPPED (Open)}, & \text{if } T_{\text{overload}} \ge \tau_{\text{trip}} \quad (\tau_{\text{trip}} = 6.0\text{ s}) \\ \text{CLOSED}, & \text{otherwise} \end{cases}$$

---

### 1.3 Power-to-Traffic Degradation Function
When feeder $k$ trips ($P_k(t) = 0$), all dependent traffic signals switch to failure mode:

$$\eta_{\text{intersection}} = \begin{cases} 1.0, & \text{Feeder Powered (Normal Cycle)} \\ 0.28, & \text{Feeder Tripped (Uncontrolled / Amber Yield)} \end{cases}$$

Vehicle discharge capacity collapses from 1800 veh/hr/lane to 500 veh/hr/lane, forming an exponential queue buildup that propagates upstream across inter-zone expressway boundaries.

---

## 2. Cybersecurity Anomaly Detection & State Estimation

### 2.1 False Data Injection (FDI) Formulation
An adversary corrupts the SCADA telemetry vector $y_{\text{telemetry}}$:

$$y_{\text{telemetry}} = y_{\text{true}} + a_{\text{attack}}$$

Where the adversary crafts $a_{\text{attack}} = -(\text{Overload}) + \epsilon$ to falsely report safe loading ($5.8 \text{ MW}$) while $P_{\text{physical}} = 16.5 \text{ MW}$.

### 2.2 Physics-Informed Residual Detector
The CityLink detection engine maintains an independent Physics State Estimator $\hat{P}_k$:

$$\hat{P}_k(t) = P_{\text{base}} + \hat{N}_{\text{EV}} \cdot \bar{p}_{\text{EV}} + \alpha \cdot \hat{\rho}_k$$

The detection residual metric $r_k(t)$ is computed:

$$r_k(t) = \left| y_{\text{telemetry}, k}(t) - \hat{P}_k(t) \right|$$

$$\text{Decision Rule:} \quad \begin{cases} r_k(t) > \tau_{\text{threshold}} (2.5\text{ MW}) \implies \text{\textbf{SECURITY ALERT: FALSE DATA INJECTION}} \\ r_k(t) \le \tau_{\text{threshold}} \implies \text{NOMINAL TELEMETRY} \end{cases}$$

---

## 3. Resilience Optimization & Automated Mitigation

The optimization objective minimizes total network travel delay while guaranteeing feeder physical load stays within thermal limits:

$$\min_{\Delta g, \Delta P_{\text{EV}}} \sum_{i} \left( \frac{v_0 - v_i}{v_0} \right)^2 + \lambda \sum_{k} \max(0, P_k(t) - C_k)^2$$

Subject to:
1. Green split bounds: $15\text{ s} \le g_j \le 45\text{ s}$.
2. EV charging curtailment: $P_{\text{EV}, k}^{\text{curtailed}} \ge 0.2 \cdot P_{\text{EV}, k}^{\text{nominal}}$.
3. Minimum cycle duration constraints.
