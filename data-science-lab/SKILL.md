---
name: Data Science Lab
description: End-to-end data science lab workflow from task planning to result analysis. Uses Jupyter notebooks, Linear for task management (optional), and exports results for analysis.
---

# Data Science Lab Skill

> [!NOTE]
> This skill is designed for data science experiments using Jupyter notebooks. It handles the complete workflow from planning to result export, supporting Supervised Learning, Unsupervised Learning, and NLP (Topic Modeling, Sentiment Analysis, Text Classification).

## Quick Decision Tree

Read **only** the workflow module you need — don't read them all:

| User Input | Read This First | Then |
|------------|----------------|------|
| Lab instructions / topic only | [01_planning.md](workflow/01_planning.md) | [02_notebook_and_data.md](workflow/02_notebook_and_data.md) |
| CSV file only (no goal) | [03_eda.md](workflow/03_eda.md) | [04_data_prep.md](workflow/04_data_prep.md) |
| CSV + explicit goal | [04_data_prep.md](workflow/04_data_prep.md) | [05_modeling.md](workflow/05_modeling.md) |
| Existing notebook | [03_eda.md](workflow/03_eda.md) | Continue from existing work |
| Generate visualizations | [07_visualization.md](workflow/07_visualization.md) | — |
| Write a report | [08_reporting.md](workflow/08_reporting.md) | — |
| Something isn't working | [troubleshooting.md](workflow/troubleshooting.md) | — |

> [!TIP]
> For a 20-line fast-path, see [QUICKSTART.md](QUICKSTART.md).

## Goal-to-Task Mapping

When user provides a goal, map to the appropriate approach:

| User Goal | Task Type | Recommended Models |
|-----------|-----------|-------------------|
| "predict X" / "forecast" | regression | Linear Regression, Random Forest, XGBoost, LSTM |
| "classify X" / "detect X" | classification | Logistic Regression, Random Forest, SVM, XGBoost |
| "segment X" / "group" | clustering | K-Means, DBSCAN, Hierarchical |
| "find patterns" | unsupervised | PCA, Association Rules, Anomaly Detection |
| "understand text" | NLP | TF-IDF + Classifier, BERT, Word2Vec |
| "sentiment analysis" | NLP | VADER, TextBlob, Transformer Models |
| "Recommend products" | recommendation | Collaborative Filtering, Matrix Factorization, KNN |

For use case examples, see [examples/README.md](examples/README.md).

## Prerequisites

- **Python 3.8+** with `uv` for environment management
- **Jupyter** — `ipykernel` for notebook kernel
- **Linear account** (optional) — for task tracking via MCP; use Markdown tasks if not available
- **Data science packages** — pandas, numpy, scikit-learn, matplotlib, seaborn, plotly, tabulate

```bash
uv venv
uv pip install pandas numpy scikit-learn matplotlib seaborn plotly tabulate ipykernel
python -m ipykernel install --user --name=my-env
```

## Helper Scripts — API Cheatsheet

> [!IMPORTANT]
> These scripts are in `scripts/`. Import and use them — **do NOT recreate them**.

```python
import sys
sys.path.insert(0, '/path/to/data-science-lab/scripts')
```

### EDA ([run_eda.py](scripts/run_eda.py))
```python
from run_eda import run_full_eda

# Full EDA pipeline — works with ANY DataFrame
eda_results = run_full_eda(
    df,                              # pandas DataFrame (required)
    title='My Dataset EDA',          # report title
    output_dir='../images',          # save figures here (None = don't save)
    target_col='species',            # categorical column for grouped analysis
    exclude_cols=['rowid', 'id'],    # columns to skip
    outlier_method='zscore',         # 'zscore' or 'iqr'
    outlier_threshold=3.0,           # z-score cutoff or IQR multiplier
)
# Returns: dict with keys: overview, quality, col_info, outliers

# Individual steps available:
from run_eda import data_overview, data_quality_report, univariate_analysis, bivariate_analysis, outlier_detection
```

### Data Preparation ([run_data_prep.py](scripts/run_data_prep.py))
```python
from run_data_prep import run_full_data_prep

result = run_full_data_prep(
    df,                              # pandas DataFrame (required)
    target_col='species',            # target column (required)
    task_type='classification',      # 'classification' or 'regression'
    exclude_cols=['rowid'],          # columns to drop
    missing_strategy='auto',        # 'auto', 'drop', or 'impute'
    encoding='label',               # 'label', 'onehot', or 'both'
    scaling_method='standard',      # 'standard', 'minmax', or 'robust'
    outlier_method='keep',          # 'keep', 'remove', or 'cap'
    feature_select_k=0,             # top-k features (0 = keep all)
    test_size=0.2,                  # train/test split ratio
    output_dir='data/prepared',     # export CSVs + pickles
    images_dir='../images',         # save plots
)
# Returns: dict with keys: df_prepared, split, encoders, scaler, col_info, feature_scores, selected_features, export_paths
# Access: result['split']['X_train'], result['split']['y_train'], etc.

# Individual steps available:
from run_data_prep import validate_data, handle_missing_values, encode_features, scale_features, handle_outliers, select_features, split_data
```

### Result Analysis ([analyze_results.py](scripts/analyze_results.py))
```python
from analyze_results import find_best_model, compare_models, generate_insights, print_summary, analyze_text_topics

best = find_best_model(results_df, metric='accuracy')         # Returns Series (best row)
ranking = compare_models(results_df, metric='accuracy')       # Returns Series (mean by model)
insights = generate_insights(results_df, metric='accuracy')   # Returns dict with insights
print_summary(results_df, metric='accuracy')                  # Prints formatted summary
topics = analyze_text_topics(df, topic_col='topic_label')     # Returns DataFrame (NLP)
```

### Visualization ([visualize.py](scripts/visualize.py))
```python
from visualize import plot_confusion_matrix, plot_metric_comparison, plot_parameter_sweep, plot_feature_importance, plot_learning_curve, save_all_plots, plot_topic_distribution, plot_word_frequencies

plot_confusion_matrix(cm, labels, save_path='images/cm.png')
plot_metric_comparison(df, 'accuracy', save_path='images/compare.png')
plot_parameter_sweep(df, 'alpha', 'accuracy', hue='model', save_path='images/sweep.png')
plot_feature_importance(features, importance, save_path='images/fi.png')
save_all_plots(df, results_dir='images', metric='accuracy')  # Quick: save all standard plots
```

### Infographics ([create_infographics.py](scripts/create_infographics.py))
```python
from create_infographics import create_experiment_infographic, create_comparison_infographic, create_mini_infographic, create_nlp_infographic, export_infographic, export_multi_format, quick_infographic

# Full infographic (hero banner, podium, heatmap, radar, stats card)
fig = create_experiment_infographic(results_df, title='Lab 1', metric='accuracy', theme='dark', palette='ocean')
export_infographic(fig, 'images/infographic.png', dpi=300)

# Comparison (classification vs regression side-by-side)
fig = create_comparison_infographic(clf_df, reg_df, title='Comparison', theme='dark')

# Compact version for reports
fig = create_mini_infographic(results_df, title='Quick Summary', theme='dark')

# One-liner from CSV
quick_infographic('results/results.csv', 'images/infographic.png', title='Results')

# Themes: 'dark', 'light'
# Palettes: 'ocean', 'sunset', 'forest', 'purple', 'slate', 'candy'
```

## Workflow Steps (Read On-Demand)

The full workflow has 10 steps. Read only what you need:

| Step | Module | When to Read |
|------|--------|-------------|
| 1-2 | [01_planning.md](workflow/01_planning.md) | Starting from scratch or lab instructions |
| 3-4 | [02_notebook_and_data.md](workflow/02_notebook_and_data.md) | Creating notebooks, loading data |
| 5 | [03_eda.md](workflow/03_eda.md) | Running exploratory data analysis |
| 6 | [04_data_prep.md](workflow/04_data_prep.md) | Cleaning, encoding, scaling, splitting data |
| 6b | [05_modeling.md](workflow/05_modeling.md) | Training and evaluating models |
| 7-8 | [06_results_and_analysis.md](workflow/06_results_and_analysis.md) | Exporting and analyzing results |
| 9 | [07_visualization.md](workflow/07_visualization.md) | Generating plots and infographics |
| 10 | [08_reporting.md](workflow/08_reporting.md) | LaTeX Beamer presentations |
| — | [troubleshooting.md](workflow/troubleshooting.md) | When something goes wrong |
