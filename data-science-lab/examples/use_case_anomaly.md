# Use Case: Anomaly Detection

This document shows how to use the data-science-lab skill for **anomaly/outlier detection** tasks.

---

## User Prompt Example

```
Detect anomalies in @[path/to/transactions.csv].
Use Isolation Forest and Local Outlier Factor.
Export results and create visualizations.
Follow the data-science-lab skill.
```

---

## Goal Interpretation

| User Goal | Task Type | Recommended Models |
|-----------|-----------|-------------------|
| "Detect anomalies" | unsupervised | Isolation Forest, Local Outlier Factor, One-Class SVM |

---

## Example: Fraud Detection

### Step 1: Load Data

```python
import pandas as pd
import numpy as np

# Sample transaction data
np.random.seed(42)
n = 1000

data = {
    'transaction_id': range(1, n + 1),
    'amount': np.random.exponential(100, n),
    'frequency': np.random.randint(1, 50, n),
    'merchant_category': np.random.choice(['retail', 'food', 'travel', 'entertainment'], n),
    'hour_of_day': np.random.randint(0, 24, n),
}

df = pd.DataFrame(data)

# Inject anomalies
anomaly_indices = np.random.choice(n, 20, replace=False)
df.loc[anomaly_indices, 'amount'] = df.loc[anomaly_indices, 'amount'] * 10
```

### Step 2: Prepare Features

```python
from sklearn.preprocessing import StandardScaler, LabelEncoder

# Encode categorical
le = LabelEncoder()
df['merchant_encoded'] = le.fit_transform(df['merchant_category'])

# Select features
features = ['amount', 'frequency', 'merchant_encoded', 'hour_of_day']
X = df[features].values

# Scale
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
```

### Step 3: Isolation Forest

```python
from sklearn.ensemble import IsolationForest

# Train model
iso_forest = IsolationForest(n_estimators=100, contamination=0.02, random_state=42)
df['anomaly_iso'] = iso_forest.fit_predict(X_scaled)

# -1 = anomaly, 1 = normal
df['is_anomaly_iso'] = df['anomaly_iso'].apply(lambda x: 'Anomaly' if x == -1 else 'Normal')

print(f"Isolation Forest found {sum(df['anomaly_iso'] == -1)} anomalies")
```

### Step 4: Local Outlier Factor

```python
from sklearn.neighbors import LocalOutlierFactor

lof = LocalOutlierFactor(n_neighbors=20, contamination=0.02)
df['anomaly_lof'] = lof.fit_predict(X_scaled)

print(f"LOF found {sum(df['anomaly_lof'] == -1)} anomalies")
```

### Step 5: Visualize Results

```python
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

# Reduce to 2D for visualization
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Isolation Forest
colors = ['red' if x == -1 else 'green' for x in df['anomaly_iso']]
axes[0].scatter(X_pca[:, 0], X_pca[:, 1], c=colors, alpha=0.6)
axes[0].set_title('Isolation Forest Anomalies')

# LOF
colors = ['red' if x == -1 else 'green' for x in df['anomaly_lof']]
axes[1].scatter(X_pca[:, 0], X_pca[:, 1], c=colors, alpha=0.6)
axes[1].set_title('Local Outlier Factor Anomalies')

plt.tight_layout()
plt.savefig('images/anomaly_detection.png', dpi=150)
plt.show()
```

### Step 6: Compare Results

```python
# Agreement between methods
agreement = (df['anomaly_iso'] == df['anomaly_lof']).mean()
print(f"Method agreement: {agreement:.2%}")

# Anomalies found by both
both_anomaly = df[(df['anomaly_iso'] == -1) & (df['anomaly_lof'] == -1)]
print(f"Anomalies detected by both: {len(both_anomaly)}")
```

### Step 7: Export Results

```python
results = df[['transaction_id', 'amount', 'is_anomaly_iso', 'anomaly_lof']].copy()
results['is_anomaly'] = results['is_anomaly_iso'] == 'Anomaly'
results.to_csv('results/anomaly_detection.csv', index=False)
print("Results saved to results/anomaly_detection.csv")
```

---

## Expected Output

| File | Description |
|------|-------------|
| `images/anomaly_detection.png` | Visualization of detected anomalies |
| `results/anomaly_detection.csv` | Transactions flagged as anomalies |

---

## Summary

- **Isolation Forest**: Fast, works well with high-dimensional data
- **LOF**: Good for detecting local density-based outliers
- **One-Class SVM**: Good for complex boundaries (not shown above)
