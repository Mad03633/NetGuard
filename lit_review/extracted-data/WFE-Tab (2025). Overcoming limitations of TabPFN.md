**Basic Information**
- Full Title: WFE-Tab: Overcoming limitations of TabPFN in IIoT-MEC environments with a weighted fusion ensemble-TabPFN model for improved IDS performance
- Authors: Sergio Ruiz-Villafranca, José Roldán-Gómez, Javier Carrillo-Mondéjar, José Luis Martinez, Carlos H. Ganán
- Year: Not Reported
- Venue (Journal / Conference): Not Reported

**Problem Definition**
- Problem addressed: TabPFN model has inherent limitations (maximum 1000 training samples and maximum 10 classes) that make it unsuitable for IIoT-MEC intrusion detection where large data volumes and many attack classes exist. The paper aims to overcome these limitations.
- Task type: Intrusion Detection

**Model Information**
- Model Family: Ensemble (based on TabPFN, which is a Prior-Data Fitted Network/Transformer)
- Method Name: WFE-Tab (Weighted Fusion Ensemble-based TabPFN)
- Key Idea: Uses K-Means++ clustering to divide data into subsets, fuses a small proportion (1–20%) of each subset with others (including an anomalous subset), trains multiple specialized TabPFN models, assigns weights to each model based on its performance on a scoring set, and aggregates predictions via weighted voting.
- Architecture details: Four stages: data collection, data preprocessing (clustering + fusion), model training, and model evaluation. The K-Means++ objective minimizes intra-cluster distances (Eq. 1). Fusion creates mixed subsets (Eq. 2). Weights are computed as correct predictions per class over total samples in scoring set (Eq. 3). Final weighted voting (Eq. 5). Algorithm 1 outlines the process.

**Dataset Information**
- Dataset(s) used: Edge-IIoTset
- NSL-KDD used: No
- Feature type: Tabular (network traffic features; 61 features selected from 1176 via ERT algorithm)

**Evaluation (exact values as reported in the paper)**
- Accuracy: 99.57% (WFE-Tab with 15 clients, Table 6, p.12; also Table 7, p.12)
- Precision: 99.81% (WFE-Tab with 15 clients, Table 6, p.12; also Table 7, p.12)
- Recall: 99.82% (WFE-Tab with 15 clients, Table 6, p.12; also Table 7, p.12)
- F1-score: 99.81% (WFE-Tab with 15 clients, Table 6, p.12; also Table 7, p.12)
- AUC: Not Reported
- Detection Rate: Not Reported
- False Positive Rate: Not Reported
- Other metrics: Training-test time: 18.6 seconds for WFE-Tab (15 clients, Table 6, p.12; Table 7, p.12)

**Results**
- Best reported performance: F1-score 99.81%, Accuracy 99.57%, Precision 99.81%, Recall 99.82% (WFE-Tab with 15 clients, Table 6, p.12)
- Comparison with baselines: WFE-Tab outperforms all baseline algorithms (DT, RF, Xgboost, LightGBM, AdaBoost, GradientBoosting, CatBoost) across all metrics. Second-best CatBoost achieved F1-score 95.95% (Table 7, p.12). Also outperforms earlier TabPFN variants: TabPFN (F1 69.79%), SMV (81.36%), EMV (82.64%), CE approach (99.53% with 9 clients) (Table 6, p.12).

**Baselines**
- Models compared against: Decision Tree (DT), Random Forest (RF), Xgboost, LightGBM, AdaBoost, GradientBoosting, CatBoost, plus TabPFN base model, Sequential Majority Voting (SMV), Enhanced Majority Voting (EMV), and Clustering-based Ensemble (CE) TabPFN.

**Analysis**
- Strengths: Overcomes TabPFN limitations (handles >1000 samples and >10 classes); can detect unknown/anomalous attacks via designated anomalous cluster; weighted voting improves reliability; achieves high F1-score (99.81%) with low training-test time (18.6s).
- Limitations: Vulnerable to data poisoning attacks during training; imbalanced classes with few samples may challenge training/scoring; anomalous samples are flagged but not assigned to known classes; only tested on IIoT-MEC environment (Section 7, p.13).
- Real-time capability: Not Reported (training-test time of 18.6s is reported, but real-time inference not explicitly stated)
- Computational complexity: Training complexity: O(N×K×d×i + K×M×|C_k|×I_tra-sco×f(n) + I_tra-sco×∑M_k×S); Prediction complexity: O(∑M_k×P) (Section 3.3, Eq. 6 & 7, p.8)

**Source Locations** (for verification)
- Accuracy 99.57%, Precision 99.81%, Recall 99.82%, F1-score 99.81% → Table 6, p.12; Table 7, p.12
- Training-test time 18.6s → Table 6, p.12; Table 7, p.12
- TabPFN limitations (max 1000 samples, max 10 classes) → Section 1, p.2; Section 3.1.1, p.5
- WFE-Tab methodology (clustering, fusion, weighting) → Section 3.2, p.6-8, Algorithm 1, p.8
- Complexity equations → Section 3.3, Eq. (6) and (7), p.8
- Limitations (poisoning, imbalanced classes, anomalous classification, single domain) → Section 7, p.13
- Dataset Edge-IIoTset description → Section 5.1, p.10, Table 2, p.9

**Relevance to Topic**
high – The paper directly addresses network intrusion detection in IIoT-MEC environments using a novel ensemble method that overcomes key limitations of TabPFN, with state-of-the-art performance and explicit focus on cybersecurity applications.
