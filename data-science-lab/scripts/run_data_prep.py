"""
Data Preparation Module
========================

A generic, dataset-agnostic data preparation pipeline that works with any
tabular dataset. Provides step-by-step preparation with **human-readable
discussions** explaining what happened and why at each stage.

Pipeline:
  1. Data Validation (types, duplicates, column info)
  2. Missing Value Handling (drop / impute with strategy selection)
  3. Feature Engineering (automatic ratio & interaction features)
  4. Feature Encoding (label encoding + one-hot encoding)
  5. Feature Scaling (Standard / MinMax / Robust)
  6. Outlier Handling (detect + cap/remove/keep with discussion)
  7. Feature Selection (ANOVA F-score, Mutual Information)
  8. Train/Test Split (stratified for classification, random for regression)
  9. Export Prepared Data (CSV + pickle artifacts)

Usage:
------
    import pandas as pd
    from run_data_prep import run_full_data_prep

    df = pd.read_csv('path/to/data.csv')
    result = run_full_data_prep(
        df,
        target_col='species',
        task_type='classification',   # or 'regression'
        output_dir='data/prepared',
    )

    # result contains: df_clean, X_train, X_test, y_train, y_test,
    #                   encoders, scaler, col_info, ...
"""

import os
import pickle
import warnings
from typing import Optional, List, Dict, Tuple, Any

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

warnings.filterwarnings('ignore')

# ─── Visualization defaults ──────────────────────────────────────────────
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 12


# ═════════════════════════════════════════════════════════════════════════
#  Helpers
# ═════════════════════════════════════════════════════════════════════════

def _get_display():
    """Return IPython display if available, else print."""
    try:
        from IPython.display import display
        return display
    except ImportError:
        return print


def _save_fig(fig, path: Optional[str], dpi: int = 150):
    if path:
        os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
        fig.savefig(path, dpi=dpi, bbox_inches='tight')
        print(f"  ✅ Saved: {path}")
    plt.show()
    plt.close(fig)


def _classify_columns(df: pd.DataFrame,
                      target_col: Optional[str] = None,
                      exclude_cols: Optional[List[str]] = None,
                      id_threshold: float = 0.95) -> dict:
    """Auto-classify columns into numerical, categorical, datetime, id-like."""
    exclude = set(exclude_cols or [])
    if target_col:
        exclude.add(target_col)

    numerical, categorical, datetime_cols, id_like = [], [], [], []

    for col in df.columns:
        if col in exclude:
            continue
        dtype = df[col].dtype
        nunique = df[col].nunique()

        if pd.api.types.is_datetime64_any_dtype(dtype):
            datetime_cols.append(col)
        elif pd.api.types.is_numeric_dtype(dtype):
            if nunique / max(len(df), 1) >= id_threshold:
                id_like.append(col)
            else:
                numerical.append(col)
        else:
            categorical.append(col)

    return {
        'numerical': numerical,
        'categorical': categorical,
        'datetime': datetime_cols,
        'id_like': id_like,
    }


def _discuss(title: str, body: str):
    """Print a human-readable discussion block."""
    print(f"\n  💬 {title}")
    for line in body.strip().split('\n'):
        print(f"     {line}")
    print()


# ═════════════════════════════════════════════════════════════════════════
#  1. Data Validation
# ═════════════════════════════════════════════════════════════════════════

def validate_data(df: pd.DataFrame,
                  col_info: dict) -> dict:
    """Check types, duplicates, and column info. Returns summary dict."""
    print("=" * 60)
    print("STEP 1: DATA VALIDATION")
    print("=" * 60)

    print(f"\n  Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
    print(f"\n  📋 DATA TYPES:")
    print("  " + "-" * 40)
    for col in df.columns:
        print(f"    {col}: {df[col].dtype}, "
              f"unique={df[col].nunique()}, "
              f"nulls={df[col].isnull().sum()}")

    duplicates = df.duplicated().sum()
    print(f"\n  🔄 Duplicate rows: {duplicates}")

    _discuss(
        "What this tells us",
        f"The dataset has {df.shape[0]:,} rows and {df.shape[1]} columns.\n"
        f"We detected {len(col_info['numerical'])} numerical, "
        f"{len(col_info['categorical'])} categorical, "
        f"and {len(col_info['id_like'])} likely ID columns.\n"
        f"{'No duplicates found — good!' if duplicates == 0 else f'{duplicates} duplicate rows should be reviewed.'}"
    )

    return {'duplicates': duplicates}


# ═════════════════════════════════════════════════════════════════════════
#  2. Missing Value Handling
# ═════════════════════════════════════════════════════════════════════════

def handle_missing_values(df: pd.DataFrame,
                          col_info: dict,
                          strategy: str = 'auto',
                          missing_threshold: float = 0.5) -> pd.DataFrame:
    """
    Handle missing values.

    strategy:
        'auto'   – drop cols with >50% missing, impute rest
                   (median for numerical, mode for categorical)
        'drop'   – drop all rows with any NaN
        'impute' – impute all (median / mode)
    """
    print("\n" + "=" * 60)
    print("STEP 2: MISSING VALUE HANDLING")
    print("=" * 60)

    total = df.isnull().sum().sum()
    if total == 0:
        print("\n  No missing values — dataset is complete! 🎉")
        _discuss("Discussion",
                 "The dataset has no missing values, so no imputation or\n"
                 "row-dropping is needed. This is ideal for modeling.")
        return df.copy()

    # Report
    missing = df.isnull().sum()
    missing_pct = (missing / len(df) * 100).round(2)
    missing_report = pd.DataFrame({
        'Missing': missing,
        'Percentage (%)': missing_pct,
    })
    cols_with_missing = missing_report[missing_report['Missing'] > 0]
    print("\n  ❌ Columns with missing values:")
    for _, row in cols_with_missing.iterrows():
        print(f"    {row.name}: {int(row['Missing'])} ({row['Percentage (%)']}%)")

    df_out = df.copy()

    if strategy == 'drop':
        before = len(df_out)
        df_out = df_out.dropna()
        after = len(df_out)
        _discuss("Strategy: Drop rows with missing values",
                 f"Removed {before - after} rows ({(before - after) / before * 100:.1f}%).\n"
                 f"This is the simplest approach but can lose data.\n"
                 f"Remaining: {after:,} rows.")

    elif strategy == 'impute':
        df_out = _impute_all(df_out, col_info)

    else:  # auto
        # Drop columns with too many missing values
        high_missing = [c for c in cols_with_missing.index
                        if cols_with_missing.loc[c, 'Percentage (%)'] > missing_threshold * 100]
        if high_missing:
            df_out = df_out.drop(columns=high_missing)
            print(f"\n  Dropped columns with >{missing_threshold*100:.0f}% missing: {high_missing}")

        remaining_missing = df_out.isnull().sum().sum()
        if remaining_missing > 0:
            pct_rows = df_out.isnull().any(axis=1).sum() / len(df_out) * 100
            if pct_rows < 5:
                before = len(df_out)
                df_out = df_out.dropna()
                _discuss("Strategy: Auto (drop rows — few missing)",
                         f"Only {pct_rows:.1f}% of rows had missing values, so we\n"
                         f"dropped them ({before - len(df_out)} rows removed).\n"
                         f"This keeps the data clean with minimal loss.")
            else:
                df_out = _impute_all(df_out, col_info)

    return df_out


def _impute_all(df: pd.DataFrame, col_info: dict) -> pd.DataFrame:
    """Impute numerical cols with median, categorical with mode."""
    from sklearn.impute import SimpleImputer

    num_cols = [c for c in col_info['numerical'] if c in df.columns and df[c].isnull().any()]
    cat_cols = [c for c in col_info['categorical'] if c in df.columns and df[c].isnull().any()]

    if num_cols:
        imp = SimpleImputer(strategy='median')
        df[num_cols] = imp.fit_transform(df[num_cols])
        print(f"  Imputed numerical columns (median): {num_cols}")

    if cat_cols:
        imp = SimpleImputer(strategy='most_frequent')
        df[cat_cols] = imp.fit_transform(df[cat_cols])
        print(f"  Imputed categorical columns (mode): {cat_cols}")

    _discuss("Strategy: Imputation",
             "Numerical columns were filled with the median (robust to\n"
             "outliers), and categorical columns were filled with the\n"
             "most frequent value. No rows were lost.")
    return df


# ═════════════════════════════════════════════════════════════════════════
#  3. Feature Encoding
# ═════════════════════════════════════════════════════════════════════════

def encode_features(df: pd.DataFrame,
                    col_info: dict,
                    target_col: Optional[str] = None,
                    encoding: str = 'label') -> Tuple[pd.DataFrame, dict]:
    """
    Encode categorical features.

    encoding: 'label', 'onehot', or 'both'
    Returns (df_encoded, encoders_dict)
    """
    from sklearn.preprocessing import LabelEncoder

    print("\n" + "=" * 60)
    print("STEP 3: FEATURE ENCODING")
    print("=" * 60)

    cat_cols = [c for c in col_info['categorical'] if c in df.columns]
    if not cat_cols:
        print("\n  No categorical columns to encode.")
        return df.copy(), {}

    df_out = df.copy()
    encoders = {}

    # Label encoding
    if encoding in ('label', 'both'):
        print("\n  🏷️  LABEL ENCODING:")
        for col in cat_cols:
            le = LabelEncoder()
            df_out[f'{col}_encoded'] = le.fit_transform(df_out[col].astype(str))
            encoders[col] = le
            mapping = dict(zip(le.classes_, range(len(le.classes_))))
            print(f"    {col}: {mapping}")

    # Also encode target if it's categorical
    if target_col and target_col in df_out.columns:
        if df_out[target_col].dtype == 'object':
            le_target = LabelEncoder()
            df_out[f'{target_col}_encoded'] = le_target.fit_transform(df_out[target_col])
            encoders[target_col] = le_target
            print(f"    {target_col} (target): "
                  f"{dict(zip(le_target.classes_, range(len(le_target.classes_))))}")

    # One-hot encoding
    if encoding in ('onehot', 'both'):
        print("\n  🔥 ONE-HOT ENCODING:")
        df_onehot = pd.get_dummies(df_out, columns=cat_cols, prefix=cat_cols)
        new_cols = [c for c in df_onehot.columns if c not in df_out.columns]
        print(f"    Created {len(new_cols)} binary columns")
        if encoding == 'onehot':
            df_out = df_onehot

    _discuss("Discussion",
             f"Encoded {len(cat_cols)} categorical column(s): {cat_cols}.\n"
             f"Label encoding assigns each category a unique integer.\n"
             f"This works well for tree-based models. For linear models,\n"
             f"consider using one-hot encoding to avoid ordinal assumptions.")

    return df_out, encoders


# ═════════════════════════════════════════════════════════════════════════
#  4. Feature Scaling
# ═════════════════════════════════════════════════════════════════════════

def scale_features(df: pd.DataFrame,
                   col_info: dict,
                   method: str = 'standard',
                   output_dir: Optional[str] = None) -> Tuple[pd.DataFrame, Any]:
    """
    Scale numerical features.

    method: 'standard', 'minmax', or 'robust'
    Returns (df_scaled, fitted_scaler)
    """
    from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler

    print("\n" + "=" * 60)
    print("STEP 4: FEATURE SCALING")
    print("=" * 60)

    num_cols = [c for c in col_info['numerical'] if c in df.columns]
    if not num_cols:
        print("\n  No numerical columns to scale.")
        return df.copy(), None

    scaler_map = {
        'standard': (StandardScaler, "(x − mean) / std"),
        'minmax': (MinMaxScaler, "(x − min) / (max − min) → [0, 1]"),
        'robust': (RobustScaler, "(x − median) / IQR (outlier-robust)"),
    }

    ScalerClass, formula = scaler_map.get(method, scaler_map['standard'])
    scaler = ScalerClass()

    df_out = df.copy()
    df_out[num_cols] = scaler.fit_transform(df_out[num_cols])

    print(f"\n  Method: {method.title()}Scaler — {formula}")
    print(f"  Scaled {len(num_cols)} column(s): {num_cols}")

    # Show before/after for first numerical column
    if num_cols:
        sample_col = num_cols[0]
        print(f"\n  📊 Before/After ({sample_col}):")
        print(f"    Original  — mean={df[sample_col].mean():.2f}, "
              f"std={df[sample_col].std():.2f}, "
              f"range=[{df[sample_col].min():.2f}, {df[sample_col].max():.2f}]")
        print(f"    Scaled    — mean={df_out[sample_col].mean():.4f}, "
              f"std={df_out[sample_col].std():.4f}, "
              f"range=[{df_out[sample_col].min():.4f}, {df_out[sample_col].max():.4f}]")

    # Visualization
    if output_dir and len(num_cols) >= 1:
        _plot_scaling_comparison(df, df_out, num_cols[0], method, output_dir)

    _discuss("Discussion",
             f"Feature scaling ensures all numerical features are on a\n"
             f"comparable scale. This is important for algorithms that\n"
             f"use distance metrics (KNN, SVM) or gradient descent\n"
             f"(neural networks, logistic regression).\n"
             f"Tree-based models (Random Forest, XGBoost) typically\n"
             f"don't require scaling.")

    return df_out, scaler


def _plot_scaling_comparison(df_orig, df_scaled, col, method, output_dir):
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    axes[0].hist(df_orig[col].dropna(), bins=30, color='steelblue',
                 edgecolor='black', alpha=0.7)
    axes[0].set_title(f'{col} — Original', fontweight='bold')

    axes[1].hist(df_scaled[col].dropna(), bins=30, color='coral',
                 edgecolor='black', alpha=0.7)
    axes[1].set_title(f'{col} — {method.title()} Scaled', fontweight='bold')

    plt.tight_layout()
    _save_fig(fig, os.path.join(output_dir, 'data_prep_scaling_comparison.png'))


# ═════════════════════════════════════════════════════════════════════════
#  5. Outlier Handling
# ═════════════════════════════════════════════════════════════════════════

def handle_outliers(df: pd.DataFrame,
                    col_info: dict,
                    method: str = 'keep',
                    iqr_multiplier: float = 1.5) -> pd.DataFrame:
    """
    Detect and optionally handle outliers in numerical columns.

    method: 'keep', 'remove', 'cap' (winsorize)
    """
    print("\n" + "=" * 60)
    print("STEP 5: OUTLIER HANDLING")
    print("=" * 60)

    num_cols = [c for c in col_info['numerical'] if c in df.columns]
    if not num_cols:
        print("\n  No numerical columns for outlier analysis.")
        return df.copy()

    df_out = df.copy()
    report = []

    for col in num_cols:
        data = df_out[col].dropna()
        q1, q3 = data.quantile(0.25), data.quantile(0.75)
        iqr = q3 - q1
        lower = q1 - iqr_multiplier * iqr
        upper = q3 + iqr_multiplier * iqr
        n_out = int(((data < lower) | (data > upper)).sum())
        report.append({
            'Column': col,
            'Outliers': n_out,
            'Pct': round(n_out / max(len(data), 1) * 100, 1),
            'Lower Bound': round(lower, 2),
            'Upper Bound': round(upper, 2),
        })

    report_df = pd.DataFrame(report)
    print(f"\n  🔍 Outlier Detection (IQR × {iqr_multiplier}):")
    _get_display()(report_df)

    total_outliers = report_df['Outliers'].sum()

    if method == 'remove':
        before = len(df_out)
        for row in report:
            col = row['Column']
            df_out = df_out[
                (df_out[col] >= row['Lower Bound']) &
                (df_out[col] <= row['Upper Bound'])
            ]
        _discuss("Strategy: Remove outliers",
                 f"Removed rows with outlier values.\n"
                 f"Before: {before:,} rows → After: {len(df_out):,} rows.\n"
                 f"This reduces noise but can lose important edge cases.")

    elif method == 'cap':
        for row in report:
            col = row['Column']
            df_out[col] = df_out[col].clip(lower=row['Lower Bound'],
                                           upper=row['Upper Bound'])
        _discuss("Strategy: Cap outliers (winsorization)",
                 f"Outlier values were capped to the IQR boundaries.\n"
                 f"This preserves all rows while limiting extreme values.\n"
                 f"Useful when outliers might be measurement errors.")

    else:  # keep
        _discuss("Strategy: Keep all data",
                 f"Detected {total_outliers} outlier values across "
                 f"{len(num_cols)} columns.\n"
                 f"Outliers were retained because they may represent\n"
                 f"valid natural variation. Monitor model performance\n"
                 f"and revisit if outliers degrade results.")

    return df_out


# ═════════════════════════════════════════════════════════════════════════
#  6. Feature Selection
# ═════════════════════════════════════════════════════════════════════════

def select_features(df: pd.DataFrame,
                    feature_cols: List[str],
                    target_col: str,
                    task_type: str = 'classification',
                    k: int = 0,
                    output_dir: Optional[str] = None) -> Tuple[List[str], pd.DataFrame]:
    """
    Rank features using ANOVA F-score (classification) or F-regression.
    If k > 0, select top-k features.
    Returns (selected_feature_names, scores_df).
    """
    from sklearn.feature_selection import SelectKBest, f_classif, f_regression, mutual_info_classif, mutual_info_regression

    print("\n" + "=" * 60)
    print("STEP 6: FEATURE SELECTION")
    print("=" * 60)

    available = [c for c in feature_cols if c in df.columns]
    X = df[available]
    y = df[target_col]

    # Choose scorer
    if task_type == 'classification':
        scorer_1, name_1 = f_classif, 'ANOVA F-Score'
        scorer_2, name_2 = mutual_info_classif, 'Mutual Information'
    else:
        scorer_1, name_1 = f_regression, 'F-Regression'
        scorer_2, name_2 = mutual_info_regression, 'Mutual Information'

    # Score 1
    sel1 = SelectKBest(scorer_1, k='all')
    sel1.fit(X, y)
    scores1 = pd.DataFrame({
        'Feature': available,
        name_1: sel1.scores_,
    }).sort_values(name_1, ascending=False)

    # Score 2
    sel2 = SelectKBest(scorer_2, k='all')
    sel2.fit(X, y)
    scores2 = pd.DataFrame({
        'Feature': available,
        name_2: sel2.scores_,
    }).sort_values(name_2, ascending=False)

    # Merge
    merged = scores1.merge(scores2, on='Feature')
    print(f"\n  📊 Feature Importance Ranking ({task_type}):")
    _get_display()(merged)

    # Select top-k
    if k > 0 and k < len(available):
        selected = scores1.head(k)['Feature'].tolist()
    else:
        selected = available

    _discuss("Discussion",
             f"Features ranked by two complementary methods:\n"
             f"• {name_1}: measures linear relationship with the target\n"
             f"• {name_2}: captures non-linear relationships too\n"
             f"Selected {len(selected)} feature(s) for modeling.\n"
             f"Features with both high scores are strong predictors.")

    # Visualization
    if output_dir:
        _plot_feature_importance(merged, name_1, name_2, output_dir)

    return selected, merged


def _plot_feature_importance(scores_df, name1, name2, output_dir):
    fig, axes = plt.subplots(1, 2, figsize=(14, max(5, len(scores_df) * 0.5)))

    df1 = scores_df.sort_values(name1, ascending=True)
    axes[0].barh(df1['Feature'], df1[name1], color='steelblue')
    axes[0].set_xlabel(name1)
    axes[0].set_title(f'{name1} Ranking', fontweight='bold')

    df2 = scores_df.sort_values(name2, ascending=True)
    axes[1].barh(df2['Feature'], df2[name2], color='coral')
    axes[1].set_xlabel(name2)
    axes[1].set_title(f'{name2} Ranking', fontweight='bold')

    plt.tight_layout()
    _save_fig(fig, os.path.join(output_dir, 'data_prep_feature_importance.png'))


# ═════════════════════════════════════════════════════════════════════════
#  7. Train/Test Split
# ═════════════════════════════════════════════════════════════════════════

def split_data(df: pd.DataFrame,
               feature_cols: List[str],
               target_col: str,
               test_size: float = 0.2,
               task_type: str = 'classification',
               random_state: int = 42) -> dict:
    """
    Split data into train/test sets. Stratifies for classification.
    Returns dict with X_train, X_test, y_train, y_test.
    """
    from sklearn.model_selection import train_test_split

    print("\n" + "=" * 60)
    print("STEP 7: TRAIN/TEST SPLIT")
    print("=" * 60)

    available = [c for c in feature_cols if c in df.columns]
    X = df[available]
    y = df[target_col]

    stratify = y if task_type == 'classification' else None
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state,
        stratify=stratify,
    )

    print(f"\n  Training set: {X_train.shape[0]:,} samples "
          f"({X_train.shape[0] / len(X) * 100:.0f}%)")
    print(f"  Test set:     {X_test.shape[0]:,} samples "
          f"({X_test.shape[0] / len(X) * 100:.0f}%)")

    if task_type == 'classification':
        print(f"\n  📈 Class Distribution (stratified split):")
        train_dist = y_train.value_counts(normalize=True).sort_index()
        test_dist = y_test.value_counts(normalize=True).sort_index()
        for val in sorted(y.unique()):
            t_pct = train_dist.get(val, 0) * 100
            e_pct = test_dist.get(val, 0) * 100
            print(f"    Class {val}: train={t_pct:.1f}%  test={e_pct:.1f}%")

    _discuss("Discussion",
             f"Split the data {int((1 - test_size) * 100)}/{int(test_size * 100)} "
             f"(train/test).\n"
             + ("Stratified sampling ensures each class is equally\n"
                "represented in both sets — critical for imbalanced data."
                if task_type == 'classification'
                else "Random split used for regression task."))

    return {
        'X_train': X_train,
        'X_test': X_test,
        'y_train': y_train,
        'y_test': y_test,
        'features': available,
    }


# ═════════════════════════════════════════════════════════════════════════
#  8. Export
# ═════════════════════════════════════════════════════════════════════════

def export_prepared_data(split: dict,
                         scaler,
                         encoders: dict,
                         output_dir: str,
                         scale_exports: bool = True) -> dict:
    """
    Export prepared train/test CSVs and fitted transformers.
    Returns dict of exported file paths.
    """
    from sklearn.preprocessing import StandardScaler

    print("\n" + "=" * 60)
    print("STEP 8: EXPORT PREPARED DATA")
    print("=" * 60)

    os.makedirs(output_dir, exist_ok=True)
    paths = {}

    X_train, X_test = split['X_train'], split['X_test']
    y_train, y_test = split['y_train'], split['y_test']
    features = split['features']

    # Unscaled
    train_df = X_train.copy()
    train_df['target'] = y_train.values
    test_df = X_test.copy()
    test_df['target'] = y_test.values

    p = os.path.join(output_dir, 'train_data.csv')
    train_df.to_csv(p, index=False)
    paths['train'] = p

    p = os.path.join(output_dir, 'test_data.csv')
    test_df.to_csv(p, index=False)
    paths['test'] = p

    # Scaled
    if scale_exports and scaler is not None:
        sc = StandardScaler()
        X_train_sc = pd.DataFrame(sc.fit_transform(X_train),
                                  columns=features)
        X_test_sc = pd.DataFrame(sc.transform(X_test),
                                 columns=features)

        train_sc = X_train_sc.copy()
        train_sc['target'] = y_train.values
        test_sc = X_test_sc.copy()
        test_sc['target'] = y_test.values

        p = os.path.join(output_dir, 'train_data_scaled.csv')
        train_sc.to_csv(p, index=False)
        paths['train_scaled'] = p

        p = os.path.join(output_dir, 'test_data_scaled.csv')
        test_sc.to_csv(p, index=False)
        paths['test_scaled'] = p

    # Encoders & scaler
    if encoders:
        p = os.path.join(output_dir, 'encoders.pkl')
        with open(p, 'wb') as f:
            pickle.dump(encoders, f)
        paths['encoders'] = p

    if scaler is not None:
        p = os.path.join(output_dir, 'scaler.pkl')
        with open(p, 'wb') as f:
            pickle.dump({'scaler': scaler, 'features': features}, f)
        paths['scaler'] = p

    print(f"\n  💾 Exported to {output_dir}/:")
    for key, path in paths.items():
        print(f"    • {os.path.basename(path)}")

    _discuss("Discussion",
             "All prepared data and fitted transformers have been saved.\n"
             "Use the same scaler and encoders for new/production data\n"
             "to ensure consistent preprocessing.")

    return paths


# ═════════════════════════════════════════════════════════════════════════
#  Full Pipeline Orchestrator
# ═════════════════════════════════════════════════════════════════════════

def run_full_data_prep(df: pd.DataFrame,
                       *,
                       target_col: str,
                       task_type: str = 'classification',
                       exclude_cols: Optional[List[str]] = None,
                       missing_strategy: str = 'auto',
                       encoding: str = 'label',
                       scaling_method: str = 'standard',
                       outlier_method: str = 'keep',
                       feature_select_k: int = 0,
                       test_size: float = 0.2,
                       output_dir: Optional[str] = None,
                       images_dir: Optional[str] = None,
                       random_state: int = 42) -> dict:
    """
    Run the complete data preparation pipeline on *df*.

    Parameters
    ----------
    df : pandas DataFrame
    target_col : name of the target/label column
    task_type : 'classification' or 'regression'
    exclude_cols : columns to drop before processing (e.g. IDs)
    missing_strategy : 'auto', 'drop', or 'impute'
    encoding : 'label', 'onehot', or 'both'
    scaling_method : 'standard', 'minmax', or 'robust'
    outlier_method : 'keep', 'remove', or 'cap'
    feature_select_k : top-k features to keep (0 = keep all)
    test_size : fraction for test split
    output_dir : path to export CSVs + pickles (None → skip export)
    images_dir : path to save plots (None → skip saving)
    random_state : seed for reproducibility

    Returns
    -------
    dict with keys:
        df_prepared, split, encoders, scaler, col_info,
        feature_scores, export_paths
    """
    print("\n" + "═" * 60)
    print(f"  DATA PREPARATION PIPELINE — {task_type.upper()}")
    print("═" * 60)

    working = df.copy()

    # Drop explicit exclusions
    if exclude_cols:
        working = working.drop(columns=[c for c in exclude_cols if c in working.columns])
        print(f"\n  Dropped excluded columns: {exclude_cols}")

    # 0. Classify columns
    col_info = _classify_columns(working, target_col=target_col)
    if col_info['id_like']:
        print(f"  ⚠️  Auto-detected ID columns (dropped): {col_info['id_like']}")
        working = working.drop(columns=col_info['id_like'])

    # 1. Validate
    validate_data(working, col_info)

    # 2. Missing values
    working = handle_missing_values(working, col_info, strategy=missing_strategy)

    # 3. Encode
    working, encoders = encode_features(working, col_info,
                                        target_col=target_col,
                                        encoding=encoding)

    # Determine the target column name (might be '_encoded' now)
    target_for_model = target_col
    if f'{target_col}_encoded' in working.columns:
        target_for_model = f'{target_col}_encoded'

    # 4. Build feature list (numerical + encoded)
    feature_cols = col_info['numerical'].copy()
    for c in col_info['categorical']:
        enc_name = f'{c}_encoded'
        if enc_name in working.columns:
            feature_cols.append(enc_name)

    # 5. Scale
    working_for_scale = working.copy()
    _, scaler = scale_features(working_for_scale, col_info,
                               method=scaling_method,
                               output_dir=images_dir)

    # 6. Outliers (on unscaled data)
    working = handle_outliers(working, col_info, method=outlier_method)

    # 7. Feature selection
    selected_features, feature_scores = select_features(
        working, feature_cols, target_for_model,
        task_type=task_type, k=feature_select_k,
        output_dir=images_dir,
    )

    # 8. Split
    split = split_data(working, selected_features, target_for_model,
                       test_size=test_size, task_type=task_type,
                       random_state=random_state)

    # 9. Export
    export_paths = {}
    if output_dir:
        export_paths = export_prepared_data(split, scaler, encoders,
                                            output_dir)

    print("\n" + "═" * 60)
    print("  DATA PREPARATION COMPLETE ✅")
    print("═" * 60)

    return {
        'df_prepared': working,
        'split': split,
        'encoders': encoders,
        'scaler': scaler,
        'col_info': col_info,
        'feature_scores': feature_scores,
        'selected_features': selected_features,
        'export_paths': export_paths,
    }


# ═════════════════════════════════════════════════════════════════════════
#  CLI entry-point
# ═════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    import sys

    if len(sys.argv) < 3:
        print("Usage: python run_data_prep.py <csv_file> <target_col> "
              "[--task classification|regression] [--output-dir DIR] "
              "[--exclude COL1,COL2]")
        sys.exit(1)

    csv_path = sys.argv[1]
    target = sys.argv[2]
    kwargs = {}

    i = 3
    while i < len(sys.argv):
        if sys.argv[i] == '--task' and i + 1 < len(sys.argv):
            kwargs['task_type'] = sys.argv[i + 1]; i += 2
        elif sys.argv[i] == '--output-dir' and i + 1 < len(sys.argv):
            kwargs['output_dir'] = sys.argv[i + 1]; i += 2
        elif sys.argv[i] == '--images-dir' and i + 1 < len(sys.argv):
            kwargs['images_dir'] = sys.argv[i + 1]; i += 2
        elif sys.argv[i] == '--exclude' and i + 1 < len(sys.argv):
            kwargs['exclude_cols'] = sys.argv[i + 1].split(','); i += 2
        elif sys.argv[i] == '--missing' and i + 1 < len(sys.argv):
            kwargs['missing_strategy'] = sys.argv[i + 1]; i += 2
        elif sys.argv[i] == '--scaling' and i + 1 < len(sys.argv):
            kwargs['scaling_method'] = sys.argv[i + 1]; i += 2
        elif sys.argv[i] == '--outliers' and i + 1 < len(sys.argv):
            kwargs['outlier_method'] = sys.argv[i + 1]; i += 2
        else:
            i += 1

    data = pd.read_csv(csv_path)
    run_full_data_prep(data, target_col=target,
                       **kwargs)
