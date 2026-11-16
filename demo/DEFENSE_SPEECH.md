# 🎓 NetGuard: Cognitive Cyber Defense — Project Defense Speech & Guide

**Course:** Cognitive technologies and decision support systems  
**Instructor:** Professor Khabiyev Zhangirkhan  
**Authors:** Madiyar B., Angsar S., Alisher A. — Group AAI-2501M  
**Live Demo Web App:** [http://localhost:8000](http://localhost:8000)  
**Notebook Reference:** [`notebook/cognitive.ipynb`](file:///home/ansinitro/NetGuard/notebook/cognitive.ipynb)  
**GitHub Repository:** [https://github.com/Mad03633/NetGuard](https://github.com/Mad03633/NetGuard)  

---

## ⚡ 30-Second Elevator Pitch (Opening Hook)

> *"Good afternoon, Professor Khabiyev. Today our team presents **NetGuard**—a real-time Cognitive Decision Support System for network anomaly defense.*
>
> *Traditional intrusion detection systems rely strictly on standalone Machine Learning models that evaluate packets in complete isolation. The core flaw is that ML classifiers frequently output **ambiguous, borderline probability scores** (around 60–70%), leaving security operations teams uncertain.*
>
> *NetGuard solves this by implementing human-like **Cognitive Architecture**—from Perception and Selective Attention, to Machine Learning inference, Short-Term Working Memory, and Long-Term Episodic Memory. When our system encounters ambiguous traffic, it consults its Long-Term Memory, identifies historical threat patterns, and dynamically escalates the verdict from Medium to High.*
>
> *Let us demonstrate our real-time system live in an enterprise multi-node network environment."*

---

## 👥 Team Role Allocation & Presentation Breakdown

| Presenter | Role | Key Sections & Actions |
| :--- | :--- | :--- |
| **Speaker 1: Madiyar** | **Problem Statement & System Topology** | • Introduces the limitations of standard standalone ML.<br>• Explains the enterprise topology (LAN PCs, Edge Router, NetGuard Brain, Next-Gen FW, SOC Quarantine).<br>• Demonstrates **Case 1: Low Risk (Normal FTP)** on Hop 1 to Hop 5. |
| **Speaker 2: Angsar** | **Perception, Attention & ML Pattern Recognition** | • Explains **Layer 1 (Perception)**: 41 NSL-KDD attributes encoded (`LabelEncoder`) & scaled (`StandardScaler`).<br>• Explains **Layer 2 (Attention)**: Saliency ranking (top 5 signal features vs. 36 suppressed noise features).<br>• Demonstrates **Case 2: High Risk (Neptune DoS)** with Rule K1 direct reflex. |
| **Speaker 3: Alisher** | **Contextual Memory, Rule K4 Escalation & Conclusion** | • Explains **Short-Term Memory** (`deque maxlen=5`) & **Long-Term Memory** (`assignment3_netguard_memory.json`).<br>• **The Hero Demo (Case 3):** Demonstrates **Apache Back DoS** triggering **Rule K4 Memory Escalation (`MEDIUM ➔ HIGH`)**.<br>• Demonstrates SOC Quarantine isolation and concludes. |

---

## 🎮 The 5-Hop Step-by-Step Defense Guide (Using Spacebar)

Open **`http://localhost:8000`** in the browser. Click **`Case 3: Memory-Aware (Apache Back ⭐)`**, then press **Spacebar** to advance through the 5 cognitive layers step-by-step:

---

### HOP 1: Ingress Source (LAN / Attacker WAN)
* **On-Screen Visual:** Packet sits at **Attacker (WAN)**. Telemetry bar highlights `Protocol: TCP`, `Service: HTTP`, `Flag: S2`, `SrcBytes: 54,540`.
* **SIEM Log:** `[INGRESS] Transmitting from Attacker (WAN): TCP/http (Flag: S2)`
* **Speaker Script (Madiyar):**
  > *"Here at **Hop 1 (Ingress Source)**, raw uninspected network traffic arrives at our network perimeter. An external attacker is launching an Apache Back denial-of-service exploit disguised across HTTP headers. In cognitive terms, this represents **raw sensory input** before neural processing."*

---

### HOP 2: Edge Router (Perception & Attention Layers)
* **Action:** Press **Spacebar** or click **`STEP NEXT HOP ➔`**.
* **On-Screen Visual:** Packet token glides into **Core Router**. The **Perception & Attention Module** card glows with a cyan focus border. Progress bars display top feature weights (`src_bytes: 17.2%`, `dst_bytes: 11.6%`, `flag: 8.0%`).
* **SIEM Log:** `[PERCEPTION] Encoded 41 attributes -> Dense Vector (1, 41)` & `[ATTENTION] Top focus: src_bytes, dst_bytes, flag`.
* **Speaker Script (Angsar):**
  > *"At **Hop 2 (Ingress Edge)**, two cognitive functions take place:*
  >
  > 1. *First is **Perception**: raw attributes are transformed via `LabelEncoder` and `StandardScaler` into a continuous 41-dimensional vector space $(1, 41)$.*
  > 2. *Second is the **Attention Module**: mirroring human selective attention, NetGuard filters out 36 low-relevance features (such as `urgent` and `land` flags) and concentrates computational resources strictly on high-signal indicators like connection flags and byte ratios."*

---

### HOP 3: NetGuard Core Brain (ML Inference & Memory Escalation ⭐)
* **Action:** Press **Spacebar** or click **`STEP NEXT HOP ➔`**.
* **On-Screen Visual:** Packet glides into **NetGuard Core**. The node pulses purple. Both **Contextual Memory State** and **Cognitive Synthesis** cards glow purple. Sound chime plays, and the **Rule K4 Escalation indicator** flashes!
* **SIEM Log:** 
  - `[ML MODEL] Random Forest predicted: Anomaly (Probability: 0.6500)`
  - `[MEMORY QUERY] Queried Long-Term Memory: Found 2 prior verified incidents for (tcp/http)`
  - `[RULE K4 TRIGGERED] Anomaly verified AND >= 2 history matches! Escalating: MEDIUM ➔ HIGH!`
* **Speaker Script (Alisher — The Hero Moment):**
  > *"Here at **Hop 3 (The Cognitive Core)** is our primary research contribution.*
  >
  > *Notice that our trained Random Forest model evaluated the packet and output an anomaly probability of **P = 0.6500 (Medium Risk)**.*
  > *In a traditional ML-only system, a 0.65 score is ambiguous—it sits in a low-priority queue while the web server suffers.*
  >
  > *NetGuard engages **Deliberative Cognition**: it queries **Long-Term Episodic Memory**. Memory reveals that this exact protocol and service pattern (`tcp/http`) has **2 prior verified attack incidents** (`test_7527` and `test_11868`).*
  >
  > *Because an established threat pattern is confirmed, our **Knowledge Engine fires Rule K4**: it resolves the ML model's uncertainty and dynamically **escalates the verdict from MEDIUM to HIGH**!"*

---

### HOP 4: Next-Gen Firewall (Policy Enforcement)
* **Action:** Press **Spacebar** or click **`STEP NEXT HOP ➔`**.
* **On-Screen Visual:** Packet glides into the **Next-Gen FW (Firewall)** node. The Firewall node glows red. The **Automated Firewall Action** box highlights `QUARANTINE_AND_SOC_ALERT`.
* **SIEM Log:** `[FIREWALL POLICY] Enforcing security rule: QUARANTINE_AND_SOC_ALERT`
* **Speaker Script (Madiyar):**
  > *"At **Hop 4 (Enforcement)**, the system bridges cognitive reasoning with operational network policy. The Next-Gen Firewall translates the escalated High-Risk verdict into an active mitigation action: dropping the TCP session and issuing a Level-2 SOC quarantine command."*

---

### HOP 5: Destination Server / SOC Quarantine Room
* **Action:** Press **Spacebar** or click **`STEP NEXT HOP ➔`**.
* **On-Screen Visual:** Packet glides along the red quarantine cable directly into the **SOC Quarantine Room** node! The SOC Quarantine card flashes red with high-intensity warning borders.
* **SIEM Log:** `[ACTION ENFORCED] QUARANTINE_AND_SOC_ALERT completed successfully.`
* **Speaker Script (Alisher):**
  > *"At **Hop 5 (Action Execution)**, the threat has been completely isolated from our internal DMZ servers (Web, Storage, Database) and contained inside the SOC Quarantine Room. The entire decision loop—from raw perception to memory-assisted decision to automated action—took milliseconds with full explainable SIEM logs."*

---

# 📖 Notebook Alignment (`notebook/cognitive.ipynb`)

Our live system is a direct, operational implementation of our Assignment 3 submission notebook:

| Notebook Requirement (Cell 46) | Notebook Implementation | Live Demo Equivalent |
| :--- | :--- | :--- |
| **Perception Layer** | 41 NSL-KDD attributes encoded and scaled | Real-time `StandardScaler` + `LabelEncoder` dense vector (Hop 2) |
| **Attention Module** | Feature importance ranking, top signal extraction | Interactive weight progress bars and noise suppression card |
| **Short-Term Memory** | Python `deque(maxlen=5)` buffer | Live 5-slot animated working memory deque |
| **Long-Term Memory** | JSON file persistence (`assignment3_netguard_memory.json`) | Persistent JSON store on disk with real write & retrieval ops |
| **Memory Influences Result** | Repeated anomalies trigger Rule K4 risk escalation | **Case 3:** $P = 0.65$ (`MEDIUM`) escalates to `HIGH` live on screen |
| **Knowledge Rules** | Rules K1, K2, K3, K4 | Knowledge Engine rule matrix and decision comparison card |
| **3 Demo Scenarios** | Low Risk, High Risk, Memory-Aware | Buttons `Case 1`, `Case 2`, `Case 3` matching notebook test indices 2, 0, and 301 |

---

# 🧠 Professor Khabiyev Q&A Cheat Sheet

### Q1: *"Why is this called 'Cognitive' rather than just a Machine Learning classifier?"*
> **Answer:** *"A standalone Machine Learning classifier is purely perceptual—it outputs a probability for a single snapshot in time without memory, context, or reasoning. NetGuard implements the full OODA cognitive loop (Observe, Orient, Decide, Act). It couples perception with Short-Term Working Memory (tracking packet bursts) and Long-Term Episodic Memory (recalling past confirmed attacks) to reason through ambiguous decisions (Rule K4)."*

### Q2: *"Why did you use Random Forest for the live demo rather than Deep Learning or Transformers?"*
> **Answer:** *"For real-time edge network defense, inference latency is paramount. Random Forest evaluates a 41-feature vector in under 2 milliseconds with >99.2% accuracy on NSL-KDD, making it ideal for microsecond gateway enforcement, while complex foundation models can be used offline for retrospective threat intelligence."*

### Q3: *"Why didn't Neptune DoS trigger memory escalation, but Apache Back did?"*
> **Answer:** *"This reflects the distinction between System 1 (Reflex) and System 2 (Deliberation):*
> 1. *For **Neptune DoS**, the ML model is **100% confident (P = 1.0000)**. NetGuard executes **Rule K1** as a direct reflex—classifying it as **HIGH** and blocking it immediately. Escalating a 100% certain attack is redundant.*
> 2. *For **Apache Back**, the attack is stealthy ($P = 0.6500$, Medium Risk). The ML model alone is uncertain. Here, NetGuard engages **System 2 Deliberation**: it queries Long-Term Memory, verifies 2 prior attacks, and **Rule K4** escalates the verdict from **MEDIUM to HIGH**."*

### Q4: *"Where is memory stored? Is it persistent across server restarts?"*
> **Answer:** *"Yes. Short-Term Memory uses an in-memory `deque(maxlen=5)` in RAM. Long-Term Memory is persisted to disk at `memory/assignment3_netguard_memory.json`. When an attack occurs, it is committed to JSON so future sessions recall historical threat actors even across server reboots."*

---

*End of Defense Speech & Documentation.*
