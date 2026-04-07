# 🛡️ Sentino-Sentinel: Enterprise Fraud Detection System

**Sentino-Sentinel** is a high-performance, end-to-end MLOps system designed to detect fraudulent financial transactions in real-time. 

## 🏗️ System Architecture
- **Data Layer:** PostgreSQL (Normalized Star Schema: Users, Merchants, Transactions).
- **ML Engine:** XGBoost Classifier with SMOTE for class imbalance handling.
- **Experiment Tracking:** MLflow (Tracking Precision, Recall, and F1-Score).
- **Inference Layer:** FastAPI REST Microservice with real-time probability scoring.

## 🚀 Key Features
- **Pattern Injection:** Simulated real-world fraud behaviors (high-value spikes, compromised merchants).
- **Audit-Ready:** Every inference includes a timestamp and confidence score.
- **Production-Ready:** Container-ready architecture for cloud deployment.

## 📈 Performance
- **Fraud Recall:** >90% (Optimized to minimize False Negatives).
- **Experiment Management:** All training runs are logged via MLflow for reproducibility.