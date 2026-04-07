# Comprehensive Literature Analysis: Next-Generation AI for Network Anomaly Detection

## 1. Paper Identification
P1 — Network Intrusion Detection with Edge-Directed Graph Multi-Head Attention Networks
P2 — Analysis of NSL-KDD for the Implementation of Machine Learning in Network Intrusion Detection System
P3 — Towards a Graph-based Foundation Model for Network Traffic Analysis
P4 — DIGNN-A: Real-Time Network Intrusion Detection with Integrated Neural Networks Based on Dynamic Graph
P5 — Enhancing Intrusion Detection Using Random Forest and SMOTE on the NSL-KDD Dataset
P6 — Foundation Models for Cybersecurity. A Comprehensive Multi-Modal Evaluation of TabPFN
P7 — Optimizing IoT Intrusion Detection—A Graph Neural Network Approach with Attribute-Based Graph Construction
P8 — Adaptive multi-view transformer ensemble for intrusion detection: Addressing data imbalance and enhancing attack classification
P9 — Transformer Tokenization Strategies for NIDS
P10 — CAGN-GAT Fusion: A Hybrid Contrastive Attentive Graph Neural Network for Network Intrusion Detection
P11 — FlowTransformer: A transformer framework for flow-based network intrusion detection systems
P12 — GNN-IDS: Graph Neural Network based Intrusion Detection System
P13 — IDS-INT: Intrusion detection system using transformer-based transfer learning for imbalanced network traffic
P14 — Network traffic foundation models: A systematic review
P15 — WFE-Tab: Overcoming limitations of TabPFN in IIoT-MEC environments with a weighted fusion ensemble-TabPFN model for improved IDS performance
P16 — netFound: Foundation Model for Network Security

---

## 2. Comparison Tables

### Table 1 — Paper Overview
| Paper ID | Year | Model Family | Task Type | NSL-KDD Used |
|---|---|---|---|---|
| P1 | 2023 | Graph Neural Network | NIDS | No |
| P2 | 2024 | Classical Machine Learning | Intrusion Detection | Yes |
| P3 | 2024 | Graph Neural Network / Foundation Model | Intrusion Detection / Botnet | No |
| P4 | 2025 | Hybrid | NIDS | No |
| P5 | 2025 | Classical Machine Learning | Intrusion Detection | Yes |
| P6 | 2025 | Foundation Model | Intrusion Detection | No |
| P7 | 2025 | Graph Neural Network | NIDS | No |
| P8 | 2026 | Hybrid | NIDS | Yes |
| P9 | 2026 | Transformer | NIDS | No |
| P10 | 2025 | Hybrid | NIDS | Yes |
| P11 | 2024 | Transformer | NIDS | Yes |
| P12 | 2024 | Graph Neural Network | Intrusion Detection | No |
| P13 | 2024 | Hybrid | NIDS | Yes |
| P14 | 2026 | Various (Review) | Traffic Classification / NIDS | Not Reported |
| P15 | 2025 | Hybrid | Intrusion Detection | No |
| P16 | 2025 | Foundation Model | Intrusion Detection | No |

### Table 2 — Model Comparison
| Paper ID | Method Name | Key Idea |
|---|---|---|
| P1 | EDGMAT | Multi-head attention GNN that aggregates nodes/edges with different weights accounting for edge directionality. |
| P2 | Decision Tree | Comparison of classic ML models via CRISP-DM methodology. |
| P3 | Spatio-temporal GNN | Self-supervised link prediction on spatio-temporal graphs for transfer learning on downstream tasks. |
| P4 | DIGNN-A | Converts dynamic graph snapshots to line graphs, using TransformerConv and GCNII-GRU to catch temporality. |
| P5 | RF-SMOTE | Random Forest with Synthetic Minority Over-sampling to detect rare minority classes effectively. |
| P6 | TabPFN / TabICL | Pre-trained tabular foundation models without per-dataset training, overcoming rare threat detection gaps. |
| P7 | TKSGF / GraphSAGE | Top-K similarity attribute graph construction instead of physical connections for GraphSAGE induction. |
| P8 | AMTE-IDS | Adaptive Multi-View Transformer Ensemble with GAN-based synthetic sample generation for data imbalance. |
| P9 | STO / FTT | Isolating tokenization strategy impact, proving sample-wise tokenization vastly outperforms feature-wise. |
| P10 | CAGN-GAT Fusion | Fusing contrastive learning with attention-based message passing for generalized discriminative embeddings. |
| P11 | FlowTransformer | Modular framework testing variable tokenization, shallow/deep transformers, and classification heads. |
| P12 | GNN-IDS | Incorporating static vulnerability attack graphs with real-time network measurements into GNN. |
| P13 | IDS-INT | Transfer learning via BERT embedded into CNN-LSTM models with SMOTE for minority classes. |
| P14 | Systematic Review | Analyzes the feasibility, limitations, and future mapping of Network Traffic Foundation Models. |
| P15 | WFE-Tab | Fixes TabPFN limits using data clustering, fusion, and weighted ensemble over multiple base instances. |
| P16 | netFound | Universal foundational transformer trained via self-supervision on telemetry with hierarchical representations. |

### Table 3 — Dataset Comparison
| Paper ID | Datasets | Feature Type |
|---|---|---|
| P1 | BoT-IoT, ToN-IoT, NF-BoT-IoT, NF-ToN-IoT | Flow-based |
| P2 | NSL-KDD | Tabular |
| P3 | UNSW-NB15, ToN-IoT, BoT-IoT, CTU13, UPC-COMNET14 | Flow-based |
| P4 | UNSW-NB15, NF-ToN-IoT-v2 | Graph-based (from flow) |
| P5 | NSL-KDD | Tabular |
| P6 | CIC-IDS2017, N-BaIoT, CIC-UNSW | Tabular / Flow-based |
| P7 | NF-BoT-IoT, NF-ToN-IoT | Flow-based |
| P8 | NSL-KDD, UNSW-NB15, CIC-IDS2017 | Tabular / Flow-based |
| P9 | CICIDS2017 | Tabular / Flow-based |
| P10 | NSL-KDD, UNSW-NB15, CICIDS2017, KDD Cup 99 | Tabular / Flow-based |
| P11 | NSL-KDD, UNSW-NB15, CSE-CIC-IDS2018, MQTT, etc. | Flow-based |
| P12 | Synthetic Use Case | Graph-based |
| P13 | UNSW-NB15, CIC-IDS2017, NSL-KDD | Flow-based |
| P14 | ISCXVPN2016, CICIoT2023, CESNET, etc. | Various |
| P15 | Edge-IIoTset | Tabular |
| P16 | Campus, Crossmarket, CICIDS2017, ISCXVPN | Packet-based / Multimodal |

### Table 4 — Performance Comparison
| Paper ID | Best Accuracy | Best F1-Score | False Positive Rate |
|---|---|---|---|
| P1 | Not Reported | 0.99 | Not Reported |
| P2 | 80% | Not Reported | Not Reported |
| P3 | Not Reported | Not Reported | Not Reported |
| P4 | 99.96% | 0.9997 | 0.03% |
| P5 | 99.78% | 99.79% | Not Reported |
| P6 | 99.59% | 1.0000 | Not Reported |
| P7 | Not Reported | 1.0000 | Not Reported |
| P8 | 98.2% | 97.7% | 1.8% |
| P9 | 95.22% | 93.54% | Not Reported |
| P10 | 0.9950 | 0.9836 | Not Reported |
| P11 | Not Reported | 99.90% | 0.55% |
| P12 | Not Reported | 96.62% | 1.27% |
| P13 | 99.21% | 99.0% | Not Reported |
| P14 | Not Applicable | Not Applicable | Not Applicable |
| P15 | 99.57% | 99.81% | Not Reported |
| P16 | 66.35% (Acc@10) | 99.99% | Not Reported |

### Table 5 — Deployment Capability
| Paper ID | Real-time Capability | Computational Complexity |
|---|---|---|
| P1 | Not Reported | Needs reduction in GPU memory |
| P2 | Not Reported | Not Reported |
| P3 | Not Reported | 732,000 parameters |
| P4 | Yes | 65.02ms per snapshot |
| P5 | Not Reported | Hardware specification mentioned |
| P6 | Not Reported | High VRAM; latency up to 97 min on whole datasets |
| P7 | Not Reported | Up to 1000+ seconds runs |
| P8 | Yes | 0.35ms latency |
| P9 | No | Not Reported |
| P10 | Not Reported | 0.16 MB memory |
| P11 | Yes | 8,534 flows/sec throughput |
| P12 | Not Reported | Not Reported |
| P13 | Not Reported | High |
| P14 | Not Reported | Quadratic for Transformers |
| P15 | Not Reported | 18.6s train-test |
| P16 | Not Reported | Up to 1296 tokens processed |

---

## 3. Paper Grouping

### 1. Transformer-based methods (P9, P11)
**Short Summary:** These papers apply standard Transformer architectures focusing heavily on optimizing the tokenization configuration (sample-wise vs. feature-wise) to maximize temporal pattern learning from tabular and flow data.
**Common Techniques:** Attention mechanisms, dense embeddings, varying classification heads.
**Strengths:** Exceptional extraction of long-term flow dependencies; highly configurable.
**Limitations:** Often lacks native support for imbalanced classes unless customized; prone to quadratic sequence scaling and high logic latency.

### 2. Graph Neural Network methods (P1, P7, P12)
**Short Summary:** Represents traffic as network topologies or attribute similarities to use neighbor-aggregation techniques.
**Common Techniques:** GraphSAGE, GAT, Top-K Node Similarity, integration of edge directional features.
**Strengths:** Captures relational connections, topological behaviors, and complex node interactions that sequential models miss. Highly competitive accuracy margins.
**Limitations:** Struggles immensely with sparse or dynamically growing datasets; computation scales heavily with edge count and dynamic snapshots.

### 3. Foundation Models (P3, P6, P14, P16)
**Short Summary:** Employs massive pre-trained variants (LLMs or tabular priors) on huge telemetry data to enable a "train-once, adapt-anywhere" zero-shot or few-shot capability.
**Common Techniques:** Self-supervised link or token prediction, TabPFN, multi-modal mapping.
**Strengths:** Phenomenal generalization; handles minority attack classes with very low training iterations post-pretraining. 
**Limitations:** Extreme GPU footprint (e.g., 20GB+ VRAM required), slow inference, and lack of massive open-license pre-training data.

### 4. Hybrid Methods (P4, P8, P10, P13, P15)
**Short Summary:** Combines two or more advanced paradigms (e.g., GNN + Attention, Transformer + Ensembles, CNN + LSTMs + Transformers).
**Common Techniques:** Multi-view paths, Contrastive learning, SMOTE/GAN integration for balance.
**Strengths:** Produces SOTA architectures (often >99.5% F1) actively balancing both spatial and temporal dynamics while negating class bias.
**Limitations:** Pipelines are rigid to build, extremely resource-intensive to train, and suffer from opaqueness (black-box).

### 5. Traditional Methods (P2, P5)
**Short Summary:** Explores standard classical ML models enhanced by strict methodology rules and statistical data augmentation.
**Common Techniques:** CRISP-DM methodology, Random Forest, SMOTE.
**Strengths:** Transparent, exceptionally fast to train, require minimal physical resources.
**Limitations:** High false alarms in real deployment; struggle with generalization and zero-day threat detection compared to deep methods.

---

## 4. Cross-Paper Analysis

- **Most used datasets:** NSL-KDD (5 papers), UNSW-NB15 (6 papers), CIC-IDS2017 (6 papers). Newer studies focus distinctly on IoT datasets (NF-BoT-IoT).
- **Most used metrics:** Accuracy and F1-score are overwhelmingly favored. F1 is treated as the primary benchmark to justify minority-class resilience.
- **Performance trends:** The reviewed literature reflects a ceiling limit where most modern frameworks easily reach 98%-99.9% F1-score on standard sets. The major trend is transitioning the performance focus from raw scoring to model generalization (zero-shot transfer via foundation models) and solving strict class imbalances.
- **Strengths and weaknesses:** GNNs dominate topological context but fall behind in temporal sequence modeling without hybrid integration. Transformers are highly accurate on flow streams but require careful tokenization. Foundation models solve few-shot obstacles but are actively held back by inference latency, meaning traditional or hybrid models still edge them out in realistic "real-time" capability tests.

---

## 5. Research Gap Analysis
1. **Real-time Latency Constraints:** While models push limits up to 99.9% detection, most Foundation Models and heavy Hybrids completely lack reporting on strict real-time throughput logic (latency <1ms).
2. **True Class Imbalance Solutions:** Utilizing naive SMOTE or basic GANs works mathematically, but creates synthetic noise. Generating true, native robustness to extremely rare threats (zero-day samples) strictly from architecture behavior remains difficult outside of few-shot foundation models.
3. **Absence of Unified Pre-training Corpora:** The rise of Network Traffic Foundation Models is heavily hampered by the lack of terabyte-size, universally open datasets, forcing papers to use synthetic or highly limited academic domains.
4. **Explainability Deficits:** Even as model complexity rises, transparent AI operations (e.g., LIME or SHAP integration) are only briefly explored in a tiny fraction of the models (e.g., P12, P13).

---

## 6. Literature Review

### Background
Intrusion Detection Systems (IDS) sit at the core of modern cybersecurity frameworks. Driven by the evolution of deep learning, contemporary network traffic analysis increasingly relies on methods bridging disparate patterns found within highly imbalanced network flow datasets. Advanced modeling techniques, particularly across Transformer architectures, Graph Neural Networks (GNNs), and newer Foundation Models, continue to push bounds on detecting unknown, minority attacks typically lost to statistical averaging.

### Transformer-based methods
Transformers approach network traffic as sequential flow, overcoming previous limits in Recurrent Neural Networks via parallel processing and attention calculation. Research (P9, P11) clearly isolates that optimization of classification heads and sample-wise tokenization alone can bridge up to a 37% gap in accuracy. Despite excelling at long-term dependencies within packet payloads, native architectures fail to intuitively grasp network topologies.

### Graph Neural Network methods
Operating on structural attributes, GNNs (P1, P7, P12) treat nodes as IP boundaries or traffic subsets. The transition from pure physical connection links to dynamically attributed links (Top-K similarities) has notably improved intrusion inference by mapping relationships rather than flat flow. Yet, as network streams compound continually, large graph sizes generate extreme spatial complexity limitations.

### Foundation model methods
Network Foundation Models (P3, P6, P14, P16) aim to introduce a definitive "train-once, adapt-everywhere" landscape. Utilizing zero-shot and few-shot capabilities, pre-trained frameworks such as TabPFN and netFound handle imbalanced structures and unseen zero-day attacks exponentially better than training from scratch. However, the models currently face astronomical hurdles concerning graphic memory throughput and the necessity of massive, open pre-training traffic corpora.

### Hybrid methods
To offset individual modality weaknesses, many solutions merge structures (P4, P8, P10, P13, P15). Methodologies combining dynamic GNN snapshots with sequence-focused Transformer attention modules yield State-of-the-Art performance bounds (>99% accuracy/F1). Further combinations with Generative Adversarial Networks actively stabilize minority-class representations, making them functionally robust at the cost of processing speed and transparency.

### Comparative discussion
An analysis across the frameworks places pure performance roughly on par between advanced GNN structures, Hybrids, and tailored Transformers. The definitive operational trade-off remains generalization versus latency. Foundation models generalize perfectly to disparate tasks (botnet routing vs network anomalies) but fail runtime inference requirements for deployment. Conversely, Hybrid Transformers offer near-real-time checks but may overfit specifically to their trained boundaries. 

### Research gaps
As indicated by literature, existing gaps are profoundly tied to operational deployment. Future network anomaly detection must migrate from offline, accuracy-centered benchmarking utilizing older datasets (like NSL-KDD) to unified tracking of concept drift and zero-day explainability. Shrinking robust Foundation Models into real-time deployable spaces represents the immediate frontier for AI network security.

---

## 7. References
[1] Xiang Li et al. "Network Intrusion Detection with Edge-Directed Graph Multi-Head Attention Networks." 2023.
[2] Yuliana et al. "Analysis of NSL-KDD for the Implementation of Machine Learning in Network Intrusion Detection System." 2024.
[3] Louis Van Langendonck et al. "Towards a Graph-based Foundation Model for Network Traffic Analysis." *GNNet '24*, 2024.
[4] Jizhao Liu and Minghao Guo. "DIGNN-A: Real-Time Network Intrusion Detection with Integrated Neural Networks Based on Dynamic Graph." *CMC*, 2025.
[5] Febri Hidayat Saputra et al. "Enhancing Intrusion Detection Using Random Forest and SMOTE on the NSL-KDD Dataset." 2025.
[6] P. García et al. "Foundation Models for Cybersecurity. A Comprehensive Multi-Modal Evaluation of TabPFN." 2025.
[7] Tien Ngo et al. "Optimizing IoT Intrusion Detection—A Graph Neural Network Approach with Attribute-Based Graph Construction." *Information*, 2025.
[8] Md Mehedi Hasan et al. "Adaptive multi-view transformer ensemble for intrusion detection: Addressing data imbalance and enhancing attack classification." *Internet of Things*, 2026.
[9] G. Aksholak et al. "Transformer Tokenization Strategies for NIDS." *Computers*, 2026.
[10] Md Abrar Jahin et al. "CAGN-GAT Fusion: A Hybrid Contrastive Attentive Graph Neural Network for Network Intrusion Detection." 2025.
[11] Liam Daly Manocchio et al. "FlowTransformer: A transformer framework for flow-based network intrusion detection systems." *Expert Systems With Applications*, 2024.
[12] Zhenlu Sun et al. "GNN-IDS: Graph Neural Network based Intrusion Detection System." *ARES 2024*, 2024.
[13] Farhan Ullah et al. "IDS-INT: Intrusion detection system using transformer-based transfer learning for imbalanced network traffic." *Digital Communications and Networks*, 2024.
[14] Rubén Pérez-Jove et al. "Network traffic foundation models: A systematic review." *Computer Networks*, 2026.
[15] Sergio Ruiz-Villafranca et al. "WFE-Tab: Overcoming limitations of TabPFN in IIoT-MEC environments with a weighted fusion ensemble-TabPFN model for improved IDS performance." 2025.
[16] Satyandra Guthula et al. "netFound: Foundation Model for Network Security." 2025.
