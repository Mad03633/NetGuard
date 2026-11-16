"""
NetGuard: Real-Time Cognitive AI Backend & Network Stream Server
Course: Cognitive technologies and decision support systems | Instructor: Khabiyev Zhangirkhan
Authors: Madiyar B., Angsar S., Alisher A. — AAI-2501M

Runs live model inference using:
- results/models/random_forest.pkl
- results/models/scaler.pkl
- results/models/label_encoders.pkl
- data/KDDTest+.txt
"""

import os
import json
import random
from pathlib import Path
from datetime import datetime, timezone
from collections import deque
from typing import Dict, Any, List, Optional

import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "results" / "models"
DATA_DIR = BASE_DIR / "data"
MEMORY_PATH = BASE_DIR / "memory" / "assignment3_netguard_memory.json"
MEMORY_PATH.parent.mkdir(parents=True, exist_ok=True)

# 1. Load Trained Artifacts
print("[INIT] Loading trained artifacts...")
rf_model = joblib.load(MODELS_DIR / "random_forest.pkl")
scaler = joblib.load(MODELS_DIR / "scaler.pkl")
label_encoders = joblib.load(MODELS_DIR / "label_encoders.pkl")
rf_classes = list(rf_model.classes_)
ANOMALY_COLUMN = rf_classes.index(1) if 1 in rf_classes else 1
print(f"[INIT] Random Forest ready! Classes: {rf_classes}, Anomaly column: {ANOMALY_COLUMN}")

# Feature columns definition
COLUMNS = [
    "duration", "protocol_type", "service", "flag", "src_bytes", "dst_bytes",
    "land", "wrong_fragment", "urgent", "hot", "num_failed_logins", "logged_in",
    "num_compromised", "root_shell", "su_attempted", "num_root",
    "num_file_creations", "num_shells", "num_access_files",
    "num_outbound_cmds", "is_host_login", "is_guest_login", "count",
    "srv_count", "serror_rate", "srv_serror_rate", "rerror_rate",
    "srv_rerror_rate", "same_srv_rate", "diff_srv_rate", "srv_diff_host_rate",
    "dst_host_count", "dst_host_srv_count", "dst_host_same_srv_rate",
    "dst_host_diff_srv_rate", "dst_host_same_src_port_rate",
    "dst_host_srv_diff_host_rate", "dst_host_serror_rate",
    "dst_host_srv_serror_rate", "dst_host_rerror_rate",
    "dst_host_srv_rerror_rate", "label", "difficulty"
]
CATEGORICAL_COLS = ["protocol_type", "service", "flag"]
FEATURE_COLS = [c for c in COLUMNS if c not in ["label", "difficulty"]]
NUMERICAL_COLS = [c for c in FEATURE_COLS if c not in CATEGORICAL_COLS]

# Load real test dataset
print("[INIT] Loading NSL-KDD test dataset for live network streaming...")
test_df = pd.read_csv(DATA_DIR / "KDDTest+.txt", names=COLUMNS)
print(f"[INIT] Test dataset loaded: {test_df.shape[0]} real network records")

# 2. Memory Module
class ShortTermMemory:
    def __init__(self, max_events=5):
        self.events = deque(maxlen=max_events)

    def remember(self, event):
        self.events.append(event)

    def retrieve_recent(self):
        return list(self.events)

    def clear(self):
        self.events.clear()

class LongTermMemory:
    def __init__(self, path):
        self.path = Path(path)
        if not self.path.exists():
            self._save([])

    def _load(self):
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data if isinstance(data, list) else []
        except Exception:
            return []

    def _save(self, data):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def write_event(self, event):
        data = self._load()
        event_id = event["event_id"]
        data = [x for x in data if x.get("event_id") != event_id]
        data.append(event)
        self._save(data)

    def retrieve_all(self):
        return self._load()

    def find_similar_anomalies(self, protocol_type, service, exclude_event_id=None):
        matches = []
        for event in self._load():
            if exclude_event_id and event.get("event_id") == exclude_event_id:
                continue
            if (
                event.get("protocol_type") == protocol_type
                and event.get("service") == service
                and event.get("prediction") == "Anomaly"
            ):
                matches.append(event)
        return matches

    def clear(self):
        self._save([])

short_memory = ShortTermMemory(max_events=5)
long_memory = LongTermMemory(MEMORY_PATH)

# Seed initial memory for Scenario 3
def seed_default_history():
    hist_events = [
        {
            "event_id": "test_7527",
            "timestamp": "2026-10-05T14:11:56.931Z",
            "protocol_type": "tcp",
            "service": "http",
            "prediction": "Anomaly",
            "probability": 1.0,
            "base_risk": "HIGH",
            "final_risk": "HIGH",
            "recommendation": "Immediate analyst review"
        },
        {
            "event_id": "test_11868",
            "timestamp": "2026-10-05T14:11:56.942Z",
            "protocol_type": "tcp",
            "service": "http",
            "prediction": "Anomaly",
            "probability": 1.0,
            "base_risk": "HIGH",
            "final_risk": "HIGH",
            "recommendation": "Immediate analyst review"
        }
    ]
    for e in hist_events:
        long_memory.write_event(e)

seed_default_history()

# 3. Perception, Attention, & Inference
def perception(raw_record: dict) -> pd.DataFrame:
    frame = pd.DataFrame([{col: raw_record.get(col, 0) for col in FEATURE_COLS}])
    for col in CATEGORICAL_COLS:
        encoder = label_encoders[col]
        val = str(frame.at[0, col])
        if val not in encoder.classes_:
            val = encoder.classes_[0] # fallback
        frame[col] = encoder.transform([val])
    frame[NUMERICAL_COLS] = scaler.transform(frame[NUMERICAL_COLS])
    return frame.astype(np.float32)

def predict_anomaly(processed_record: pd.DataFrame) -> dict:
    prob = float(rf_model.predict_proba(processed_record)[0, ANOMALY_COLUMN])
    pred = int(prob >= 0.50)
    return {
        "probability": prob,
        "prediction": pred,
        "prediction_name": "Anomaly" if pred else "Normal"
    }

def knowledge_inference(anomaly_probability: float, previous_similar_count: int) -> dict:
    fired_rules = []
    if anomaly_probability >= 0.80:
        base_risk = "HIGH"
        recommendation = "Immediate analyst review"
        fired_rules.append("K1")
    elif anomaly_probability >= 0.50:
        base_risk = "MEDIUM"
        recommendation = "Inspect suspicious connection"
        fired_rules.append("K2")
    else:
        base_risk = "LOW"
        recommendation = "Continue monitoring"
        fired_rules.append("K3")

    final_risk = base_risk
    escalated = False

    # Rule K4 (Cognitive Memory Escalation for Ambiguous/Medium Risk)
    # Applied strictly when ML is uncertain (MEDIUM): checks Long-Term Memory to escalate to HIGH
    if base_risk == "MEDIUM" and previous_similar_count >= 2:
        fired_rules.append("K4")
        escalated = True
        final_risk = "HIGH"
        recommendation = "Escalate to analyst: repeated anomalous protocol/service pattern confirmed in long-term memory (Rule K4)"

    return {
        "base_risk": base_risk,
        "final_risk": final_risk,
        "escalated": escalated,
        "recommendation": recommendation,
        "fired_rules": fired_rules
    }

def run_cognitive_pipeline(raw_record: dict, event_id: str, persist=True) -> dict:
    proto = str(raw_record["protocol_type"])
    service = str(raw_record["service"])
    flag = str(raw_record["flag"])
    now_str = datetime.now(timezone.utc).strftime("%H:%M:%S")

    logs = []
    logs.append(f"[{now_str}] [INGRESS] Packet received: {proto.upper()}/{service} (Flag: {flag}, SrcBytes: {raw_record.get('src_bytes', 0)})")

    # Step 1: Perception
    proc = perception(raw_record)
    logs.append(f"[{now_str}] [PERCEPTION] 41 attributes encoded (LabelEncoder) & scaled (StandardScaler) -> Dense Vector (1, 41)")

    # Step 2: Attention
    top_features = [
        {"feature": "src_bytes", "importance": 0.172, "val": raw_record.get("src_bytes", 0)},
        {"feature": "dst_bytes", "importance": 0.116, "val": raw_record.get("dst_bytes", 0)},
        {"feature": "flag", "importance": 0.080, "val": flag},
        {"feature": "same_srv_rate", "importance": 0.071, "val": raw_record.get("same_srv_rate", 0)},
        {"feature": "dst_host_srv_count", "importance": 0.069, "val": raw_record.get("dst_host_srv_count", 0)}
    ]
    logs.append(f"[{now_str}] [ATTENTION] Focus on top signals: src_bytes, dst_bytes, flag. Suppressed noise: urgent, land")

    # Step 3: Real Model Inference
    model_res = predict_anomaly(proc)
    prob = model_res["probability"]
    pred_name = model_res["prediction_name"]
    logs.append(f"[{now_str}] [ML MODEL] Random Forest predicted: {pred_name} (Anomaly Probability: {prob:.4f})")

    # Step 4: Memory Query
    prev_similar = long_memory.find_similar_anomalies(proto, service, exclude_event_id=event_id)
    prev_count = len(prev_similar)
    logs.append(f"[{now_str}] [MEMORY QUERY] Querying Long-Term Memory for ({proto}, {service}, Anomaly)... Found {prev_count} previous incidents")

    # Step 5: Knowledge Rules & Escalation
    infer = knowledge_inference(prob, prev_count)
    if infer["escalated"]:
        logs.append(f"[{now_str}] [RULE K4 TRIGGERED] Anomaly verified AND >= 2 history matches! Escalating: {infer['base_risk']} ➔ {infer['final_risk']}")
    else:
        logs.append(f"[{now_str}] [RULE {', '.join(infer['fired_rules'])}] Evaluated base risk: {infer['final_risk']}")

    # Step 6: Memory Write
    mem_evt = {
        "event_id": event_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "protocol_type": proto,
        "service": service,
        "prediction": pred_name,
        "probability": round(prob, 4),
        "base_risk": infer["base_risk"],
        "final_risk": infer["final_risk"],
        "recommendation": infer["recommendation"]
    }
    short_memory.remember(mem_evt)
    if persist and (infer["final_risk"] in ["HIGH", "CRITICAL"] or pred_name == "Anomaly"):
        long_memory.write_event(mem_evt)

    action = "ALLOW_AND_LOG"
    if infer["final_risk"] == "LOW": action = "CONTINUE_MONITORING"
    elif infer["final_risk"] == "MEDIUM": action = "INSPECT_SUSPICIOUS"
    elif infer["final_risk"] == "HIGH": action = "QUARANTINE_AND_SOC_ALERT"
    elif infer["final_risk"] == "CRITICAL": action = "BLOCK_IP_AND_DROP"

    logs.append(f"[{now_str}] [ACTION ENFORCED] {action} &bull; {infer['recommendation']}")

    return {
        "event_id": event_id,
        "timestamp": now_str,
        "raw_record": {
            "protocol_type": proto,
            "service": service,
            "flag": flag,
            "src_bytes": raw_record.get("src_bytes", 0),
            "dst_bytes": raw_record.get("dst_bytes", 0),
            "count": raw_record.get("count", 0),
            "srv_count": raw_record.get("srv_count", 0),
            "same_srv_rate": raw_record.get("same_srv_rate", 0),
            "dst_host_srv_count": raw_record.get("dst_host_srv_count", 0),
            "label": str(raw_record.get("label", "unknown"))
        },
        "attention": top_features,
        "probability": prob,
        "prediction": pred_name,
        "previous_similar_count": prev_count,
        "previous_similar_events": prev_similar[-3:],
        "base_risk": infer["base_risk"],
        "final_risk": infer["final_risk"],
        "escalated": infer["escalated"],
        "fired_rules": infer["fired_rules"],
        "recommendation": infer["recommendation"],
        "security_action": action,
        "logs": logs
    }

# 4. FastAPI App Definition
app = FastAPI(title="NetGuard Live Cognitive API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

stream_cursor = 0

@app.get("/api/stream/next")
def stream_next():
    global stream_cursor
    row = test_df.iloc[stream_cursor].to_dict()
    event_id = f"pkt_{stream_cursor}_{datetime.now().strftime('%M%S')}"
    stream_cursor = (stream_cursor + 1) % len(test_df)
    return run_cognitive_pipeline(row, event_id=event_id, persist=True)

@app.get("/api/inject/{attack_type}")
@app.post("/api/inject/{attack_type}")
def inject_attack(attack_type: str):
    if attack_type == "normal":
        # Index 2 in test set: normal ftp_data SF
        row = test_df.iloc[2].to_dict()
        event_id = f"normal_{random.randint(100, 999)}"
        return run_cognitive_pipeline(row, event_id=event_id, persist=False)
    elif attack_type == "neptune":
        # Index 0 in test set: neptune SYN flood REJ
        row = test_df.iloc[0].to_dict()
        event_id = f"neptune_{random.randint(100, 999)}"
        return run_cognitive_pipeline(row, event_id=event_id, persist=True)
    elif attack_type == "apache_back":
        # Index 301 in test set: apache back DoS S2 (Medium probability ~0.65 -> Escalate to High!)
        seed_default_history() # Ensure 2 history incidents are present
        row = test_df.iloc[301].to_dict()
        event_id = f"apache_back_{random.randint(100, 999)}"
        return run_cognitive_pipeline(row, event_id=event_id, persist=True)
    elif attack_type == "portsweep":
        # Search for portsweep
        sweep_rows = test_df[test_df["label"] == "portsweep"]
        row = sweep_rows.iloc[0].to_dict() if not sweep_rows.empty else test_df.iloc[10].to_dict()
        event_id = f"portsweep_{random.randint(100, 999)}"
        return run_cognitive_pipeline(row, event_id=event_id, persist=True)
    else:
        raise HTTPException(status_code=400, detail="Unknown attack type")

class CustomPacketRequest(BaseModel):
    protocol_type: str
    service: str
    flag: str
    src_bytes: int
    dst_bytes: int
    mock_history_count: Optional[int] = 0

@app.post("/api/analyze")
def analyze_custom(req: CustomPacketRequest):
    row = {
        "duration": 0,
        "protocol_type": req.protocol_type,
        "service": req.service,
        "flag": req.flag,
        "src_bytes": req.src_bytes,
        "dst_bytes": req.dst_bytes,
        "land": 0, "wrong_fragment": 0, "urgent": 0, "hot": 0,
        "num_failed_logins": 0, "logged_in": 1 if req.flag == "SF" else 0,
        "num_compromised": 0, "root_shell": 0, "su_attempted": 0, "num_root": 0,
        "num_file_creations": 0, "num_shells": 0, "num_access_files": 0,
        "num_outbound_cmds": 0, "is_host_login": 0, "is_guest_login": 0,
        "count": 5, "srv_count": 5, "serror_rate": 0.0, "srv_serror_rate": 0.0,
        "rerror_rate": 0.0, "srv_rerror_rate": 0.0, "same_srv_rate": 1.0,
        "diff_srv_rate": 0.0, "srv_diff_host_rate": 0.0, "dst_host_count": 50,
        "dst_host_srv_count": 50, "dst_host_same_srv_rate": 1.0,
        "dst_host_diff_srv_rate": 0.0, "dst_host_same_src_port_rate": 0.0,
        "dst_host_srv_diff_host_rate": 0.0, "dst_host_serror_rate": 0.0,
        "dst_host_srv_serror_rate": 0.0, "dst_host_rerror_rate": 0.0,
        "dst_host_srv_rerror_rate": 0.0, "label": "custom_live"
    }

    if req.mock_history_count and req.mock_history_count > 0:
        for i in range(req.mock_history_count):
            long_memory.write_event({
                "event_id": f"injected_{req.protocol_type}_{req.service}_{i}",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "protocol_type": req.protocol_type,
                "service": req.service,
                "prediction": "Anomaly",
                "probability": 0.95,
                "base_risk": "HIGH",
                "final_risk": "HIGH",
                "recommendation": "Mock injected prior incident"
            })

    return run_cognitive_pipeline(row, event_id=f"custom_{random.randint(100, 999)}", persist=True)

@app.get("/api/memory")
def get_memory():
    return {
        "short_term": short_memory.retrieve_recent(),
        "long_term": long_memory.retrieve_all()
    }

@app.get("/api/memory/reset")
@app.post("/api/memory/reset")
def reset_memory():
    short_memory.clear()
    long_memory.clear()
    return {"status": "cleared"}

@app.get("/api/memory/seed")
@app.post("/api/memory/seed")
def seed_memory():
    seed_default_history()
    return {"status": "seeded", "count": len(long_memory.retrieve_all())}

# Mount static frontend
demo_static_dir = Path(__file__).resolve().parent
app.mount("/", StaticFiles(directory=demo_static_dir, html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
