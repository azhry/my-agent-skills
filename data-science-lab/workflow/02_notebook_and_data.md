# Step 3-4: Notebook Creation & Data Handling

## Step 3: Notebook Creation

- Use `.ipynb` format for all experiments
- Create separate directories for each lab/experiment
- Use `uv` for Python environment management

### Recommended Project Structure
```
lab1/
├── notebooks/
│   └── experiment.ipynb
├── data/
│   └── raw_data.csv
├── results/
│   └── results.csv
├── images/
│   └── *.png
└── reports/
    └── report.tex
```

## Step 4: Data Handling

- Load data from local files or remote sources
- Handle missing values appropriately
- Use proper path resolution (handle both script and notebook execution):

```python
import os

# Resolve base directory — works in both scripts and notebooks
try:
    base_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    base_dir = os.getcwd()

data_path = os.path.join(base_dir, '..', 'data', 'file.csv')
```

> [!WARNING]
> Use `__file__` (the Python variable), NOT `'__file__'` (a string literal). The string version resolves the literal filename `"__file__"` relative to cwd, which is incorrect.

### Handling CSV/Dataset-Only Prompts

When the user provides **only a CSV or dataset** (without explicit task type), the agent should:

1. **Load and inspect the data** — Use EDA to understand structure, columns, data types
2. **Auto-detect task type** based on the target column:
   - If target column is **categorical** (few unique values, string or int with low cardinality) → `classification`
   - If target column is **continuous numerical** → `regression`
   - If no clear target → treat as **unsupervised** (clustering, PCA, etc.)
3. **Suggest experiment type** to user and proceed

```python
# Auto-detect task type example
def detect_task_type(df, target_col):
    if target_col not in df.columns:
        return 'unsupervised'
    
    unique_ratio = df[target_col].nunique() / len(df)
    
    if df[target_col].dtype in ['object', 'str'] or unique_ratio < 0.05:
        return 'classification'
    elif unique_ratio > 0.5 and df[target_col].dtype in ['int64', 'float64']:
        return 'regression'
    else:
        return 'classification'  # default
```

### Flexible Workflow Entry Points

| User Input | Start at Step | Notes |
|------------|---------------|-------|
| Topic/Problem only | Step 1: Task Planning | Create experiment from scratch |
| CSV only | Step 4: Data Handling | Auto-detect task type |
| CSV + Goal | Step 4: Data Handling | Use specified target column |
| Existing notebook | Step 5: EDA | Continue from existing work |
