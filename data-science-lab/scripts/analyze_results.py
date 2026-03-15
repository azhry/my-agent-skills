"""Analysis helper for experiment results."""

import pandas as pd
import numpy as np


def find_best_model(df, metric='accuracy'):
    """
    Find the best performing model.
    
    Args:
        df: DataFrame with experiment results
        metric: Metric column to optimize (default: 'accuracy')
    
    Returns:
        Series with best model row
    """
    if metric not in df.columns:
        raise ValueError(f"Metric '{metric}' not found in DataFrame. Available: {df.columns.tolist()}")
    
    best_idx = df[metric].idxmax()
    return df.loc[best_idx]


def compare_models(df, metric='accuracy'):
    """
    Compare models by metric.
    
    Args:
        df: DataFrame with experiment results
        metric: Metric column to compare
    
    Returns:
        Series with mean metric by model
    """
    if 'model' not in df.columns:
        raise ValueError("DataFrame must have 'model' column")
    
    return df.groupby('model')[metric].mean().sort_values(ascending=False)


def compare_experiments(df, group_by='experiment', metric='accuracy'):
    """
    Compare experiment types.
    
    Args:
        df: DataFrame with experiment results
        group_by: Column to group by
        metric: Metric column to compare
    
    Returns:
        DataFrame with grouped statistics
    """
    return df.groupby(group_by)[metric].agg(['mean', 'std', 'min', 'max']).round(4)


def find_optimal_parameter(df, param_col, metric='accuracy'):
    """
    Find optimal parameter value.
    
    Args:
        df: DataFrame with parameter values
        param_col: Parameter column name
        metric: Metric to optimize
    
    Returns:
        Optimal parameter value
    """
    best_idx = df[metric].idxmax()
    return df.loc[best_idx, param_col]


def generate_insights(df, metric='accuracy'):
    """
    Generate key insights from experiment results.
    
    Args:
        df: DataFrame with experiment results
        metric: Primary metric
    
    Returns:
        Dictionary with insights
    """
    insights = {}
    
    # Best model
    best = find_best_model(df, metric)
    insights['best_model'] = best.get('model', 'Unknown')
    insights['best_score'] = best.get(metric, 0)
    
    # Model comparison
    if 'model' in df.columns:
        model_comparison = compare_models(df, metric)
        insights['model_ranking'] = model_comparison.to_dict()
    
    # Experiment type comparison
    if 'experiment' in df.columns:
        exp_comparison = compare_experiments(df, 'experiment', metric)
        insights['experiment_ranking'] = exp_comparison.to_dict()
    
    # Overall statistics
    insights['overall_stats'] = {
        'mean': df[metric].mean(),
        'std': df[metric].std(),
        'min': df[metric].min(),
        'max': df[metric].max()
    }
    
    return insights


def summarize_experiments(df):
    """
    Generate summary statistics.
    
    Args:
        df: DataFrame with experiment results
    
    Returns:
        DataFrame with summary statistics
    """
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    return df[numeric_cols].describe().round(4)


def print_summary(df, metric='accuracy'):
    """
    Print a formatted summary of experiment results.
    
    Args:
        df: DataFrame with experiment results
        metric: Primary metric to highlight
    """
    print("=" * 60)
    print("EXPERIMENT SUMMARY")
    print("=" * 60)
    
    # Best model
    best = find_best_model(df, metric)
    print(f"\n🏆 Best Model: {best.get('model', 'Unknown')}")
    print(f"   {metric}: {best.get(metric, 0):.4f}")
    
    # Model comparison
    if 'model' in df.columns:
        print("\n📊 Model Rankings:")
        for model, score in compare_models(df, metric).items():
            print(f"   {model}: {score:.4f}")
    
    # Summary stats
    print("\n📈 Overall Statistics:")
    stats = df[metric].describe()
    print(f"   Mean: {stats['mean']:.4f}")
    print(f"   Std:  {stats['std']:.4f}")
    print(f"   Min:  {stats['min']:.4f}")
    print(f"   Max:  {stats['max']:.4f}")
    
    print("=" * 60)


# ---------------------------------------------------------------------------
# NLP & Qualitative Analysis Support
# ---------------------------------------------------------------------------

def analyze_text_topics(df, topic_col='topic_label', text_col='text'):
    """
    Analyze topic distribution and characteristics from NLP experiments.
    
    Args:
        df: DataFrame with mapped topics
        topic_col: Name of the column containing assigned topics
        text_col: Name of the column containing raw text
        
    Returns:
        DataFrame summarizing topic frequencies and sample lengths
    """
    if topic_col not in df.columns:
        raise ValueError(f"Topic column '{topic_col}' not found. Available: {df.columns.tolist()}")
        
    # Basic value counts
    topic_counts = df[topic_col].value_counts().reset_index()
    topic_counts.columns = ['Topic', 'Count']
    topic_counts['Percentage'] = (topic_counts['Count'] / len(df) * 100).round(2)
    
    # Analyze text length per topic if text is available
    if text_col in df.columns:
        df_copy = df.copy()
        df_copy['text_length'] = df_copy[text_col].astype(str).apply(len)
        length_stats = df_copy.groupby(topic_col)['text_length'].mean().round(0).reset_index()
        length_stats.columns = ['Topic', 'Avg_Length_Chars']
        topic_counts = pd.merge(topic_counts, length_stats, on='Topic', how='left')
        
    return topic_counts

