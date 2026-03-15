# Step 6: Data Preparation

> [!IMPORTANT]
> **Run data preparation after EDA and before modeling.** This step cleans, encodes, scales, and splits your data. Use the generic `run_data_prep.py` script — it works with **any** tabular dataset and produces **human-readable discussions** explaining every decision.

## Full Data Preparation Pipeline

```python
import sys
sys.path.insert(0, '/path/to/data-science-lab/scripts')

from run_data_prep import run_full_data_prep

result = run_full_data_prep(
    df,
    target_col='species',
    task_type='classification',       # or 'regression'
    output_dir='../data/prepared',
    images_dir='../images',
)

# Ready for modeling
X_train = result['split']['X_train']
X_test  = result['split']['X_test']
y_train = result['split']['y_train']
y_test  = result['split']['y_test']
```

## All Parameters

```python
result = run_full_data_prep(
    df,
    target_col='species',             # target column (required)
    task_type='classification',       # 'classification' or 'regression'
    exclude_cols=['rowid'],           # columns to drop before processing
    missing_strategy='auto',          # 'auto', 'drop', or 'impute'
    encoding='label',                 # 'label', 'onehot', or 'both'
    scaling_method='standard',        # 'standard', 'minmax', or 'robust'
    outlier_method='keep',            # 'keep', 'remove', or 'cap'
    feature_select_k=0,              # top-k features (0 = keep all)
    test_size=0.2,                   # train/test split ratio
    output_dir='data/prepared',       # export CSVs + pickles (None = skip)
    images_dir='../images',           # save plots (None = skip)
    random_state=42,                  # seed for reproducibility
)
```

## What Each Step Produces

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

## Individual Steps

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

## CLI Usage

```bash
python run_data_prep.py data/customers.csv churn \
    --task classification \
    --output-dir data/prepared \
    --images-dir images \
    --exclude customer_id,name \
    --missing auto \
    --scaling standard \
    --outliers keep
```

## Expected Output Files

After running, the `output_dir` should contain:
```
data/prepared/
├── train_data.csv
├── test_data.csv
├── train_data_scaled.csv
├── test_data_scaled.csv
├── encoders.pkl
└── scaler.pkl
```
