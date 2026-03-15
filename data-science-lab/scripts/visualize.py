"""Visualization helpers for experiment results."""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd


# Set default style
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 10


def plot_confusion_matrix(cm, labels, title='Confusion Matrix', save_path=None):
    """
    Plot confusion matrix heatmap.
    
    Args:
        cm: Confusion matrix array
        labels: List of class labels
        title: Plot title
        save_path: Optional path to save figure
    
    Returns:
        matplotlib Figure
    """
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=labels, yticklabels=labels)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlabel('Predicted', fontsize=12)
    plt.ylabel('Actual', fontsize=12)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Saved: {save_path}")
    
    return plt.gcf()


def plot_regression_results(y_true, y_pred, title='Actual vs Predicted', save_path=None):
    """
    Plot regression predictions vs actual values.
    
    Args:
        y_true: True values
        y_pred: Predicted values
        title: Plot title
        save_path: Optional path to save figure
    
    Returns:
        matplotlib Figure
    """
    plt.figure(figsize=(10, 6))
    plt.scatter(y_true, y_pred, alpha=0.6, edgecolors='k', linewidth=0.5)
    
    # Perfect prediction line
    min_val = min(y_true.min(), y_pred.min())
    max_val = max(y_true.max(), y_pred.max())
    plt.plot([min_val, max_val], [min_val, max_val], 'r--', lw=2, label='Perfect Prediction')
    
    plt.xlabel('Actual', fontsize=12)
    plt.ylabel('Predicted', fontsize=12)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.legend()
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Saved: {save_path}")
    
    return plt.gcf()


def plot_metric_comparison(df, metric, title=None, save_path=None):
    """
    Plot bar chart comparing models by metric.
    
    Args:
        df: DataFrame with experiment results
        metric: Metric column to plot
        title: Plot title (auto-generated if None)
        save_path: Optional path to save figure
    
    Returns:
        matplotlib Figure
    """
    if 'model' not in df.columns:
        raise ValueError("DataFrame must have 'model' column")
    
    plt.figure(figsize=(10, 6))
    df_sorted = df.sort_values(metric, ascending=False)
    sns.barplot(data=df_sorted, x='model', y=metric, palette='viridis')
    
    plt.title(title or f'{metric.capitalize()} by Model', fontsize=14, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    plt.xlabel('Model', fontsize=12)
    plt.ylabel(metric.capitalize(), fontsize=12)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Saved: {save_path}")
    
    return plt.gcf()


def plot_parameter_sweep(df, param_col, metric, title=None, hue=None, save_path=None):
    """
    Plot parameter sweep results (line plot).
    
    Args:
        df: DataFrame with experiment results
        param_col: Parameter column name
        metric: Metric to plot
        hue: Optional grouping variable
        title: Plot title
        save_path: Optional path to save figure
    
    Returns:
        matplotlib Figure
    """
    plt.figure(figsize=(10, 6))
    
    if hue:
        sns.lineplot(data=df, x=param_col, y=metric, hue=hue, marker='o')
    else:
        sns.lineplot(data=df, x=param_col, y=metric, marker='o')
    
    plt.title(title or f'{metric.capitalize()} vs {param_col}', fontsize=14, fontweight='bold')
    plt.xlabel(param_col, fontsize=12)
    plt.ylabel(metric.capitalize(), fontsize=12)
    
    if df[param_col].dtype in [np.float64, np.int64]:
        try:
            plt.xscale('log')
        except:
            pass
    
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Saved: {save_path}")
    
    return plt.gcf()


def plot_feature_importance(features, importance, title='Feature Importance', save_path=None):
    """
    Plot feature importance bar chart.
    
    Args:
        features: List of feature names
        importance: Array of importance values
        title: Plot title
        save_path: Optional path to save figure
    
    Returns:
        matplotlib Figure
    """
    # Sort by importance
    indices = np.argsort(importance)[::-1]
    
    plt.figure(figsize=(10, 6))
    plt.bar(range(len(features)), importance[indices], color='steelblue')
    plt.xticks(range(len(features)), [features[i] for i in indices], rotation=45, ha='right')
    plt.xlabel('Features', fontsize=12)
    plt.ylabel('Importance', fontsize=12)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Saved: {save_path}")
    
    return plt.gcf()


def plot_learning_curve(train_sizes, train_scores, test_scores, title='Learning Curve', save_path=None):
    """
    Plot learning curve.
    
    Args:
        train_sizes: Array of training set sizes
        train_scores: Array of training scores
        test_scores: Array of test scores
        title: Plot title
        save_path: Optional path to save figure
    
    Returns:
        matplotlib Figure
    """
    train_mean = np.mean(train_scores, axis=1)
    train_std = np.std(train_scores, axis=1)
    test_mean = np.mean(test_scores, axis=1)
    test_std = np.std(test_scores, axis=1)
    
    plt.figure(figsize=(10, 6))
    plt.plot(train_sizes, train_mean, 'o-', color='steelblue', label='Training Score')
    plt.plot(train_sizes, test_mean, 'o-', color='orange', label='Validation Score')
    
    plt.fill_between(train_sizes, train_mean - train_std, train_mean + train_std, alpha=0.1, color='steelblue')
    plt.fill_between(train_sizes, test_mean - test_std, test_mean + test_std, alpha=0.1, color='orange')
    
    plt.xlabel('Training Set Size', fontsize=12)
    plt.ylabel('Score', fontsize=12)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.legend(loc='best')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Saved: {save_path}")
    
    return plt.gcf()


def save_all_plots(df, results_dir='images', metric='accuracy'):
    """
    Save all standard plots.
    
    Args:
        df: DataFrame with experiment results
        results_dir: Directory to save plots
        metric: Primary metric
    """
    import os
    os.makedirs(results_dir, exist_ok=True)
    
    # Metric comparison
    if 'model' in df.columns:
        plot_metric_comparison(df, metric, save_path=f'{results_dir}/metric_comparison.png')
    
    # Parameter sweeps
    if 'alpha' in df.columns:
        plot_parameter_sweep(df, 'alpha', metric, hue='model', save_path=f'{results_dir}/parameter_sweep.png')
    
    print(f"All plots saved to {results_dir}/")


# ---------------------------------------------------------------------------
# NLP & Qualitative Visualization Support
# ---------------------------------------------------------------------------

def plot_topic_distribution(topic_counts, title='Topic Distribution', save_path=None):
    """
    Plot the distribution of topics as a bar chart.
    
    Args:
        topic_counts: DataFrame from analyze_text_topics
        title: Plot title
        save_path: Optional path to save figure
    
    Returns:
        matplotlib Figure
    """
    if 'Topic' not in topic_counts.columns or 'Count' not in topic_counts.columns:
        raise ValueError("topic_counts DataFrame must have 'Topic' and 'Count' columns")

    plt.figure(figsize=(10, 6))
    sns.barplot(data=topic_counts, x='Count', y='Topic', palette='viridis')
    
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlabel('Number of Documents', fontsize=12)
    plt.ylabel('Topic', fontsize=12)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Saved: {save_path}")
    
    return plt.gcf()


def plot_word_frequencies(keywords, title='Top Word Frequencies', save_path=None):
    """
    Plot top words and their frequencies/scores.
    
    Args:
        keywords: List of (word, score) tuples OR DataFrame with 'word', 'score' columns
        title: Plot title
        save_path: Optional path to save figure
        
    Returns:
        matplotlib Figure
    """
    if not isinstance(keywords, pd.DataFrame):
        df_kw = pd.DataFrame(keywords, columns=['word', 'score'])
    else:
        df_kw = keywords.copy()
        
    df_kw = df_kw.sort_values(by='score', ascending=False).head(20)
        
    plt.figure(figsize=(10, 8))
    sns.barplot(data=df_kw, x='score', y='word', palette='mako')
    
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlabel('Importance / Frequency Score', fontsize=12)
    plt.ylabel('Word', fontsize=12)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Saved: {save_path}")
    
    return plt.gcf()

