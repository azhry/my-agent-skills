# Use Case Examples — Based on SKILL.md

This directory contains use case examples covering all scenarios from the data-science-lab SKILL.md.

## Current Examples

| File | Use Case | Task Type | Description |
|------|----------|-----------|-------------|
| `lab1_supervised_learning.ipynb` | Wine Quality + Housing | Classification, Regression | Full supervised learning workflow |
| `eda_and_data_prep.md` | Generic EDA + Data Prep | EDA, Preprocessing | How to use run_eda.py and run_data_prep.py |
| `lab_instructions.md` | Lab Assignment | Reference | Example professor instructions |
| `usage.md` | General Usage | Reference | Quick start prompts |
| `use_case_clustering.ipynb` | Customer Segmentation | Clustering | K-Means, DBSCAN, Hierarchical |
| `use_case_nlp_sentiment.ipynb` | Review Sentiment Analysis | NLP | Text classification, VADER, TF-IDF |
| `use_case_nlp_topic.md` | Topic Modeling | NLP | LDA, NMF for text analysis |
| `use_case_anomaly.md` | Fraud Detection | Anomaly Detection | Isolation Forest, Local Outlier Factor |
| `use_case_forecasting.md` | Sales Forecasting | Time Series | ARIMA, Holt-Winters |
| `use_case_recommendation.md` | Product Recommendation | Collaborative Filtering | Matrix Factorization, KNN |

## Quick Mapping: User Goal → Example

| User Goal | Example File | Key Models |
|-----------|-------------|-----------|
| "Segment customers" | `use_case_clustering.ipynb` | K-Means, DBSCAN |
| "Sentiment analysis" | `use_case_nlp_sentiment.ipynb` | VADER, Logistic Regression |
| "Find topics in documents" | `use_case_nlp_topic.md` | LDA, NMF |
| "Detect fraud" | `use_case_anomaly.md` | Isolation Forest, LOF |
| "Forecast sales" | `use_case_forecasting.md` | ARIMA, Holt-Winters |
| "Recommend products" | `use_case_recommendation.md` | SVD, KNN |
| "Predict prices" | `lab1_supervised_learning.ipynb` | Regression models |
| "Classify categories" | `lab1_supervised_learning.ipynb` | Classification models |
| "EDA on any dataset" | `eda_and_data_prep.md` | run_eda.py, run_data_prep.py |

## Goal-to-Task Mapping (from SKILL.md)

| User Goal | Task Type | Recommended Models |
|-----------|-----------|-------------------|
| "predict X" / "forecast" | regression | Linear Regression, Random Forest, XGBoost |
| "classify X" / "detect X" | classification | Logistic Regression, Random Forest, SVM |
| "segment X" / "group" | clustering | K-Means, DBSCAN, Hierarchical |
| "find patterns" | unsupervised | PCA, Association Rules, Anomaly Detection |
| "understand text" | NLP | TF-IDF + Classifier, BERT |
| "sentiment analysis" | NLP | VADER, TextBlob |
| "Recommend products" | recommendation | Collaborative Filtering |
