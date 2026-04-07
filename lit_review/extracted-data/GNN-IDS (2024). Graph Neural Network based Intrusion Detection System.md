**Basic Information**
- Full Title: GNN-IDS: Graph Neural Network based Intrusion Detection System
- Authors: Zhenlu Sun, Andre M.H. Teixeira, Salman Toor
- Year: 2024
- Venue: The 19th International Conference on Availability, Reliability and Security (ARES 2024)

**Problem Definition**
- Problem addressed: Existing ML-based intrusion detection systems treat each data sample independently and do not capture inter-dependencies of network entities, leading to uncertain predictions, false positives, and false negatives. Additionally, abundant network information such as vulnerabilities is not fully utilized.
- Task type: Intrusion Detection / Anomaly-based IDS (binary classification at node-level: predicting whether a node is under attack or not)

**Model Information**
- Model Family: Graph Neural Network
- Method Name: GNN-IDS
- Key Idea: Incorporate attack graph (static structural information and vulnerabilities) and real-time measurements (dynamic attributes) into a unified graph representation, then use Graph Neural Networks as the inference engine to learn network connectivity, node features, and attack patterns for more reliable intrusion detection.
- Architecture details: Three GNN models are developed: Graph Convolution Network (GCN), Graph Convolution Network with learnable Edge Weights (GCN-EW), and Graph Attention Network (GAT). Input graphs are constructed by concatenating encoded attack graph features (D-dimensional) with real-time measurements (K-dimensional) for each node. For nodes without measurements, zero-padding is applied. All models use 2 hidden layers. GAT uses 4-head attention. Output is a sigmoid layer for binary node-level classification.

**Dataset Information**
- Dataset(s) used: Two synthetic datasets specific to a use case network: Dataset 1 (artificial, measurements follow Gaussian/Poisson distributions) and Dataset 2 (synthetically created using network traffic samples from public CIC-IDS2017 dataset)
- NSL-KDD used: No
- Feature type: Graph-based (nodes have concatenated features from attack graph encoding and real-time measurements; edges represent connectivity in attack graph)

**Evaluation (exact values as reported in the paper)**
- Accuracy: Not Reported (accuracy not reported; F1-score and AUC used)
- Precision: Dataset 1: GAT 86.61%, GCN-EW 86.84%; Dataset 2: GAT 94.74%, GCN-EW 94.14% (Table 4, p.10)
- Recall: Dataset 1: GAT 95.49%, GCN-EW 95.47%; Dataset 2: GAT 98.72%, GCN-EW 98.02% (Table 4, p.10)
- F1-score: Dataset 1: GAT 90.39%, GCN-EW 90.53%; Dataset 2: GAT 96.62%, GCN-EW 95.97% (Table 4, p.10)
- AUC: Dataset 1: GAT 98.87%, GCN-EW 98.94%; Dataset 2: GAT 99.72%, GCN-EW 99.65% (Table 4, p.10)
- Detection Rate: Not explicitly reported; recall can be considered detection rate for malicious class.
- False Positive Rate: Dataset 1: GAT 3.73%, GCN-EW 3.63%; Dataset 2: GAT 1.27%, GCN-EW 1.40% (Table 4, p.10)
- Other metrics: False Negative Rate (FNR) reported in Table 5 for robustness evaluation (e.g., Dataset 2 original vs noisy: GAT FNR change +6.00%, GCN-EW +2.86%, GCN +1.57%)

**Results**
- Best reported performance: For Dataset 2 (more realistic): GAT achieves Precision 94.74%, Recall 98.72%, F1-score 96.62%, AUC 99.72%, FPR 1.27% (Table 4, p.10). For Dataset 1: GCN-EW achieves slightly better F1 (90.53%) and AUC (98.94%) than GAT, but differences are small.
- Comparison with baselines: GNN models (GCN, GCN-EW, GAT) outperform classical Neural Network (NN) on all standard metrics for Dataset 1. For Dataset 2, GNN models achieve superior performance especially in Precision, F1-score, and FPR. GNN models also show smaller performance degradation when adding noise, indicating higher robustness (Table 5, p.12). ROC curves (Fig. 7, p.10) and AUC improvements (e.g., Dataset 1 AUC +5% for GNN) demonstrate more confident predictions.

**Baselines**
- Models compared against: Classical Neural Network (NN) with architecture: ReLU(Linear(K,20)), ReLU(Linear(20,20)), Sigmoid(Linear(20,1)) – inputs are individual samples (not graph-structured) (Table 3, p.10)

**Analysis**
- Strengths: GNN-IDS provides more confident predictions (lower uncertainty) by learning network topology and node interdependencies; predictions are explainable via GNNExplainer (identifying important neighboring nodes and features); robust to evolving networks (adversarial noise) due to stable latent representations.
- Limitations: Structural evolution of computer networks (changes in graph topology over time) and intra-dependencies between sequential input graphs are not studied. Temporal relations among time series data need deeper investigation. The approach relies on action-level measurements and assumes at most one asset attacked at a time.
- Real-time capability: Not Reported (but deployment steps mention "real-time measurements" and "snapshots" at time t; no explicit latency or throughput numbers)
- Computational complexity: Not Reported

**Source Locations** (for verification)
- Precision/Recall/F1/AUC/FPR values → Section 5.2, Table 4, p.10
- ROC curves and AUC improvements → Section 5.2, Figure 7, p.10
- Robustness results (Table 5) → Section 5.2, Table 5, p.12
- Model architectures → Section 5.1, Table 3, p.10
- Dataset descriptions → Section 4.2, pp.8-9
- Explainability with GNNExplainer → Section 5.2, Figures 9-10, pp.10-11
- Limitations (structural evolution, temporal relations) → Section 6, p.12

**Relevance to Topic**
high – The paper directly addresses network intrusion detection using Graph Neural Networks, a core topic in AI for cybersecurity, and provides detailed evaluation on uncertainty, explainability, and robustness.
