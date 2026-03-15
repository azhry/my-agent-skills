# Step 9: Visualizations

## Standard Plots

Use the helper scripts to generate plots:

```python
import sys
sys.path.insert(0, '/path/to/data-science-lab/scripts')

from visualize import plot_confusion_matrix, plot_metric_comparison, plot_parameter_sweep, save_all_plots

# Quick: save all standard plots at once
save_all_plots(results_df, results_dir='images', metric='accuracy')

# Or generate individual plots:
plot_metric_comparison(results_df, 'accuracy', save_path='images/model_comparison.png')
plot_parameter_sweep(results_df, 'alpha', 'accuracy', hue='model', save_path='images/param_sweep.png')
plot_confusion_matrix(cm, labels=['Class A', 'Class B'], save_path='images/confusion_matrix.png')
```

### Additional Plot Functions

```python
from visualize import plot_feature_importance, plot_learning_curve, plot_regression_results

# Feature importance (for tree-based models)
plot_feature_importance(feature_names, model.feature_importances_, save_path='images/fi.png')

# Learning curve
plot_learning_curve(train_sizes, train_scores, test_scores, save_path='images/learning.png')

# Regression: actual vs predicted
plot_regression_results(y_test, y_pred, save_path='images/actual_vs_predicted.png')
```

### NLP Visualization

```python
from visualize import plot_topic_distribution, plot_word_frequencies

# Topic distribution bar chart
plot_topic_distribution(topic_counts_df, save_path='images/topics.png')

# Top word frequencies
plot_word_frequencies(keywords_list, save_path='images/keywords.png')
```

## Infographics

For publication-quality, multi-panel infographics:

```python
from create_infographics import (
    create_experiment_infographic,
    create_comparison_infographic,
    create_mini_infographic,
    create_nlp_infographic,
    export_infographic,
    export_multi_format,
)

# Full infographic with hero banner, podium, heatmap, radar, stats card
fig = create_experiment_infographic(
    results_df, title='Lab 1 Results', metric='accuracy',
    theme='dark', palette='ocean'
)
export_infographic(fig, 'images/lab1_infographic.png')

# Compact version for embedding in reports
fig_mini = create_mini_infographic(results_df, title='Quick Summary')
export_infographic(fig_mini, 'images/lab1_mini.png')

# Compare classification vs regression side-by-side
fig_cmp = create_comparison_infographic(clf_df, reg_df, title='Classification vs Regression')
export_multi_format(fig_cmp, 'images/comparison')  # saves .png and .pdf

# NLP-specific infographic
fig_nlp = create_nlp_infographic(topic_counts, keywords_df, title='NLP Results')
export_infographic(fig_nlp, 'images/nlp_infographic.png')
```

### Infographic Options

| Option | Values | Default |
|--------|--------|---------|
| `theme` | `'dark'`, `'light'` | `'dark'` |
| `palette` | `'ocean'`, `'sunset'`, `'forest'`, `'purple'`, `'slate'`, `'candy'` | `'ocean'` |
| `dpi` | Any integer | `300` |

### One-Liner Convenience Functions

```python
from create_infographics import quick_infographic, quick_comparison

# CSV → infographic in one call
quick_infographic('results/results.csv', 'images/infographic.png', title='Results')

# Two CSVs → comparison infographic
quick_comparison('results/clf.csv', 'results/reg.csv', 'images/comparison.png')
```

Save all visualizations to an `images/` or `figures/` directory.
