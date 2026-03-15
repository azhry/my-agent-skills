"""
Exploratory Data Analysis (EDA) Module
=======================================

A generic, dataset-agnostic EDA module that works with any tabular dataset.
Provides comprehensive analysis including:
  - Data overview (shape, types, head/tail)
  - Data quality assessment (missing values, duplicates, cardinality)
  - Univariate analysis (distributions of numerical & categorical features)
  - Bivariate analysis (correlations, grouped comparisons)
  - Outlier detection (z-score & IQR methods)
  - Summary report generation

Usage:
------
    # In a notebook or script:
    import pandas as pd
    from run_eda import run_full_eda

    df = pd.read_csv('path/to/data.csv')
    run_full_eda(df, output_dir='images', title='My Dataset EDA')

    # Or use individual functions:
    from run_eda import (
        data_overview, data_quality_report, univariate_analysis,
        bivariate_analysis, outlier_detection
    )
"""

import os
import warnings
from typing import Optional, List, Tuple

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

warnings.filterwarnings('ignore')

# ─── Visualization defaults ──────────────────────────────────────────────
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 12
sns.set_palette('husl')

# Force non-interactive backend to avoid blocking dialogs
import matplotlib
matplotlib.use('Agg')

MAX_CATEGORIES_FOR_PIE = 10
MAX_CATEGORIES_FOR_BAR = 30
OUTLIER_ZSCORE_THRESHOLD = 3.0


# ═════════════════════════════════════════════════════════════════════════
#  Helpers
# ═════════════════════════════════════════════════════════════════════════

def _classify_columns(df: pd.DataFrame,
                      exclude_cols: Optional[List[str]] = None,
                      id_threshold: float = 0.95) -> dict:
    """
    Automatically classify columns into numerical, categorical, datetime,
    and potential ID columns.

    Parameters
    ----------
    df : DataFrame
    exclude_cols : list of column names to ignore
    id_threshold : ratio of unique-values / row-count above which an
                   integer column is treated as a likely ID column

    Returns
    -------
    dict with keys: 'numerical', 'categorical', 'datetime', 'id_like'
    """
    exclude = set(exclude_cols or [])
    numerical, categorical, datetime_cols, id_like = [], [], [], []

    for col in df.columns:
        if col in exclude:
            continue

        dtype = df[col].dtype
        nunique = df[col].nunique()

        # datetime
        if pd.api.types.is_datetime64_any_dtype(dtype):
            datetime_cols.append(col)
            continue

        # numerical
        if pd.api.types.is_numeric_dtype(dtype):
            # heuristic: if almost every value is unique → probably an ID
            if nunique / max(len(df), 1) >= id_threshold:
                id_like.append(col)
            else:
                numerical.append(col)
            continue

        # everything else is categorical
        categorical.append(col)

    return {
        'numerical': numerical,
        'categorical': categorical,
        'datetime': datetime_cols,
        'id_like': id_like,
    }


def _discuss(title: str, body: str):
    """Print a human-readable discussion block with rationale."""
    print(f"\n  💬 {title}")
    for line in body.strip().split('\n'):
        print(f"     {line}")
    print()


def _save_fig(fig, path: Optional[str], dpi: int = 150):
    """Save figure to *path* (creating dirs)."""
    if path:
        os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
        fig.savefig(path, dpi=dpi, bbox_inches='tight')
        print(f"\n✅ Saved: {path}")
        
    plt.close(fig)


# ═════════════════════════════════════════════════════════════════════════
#  1.  Data overview
# ═════════════════════════════════════════════════════════════════════════

def data_overview(df: pd.DataFrame,
                  n_rows: int = 10) -> dict:
    """
    Print (and return) a quick overview of the dataset:
    shape, dtypes, head, statistical summary.
    """
    print("=" * 60)
    print("DATASET OVERVIEW")
    print("=" * 60)
    print(f"\nDataset Shape: {df.shape[0]} rows × {df.shape[1]} columns")
    print(f"\nColumn Names:\n{df.columns.tolist()}")

    print("\n📊 DATA TYPES:")
    print("-" * 40)
    print(df.dtypes)

    print(f"\n📋 FIRST {n_rows} ROWS:")
    print("-" * 40)
    display_func = _get_display()
    display_func(df.head(n_rows))

    print("\n📈 STATISTICAL SUMMARY (Numeric Columns):")
    print("-" * 60)
    desc = df.describe().round(2)
    display_func(desc)

    # Build dynamic discussion
    n_num = len(df.select_dtypes(include='number').columns)
    n_cat = len(df.select_dtypes(include='object').columns)
    _discuss(
        "Why this matters",
        f"Understanding the dataset shape and types is the first step\n"
        f"in any analysis. We have {df.shape[0]:,} observations across\n"
        f"{df.shape[1]} features ({n_num} numerical, {n_cat} categorical).\n"
        f"The statistical summary shows the central tendency (mean/median),\n"
        f"spread (std, min-max), and quartiles of each numerical feature.\n"
        f"Look for: large differences between mean and median (potential\n"
        f"skewness), very high std relative to mean (high variability),\n"
        f"or suspicious min/max values (data entry errors)."
    )

    return {
        'shape': df.shape,
        'dtypes': df.dtypes.to_dict(),
        'describe': desc,
    }


# ═════════════════════════════════════════════════════════════════════════
#  2.  Data‑quality assessment
# ═════════════════════════════════════════════════════════════════════════

def data_quality_report(df: pd.DataFrame) -> dict:
    """
    Assess data quality: missing values, duplicates, column cardinality.
    """
    print("\n" + "=" * 60)
    print("DATA QUALITY ASSESSMENT")
    print("=" * 60)

    # ── Missing values ────────────────────────────────────────────
    print("\n❌ MISSING VALUES ANALYSIS:")
    print("-" * 50)
    missing = df.isnull().sum()
    missing_pct = (missing / len(df) * 100).round(2)
    missing_df = pd.DataFrame({
        'Missing Count': missing,
        'Percentage (%)': missing_pct
    })
    cols_with_missing = missing_df[missing_df['Missing Count'] > 0]
    if len(cols_with_missing):
        print(cols_with_missing)
    else:
        print("No missing values found – dataset is complete! 🎉")

    total_missing = df.isnull().sum().sum()
    complete_rows = df.dropna().shape[0]
    print(f"\nTotal missing values: {total_missing}")
    print(f"Complete rows: {complete_rows} ({complete_rows / max(len(df), 1) * 100:.1f}%)")

    # ── Duplicates ────────────────────────────────────────────────
    print("\n🔄 DUPLICATE ROWS:")
    print("-" * 40)
    dup_count = df.duplicated().sum()
    print(f"Total duplicate rows: {dup_count}")
    if dup_count > 0:
        print("Sample duplicates:")
        _get_display()(df[df.duplicated()].head())

    # ── Cardinality ───────────────────────────────────────────────
    print("\n📊 COLUMN CARDINALITY:")
    print("-" * 50)
    cardinality = pd.DataFrame({
        'Unique Values': df.nunique(),
        'Type': df.dtypes,
    })
    _get_display()(cardinality)

    # Build dynamic discussion
    completeness_pct = complete_rows / max(len(df), 1) * 100
    if total_missing == 0:
        missing_msg = ("The dataset is complete with no missing values — no\n"
                       "imputation or row-dropping will be needed.")
    elif completeness_pct > 95:
        missing_msg = (f"Only {100 - completeness_pct:.1f}% of rows have missing values.\n"
                       f"This is a small fraction — dropping these rows is a safe\n"
                       f"option, or you can impute with median/mode if you prefer\n"
                       f"to preserve every observation.")
    else:
        missing_msg = (f"{100 - completeness_pct:.1f}% of rows have missing values.\n"
                       f"This is significant — imputation (median for numbers,\n"
                       f"mode for categories) is recommended over dropping rows\n"
                       f"to avoid losing too much data.")

    dup_msg = ("No duplicate rows found — the data appears clean."
              if dup_count == 0
              else f"{dup_count} duplicate rows detected. Investigate whether\n"
                   f"they are true duplicates (remove them) or valid repeated\n"
                   f"observations (keep them).")

    _discuss(
        "Data Quality Assessment",
        f"{missing_msg}\n\n"
        f"{dup_msg}\n\n"
        f"Cardinality (unique value count) helps identify:\n"
        f"• Columns with only 1 value → useless for prediction (drop them)\n"
        f"• Very high cardinality → likely IDs or free-text (exclude from modeling)\n"
        f"• Low cardinality numbers → consider treating as categorical"
    )

    return {
        'missing': cols_with_missing,
        'total_missing': total_missing,
        'complete_rows': complete_rows,
        'duplicates': dup_count,
        'cardinality': cardinality,
    }


# ═════════════════════════════════════════════════════════════════════════
#  3.  Univariate analysis
# ═════════════════════════════════════════════════════════════════════════

def univariate_analysis(df: pd.DataFrame,
                        col_info: Optional[dict] = None,
                        output_dir: Optional[str] = None) -> None:
    """
    Univariate distributions for every detected numerical and categorical
    column.  Figures are optionally saved to *output_dir*.
    """
    if col_info is None:
        col_info = _classify_columns(df)

    print("\n" + "=" * 60)
    print("UNIVARIATE ANALYSIS")
    print("=" * 60)

    # ── Categorical ───────────────────────────────────────────────
    cat_cols = col_info['categorical']
    if cat_cols:
        _plot_categorical_distributions(df, cat_cols, output_dir)

        # Discussion for categorical
        imbalanced = []
        for col in cat_cols:
            vc = df[col].value_counts(normalize=True)
            if vc.iloc[0] > 0.8:
                imbalanced.append(col)

        cat_msg = f"Plotted distributions for {len(cat_cols)} categorical feature(s).\n"
        if imbalanced:
            cat_msg += (f"⚠️ Imbalanced categories detected in: {imbalanced}.\n"
                        f"Dominant categories (>80%) can bias models — consider\n"
                        f"oversampling, undersampling, or weighted loss functions.\n")
        else:
            cat_msg += "Category distributions appear reasonably balanced.\n"
        cat_msg += ("Pie charts show relative proportions, bar charts show\n"
                    "absolute counts. Use this to understand class balance\n"
                    "and decide if stratification is needed during splitting.")
        _discuss("Categorical Distributions — What to look for", cat_msg)

    # ── Numerical ─────────────────────────────────────────────────
    num_cols = col_info['numerical']
    if num_cols:
        _plot_numerical_distributions(df, num_cols, output_dir)

        # Discussion for numerical
        skewed = []
        for col in num_cols:
            skew_val = df[col].skew()
            if abs(skew_val) > 1:
                skewed.append((col, round(skew_val, 2)))

        num_msg = f"Plotted distributions for {len(num_cols)} numerical feature(s).\n"
        if skewed:
            skew_list = ', '.join(f"{c} (skew={s})" for c, s in skewed)
            num_msg += (f"⚠️ Skewed features detected: {skew_list}.\n"
                        f"Highly skewed distributions can affect models that\n"
                        f"assume normality (e.g., linear regression). Consider\n"
                        f"log or Box-Cox transformations for these features.\n")
        else:
            num_msg += "All numerical features appear approximately symmetric.\n"
        num_msg += ("The red KDE curve overlaid on each histogram shows the\n"
                    "estimated probability density. Multi-modal distributions\n"
                    "(multiple peaks) may indicate subgroups in the data.")
        _discuss("Numerical Distributions — What to look for", num_msg)


def _plot_categorical_distributions(df, cols, output_dir):
    n = len(cols)
    if n == 0:
        return
    ncols_grid = min(n, 2)
    nrows_grid = (n + ncols_grid - 1) // ncols_grid
    fig, axes = plt.subplots(nrows_grid, ncols_grid,
                             figsize=(7 * ncols_grid, 5 * nrows_grid))
    if n == 1:
        axes = np.array([axes])
    axes = axes.flatten()

    fig.suptitle('Categorical Feature Distributions', fontsize=20, fontweight='bold', y=1.02)
    plt.figtext(0.5, 0.01, "Percentage (%) for pie charts, Absolute counts for bar charts. Use for identifying class imbalance.", ha="center", fontsize=12, bbox={"facecolor":"orange", "alpha":0.2, "pad":5})

    for idx, col in enumerate(cols):
        ax = axes[idx]
        vc = df[col].value_counts()
        n_cats = len(vc)

        if n_cats <= MAX_CATEGORIES_FOR_PIE:
            wedges, texts, autotexts = ax.pie(vc, labels=vc.index, autopct='%1.1f%%',
                   colors=sns.color_palette('husl', n_cats), startangle=90)
            ax.legend(wedges, vc.index, title=col, loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        elif n_cats <= MAX_CATEGORIES_FOR_BAR:
            ax.barh(vc.index, vc.values,
                    color=sns.color_palette('Set2', n_cats))
            ax.set_xlabel('Count')
        else:
            vc_top = vc.head(MAX_CATEGORIES_FOR_BAR)
            ax.barh(vc_top.index, vc_top.values,
                    color=sns.color_palette('Set2', len(vc_top)))
            ax.set_xlabel('Count')
            ax.set_title(f'{col} (top {MAX_CATEGORIES_FOR_BAR})',
                         fontsize=14, fontweight='bold')
            continue

        ax.set_title(f'{col} Distribution', fontsize=14, fontweight='bold')

    for idx in range(n, len(axes)):
        axes[idx].set_visible(False)

    plt.tight_layout()
    _save_fig(fig, os.path.join(output_dir, 'eda_categorical_distributions.png')
              if output_dir else None)


def _plot_numerical_distributions(df, cols, output_dir):
    n = len(cols)
    if n == 0:
        return
    ncols_grid = min(n, 2)
    nrows_grid = (n + ncols_grid - 1) // ncols_grid
    fig, axes = plt.subplots(nrows_grid, ncols_grid,
                             figsize=(7 * ncols_grid, 5 * nrows_grid))
    if n == 1:
        axes = np.array([axes])
    axes = axes.flatten()

    fig.suptitle('Numerical Feature Distributions', fontsize=20, fontweight='bold', y=1.02)
    plt.figtext(0.5, 0.01, "Histograms show frequency; Red curve is KDE (Probability Density). Look for skewness or multi-modality.", ha="center", fontsize=12, bbox={"facecolor":"blue", "alpha":0.1, "pad":5})

    for idx, col in enumerate(cols):
        ax = axes[idx]
        data = df[col].dropna()
        ax.hist(data, bins='auto', edgecolor='black', alpha=0.7,
                color=sns.color_palette('husl')[idx % len(sns.color_palette('husl'))])
        ax.set_title(f'{col} Distribution', fontsize=14, fontweight='bold')
        ax.set_xlabel(col)
        ax.set_ylabel('Frequency')

        # overlay KDE on twin axis
        ax2 = ax.twinx()
        try:
            sns.kdeplot(data, ax=ax2, color='red', linewidth=2)
        except Exception:
            pass
        ax2.set_ylabel('')
        ax2.set_yticks([])

    for idx in range(n, len(axes)):
        axes[idx].set_visible(False)

    plt.tight_layout()
    _save_fig(fig, os.path.join(output_dir, 'eda_numerical_distributions.png')
              if output_dir else None)


# ═════════════════════════════════════════════════════════════════════════
#  4.  Bivariate / multivariate analysis
# ═════════════════════════════════════════════════════════════════════════

def bivariate_analysis(df: pd.DataFrame,
                       col_info: Optional[dict] = None,
                       target_col: Optional[str] = None,
                       output_dir: Optional[str] = None) -> None:
    """
    Bivariate analysis:
      • Correlation heatmap for numerical features
      • Box-plots of numerical features grouped by *target_col* (if categorical)
      • Cross-tabulations between categorical features
    """
    if col_info is None:
        col_info = _classify_columns(df)

    print("\n" + "=" * 60)
    print("BIVARIATE / MULTIVARIATE ANALYSIS")
    print("=" * 60)

    num_cols = col_info['numerical']
    cat_cols = col_info['categorical']

    # ── Correlation heatmap ───────────────────────────────────────
    if len(num_cols) >= 2:
        _plot_correlation_heatmap(df, num_cols, output_dir)

        # Discussion: correlations
        corr = df[num_cols].corr()
        high_corr = []
        for i in range(len(num_cols)):
            for j in range(i + 1, len(num_cols)):
                r = abs(corr.iloc[i, j])
                if r > 0.7:
                    high_corr.append((num_cols[i], num_cols[j], round(r, 2)))

        corr_msg = "The correlation heatmap reveals linear relationships\n"
        corr_msg += "between numerical features.\n"
        if high_corr:
            pairs = ', '.join(f"{a} ↔ {b} (r={r})" for a, b, r in high_corr)
            corr_msg += (f"\n⚠️ Highly correlated pairs (|r| > 0.7): {pairs}.\n"
                         f"High correlation means these features carry similar\n"
                         f"information. Consider dropping one from each pair to\n"
                         f"reduce multicollinearity, especially for linear models.")
        else:
            corr_msg += ("\nNo strongly correlated pairs found (all |r| < 0.7).\n"
                         "Features appear to carry independent information.")
        _discuss("Correlation Analysis — Rationale", corr_msg)

    # ── Grouped box-plots ────────────────────────────────────────
    if target_col and target_col in cat_cols and len(num_cols) > 0:
        if df[target_col].nunique() <= MAX_CATEGORIES_FOR_PIE:
            _plot_grouped_boxplots(df, num_cols, target_col, output_dir)

            _discuss(
                f"Grouped Analysis by '{target_col}' — Rationale",
                f"Box-plots grouped by the target variable show how each\n"
                f"numerical feature differs across categories. Features\n"
                f"with clearly separated boxes (non-overlapping medians\n"
                f"and IQR ranges) are strong candidates for prediction.\n"
                f"Features where boxes overlap heavily may contribute\n"
                f"less discriminative power to the model."
            )

    # ── Scatter matrix ────────────────────────────────────────────
    if 2 <= len(num_cols) <= 8:
        _plot_scatter_matrix(df, num_cols, target_col, output_dir)

    # ── Cross-tabs ────────────────────────────────────────────────
    if len(cat_cols) >= 2:
        _print_cross_tabs(df, cat_cols)


def _plot_correlation_heatmap(df, num_cols, output_dir):
    corr = df[num_cols].corr().round(2)
    fig, ax = plt.subplots(figsize=(max(8, len(num_cols)),
                                     max(6, len(num_cols) * 0.8)))
    sns.heatmap(corr, annot=True, cmap='coolwarm', center=0,
                fmt='.2f', linewidths=0.5, ax=ax)
    ax.set_title('Correlation Heatmap', fontsize=16, fontweight='bold')
    plt.tight_layout()
    _save_fig(fig, os.path.join(output_dir, 'eda_correlation_heatmap.png')
              if output_dir else None)


def _plot_grouped_boxplots(df, num_cols, target_col, output_dir):
    n = len(num_cols)
    ncols_grid = min(n, 2)
    nrows_grid = (n + ncols_grid - 1) // ncols_grid
    fig, axes = plt.subplots(nrows_grid, ncols_grid,
                             figsize=(7 * ncols_grid, 5 * nrows_grid))
    if n == 1:
        axes = np.array([axes])
    axes = axes.flatten()

    fig.suptitle('Numerical Features Grouped by Target', fontsize=20, fontweight='bold', y=1.02)
    plt.figtext(0.5, 0.01, f"Boxplots grouped by '{target_col}'. Separation between boxes suggests strong predictive power for that feature.", ha="center", fontsize=12, bbox={"facecolor":"green", "alpha":0.1, "pad":5})

    for idx, col in enumerate(num_cols):
        ax = axes[idx]
        sns.boxplot(data=df, x=target_col, y=col, ax=ax)
        ax.set_title(f'{col} by {target_col}', fontsize=14, fontweight='bold')

    for idx in range(n, len(axes)):
        axes[idx].set_visible(False)

    plt.tight_layout()
    _save_fig(fig, os.path.join(output_dir, f'eda_grouped_by_{target_col}.png')
              if output_dir else None)


def _plot_scatter_matrix(df, num_cols, target_col, output_dir):
    try:
        fig = plt.figure(figsize=(max(10, len(num_cols) * 3),
                                  max(8, len(num_cols) * 2.5)))
        hue = target_col if (target_col and target_col in df.columns
                             and df[target_col].nunique() <= MAX_CATEGORIES_FOR_PIE) else None
        sns.pairplot(df[num_cols + ([hue] if hue else [])].dropna(),
                     hue=hue, diag_kind='kde', corner=True)
        plt.suptitle('Scatter Matrix', y=1.02, fontsize=16, fontweight='bold')
        plt.figtext(0.5, 0.01, "Pairwise relationships between numerical features. Diagonal shows KDE distributions. Useful for spotting linear correlations and clusters.", ha="center", fontsize=12, bbox={"facecolor":"purple", "alpha":0.1, "pad":5})

        if output_dir:
            path = os.path.join(output_dir, 'eda_scatter_matrix.png')
            os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
            plt.savefig(path, dpi=150, bbox_inches='tight')
            print(f"\n✅ Saved: {path}")
            
        plt.close('all')
    except Exception as e:
        print(f"⚠️  Scatter matrix skipped: {e}")


def _print_cross_tabs(df, cat_cols, max_pairs=3):
    print("\n📊 CROSS-TABULATIONS:")
    print("-" * 50)
    pairs_done = 0
    for i, c1 in enumerate(cat_cols):
        if pairs_done >= max_pairs:
            break
        for c2 in cat_cols[i + 1:]:
            if pairs_done >= max_pairs:
                break
            if df[c1].nunique() <= MAX_CATEGORIES_FOR_PIE and \
               df[c2].nunique() <= MAX_CATEGORIES_FOR_PIE:
                print(f"\n{c1} vs {c2}:")
                ct = pd.crosstab(df[c1], df[c2], margins=True)
                _get_display()(ct)
                pairs_done += 1


# ═════════════════════════════════════════════════════════════════════════
#  5.  Outlier detection
# ═════════════════════════════════════════════════════════════════════════

def outlier_detection(df: pd.DataFrame,
                      col_info: Optional[dict] = None,
                      method: str = 'zscore',
                      threshold: float = OUTLIER_ZSCORE_THRESHOLD,
                      output_dir: Optional[str] = None) -> pd.DataFrame:
    """
    Detect outliers in numerical columns using *method*
    ('zscore' or 'iqr').  Returns a summary DataFrame.
    """
    if col_info is None:
        col_info = _classify_columns(df)

    num_cols = col_info['numerical']
    if not num_cols:
        print("No numerical columns to check for outliers.")
        return pd.DataFrame()

    print("\n" + "=" * 60)
    print(f"OUTLIER DETECTION  (method={method}, threshold={threshold})")
    print("=" * 60)

    records = []
    for col in num_cols:
        data = df[col].dropna()
        if method == 'zscore':
            from scipy import stats
            z = np.abs(stats.zscore(data))
            n_outliers = int((z > threshold).sum())
        elif method == 'iqr':
            q1, q3 = data.quantile(0.25), data.quantile(0.75)
            iqr = q3 - q1
            lower, upper = q1 - threshold * iqr, q3 + threshold * iqr
            n_outliers = int(((data < lower) | (data > upper)).sum())
        else:
            raise ValueError(f"Unknown method: {method}")

        records.append({
            'Column': col,
            'Count': len(data),
            'Outliers': n_outliers,
            'Outlier %': round(n_outliers / max(len(data), 1) * 100, 2),
        })

    summary = pd.DataFrame(records)
    _get_display()(summary)

    # Quick box-plot overview
    if len(num_cols) <= 12:
        _plot_outlier_boxplots(df, num_cols, output_dir)

    # Discussion
    total_outliers = sum(r['Outliers'] for r in records)
    heavy_outlier_cols = [r['Column'] for r in records if r['Outlier %'] > 5]

    outlier_msg = (f"Detected {total_outliers} total outlier values across "
                   f"{len(num_cols)} numerical columns.\n")
    if heavy_outlier_cols:
        outlier_msg += (f"\n⚠️ Columns with >5% outliers: {heavy_outlier_cols}.\n"
                        f"High outlier rates may indicate:\n"
                        f"• Natural heavy-tailed distributions (consider robust models)\n"
                        f"• Data entry errors (investigate specific values)\n"
                        f"• Genuine extreme observations (keep if domain-valid)\n")
    else:
        outlier_msg += "\nOutlier rates are low across all features — good.\n"

    method_desc = {
        'zscore': ('z-score', 'measures how many standard deviations a value is from the mean'),
        'iqr': ('IQR', 'uses the interquartile range — more robust to non-normal distributions'),
    }
    m_name, m_explain = method_desc.get(method, ('unknown', ''))
    outlier_msg += (f"\nMethod used: {m_name} — {m_explain}.\n"
                    f"Next steps: decide whether to keep, cap (winsorize),\n"
                    f"or remove outliers based on domain knowledge.")

    _discuss("Outlier Detection — Rationale", outlier_msg)

    return summary


def _plot_outlier_boxplots(df, num_cols, output_dir):
    n = len(num_cols)
    ncols_grid = min(n, 3)
    nrows_grid = (n + ncols_grid - 1) // ncols_grid
    fig, axes = plt.subplots(nrows_grid, ncols_grid,
                             figsize=(6 * ncols_grid, 4 * nrows_grid))
    if n == 1:
        axes = np.array([axes])
    axes = axes.flatten()

    for idx, col in enumerate(num_cols):
        ax = axes[idx]
        sns.boxplot(y=df[col].dropna(), ax=ax)
        ax.set_title(col, fontsize=13, fontweight='bold')

    for idx in range(n, len(axes)):
        axes[idx].set_visible(False)

    plt.suptitle('Outlier Overview (Box-Plots)', fontsize=16, fontweight='bold')
    plt.tight_layout()
    _save_fig(fig, os.path.join(output_dir, 'eda_outlier_boxplots.png')
              if output_dir else None)


# ═════════════════════════════════════════════════════════════════════════
#  Full EDA orchestrator
# ═════════════════════════════════════════════════════════════════════════

def run_full_eda(df: pd.DataFrame,
                 *,
                 title: str = 'Exploratory Data Analysis',
                 output_dir: Optional[str] = None,
                 target_col: Optional[str] = None,
                 exclude_cols: Optional[List[str]] = None,
                 outlier_method: str = 'zscore',
                 outlier_threshold: float = OUTLIER_ZSCORE_THRESHOLD) -> dict:
    """
    Run a full, generic EDA pipeline on *df*.

    Parameters
    ----------
    df : pandas DataFrame
    title : report title printed at the top
    output_dir : directory to save figures (None → don't save)
    target_col : optional categorical column to use for grouped analyses
    exclude_cols : columns to exclude from analysis (e.g. ID columns)
    outlier_method : 'zscore' or 'iqr'
    outlier_threshold : threshold for outlier detection

    Returns
    -------
    dict with keys:
        overview, quality, col_info, outliers
    """
    print("=" * 60)
    print(f"  {title}")
    print("=" * 60)

    # 0. Classify columns
    col_info = _classify_columns(df, exclude_cols=exclude_cols)

    if col_info['id_like']:
        print(f"\n⚠️  Potential ID columns detected (excluded from analysis): "
              f"{col_info['id_like']}")

    # 1. Overview
    overview = data_overview(df)

    # 2. Quality
    quality = data_quality_report(df)

    # 3. Univariate
    univariate_analysis(df, col_info, output_dir)

    # 4. Bivariate
    bivariate_analysis(df, col_info, target_col, output_dir)

    # 5. Outliers
    outliers = outlier_detection(df, col_info, outlier_method,
                                 outlier_threshold, output_dir)

    # ── Final EDA summary ─────────────────────────────────────────
    _generate_eda_summary(df, col_info, quality, outliers)

    print("\n" + "=" * 60)
    print("  EDA COMPLETE ✅")
    print("=" * 60)

    return {
        'overview': overview,
        'quality': quality,
        'col_info': col_info,
        'outliers': outliers,
    }


def _generate_eda_summary(df, col_info, quality, outlier_summary):
    """Print a comprehensive narrative summary of all EDA findings."""
    print("\n" + "=" * 60)
    print("  EDA SUMMARY & RECOMMENDATIONS")
    print("=" * 60)

    total_missing = quality.get('total_missing', 0)
    duplicates = quality.get('duplicates', 0)
    n_num = len(col_info['numerical'])
    n_cat = len(col_info['categorical'])

    lines = [
        f"Dataset: {df.shape[0]:,} rows × {df.shape[1]} columns "
        f"({n_num} numerical, {n_cat} categorical).",
        "",
    ]

    # Quality
    if total_missing == 0 and duplicates == 0:
        lines.append("✅ Data quality is excellent — no missing values or duplicates.")
    else:
        if total_missing > 0:
            lines.append(f"⚠️  {total_missing} missing values found — "
                         f"handle before modeling (impute or drop).")
        if duplicates > 0:
            lines.append(f"⚠️  {duplicates} duplicate rows — review and deduplicate.")
    lines.append("")

    # Skewness
    skewed = []
    for col in col_info['numerical']:
        try:
            s = df[col].skew()
            if abs(s) > 1:
                skewed.append((col, round(s, 2)))
        except Exception:
            pass
    if skewed:
        skew_list = ', '.join(f"{c} ({s:+.2f})" for c, s in skewed)
        lines.append(f"⚠️  Skewed features: {skew_list}")
        lines.append("   Consider log/sqrt transforms before linear models.")
        lines.append("")

    # Correlations
    if n_num >= 2:
        corr = df[col_info['numerical']].corr()
        high = []
        for i in range(n_num):
            for j in range(i + 1, n_num):
                r = abs(corr.iloc[i, j])
                if r > 0.7:
                    high.append((col_info['numerical'][i],
                                 col_info['numerical'][j], round(r, 2)))
        if high:
            lines.append("⚠️  Highly correlated feature pairs (|r| > 0.7):")
            for a, b, r in high:
                lines.append(f"   • {a} ↔ {b}: r = {r}")
            lines.append("   Consider removing one from each pair for linear models.")
            lines.append("")

    # Outliers
    if isinstance(outlier_summary, pd.DataFrame) and len(outlier_summary) > 0:
        total_out = outlier_summary['Outliers'].sum() if 'Outliers' in outlier_summary.columns else 0
        if total_out > 0:
            lines.append(f"⚠️  {int(total_out)} outlier values detected.")
            lines.append("   Decide: keep (natural variation), cap, or remove.")
        else:
            lines.append("✅ No significant outliers detected.")
        lines.append("")

    # Recommendations
    lines.append("📋 RECOMMENDED NEXT STEPS:")
    lines.append("  1. Handle missing values (if any)")
    lines.append("  2. Address skewness with transforms (if needed)")
    lines.append("  3. Drop or combine highly correlated features")
    lines.append("  4. Encode categorical features for modeling")
    lines.append("  5. Scale numerical features (for distance-based models)")
    lines.append("  6. Proceed to data preparation and modeling")

    _discuss("Summary & Recommendations", '\n'.join(lines))


# ═════════════════════════════════════════════════════════════════════════
#  Utility
# ═════════════════════════════════════════════════════════════════════════

def _get_display():
    """Return IPython display if available, else print."""
    try:
        from IPython.display import display
        return display
    except ImportError:
        return print


# ═════════════════════════════════════════════════════════════════════════
#  CLI entry-point  (python run_eda.py path/to/data.csv)
# ═════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: python run_eda.py <csv_file> [--output-dir DIR] "
              "[--target COL] [--exclude COL1,COL2]")
        sys.exit(1)

    csv_path = sys.argv[1]
    kwargs = {}

    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == '--output-dir' and i + 1 < len(sys.argv):
            kwargs['output_dir'] = sys.argv[i + 1]; i += 2
        elif sys.argv[i] == '--target' and i + 1 < len(sys.argv):
            kwargs['target_col'] = sys.argv[i + 1]; i += 2
        elif sys.argv[i] == '--exclude' and i + 1 < len(sys.argv):
            kwargs['exclude_cols'] = sys.argv[i + 1].split(','); i += 2
        else:
            i += 1

    data = pd.read_csv(csv_path)
    run_full_eda(data, title=f'EDA: {os.path.basename(csv_path)}', **kwargs)
