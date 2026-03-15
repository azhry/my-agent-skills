# EDA & Data Preparation — Usage Examples

This document shows how to use the `run_eda.py` and `run_data_prep.py` scripts
for any dataset. Both scripts produce **human-readable discussions** that
explain the findings and decisions in plain language.

---

## Example 1: Quick EDA on any CSV

```python
import pandas as pd
import sys
sys.path.insert(0, '/path/to/data-science-lab/scripts')

from run_eda import run_full_eda

# Load any dataset
df = pd.read_csv('data/my_dataset.csv')

# Run full EDA — works with ANY tabular data
eda = run_full_eda(
    df,
    title='Customer Churn EDA',
    output_dir='../images',
    target_col='churn',         # optional: group analysis by this column
    exclude_cols=['customer_id'],  # optional: skip ID columns
)
```

### What you'll get

The script automatically:
- **Classifies** every column as numerical, categorical, datetime, or ID-like
- **Reports** missing values with exact counts and percentages
- **Plots** distributions for every column (histograms + KDE for numbers, pie/bar for categories)
- **Generates** a correlation heatmap and scatter matrix
- **Detects** outliers using z-score or IQR methods
- **Saves** all figures to the output directory

---

## Example 2: EDA with individual steps

```python
from run_eda import (
    data_overview,
    data_quality_report,
    univariate_analysis,
    bivariate_analysis,
    outlier_detection,
)

# Run only what you need
overview = data_overview(df)
quality  = data_quality_report(df)
univariate_analysis(df, output_dir='../images')
bivariate_analysis(df, target_col='species', output_dir='../images')
outliers = outlier_detection(df, method='iqr', threshold=1.5)
```

---

## Example 3: Full Data Preparation Pipeline

```python
from run_data_prep import run_full_data_prep

df = pd.read_csv('data/penguins.csv')

result = run_full_data_prep(
    df,
    target_col='species',
    task_type='classification',
    exclude_cols=['rowid'],
    missing_strategy='auto',       # 'auto', 'drop', or 'impute'
    encoding='label',              # 'label', 'onehot', or 'both'
    scaling_method='standard',     # 'standard', 'minmax', or 'robust'
    outlier_method='keep',         # 'keep', 'remove', or 'cap'
    test_size=0.2,
    output_dir='data/prepared',
    images_dir='../images',
)

# Access results
X_train = result['split']['X_train']
X_test  = result['split']['X_test']
y_train = result['split']['y_train']
y_test  = result['split']['y_test']
encoders = result['encoders']
scaler   = result['scaler']
```

### What each step produces

| Step | Output | Discussion |
|------|--------|------------|
| **Validation** | Column types, duplicates | "The dataset has 344 rows and 7 columns. We detected 4 numerical, 3 categorical..." |
| **Missing Values** | Clean dataset | "Only 0.6% of rows had missing values, so we dropped them (2 rows removed)..." |
| **Encoding** | Encoded categories | "Encoded 3 categorical columns: species → {Adelie: 0, Chinstrap: 1, Gentoo: 2}..." |
| **Scaling** | Normalized features | "Feature scaling ensures all numerical features are on a comparable scale..." |
| **Outliers** | Detection report | "Detected 5 outlier values. Outliers were retained because they may represent valid variation..." |
| **Feature Selection** | Ranked features | "Features ranked by ANOVA F-score and Mutual Information. bill_length_mm and flipper_length_mm are the strongest predictors..." |
| **Train/Test Split** | X_train, X_test, y_train, y_test | "Split 80/20. Stratified sampling ensures each class is equally represented..." |
| **Export** | CSV + pickle files | "All prepared data and fitted transformers have been saved..." |

---

## Example 4: Data Preparation with individual steps

```python
from run_data_prep import (
    validate_data,
    handle_missing_values,
    encode_features,
    scale_features,
    handle_outliers,
    select_features,
    split_data,
    export_prepared_data,
)

# Auto-classify columns
from run_data_prep import _classify_columns
col_info = _classify_columns(df, target_col='species', exclude_cols=['rowid'])

# Run steps individually
validate_data(df, col_info)
df_clean = handle_missing_values(df, col_info, strategy='drop')
df_encoded, encoders = encode_features(df_clean, col_info, target_col='species')
df_scaled, scaler = scale_features(df_encoded, col_info, method='standard')
df_no_outliers = handle_outliers(df_encoded, col_info, method='cap')
```

---

## Example 5: EDA + Data Prep together in a notebook

This is the **recommended workflow** — EDA first, then data preparation:

```python
import pandas as pd
import sys
sys.path.insert(0, '/path/to/data-science-lab/scripts')

from run_eda import run_full_eda
from run_data_prep import run_full_data_prep

# =============================================================
# STEP 1: Load data
# =============================================================
df = pd.read_csv('data/housing.csv')

# =============================================================
# STEP 2: EDA — understand the data first
# =============================================================
eda = run_full_eda(
    df,
    title='Housing Price EDA',
    output_dir='images',
    target_col='price',
)

# Review EDA results before proceeding:
# - Check which features have missing values
# - Check which features are highly correlated
# - Check for outliers that need handling

# =============================================================
# STEP 3: Data Preparation — clean and transform
# =============================================================
result = run_full_data_prep(
    df,
    target_col='price',
    task_type='regression',         # regression for continuous targets
    exclude_cols=['id', 'date'],
    missing_strategy='impute',      # impute rather than drop
    scaling_method='robust',        # robust to outliers
    outlier_method='cap',           # cap extreme values
    output_dir='data/prepared',
    images_dir='images',
)

# =============================================================
# STEP 4: Ready for modeling!
# =============================================================
X_train = result['split']['X_train']
y_train = result['split']['y_train']
```

---

## Example 6: CLI usage

Both scripts can be run from the command line:

```bash
# EDA
python run_eda.py data/customers.csv \
    --output-dir images \
    --target churn \
    --exclude customer_id,name

# Data Preparation
python run_data_prep.py data/customers.csv churn \
    --task classification \
    --output-dir data/prepared \
    --images-dir images \
    --exclude customer_id,name \
    --missing auto \
    --scaling standard \
    --outliers keep
```

---

## Expected output files

After running EDA + Data Preparation, the project directory should look like:

```
project/
├── data/
│   ├── raw_data.csv
│   └── prepared/
│       ├── train_data.csv
│       ├── test_data.csv
│       ├── train_data_scaled.csv
│       ├── test_data_scaled.csv
│       ├── encoders.pkl
│       └── scaler.pkl
├── images/
│   ├── eda_categorical_distributions.png
│   ├── eda_numerical_distributions.png
│   ├── eda_correlation_heatmap.png
│   ├── eda_scatter_matrix.png
│   ├── eda_outlier_boxplots.png
│   ├── data_prep_scaling_comparison.png
│   └── data_prep_feature_importance.png
├── notebooks/
│   └── experiment.ipynb
└── results/
    └── ...
```
