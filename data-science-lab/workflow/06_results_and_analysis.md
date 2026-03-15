# Steps 7-8: Results Export & Analysis

## Step 7: Results Export

Save experiment results to CSV files in a `results/` subdirectory. Include all parameters and metrics.

```python
import os
import pandas as pd

results_dir = os.path.join(os.path.dirname(data_path), '..', 'results')
os.makedirs(results_dir, exist_ok=True)

results = []
for param in params:
    # run experiment...
    results.append({'model': model_name, 'param': param, 'accuracy': score})

df = pd.DataFrame(results)
df.to_csv(os.path.join(results_dir, 'results.csv'), index=False)
```

### Classification Results Format

```csv
model,param,accuracy,precision,recall,f1_score
Logistic Regression,C=0.01,0.8542,0.8301,0.8542,0.8356
Logistic Regression,C=0.1,0.8695,0.8512,0.8695,0.8543
Random Forest,n_estimators=100,0.9213,0.9187,0.9213,0.9195
```

### Regression Results Format

```csv
model,param,mse,rmse,mae,r2_score
Linear Regression,baseline,0.5243,0.7240,0.5321,0.6055
Ridge,alpha=0.1,0.5198,0.7210,0.5287,0.6089
Lasso,alpha=0.01,0.5301,0.7281,0.5356,0.6012
```

## Step 8: Analysis & Findings

After exporting results, use the helper scripts to analyze them:

```python
import sys
sys.path.insert(0, '/path/to/data-science-lab/scripts')

from analyze_results import find_best_model, compare_models, generate_insights, print_summary

# Load results
results_df = pd.read_csv('results/results.csv')

# Find best model
best = find_best_model(results_df, metric='accuracy')

# Compare all models
comparison = compare_models(results_df, metric='accuracy')

# Generate structured insights
insights = generate_insights(results_df, metric='accuracy')

# Print formatted summary
print_summary(results_df, metric='accuracy')
```

### For NLP experiments

```python
from analyze_results import analyze_text_topics

# Analyze topic distributions
topics = analyze_text_topics(df, topic_col='dominant_topic', text_col='document')
print(topics)
```

### What the Agent Should Do

- **Analyze results**: Compare metrics across different models/parameters
- **Identify patterns**: Find what works best and why
- **Document findings**: Write clear summaries of what the experiments show
- **Generate insights**: Explain what the results mean for the problem
