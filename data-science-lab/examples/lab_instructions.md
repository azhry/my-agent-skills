# Lab 1: Supervised Learning — Classification & Regression

## Course Information
- **Course**: CS4210 — Introduction to Machine Learning
- **Semester**: Spring 2026
- **Due Date**: March 28, 2026

---

## Objective

In this lab, you will explore supervised learning techniques for both **classification** and **regression** tasks. You will:

1. Load and preprocess two datasets
2. Train multiple models with hyperparameter tuning
3. Evaluate performance using appropriate metrics
4. Compare results and document findings

---

## Part 1: Classification (50 points)

### Dataset
Use the **Wine Quality** dataset from UCI ML Repository.
- Download: https://archive.ics.uci.edu/dataset/186/wine+quality
- Target: `quality` (classify as "good" if quality ≥ 7, "bad" otherwise)
- Features: 11 physicochemical properties

### Tasks

#### 1.1 Data Exploration (10 pts)
- Load the dataset and display basic statistics
- Check for missing values and class distribution
- Create at least 2 visualizations (histograms, correlation heatmap, etc.)

#### 1.2 Preprocessing (10 pts)
- Handle any missing values
- Apply feature scaling (StandardScaler or MinMaxScaler)
- Split data into 80% train / 20% test with `random_state=42`

#### 1.3 Model Training (20 pts)
Train the following classifiers:
- **Logistic Regression** with regularization parameters: C = [0.01, 0.1, 1, 10, 100]
- **Support Vector Machine** with kernels: ['linear', 'rbf', 'poly']
- **Random Forest** with n_estimators: [50, 100, 200] and max_depth: [5, 10, None]
- **K-Nearest Neighbors** with k = [3, 5, 7, 9, 11]

For each model configuration, record:
- Model name and parameters
- Accuracy
- Precision (weighted)
- Recall (weighted)
- F1-Score (weighted)

#### 1.4 Evaluation (10 pts)
- Generate confusion matrix for the best model
- Plot ROC curves for each model type
- Create a comparison bar chart of F1-scores

---

## Part 2: Regression (50 points)

### Dataset
Use the **California Housing** dataset from scikit-learn.
- `from sklearn.datasets import fetch_california_housing`
- Target: `MedHouseVal` (median house value)
- Features: 8 attributes

### Tasks

#### 2.1 Data Exploration (10 pts)
- Load the dataset and display basic statistics
- Create scatter plots of features vs. target
- Check for outliers

#### 2.2 Preprocessing (10 pts)
- Handle outliers (clip or remove)
- Apply feature scaling
- Split data 80/20 with `random_state=42`

#### 2.3 Model Training (20 pts)
Train the following regressors:
- **Linear Regression** (baseline)
- **Ridge Regression** with alpha = [0.01, 0.1, 1, 10, 100]
- **Lasso Regression** with alpha = [0.01, 0.1, 1, 10, 100]
- **Random Forest Regressor** with n_estimators: [50, 100, 200]
- **Gradient Boosting** with learning_rate: [0.01, 0.05, 0.1] and n_estimators: [100, 200]

For each model configuration, record:
- Model name and parameters
- MSE (Mean Squared Error)
- RMSE (Root Mean Squared Error)
- MAE (Mean Absolute Error)
- R² Score

#### 2.4 Evaluation (10 pts)
- Plot actual vs. predicted for the best model
- Compare R² scores across all models
- Feature importance analysis for tree-based models

---

## Deliverables

1. **Jupyter Notebook** (`.ipynb`) — All code, visualizations, and markdown explanations
2. **Results CSV** — All experiment results in a CSV file
3. **Report** — A summary report (markdown or PDF) with:
   - Best model for each task and why
   - Key insights from the experiments
   - At least one infographic summarizing results
4. **Infographic** — A visualization comparing classification and regression results

---

## Grading Rubric

| Component | Points |
|-----------|--------|
| Part 1: Classification | 50 |
| Part 2: Regression | 50 |
| Code quality & documentation | +5 bonus |
| Insightful analysis beyond requirements | +5 bonus |
| **Total** | **100 + 10 bonus** |

---

## Submission

Submit via the course LMS by **March 28, 2026, 11:59 PM**.

Upload:
- `lab1_supervised_learning.ipynb`
- `results/classification_results.csv`
- `results/regression_results.csv`
- `reports/lab1_report.md`
- `images/lab1_infographic.png`
