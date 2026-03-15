# Step 5: Exploratory Data Analysis (EDA)

> [!IMPORTANT]
> **Always run EDA before any modeling or experiments.** This step helps you understand the dataset structure, quality, and distributions. Use the generic `run_eda.py` script — it works with **any** tabular dataset.

## Full EDA Pipeline

```python
import sys
sys.path.insert(0, '/path/to/data-science-lab/scripts')

from run_eda import run_full_eda

# Basic usage — works with any DataFrame
eda_results = run_full_eda(df, output_dir='../images', title='My Dataset EDA')
```

## Customization Options

```python
# Specify a target column for grouped analysis (e.g. the label column)
eda_results = run_full_eda(
    df,
    output_dir='../images',
    title='Penguins EDA',
    target_col='species',           # categorical column for grouping
    exclude_cols=['rowid', 'id'],   # columns to skip
    outlier_method='iqr',           # 'zscore' (default) or 'iqr'
    outlier_threshold=1.5,          # IQR multiplier or z-score cutoff
)
```

## Individual Steps

You can also call individual EDA steps:

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
outliers = outlier_detection(df, method='zscore')
```

## What the EDA Module Does Automatically

- Classifies columns as numerical, categorical, datetime, or ID-like
- Generates missing-value reports and duplicate counts
- Creates distribution plots (histograms + KDE for numerical, pie/bar for categorical)
- Produces correlation heatmaps and scatter matrices
- Detects outliers via z-score or IQR methods
- Saves all figures to the specified `output_dir`

## CLI Usage

```bash
python run_eda.py data/customers.csv \
    --output-dir images \
    --target churn \
    --exclude customer_id,name
```
