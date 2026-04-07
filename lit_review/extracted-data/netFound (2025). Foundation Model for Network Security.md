---
**Paper ID:** P01

**Basic Information**
- Full Title: netFound: Foundation Model for Network Security
- Authors: Satyandra Guthula, Roman Beltiukov, Navya Battula, Wenbo Guo, Arpit Gupta, Inder Monga
- Year: 2025
- Venue (Journal / Conference): Not Reported

**Problem Definition**
- Problem addressed: Developing generalizable ML-based solutions for network security that overcome the limitations of supervised learning (e.g., sparse, noisy, skewed labeled data) by leveraging unlabeled network telemetry data.
- Task type (Intrusion Detection / Anomaly Detection / NIDS / etc.): Intrusion Detection, Traffic Classification, Application Fingerprinting, Anomaly Detection, Brute-force Attack Detection

**Model Information**
- Model Family: Foundation Model (Transformer-based)
- Method Name: netFound
- Key Idea (2-3 concise sentences): netFound uses self-supervised learning on abundant unlabeled network telemetry data, incorporating domain-specific designs (multimodal embeddings, protocol-aware tokenization, data-driven token composition, hierarchical transformers) to capture hidden networking context. The pre-trained model can then be fine-tuned for various downstream network security tasks, even with challenging labeled datasets.
- Architecture details (if available): Hierarchical transformer with burst encoder and flow encoder, skip connections, 12 layers, hidden dimension 768, 24 attention heads. Processes up to 12 bursts per flow and 6 packets per burst (max 1296 tokens per flow). Uses [CLS-B] and [CLS-F] tokens for burst and flow representations.

**Dataset Information**
- Dataset(s) used: Campus dataset (own collection), Crossmarket [59], ISCXVPN2016 [60], CIC-IDS-2017 [61], HTTP bruteforce attack detection dataset (netUnicorn [5])
- NSL-KDD used (Yes/No): No
- Feature type: Packet-based / Multimodal (packet fields, temporal details, statistical aggregates, contextual information)

**Evaluation (exact values as reported in the paper)**
- Accuracy: For Crossmarkets (Acc@10): 66.35 ± 0.99% (Table 2, p. 11)
- Precision: Not Reported
- Recall: Not Reported
- F1-score: Traffic Classification (Campus dataset): 96.08 ± 0.04% (Table 2, p. 11); Intrusion Detection (CICIDS2017): 91.02 ± 0.10% and 99.99 ± 0.01% (Table 2, p. 11); HTTP Bruteforce Detection: 99.01 ± 0.01% (Table 2, p. 11)
- AUC: Not Reported
- Detection Rate: Not Reported
- False Positive Rate: Not Reported
- Other metrics: Token prediction F1 scores on pre-training: 85.89% (masked 10%), 85.26% (masked 30%), 83.29% (masked 50%) on Campus 1 dataset (Table 1, p. 9)

**Results**
- Best reported performance: 99.99% F1 on CICIDS2017 intrusion detection task (Table 2, p. 11); 96.08% F1 on traffic classification (Table 2, p. 11)
- Comparison with baselines: netFound outperforms all four baselines (Curtains, nPrintML, ET-BERT, YaTC) across all five downstream tasks with statistically significant margins (p < 0.05 in most cases). For traffic classification, netFound achieves 96.08% vs. next best nPrintML at 87.22% (Table 2, p. 11).

**Baselines**
- Models compared against: Curtains [6], nPrintML [27], ET-BERT [18], YaTC [19]

**Analysis**
- Strengths: Domain-specific design (protocol-aware tokenization, multimodal embeddings, hierarchical transformer); robustness to noisy labels (<5% accuracy drop at 40% noise) and learning shortcuts; handles heavy-tailed sequence distributions; effective pre-training on unlabeled data.
- Limitations: Pre-trained on ~1.8M flows only; impact of more diverse data uncertain; bias and fairness not explored; adversarial robustness not assessed; offline evaluation only (online setup future work).
- Real-time capability (Yes / No / Not Reported): Not Reported (future work mentions online setups)
- Computational complexity (if mentioned): Not Reported; notes handling up to 1296 tokens per flow with hierarchical design to reduce complexity.

**Source Locations** (for verification)
- Key claims and page/section where found (e.g. "Accuracy 98.7% → Section 4.2, Table 3, p. 8"):
  - F1 96.08% on traffic classification → Table 2, p. 11
  - F1 99.99% on CICIDS2017 → Table 2, p. 11
  - Robustness to noisy labels (<5% drop at 40% noise) → Section 6.4, Fig. 5, p. 12
  - Resilience to learning shortcuts (Heartbleed and TCP Options) → Section 6.3, Table 3, p. 12
  - Token prediction F1 scores → Table 1, p. 9
  - Ablation study results → Table 4, p. 13; Fig. 4, p. 10
  - Model architecture (hierarchical transformer with skip connections) → Section 3.4, Section 4.3, pp. 5-8
  - Protocol-aware tokenization → Section 3.1, p. 4; Section 4.1, pp. 6-7

**Relevance to Topic**
high + Directly proposes a foundation model for network security with strong empirical results on intrusion detection, traffic classification, and related tasks, addressing key challenges like label noise and learning shortcuts.
---