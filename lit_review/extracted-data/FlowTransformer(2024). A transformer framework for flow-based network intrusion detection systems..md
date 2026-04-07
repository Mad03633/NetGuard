**Basic Information**
- Full Title: FlowTransformer: A transformer framework for flow-based network intrusion detection systems
- Authors: Liam Daly Manocchio, Siamak Layeghy, Wai Weng Lo, Gayan K. Kulatilleke, Mohanad Sarhan, Marius Portmann
- Year: 2024
- Venue (Journal / Conference): Expert Systems With Applications

**Problem Definition**
- Problem addressed: Implementing transformer-based Network Intrusion Detection Systems (NIDSs) for flow-based network traffic is challenging due to critical decisions about input encoding, transformer model selection, and classification heads. No existing work provides systematic evaluation of these components in the NIDS domain.
- Task type: Network Intrusion Detection / NIDS (binary classification of benign vs malicious flows)

**Model Information**
- Model Family: Transformer
- Method Name: FlowTransformer
- Key Idea: FlowTransformer is a modular framework that enables systematic evaluation of transformer-based NIDS by allowing interchangeable components (input encoding, transformer model, classification head). It captures long-term dependencies in network flow sequences and identifies optimal configurations for performance, model size, and speed.
- Architecture details: Three main components: (1) input encoding module (transforms flow records into fixed-length vectors via categorical-only or record-level embedding/projection), (2) transformer blocks (encoder or decoder, shallow or deep including GPT-2.0 and BERT), (3) classification head (converts sequential output to classification: Last Token, Flatten, Featurewise Embedding, Featurewise Projection, Global Average Pooling, or CLS token). Built as TensorFlow Keras model.

**Dataset Information**
- Dataset(s) used: NSL-KDD, UNSW-NB15, CSE-CIC-IDS2018, plus additional: MQTT-IoT-IDS2020, CSE-CIC-IDS2018 (newer version), TON-IOT
- NSL-KDD used: Yes
- Feature type: Flow-based (tabular flow records with categorical and numerical features)

**Evaluation (exact values as reported in the paper)**
- Accuracy: Not Reported
- Precision: Not Reported
- Recall: Not Reported
- F1-score: 98.00% (NSL-KDD, best model), 99.62% (CSE-CIC-IDSv2), 90.45% (UNSW-NB15), 99.90% (MQTT) — from Table 4, p. 12
- AUC: Not Reported
- Detection Rate: 98.48% (NSL-KDD best model, Table 3, p. 11)
- False Positive Rate: 0.55% (NSL-KDD best model, Table 3, p. 11)
- Other metrics: Model parameters (e.g., 186K to 123M), training throughput (flows/s), inference throughput (flows/s), training time (25.5 seconds for best model on CSE-CIC-IDS, Table 5, p. 12)

**Results**
- Best reported performance: F1 score of 99.90% on MQTT dataset (Table 4, p. 12). On benchmark datasets: 98.00% F1 on NSL-KDD, 97.05% on CSE-CIC-IDS2018, 90.45% on UNSW-NB15 (Table 4, p. 12).
- Comparison with baselines: Outperforms state-of-the-art on NSL-KDD (98.00% vs. 88.20% from Liu & Wu, 2023). On CSE-CIC-IDS, achieves 97.05% F1 compared to RTIDS (99.17%) but with much faster training (25.5s vs. 195.6s) and far faster than CNN-Transformer (7,350s) (Table 5, p. 12).

**Baselines**
- Models compared against: RTIDS (Wu et al., 2022), VIT (Yang et al., 2022), CNN-Transformer (Zhang & Wang, 2022), and the model by Liu & Wu (2023) — from Table 5, p. 12.

**Analysis**
- Strengths: Modular framework enabling systematic evaluation of transformer components; identifies that classification head choice is most critical (Last Token works best); shows shallow transformers are sufficient; record-level encoding reduces model size by >50% without performance loss; fast training and inference.
- Limitations: Does not address transferability, concept drift, explainability, or open-world applications out-of-the-box; limited to flow-based data; requires sequences of flows.
- Real-time capability: Yes — inference throughput reported (e.g., 8,534 flows/s for shallow encoder on CSE dataset, Table 3, p. 11) indicates real-time processing capability.
- Computational complexity: Reported in model parameters (shallow encoder ~186K–1.3M; deep GPT/BERT ~29M–123M) and throughput (flows per second). No theoretical complexity (e.g., O(n²)) given.

**Source Locations** (for verification)
- F1 98.00% on NSL-KDD → Table 4, p. 12 and Table 5, p. 12
- F1 99.90% on MQTT → Table 4, p. 12
- Classification head most critical factor → Section 8.3, p. 9-10; Fig. 11, p. 10
- Last token classification head best → Fig. 11, p. 10; Section 8.3, p. 10
- Record level embedding reduces model size by >50% → Section 8.1, p. 8; Table 2, p. 9
- Training time 25.5s → Table 5, p. 12
- Shallow models outperform deeper models → Fig. 8, p. 9; Section 8.2, p. 9
- Framework architecture → Section 5, p. 4-5; Fig. 2, p. 3; Fig. 6, p. 7

**Relevance to Topic**
High — The paper directly addresses transformer-based network intrusion detection systems for flow-based traffic, a core application of AI in cybersecurity, and provides systematic evaluation and design guidelines.
