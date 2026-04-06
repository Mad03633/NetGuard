# Next-Generation AI for Network Anomaly Detection

This repository contains the implementation for the **Introduction to Multi-Agent Systems**:

**Next-Generation AI for Network Anomaly Detection: Comparative Analysis of Transformer, Graph Neural Networks, and Foundation Models on NSL-KDD Dataset**

**Author:** Madiyar Bolatov, Angsar Shaumen
**Supervisor:** Professor, Dr. PhD Seema Rawat 
**Program:** Applied Artificial Intelligence (MSc), Astana IT University  
**Year:** 2026

## Overview

This project presents a comparative study of modern machine learning approaches for **network anomaly detection** using the NSL-KDD dataset.

The goal is to evaluate the effectiveness of next-generation AI models in identifying malicious network activity and to analyze trade-offs between classical, deep learning, and foundation-style models.

---

## Models Compared

The following approaches are implemented and evaluated:

- **FT-Transformer (Feature Tokenizer Transformer)**  
  Transformer-based model for tabular data where each feature is treated as a token.

- **Graph Neural Network (GNN)**  
  Models relationships between samples using graph structure.

- **TabPFN (Foundation Model for Tabular Data)**  
  Pretrained transformer designed for small tabular datasets.

- **Random Forest (Baseline)**  
  Classical ensemble method used as a benchmark.

---

## Objectives

- Perform **Exploratory Data Analysis (EDA)** on NSL-KDD dataset  
- Preprocess network traffic data for machine learning  
- Implement and train multiple AI models  
- Compare models using standard evaluation metrics  
- Save trained models and results for reproducibility

---

## Dataset

The project uses the **NSL-KDD dataset**, an improved version of the KDD Cup 1999 dataset.

### Files
- `KDDTrain+.txt`
- `KDDTest+.txt`

### Task
Binary classification:
- `0` → Normal traffic  
- `1` → Anomaly (attack)

---

## Installation

### Python version
Python 3.10 is required (important for compatibility)

### 1. Create virtual environment

```bash
py -3.10 -m venv venv310
```

### 2. Activate environment

Windows:
```bash
venv310\Scripts\activate
```

Linux / Mac:
```bash
source venv310/bin/activate
```

### 3. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```