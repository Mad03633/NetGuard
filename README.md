# Next-Generation AI for Network Anomaly Detection

This repository contains the implementation for the **Introduction to Multi-Agent Systems**:

**Next-Generation AI for Network Anomaly Detection: Comparative Analysis of Transformer, Graph Neural Networks, and Foundation Models on NSL-KDD Dataset**

**Author:** Madiyar Bolatov, Angsar Shaumen
**Supervisor:** Professor, Dr. PhD Seema Rawat 
**Program:** Applied Artificial Intelligence (MSc), Astana IT University  
**Year:** 2026

## Overview

This project implements a comparative study of modern machine learning approaches for network anomaly detection using the NSL-KDD dataset. The goal is to evaluate the effectiveness of next-generation AI models in detecting malicious network activity.

The study compares three advanced paradigms:

- Transformer-based tabular model
- Graph Neural Network (GNN)
- Foundation-style tabular model (TabPFN)

Additionally, a classical baseline (Random Forest) is included for comparison.

---

## Objectives

- Perform exploratory data analysis (EDA) on NSL-KDD dataset
- Preprocess network traffic data for machine learning
- Implement and train multiple AI models
- Compare models using standard evaluation metrics
- Save trained models and results for reproducibility

---

## Dataset

The project uses the NSL-KDD dataset, an improved version of the KDD Cup 1999 dataset.

Files:
- `KDDTrain+.txt`
- `KDDTest+.txt`

Task:
- Binary classification: Normal vs Anomaly

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