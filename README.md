# 🔀 GridlockPulse: Predictive Event-Driven Traffic Optimization Engine

### **Flipkart Gridlock Hackathon 2.0 — Prototype Submission (Theme 2)**
**Live Production URL:** [Insert your deployed Streamlit link here]

---

## 📌 Project Overview
Urban centers face immense, cascading traffic gridlock during scheduled mass gatherings (festivals, political rallies, sporting events) and infrastructure disruptions. **GridlockPulse** is an automated, data-driven spatiotemporal planning dashboard designed for city administrators and traffic enforcement authorities. 

By ingesting historical city-scale incident records, GridlockPulse models the structural impact of traffic disruptions, quantifies regional breakdown probabilities, and automatically generates real-time, optimized field resource allocation plans (manpower, barriers, detours).

---

## 📊 Data Insights & Engineering (Astram Dataset Analysis)
The core analytical engine of this prototype is calibrated using the historical **Astram Event and Traffic Incident Database for Bengaluru** (8,173 real-world records). Key insights mined during development include:

1. **Structural Severity Over Frequency:** While routine vehicle breakdowns represent the highest total volume of daily disruptions, they carry a low road-closure probability ($<5\%$). Conversely, incidents classified under `vip_movement`, `debris`, `public_event`, and `protest` have a drastically higher probability ($40\% - 100\%$) of requiring full road closures.
2. **Spatiotemporal Choke Points:** Spatial clustering identified clear bottleneck anomalies across specific $5$-character grid sectors, with sector **`tdr1v`** recording a massive historical concentration of over 1,200 traffic incidents.
3. **Temporal Footprints:** Deep timeline logging revealed that infrastructure bottlenecks like `road_conditions` and `construction` choke lanes for localized periods spanning $8$ to $14$ hours, compared to dynamic movements which clear within $2$ to $4$ hours.

---

## 🛠️ System Architecture & Logic Matrix
GridlockPulse combines multi-factor predictive scoring with an operational dispatch matrix:

* **Pure-Python Spatiotemporal Encoder:** Dynamically translates arbitrary geographical coordinates (`Latitude` / `Longitude`) into deterministic 5-character Geohash sectors to look up historical risk weight arrays instantly.
* **Disruption Complexity Formula:** Calculates a unified vulnerability decimal using weighted constraints:
  $$S_{\text{disruption}} = (\text{Volume Factor} \times 0.4) + (\text{Closure Probability} \times 0.4) + (\text{Regional Hazard Weight} \times 0.2)$$
* **Automated Tactical Allocation:** Maps the resulting score against target volume to generate mathematically backed logistics recommendations:
  * **Traffic Manpower Deployed:** Deploys personnel specifically scaled to handle structural intersection filtering.
  * **Physical Barricading Units:** Recommends barrier counts driven directly by historical closure risks.
  * **Diversion Route detours:** Activates progressive rerouting plans based on systemic breakdown thresholds.

---

## 🔄 Post-Event Continuous Learning System
Fulfilling the core hackathon requirement for long-term iterative optimization, the prototype features a built-in **Continuous Evaluation Registry**. 

Field supervisors can log post-event operational ratings ("Optimal", "Understaffed", "Overstaffed") and notes directly into a state-managed local data array. This stream bridges the gap between predictive theory and live field constraints, providing the logging infrastructure needed to retrain baseline models over time.

---

## ⚙️ How to Run Locally

If you wish to execute the web dashboard framework on your local machine, follow these steps:

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/](https://github.com/)[YOUR-USERNAME]/GridlockPulse-Event-Optimizer.git
   cd GridlockPulse-Event-Optimizer

2. Streamlit: https://gridlockpulse-theme2-richieseb29.streamlit.app/
