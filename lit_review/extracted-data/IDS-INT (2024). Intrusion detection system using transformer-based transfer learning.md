**Basic Information**
- Full Title: IDS-INT: Intrusion detection system using transformer-based transfer learning for imbalanced network traffic
- Authors: Farhan Ullah, Shamser Ullah, Gautam Srivastava, Jerry Chun-Wei Lin
- Year: 2024
- Venue (Journal / Conference): Digital Communications and Networks

**Problem Definition**
- Problem addressed: Detecting network intrusions (various types of attacks) in imbalanced network traffic with complex features, where normal traffic samples surpass minority attacks, making it challenging to identify specific attacks.
- Task type: Intrusion Detection / Network Intrusion Detection System (NIDS)

**Model Information**
- Model Family: Transformer-based Transfer Learning + Hybrid Deep Learning (CNN-LSTM)
- Method Name: IDS-INT (Intrusion Detection System using transformer-based transfer learning for Imbalanced Network Traffic)
- Key Idea: Use transformer-based transfer learning (BERT large) to learn detailed feature interactions from network traffic descriptions; apply SMOTE to balance minority attacks; extract deep features with CNN; and detect attacks using a hybrid CNN-LSTM model.
- Architecture details: BERT large (24 encoder layers, 1024 hidden size, 16 self-attention heads, 340M parameters) for feature extraction; SMOTE for oversampling; 1-D CNN with four convolution layers (64,128,156,512 filters) plus max-pooling, dropout, batch normalization; followed by LSTM layers with input, forget, output gates; final fully connected layer for classification.

**Dataset Information**
- Dataset(s) used: UNSW-NB15, CIC-IDS2017, NSL-KDD
- NSL-KDD used: Yes
- Feature type: Flow-based (tabular features derived from PCAP, including basic, contents, connection, time subsets)

**Evaluation (exact values as reported in the paper)**
- Accuracy: 99.21% (UNSW-NB15, basic subset, CNN-LSTM)
- Precision: 99% (UNSW-NB15, basic subset, CNN-LSTM)
- Recall: 100% (UNSW-NB15, basic subset, CNN-LSTM)
- F1-score: 99% (UNSW-NB15, basic subset, CNN-LSTM)
- AUC: Not Reported
- Detection Rate: 99% (reported as Recall for some attacks)
- False Positive Rate: Not Reported
- Other metrics: Confusion matrices for each dataset; for CIC-IDS2017: Web Attacks Accuracy 99.32%; for NSL-KDD KDDTrain+: Accuracy 98.1%, Precision 99%, Recall 98%, F1-score 97%.

**Results**
- Best reported performance: On UNSW-NB15 basic subset with CNN-LSTM: Precision 99%, Recall 100%, F1-score 99%, Accuracy 99.21%. On CIC-IDS2017: Web Attacks Accuracy 99.32%. On NSL-KDD: KDDTest+ Accuracy 98.45%.
- Comparison with baselines: Outperforms CNN-RNN and CNN-GRU across all datasets and subsets. For UNSW-NB15 basic, CNN-RNN Accuracy 97.14%, CNN-GRU Accuracy 94.20%; proposed CNN-LSTM achieves 99.21%.

**Baselines**
- Models compared against: CNN-RNN, CNN-GRU

**Analysis**
- Strengths: Addresses class imbalance via SMOTE; uses transformer-based transfer learning (BERT large) for semantic feature extraction; explainable AI (LIME, SHAP) for model interpretability; high accuracy across multiple standard datasets.
- Limitations: Not Reported explicitly; computational complexity mentioned as high for deep learning but not quantified; real-time capability not explicitly stated.
- Real-time capability: Not Reported
- Computational complexity: Not Reported

**Source Locations** (for verification)
- Accuracy 99.21% → Table 6, p. 11 (UNSW-NB15 basic CNN-LSTM)
- Precision 99%, Recall 100%, F1-score 99% → Table 6, p. 11
- BERT large architecture (24 layers, 1024 hidden, 16 heads, 340M params) → Section 1, p. 2
- SMOTE oversampling equation → Section 3.3, p. 5, Equation (1)
- CNN-LSTM architecture and equations → Section 3.5, p. 6, Equation (3) and Fig. 5
- Datasets (UNSW-NB15, CIC-IDS2017, NSL-KDD) → Section 4.1, p. 7, Tables 2,4,5
- Comparison with CNN-RNN and CNN-GRU → Table 6, p. 11; Table 7, p. 11; Table 8, p. 11
- Explainable AI (LIME, SHAP) → Section 4.4, p. 11-14, Figs. 11-16

**Relevance to Topic**
high – The paper directly focuses on network intrusion detection using transformer-based transfer learning and addresses imbalanced traffic, which is a core topic in AI for cybersecurity.
