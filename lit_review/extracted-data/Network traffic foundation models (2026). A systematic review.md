**Basic Information**
- Full Title: Network traffic foundation models: A systematic review
- Authors: Rubén Pérez-Jove, Cristian R. Munteanu, Julián Dorado, Alejandro Pazos, Jose Vázquez-Naya
- Year: 2026
- Venue (Journal / Conference): Computer Networks (journal)

**Problem Definition**
- Problem addressed: The paper systematically reviews whether it is feasible to develop Network Traffic Foundation Models (NT-FMs) that enable a "train-once, adapt-anywhere" paradigm for automated traffic management, addressing fragmentation in current research. (Section 1, p. 1; Section 3.1, Table 1)
- Task type: Systematic literature review covering Intrusion Detection, Anomaly Detection, Traffic Classification, Traffic Generation, Performance Prediction, etc. (Section 1, p. 1; Section 2.1.1, p. 2)

**Model Information**
- Model Family: Various (Transformer, Graph Neural Network, State Space Model, Autoencoder, Hybrid) – the review analyzes 51 primary studies. (Section 4.1.2, p. 7-9; Table 6, p. 15)
- Method Name: Not applicable (survey paper)
- Key Idea (2-3 concise sentences): Not applicable (survey paper)
- Architecture details (if available): Not applicable (survey paper)

**Dataset Information**
- Dataset(s) used: Multiple public datasets including ISCXVPN2016, ISCXTor2016, USTC-TFC2016, CICIoT2023, CESNET-TLS22, CESNET-QUIC22, NetBench, etc. (Section 5.1.4, Table 8, p. 18-20)
- NSL-KDD used (Yes/No): Not Reported (NSL-KDD not mentioned in the paper)
- Feature type: Various (Flow-based, Packet-based, Raw byte, Statistical, Header/Payload, Graph-based, Multimodal) (Section 5.1.2, Table 7, p. 16)

**Evaluation (exact values as reported in the paper)**
- Accuracy: Not reported for a single model (review reports multiple: e.g., ET-BERT >99.9% precision, YaTC surpasses ET-BERT by up to 6 percentage points on F1, etc. – Section 4.1.2, p. 7-8)
- Precision: Not reported for a single model
- Recall: Not reported for a single model
- F1-score: Not reported for a single model (example: GETRF achieves 99.12% F1 across five tasks – Section 4.1.2, p. 8)
- AUC: Not reported for a single model
- Detection Rate: Not reported for a single model
- False Positive Rate: Not reported for a single model
- Other metrics: Not applicable

**Results**
- Best reported performance: Not applicable (survey paper)
- Comparison with baselines: Not applicable (survey paper)

**Baselines**
- Models compared against: Not applicable (survey paper)

**Analysis**
- Strengths: Comprehensive mapping of NT-FM state of the art (first systematic review on NT-FMs); four-dimensional analysis covering architectures, representations, tasks/environments, and datasets; identifies persistent gaps and proposes research agenda. (Section 1, Contributions, p. 2)
- Limitations: Terabyte-scale corpora are scarce; cross-task transfer remains limited; efficiency techniques only beginning to emerge; most models are "pre-trained domain encoders" not true foundation models; data ecosystem lacks massive, diverse, openly licensed raw traffic corpora. (Abstract, p. 1; Section 6, p. 21)
- Real-time capability (Yes / No / Not Reported): Not Reported (though some models mention inference times, e.g., NetMamba up to 60× faster – Section 5.1.1, p. 14)
- Computational complexity (if mentioned): Transformer NT-FMs have quadratic self-attention; NetMamba (state-space) has linear complexity; GNN-FM scales with edges; efficiency metrics (energy/power) not reported. (Section 5.1.1, p. 14)

**Source Locations** (for verification)
- Feasibility of NT-FMs → Section 6, p. 21
- ET-BERT >99.9% precision → Section 4.1.2, p. 7
- GETRF 99.12% F1 → Section 4.1.2, p. 8
- YaTC surpasses ET-BERT by up to 6 percentage points → Section 4.1.2, p. 8
- NetMamba 60× faster → Section 5.1.1, p. 14
- Data scarcity and limitations → Abstract, p. 1; Section 6, p. 21
- Dataset list → Table 8, p. 18-20

**Relevance to Topic**
High – This systematic review directly focuses on foundation models for network traffic, with extensive coverage of intrusion detection, anomaly detection, and security tasks, providing a comprehensive reference for AI in cybersecurity and NIDS research.
