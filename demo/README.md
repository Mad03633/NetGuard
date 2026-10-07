# NetGuard: Live Cognitive AI Defense Demo

**Course:** Cognitive technologies and decision support systems | Instructor: Khabiyev Zhangirkhan  
**Authors:** Madiyar B., Angsar S., Alisher A. — AAI-2501M  
**Project:** [NetGuard GitHub Repository](https://github.com/Mad03633/NetGuard)

---

## ⚡ Real-Time Live Architecture

This is a **true live demonstration**, not a static mock. It connects directly to your trained models:
- **Trained Model:** `results/models/random_forest.pkl` (Scikit-Learn Random Forest)
- **Feature Scaler:** `results/models/scaler.pkl` (StandardScaler)
- **Categorical Encoders:** `results/models/label_encoders.pkl` (LabelEncoder)
- **Real Traffic Stream:** `data/KDDTest+.txt` (22,544 test network connections)
- **Long-Term Memory File:** `memory/assignment3_netguard_memory.json` (Real JSON persistence)

---

## 🚀 How to Run the Live Server

The live server is currently running in the background at **`http://localhost:8000`**.

If you ever need to start it manually:
```bash
cd /home/ansinitro/NetGuard/demo
python3 server.py
```
*(Or: `python3 -m uvicorn server:app --host 0.0.0.0 --port 8000`)*

Then open **`http://localhost:8000`** in your browser.

---

## 🎤 How to Defend Your Project in Front of Your Teacher

When presenting to your instructor, follow this clean, powerful narrative:

### Step 1: Show Real Traffic Streaming Live
1. Open `http://localhost:8000`.
2. Notice the status indicator: `BACKEND: LIVE MODEL ONLINE`.
3. Click **"▶ Start Live Stream"**.
4. **Explain to the teacher:**
   > *"Here you can see our trained Random Forest model actively analyzing real network packets from the NSL-KDD test set. The packets physically traverse the ingress router into NetGuard, where 41 features are normalized and scored in real-time."*
5. Point to the **Live Terminal Console** on the right side:
   > *"Every step—Ingress, Perception (41-dim vector), Attention filtering, Model Inference, Memory Query, and Enforcement—is output in real-time."*

---

### Step 2: Show the Core Cognitive Highlight (Memory Escalation!)
1. Click the button: **"🔮 Apache Back (⭐ Memory Escalation)"**.
2. **Watch the live transition:**
   - **ML Model Output:** Probability = **0.6500 (Medium Risk)**
   - **Long-Term Memory:** Discovers **2 previous verified incidents** on `tcp/http` (`test_7527`, `test_11868`)
   - **Rule K4 Fires:** `IF Anomaly = True AND Previous Similar >= 2`
   - **Cognitive Verdict:** **ESCALATED: MEDIUM ➔ HIGH!**
   - **Action:** Gateway Firewall quarantines the connection and triggers a Level-2 SOC alert.
3. **Explain to the teacher (addressing your teammate's key point):**
   > *"If we only used pure Machine Learning, this packet would just be flagged as 'Medium', meaning it might get ignored or handled with low priority. But NetGuard has cognitive memory. It queries past threat logs, detects that this specific protocol/service has repeatedly shown malicious behavior, and dynamically escalates the priority to HIGH!"*

---

### Step 3: Contrast with Other Real Scenarios
1. Click **"🟢 Normal FTP"**:
   - Probability = **0.0000**
   - Memory = **0 prior incidents**
   - Rule = **K3**
   - Verdict = **LOW (Continue Monitoring & Pass Traffic)**
2. Click **"🔴 Neptune DoS"**:
   - Probability = **1.0000**
   - Rule = **K1**
   - Verdict = **HIGH (Immediate Analyst Review)**

---

## 🛠️ API Endpoints Available

- `GET /api/stream/next` — Fetches and analyzes the next real packet from `KDDTest+.txt`.
- `POST /api/inject/{attack_type}` — Injects verified attacks: `normal`, `neptune`, `apache_back`, `portsweep`.
- `POST /api/analyze` — Analyzes a custom payload with user-defined attributes.
- `GET /api/memory` — Returns current Short-Term deque events and Long-Term JSON store.
- `POST /api/memory/reset` — Clears persistent memory.
- `POST /api/memory/seed` — Seeds default HTTP anomalies for demo escalation.
