# Troubleshooting

Common issues and how to fix them when using the data-science-lab skill.

## Package & Environment Issues

### `ModuleNotFoundError: No module named 'sklearn'`

**Cause**: Data science packages not installed in the active environment.

**Fix**:
```bash
uv pip install pandas numpy scikit-learn matplotlib seaborn plotly tabulate ipykernel
```

### `ModuleNotFoundError: No module named 'run_eda'`

**Cause**: Script path not added to Python path.

**Fix**: Add the scripts directory to `sys.path` before importing:
```python
import sys
sys.path.insert(0, '/absolute/path/to/data-science-lab/scripts')
from run_eda import run_full_eda
```

### `No module named 'xgboost'`

**Cause**: XGBoost is not included in the base install.

**Fix**:
```bash
uv pip install xgboost
```

### Jupyter kernel not found

**Cause**: ipykernel not registered.

**Fix**:
```bash
python -m ipykernel install --user --name=my-env
```

## Data Issues

### `KeyError: 'column_name'`

**Cause**: Target column name doesn't match what's in the CSV.

**Fix**: Check actual column names first:
```python
print(df.columns.tolist())
```

### `ValueError: could not convert string to float`

**Cause**: Categorical columns not encoded before modeling.

**Fix**: Run data preparation with encoding:
```python
result = run_full_data_prep(df, target_col='target', encoding='label')
```

### All metrics are 0.0 or NaN

**Cause**: Usually one of:
1. Wrong target column (all same value)
2. Data leakage in splitting
3. Features and target misaligned after encoding

**Fix**: Check these:
```python
# Check target distribution
print(df['target'].value_counts())

# Check for data leakage
print(f"X_train shape: {X_train.shape}, y_train shape: {y_train.shape}")

# Make sure target isn't in features
print([c for c in X_train.columns if 'target' in c.lower()])
```

### `ValueError: Input contains NaN`

**Cause**: Missing values not handled before modeling.

**Fix**: Run data prep with missing value handling:
```python
result = run_full_data_prep(df, target_col='target', missing_strategy='auto')
```
Or handle manually:
```python
df = df.dropna()
# or
df = df.fillna(df.median(numeric_only=True))
```

## Visualization Issues

### Plots not showing in Jupyter

**Cause**: Matplotlib backend issue.

**Fix**: Add at the top of your notebook:
```python
%matplotlib inline
```

### `FileNotFoundError` when saving plots

**Cause**: Output directory doesn't exist.

**Fix**: Create it first:
```python
import os
os.makedirs('images', exist_ok=True)
```

### Infographic looks wrong (overlapping text)

**Cause**: Not enough data points or too many models.

**Fix**: Use `create_mini_infographic()` for small datasets:
```python
from create_infographics import create_mini_infographic, export_infographic
fig = create_mini_infographic(results_df, title='Results')
export_infographic(fig, 'images/mini.png')
```

## Path Issues

### `__file__` not defined in Jupyter

**Cause**: `__file__` is a script-only variable; it's not defined in notebooks.

**Fix**: Use the try/except pattern:
```python
try:
    base_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    base_dir = os.getcwd()
```

> [!WARNING]
> Use `__file__` (the Python variable), NOT `'__file__'` (a string literal). The string version would look for a file literally named `__file__`.

### Windows path issues

**Cause**: Backslashes in paths cause escape character problems.

**Fix**: Use raw strings or forward slashes:
```python
# These all work on Windows:
path = r'C:\Users\data\file.csv'
path = 'C:/Users/data/file.csv'
path = os.path.join('C:', 'Users', 'data', 'file.csv')
```

## Linear Integration Issues

### Linear MCP tools not available

**Cause**: Linear MCP server not configured.

**Fix**: Use markdown-based task tracking instead:
```markdown
# Lab Tasks: [Experiment Name]

- [ ] Step 1: Load and explore data
- [ ] Step 2: Data cleaning and preprocessing
- [ ] Step 3: Build and train model
```

## LaTeX Issues

### Docker not found

**Cause**: Docker not installed or not running.

**Fix**: Either install Docker Desktop, or install TeX Live locally:
```bash
# On Windows with Chocolatey
choco install miktex

# On macOS with Homebrew
brew install --cask mactex
```

### LaTeX compilation fails

**Fix**: Run with non-stop mode to see all errors:
```bash
pdflatex -interaction=nonstopmode main.tex
```

Check the [08_reporting.md](08_reporting.md) module for common LaTeX error fixes.
