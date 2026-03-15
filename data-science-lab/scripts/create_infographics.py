"""
Sophisticated infographics generator for data science experiment results.

Creates publication-quality, multi-panel infographics with modern styling,
custom color palettes, professional typography, and rich annotations.

Usage:
    from create_infographics import create_experiment_infographic, quick_infographic

    fig = create_experiment_infographic(results_df, title='My Experiment')
    export_infographic(fig, 'output/infographic.png')
"""

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
import matplotlib.patheffects as path_effects
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns
import pandas as pd
import numpy as np
import os
from datetime import datetime
from textwrap import wrap


# ---------------------------------------------------------------------------
# Theme & Style Configuration
# ---------------------------------------------------------------------------

# Modern color palettes
PALETTES = {
    'ocean': ['#0B3D91', '#1565C0', '#1E88E5', '#42A5F5', '#90CAF9', '#BBDEFB'],
    'sunset': ['#BF360C', '#E64A19', '#FF7043', '#FF8A65', '#FFAB91', '#FFCCBC'],
    'forest': ['#1B5E20', '#2E7D32', '#43A047', '#66BB6A', '#A5D6A7', '#C8E6C9'],
    'purple': ['#4A148C', '#6A1B9A', '#8E24AA', '#AB47BC', '#CE93D8', '#E1BEE7'],
    'slate':  ['#263238', '#37474F', '#546E7A', '#78909C', '#B0BEC5', '#CFD8DC'],
    'candy':  ['#AD1457', '#D81B60', '#EC407A', '#F48FB1', '#F8BBD0', '#FCE4EC'],
}

# Gradient background colors
BG_GRADIENT_DARK = '#0F172A'
BG_GRADIENT_MID = '#1E293B'
BG_CARD = '#1E293B'
BG_CARD_BORDER = '#334155'
TEXT_PRIMARY = '#F1F5F9'
TEXT_SECONDARY = '#94A3B8'
TEXT_ACCENT = '#38BDF8'
GOLD = '#FBBF24'
SILVER = '#94A3B8'
BRONZE = '#D97706'
POSITIVE = '#34D399'
NEGATIVE = '#F87171'
DIVIDER = '#334155'

# Light theme alternative
BG_LIGHT = '#FAFBFC'
BG_CARD_LIGHT = '#FFFFFF'
BG_CARD_BORDER_LIGHT = '#E2E8F0'
TEXT_PRIMARY_LIGHT = '#1E293B'
TEXT_SECONDARY_LIGHT = '#64748B'
TEXT_ACCENT_LIGHT = '#2563EB'


def _apply_dark_theme():
    """Apply the dark professional theme to matplotlib."""
    plt.rcParams.update({
        'figure.facecolor': BG_GRADIENT_DARK,
        'axes.facecolor': BG_CARD,
        'axes.edgecolor': BG_CARD_BORDER,
        'axes.labelcolor': TEXT_SECONDARY,
        'axes.titlecolor': TEXT_PRIMARY,
        'text.color': TEXT_PRIMARY,
        'xtick.color': TEXT_SECONDARY,
        'ytick.color': TEXT_SECONDARY,
        'grid.color': BG_CARD_BORDER,
        'grid.alpha': 0.3,
        'font.family': 'sans-serif',
        'font.size': 10,
        'axes.titlesize': 13,
        'axes.labelsize': 11,
    })


def _apply_light_theme():
    """Apply a clean light theme to matplotlib."""
    plt.rcParams.update({
        'figure.facecolor': BG_LIGHT,
        'axes.facecolor': BG_CARD_LIGHT,
        'axes.edgecolor': BG_CARD_BORDER_LIGHT,
        'axes.labelcolor': TEXT_SECONDARY_LIGHT,
        'axes.titlecolor': TEXT_PRIMARY_LIGHT,
        'text.color': TEXT_PRIMARY_LIGHT,
        'xtick.color': TEXT_SECONDARY_LIGHT,
        'ytick.color': TEXT_SECONDARY_LIGHT,
        'grid.color': BG_CARD_BORDER_LIGHT,
        'grid.alpha': 0.5,
        'font.family': 'sans-serif',
        'font.size': 10,
        'axes.titlesize': 13,
        'axes.labelsize': 11,
    })


def _detect_metric(df, preferred='accuracy'):
    """Auto-detect the best metric column to use."""
    if preferred in df.columns:
        return preferred
    candidates = [
        'accuracy', 'f1_score', 'f1', 'r2_score', 'r2',
        'precision', 'recall', 'auc', 'roc_auc', 'mse', 'rmse', 'mae',
    ]
    for c in candidates:
        if c in df.columns:
            return c
    # Fall back to first numeric column
    numeric = df.select_dtypes(include=[np.number]).columns.tolist()
    return numeric[0] if numeric else None


def _safe_wrap(text, width=18):
    """Wrap long text for axis labels."""
    if not isinstance(text, str):
        text = str(text)
    lines = wrap(text, width)
    return '\n'.join(lines)


def _add_card_background(ax, facecolor=BG_CARD, edgecolor=BG_CARD_BORDER,
                          radius=0.02, linewidth=1.2):
    """Draw a rounded card background behind an axes."""
    rect = mpatches.FancyBboxPatch(
        (0, 0), 1, 1, boxstyle=f"round,pad={radius}",
        facecolor=facecolor, edgecolor=edgecolor,
        linewidth=linewidth, transform=ax.transAxes, zorder=-1,
    )
    ax.add_patch(rect)


def _add_glow_text(ax, x, y, text, fontsize=24, color=TEXT_ACCENT, **kwargs):
    """Add text with a subtle glow / shadow effect."""
    txt = ax.text(x, y, text, fontsize=fontsize, color=color,
                  fontweight='bold', ha='center', va='center',
                  transform=ax.transAxes, **kwargs)
    txt.set_path_effects([
        path_effects.withStroke(linewidth=4, foreground=color + '33'),
    ])
    return txt


# ---------------------------------------------------------------------------
# Panel Renderers
# ---------------------------------------------------------------------------

def _render_hero_banner(ax, title, subtitle, metric, df, timestamp):
    """Render the top hero banner with title and key stats."""
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Title
    ax.text(0.02, 0.72, title, fontsize=22, fontweight='bold',
            color=TEXT_PRIMARY, va='center', ha='left')

    # Subtitle
    ax.text(0.02, 0.38, subtitle, fontsize=11,
            color=TEXT_SECONDARY, va='center', ha='left')

    # Timestamp
    ax.text(0.02, 0.10, f"Generated: {timestamp}",
            fontsize=8, color=TEXT_SECONDARY, va='center', ha='left',
            style='italic')

    # Key stat badges on the right
    if metric and metric in df.columns:
        best_score = df[metric].max()
        n_experiments = len(df)
        n_models = df['model'].nunique() if 'model' in df.columns else '—'

        badges = [
            ('BEST SCORE', f'{best_score:.4f}', GOLD),
            ('EXPERIMENTS', str(n_experiments), TEXT_ACCENT),
            ('MODELS', str(n_models), POSITIVE),
        ]

        for i, (label, value, color) in enumerate(badges):
            bx = 0.65 + i * 0.125
            # Badge background
            badge = mpatches.FancyBboxPatch(
                (bx - 0.05, 0.15), 0.10, 0.70,
                boxstyle="round,pad=0.015",
                facecolor=color + '18', edgecolor=color + '55',
                linewidth=1, transform=ax.transAxes,
            )
            ax.add_patch(badge)
            ax.text(bx, 0.62, value, fontsize=14, fontweight='bold',
                    color=color, ha='center', va='center')
            ax.text(bx, 0.30, label, fontsize=6.5, color=TEXT_SECONDARY,
                    ha='center', va='center', fontweight='bold',
                    letter_spacing=0.5 if hasattr(ax, 'letter_spacing') else None)


def _render_podium(ax, df, metric, palette_colors):
    """Render a medal podium chart for top 3 models."""
    ax.axis('off')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    if 'model' not in df.columns or metric not in df.columns:
        ax.text(0.5, 0.5, 'No model data', ha='center', va='center',
                color=TEXT_SECONDARY, fontsize=12)
        return

    top = df.nlargest(min(3, len(df)), metric)
    models = top['model'].astype(str).tolist()
    scores = top[metric].tolist()

    medal_colors = [GOLD, SILVER, BRONZE]
    medal_labels = ['🥇', '🥈', '🥉']

    # Podium heights proportional to scores
    max_score = max(scores) if scores else 1
    heights = [s / max_score * 0.50 for s in scores]

    positions = []
    if len(models) == 1:
        positions = [0.5]
    elif len(models) == 2:
        positions = [0.35, 0.65]
    else:
        positions = [0.22, 0.50, 0.78]

    # Title
    ax.text(0.5, 0.95, '🏆 Top Models', fontsize=13, fontweight='bold',
            color=TEXT_PRIMARY, ha='center', va='top')

    for i, (pos, height) in enumerate(zip(positions, heights)):
        color = medal_colors[i]
        y_base = 0.18

        # Podium bar
        bar = mpatches.FancyBboxPatch(
            (pos - 0.10, y_base), 0.20, height,
            boxstyle="round,pad=0.01",
            facecolor=color + '30', edgecolor=color,
            linewidth=1.5, transform=ax.transAxes,
        )
        ax.add_patch(bar)

        # Medal icon
        ax.text(pos, y_base + height + 0.08, medal_labels[i],
                fontsize=18, ha='center', va='center')

        # Score
        ax.text(pos, y_base + height + 0.02, f'{scores[i]:.4f}',
                fontsize=10, fontweight='bold', color=color,
                ha='center', va='bottom')

        # Model name
        name = _safe_wrap(models[i], 14)
        ax.text(pos, y_base - 0.04, name,
                fontsize=8, color=TEXT_SECONDARY,
                ha='center', va='top')


def _render_bar_ranking(ax, df, metric, palette_colors, top_n=8):
    """Render a horizontal bar ranking for all models."""
    if 'model' not in df.columns or metric not in df.columns:
        ax.text(0.5, 0.5, 'No model data', ha='center', va='center',
                color=TEXT_SECONDARY, fontsize=11, transform=ax.transAxes)
        ax.axis('off')
        return

    # Aggregate by model if duplicates exist
    agg = df.groupby('model')[metric].mean().sort_values(ascending=True)
    agg = agg.tail(top_n)

    n = len(agg)
    colors = sns.color_palette('viridis', n_colors=n)

    bars = ax.barh(range(n), agg.values, color=colors, height=0.65,
                   edgecolor=[c + (0.8,) for c in colors], linewidth=0.5)

    ax.set_yticks(range(n))
    ax.set_yticklabels([_safe_wrap(str(m), 20) for m in agg.index], fontsize=9)

    # Value labels
    x_max = agg.max()
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax.text(width + x_max * 0.02, bar.get_y() + bar.get_height() / 2,
                f'{width:.4f}', va='center', ha='left',
                fontsize=8, color=TEXT_SECONDARY, fontweight='bold')

    ax.set_xlim(0, x_max * 1.18)
    ax.set_xlabel(metric.replace('_', ' ').title(), fontsize=10)
    ax.set_title('Model Ranking', fontsize=12, fontweight='bold', pad=8)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(left=False)
    ax.grid(axis='x', alpha=0.15)


def _render_distribution(ax, df, metric):
    """Render a styled distribution plot with KDE and statistical markers."""
    if metric not in df.columns:
        ax.text(0.5, 0.5, 'No metric data', ha='center', va='center',
                color=TEXT_SECONDARY, fontsize=11, transform=ax.transAxes)
        ax.axis('off')
        return

    values = df[metric].dropna()
    if len(values) < 2:
        ax.text(0.5, 0.5, 'Not enough data', ha='center', va='center',
                color=TEXT_SECONDARY, fontsize=11, transform=ax.transAxes)
        return

    # Histogram with KDE
    sns.histplot(values, kde=True, ax=ax, color='#38BDF8', alpha=0.35,
                 edgecolor='#38BDF880', linewidth=0.8, bins='auto',
                 line_kws={'linewidth': 2, 'color': '#38BDF8'})

    # Statistical lines
    mean_val = values.mean()
    median_val = values.median()
    std_val = values.std()

    ax.axvline(mean_val, color=NEGATIVE, linestyle='--', linewidth=1.5, alpha=0.8,
               label=f'Mean: {mean_val:.4f}')
    ax.axvline(median_val, color=POSITIVE, linestyle=':', linewidth=1.5, alpha=0.8,
               label=f'Median: {median_val:.4f}')

    # Shade ±1 std region
    ax.axvspan(mean_val - std_val, mean_val + std_val,
               alpha=0.08, color=TEXT_ACCENT, label=f'±1σ ({std_val:.4f})')

    ax.legend(fontsize=7.5, loc='upper right', framealpha=0.5,
              edgecolor=DIVIDER)
    ax.set_title(f'{metric.replace("_", " ").title()} Distribution',
                 fontsize=12, fontweight='bold', pad=8)
    ax.set_xlabel(metric.replace('_', ' ').title(), fontsize=10)
    ax.set_ylabel('Count', fontsize=10)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)


def _render_parameter_heatmap(ax, df, metric, param_col=None, model_col='model'):
    """Render a heatmap of parameter vs model performance."""
    # Auto-detect parameter column
    if param_col is None:
        skip = {metric, model_col, 'experiment', 'dataset'}
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        candidates = [c for c in numeric_cols if c not in skip]
        if not candidates:
            ax.text(0.5, 0.5, 'No parameter data\nfor heatmap',
                    ha='center', va='center', color=TEXT_SECONDARY,
                    fontsize=11, transform=ax.transAxes)
            ax.axis('off')
            return
        param_col = candidates[0]

    if model_col not in df.columns:
        ax.text(0.5, 0.5, 'No model column', ha='center', va='center',
                color=TEXT_SECONDARY, fontsize=11, transform=ax.transAxes)
        ax.axis('off')
        return

    try:
        pivot = df.pivot_table(values=metric, index=model_col,
                               columns=param_col, aggfunc='mean')
        if pivot.empty:
            raise ValueError("Empty pivot")

        # Custom colormap
        cmap = LinearSegmentedColormap.from_list(
            'custom', ['#1E293B', '#0EA5E9', '#22D3EE', '#34D399'], N=256
        )

        sns.heatmap(pivot, annot=True, fmt='.3f', cmap=cmap, ax=ax,
                    linewidths=0.5, linecolor=BG_CARD_BORDER,
                    cbar_kws={'shrink': 0.8, 'label': metric.title()},
                    annot_kws={'fontsize': 8, 'color': TEXT_PRIMARY})

        ax.set_title(f'{metric.title()} by {param_col.title()} × Model',
                     fontsize=12, fontweight='bold', pad=8)
        ax.set_xlabel(param_col.replace('_', ' ').title(), fontsize=10)
        ax.set_ylabel('')
        ax.tick_params(axis='y', rotation=0)

    except Exception:
        # Fallback: show box plot instead
        if model_col in df.columns and metric in df.columns:
            sns.boxplot(data=df, x=model_col, y=metric, ax=ax,
                        palette='viridis', linewidth=0.8)
            ax.set_title(f'{metric.title()} Distribution by Model',
                         fontsize=12, fontweight='bold', pad=8)
            ax.tick_params(axis='x', rotation=45)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
        else:
            ax.text(0.5, 0.5, 'Cannot create heatmap',
                    ha='center', va='center', color=TEXT_SECONDARY,
                    fontsize=11, transform=ax.transAxes)
            ax.axis('off')


def _render_radar(ax, df, metric, top_n=5):
    """Render a radar / spider chart comparing top models across metrics."""
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if 'model' not in df.columns or len(numeric_cols) < 3:
        ax.text(0.5, 0.5, 'Need ≥3 metrics\nfor radar chart',
                ha='center', va='center', color=TEXT_SECONDARY,
                fontsize=11, transform=ax.transAxes)
        ax.axis('off')
        return

    # Get top models
    top_models = (df.groupby('model')[metric].mean()
                  .nlargest(min(top_n, df['model'].nunique()))
                  .index.tolist())
    sub = df[df['model'].isin(top_models)]

    # Pick metrics to show (max 8)
    metrics_to_show = [c for c in numeric_cols
                       if c != 'index' and sub[c].std() > 0][:8]

    if len(metrics_to_show) < 3:
        ax.text(0.5, 0.5, 'Need ≥3 varying metrics',
                ha='center', va='center', color=TEXT_SECONDARY,
                fontsize=11, transform=ax.transAxes)
        ax.axis('off')
        return

    N = len(metrics_to_show)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    angles += angles[:1]  # close polygon

    ax_polar = ax.figure.add_axes(ax.get_position(), polar=True,
                                   facecolor=BG_CARD)
    ax.axis('off')

    colors = sns.color_palette('Set2', len(top_models))

    for i, model in enumerate(top_models):
        model_data = sub[sub['model'] == model][metrics_to_show].mean()
        # Normalize to 0-1 range per metric
        mins = sub[metrics_to_show].min()
        maxes = sub[metrics_to_show].max()
        ranges = maxes - mins
        ranges[ranges == 0] = 1  # avoid division by zero
        normalized = ((model_data - mins) / ranges).tolist()
        normalized += normalized[:1]

        ax_polar.plot(angles, normalized, 'o-', color=colors[i],
                      linewidth=1.5, markersize=4, label=_safe_wrap(str(model), 12))
        ax_polar.fill(angles, normalized, alpha=0.1, color=colors[i])

    ax_polar.set_xticks(angles[:-1])
    ax_polar.set_xticklabels([_safe_wrap(m.replace('_', ' ').title(), 10)
                               for m in metrics_to_show],
                              fontsize=7, color=TEXT_SECONDARY)
    ax_polar.set_yticks([0.25, 0.5, 0.75, 1.0])
    ax_polar.set_yticklabels(['25%', '50%', '75%', '100%'],
                              fontsize=6, color=TEXT_SECONDARY)
    ax_polar.set_rlabel_position(30)
    ax_polar.spines['polar'].set_color(BG_CARD_BORDER)
    ax_polar.grid(color=BG_CARD_BORDER, alpha=0.3)
    ax_polar.set_facecolor(BG_CARD)

    ax_polar.legend(loc='lower right', bbox_to_anchor=(1.3, -0.05),
                    fontsize=7, framealpha=0.5, edgecolor=DIVIDER)
    ax_polar.set_title('Multi-Metric Radar', fontsize=12, fontweight='bold',
                       pad=20, color=TEXT_PRIMARY)


def _render_stats_card(ax, df, metric):
    """Render a rich statistics summary card."""
    ax.axis('off')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    ax.text(0.5, 0.95, '📋 Summary Statistics', fontsize=13, fontweight='bold',
            color=TEXT_PRIMARY, ha='center', va='top')

    if metric not in df.columns:
        ax.text(0.5, 0.5, 'No data', ha='center', va='center',
                color=TEXT_SECONDARY, fontsize=11)
        return

    values = df[metric].dropna()
    best_model = '—'
    if 'model' in df.columns:
        best_model = str(df.loc[df[metric].idxmax(), 'model'])

    stats = [
        ('Total Experiments', str(len(df)), TEXT_ACCENT),
        ('Best Model', _safe_wrap(best_model, 22), GOLD),
        ('Best Score', f'{values.max():.4f}', GOLD),
        ('Mean ± Std', f'{values.mean():.4f} ± {values.std():.4f}', TEXT_PRIMARY),
        ('Median', f'{values.median():.4f}', TEXT_PRIMARY),
        ('Range', f'{values.min():.4f} → {values.max():.4f}', TEXT_PRIMARY),
    ]

    if 'model' in df.columns:
        n_models = df['model'].nunique()
        stats.insert(1, ('Unique Models', str(n_models), POSITIVE))

    y_start = 0.82
    y_step = 0.095
    for i, (label, value, color) in enumerate(stats):
        y = y_start - i * y_step
        # Row background
        if i % 2 == 0:
            row_bg = mpatches.FancyBboxPatch(
                (0.03, y - 0.035), 0.94, 0.07,
                boxstyle="round,pad=0.005",
                facecolor=BG_CARD_BORDER + '40', edgecolor='none',
                transform=ax.transAxes,
            )
            ax.add_patch(row_bg)
        ax.text(0.08, y, label, fontsize=9, color=TEXT_SECONDARY,
                va='center', ha='left')
        ax.text(0.92, y, value, fontsize=9, color=color,
                va='center', ha='right', fontweight='bold')


def _render_improvement_arrows(ax, df, metric):
    """Show improvement between worst and best model with directional arrows."""
    ax.axis('off')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    if 'model' not in df.columns or metric not in df.columns:
        ax.text(0.5, 0.5, 'No model data', ha='center', va='center',
                color=TEXT_SECONDARY, fontsize=11)
        return

    agg = df.groupby('model')[metric].mean().sort_values(ascending=True)
    if len(agg) < 2:
        ax.text(0.5, 0.5, 'Need ≥2 models', ha='center', va='center',
                color=TEXT_SECONDARY, fontsize=11)
        return

    worst_model = str(agg.index[0])
    worst_val = agg.iloc[0]
    best_model = str(agg.index[-1])
    best_val = agg.iloc[-1]

    improvement = best_val - worst_val
    pct = (improvement / worst_val * 100) if worst_val != 0 else 0

    ax.text(0.5, 0.92, '📈 Improvement Gap', fontsize=13, fontweight='bold',
            color=TEXT_PRIMARY, ha='center', va='top')

    # Worst model
    ax.text(0.5, 0.72, _safe_wrap(worst_model, 25), fontsize=9,
            color=NEGATIVE, ha='center', va='center', fontweight='bold')
    ax.text(0.5, 0.62, f'{worst_val:.4f}', fontsize=12,
            color=NEGATIVE, ha='center', va='center')

    # Arrow
    ax.annotate('', xy=(0.5, 0.42), xytext=(0.5, 0.56),
                arrowprops=dict(arrowstyle='->', color=POSITIVE,
                                lw=2.5, mutation_scale=20),
                transform=ax.transAxes)

    # Improvement badge
    badge = mpatches.FancyBboxPatch(
        (0.28, 0.43), 0.44, 0.10,
        boxstyle="round,pad=0.01",
        facecolor=POSITIVE + '20', edgecolor=POSITIVE,
        linewidth=1, transform=ax.transAxes,
    )
    ax.add_patch(badge)
    ax.text(0.5, 0.48, f'+{improvement:.4f} ({pct:+.1f}%)',
            fontsize=11, fontweight='bold', color=POSITIVE,
            ha='center', va='center')

    # Best model
    ax.text(0.5, 0.32, _safe_wrap(best_model, 25), fontsize=9,
            color=GOLD, ha='center', va='center', fontweight='bold')
    ax.text(0.5, 0.22, f'{best_val:.4f}', fontsize=12,
            color=GOLD, ha='center', va='center')

    # Medal
    ax.text(0.5, 0.10, '🏆', fontsize=22, ha='center', va='center')


# ---------------------------------------------------------------------------
# Main Infographic Builders
# ---------------------------------------------------------------------------

def create_experiment_infographic(df, title='Experiment Results', metric=None,
                                   subtitle=None, theme='dark', palette='ocean'):
    """
    Create a comprehensive, publication-quality experiment infographic.

    Args:
        df: DataFrame with experiment results (must have a numeric metric column;
            optionally 'model', parameter columns, etc.)
        title: Main title displayed on the hero banner
        metric: Primary metric column name (auto-detected if None)
        subtitle: Subtitle text (auto-generated if None)
        theme: 'dark' or 'light'
        palette: Color palette name from PALETTES dict

    Returns:
        matplotlib Figure
    """
    # Theme
    if theme == 'dark':
        _apply_dark_theme()
    else:
        _apply_light_theme()

    # Auto-detect metric
    if metric is None:
        metric = _detect_metric(df)
    if metric is None:
        raise ValueError(f"No numeric metric column found. Columns: {df.columns.tolist()}")

    palette_colors = PALETTES.get(palette, PALETTES['ocean'])
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')

    if subtitle is None:
        n = len(df)
        n_models = df['model'].nunique() if 'model' in df.columns else 0
        subtitle = f'{n} experiments'
        if n_models:
            subtitle += f' across {n_models} models'
        subtitle += f'  •  Primary metric: {metric.replace("_", " ").title()}'

    # Build layout with GridSpec
    fig = plt.figure(figsize=(20, 24))
    gs = gridspec.GridSpec(
        5, 2,
        height_ratios=[0.6, 1.8, 1.8, 1.8, 1.8],
        hspace=0.30, wspace=0.25,
        left=0.06, right=0.94, top=0.96, bottom=0.03,
    )

    # Row 0: Hero banner (full width)
    ax_hero = fig.add_subplot(gs[0, :])
    _render_hero_banner(ax_hero, title, subtitle, metric, df, timestamp)

    # Divider
    fig.add_artist(plt.Line2D([0.06, 0.94], [0.835, 0.835],
                              color=DIVIDER, linewidth=0.8,
                              transform=fig.transFigure))

    # Row 1: Podium + Bar Ranking
    ax_podium = fig.add_subplot(gs[1, 0])
    _render_podium(ax_podium, df, metric, palette_colors)

    ax_bars = fig.add_subplot(gs[1, 1])
    _render_bar_ranking(ax_bars, df, metric, palette_colors)

    # Row 2: Distribution + Parameter Heatmap
    ax_dist = fig.add_subplot(gs[2, 0])
    _render_distribution(ax_dist, df, metric)

    ax_heatmap = fig.add_subplot(gs[2, 1])
    _render_parameter_heatmap(ax_heatmap, df, metric)

    # Row 3: Radar + Improvement Arrows
    ax_radar = fig.add_subplot(gs[3, 0])
    _render_radar(ax_radar, df, metric)

    ax_improve = fig.add_subplot(gs[3, 1])
    _render_improvement_arrows(ax_improve, df, metric)

    # Row 4: Stats Card (full width)
    ax_stats = fig.add_subplot(gs[4, :])
    _render_stats_card(ax_stats, df, metric)

    return fig


def create_comparison_infographic(classification_df, regression_df,
                                   title='Classification vs Regression',
                                   theme='dark'):
    """
    Create a side-by-side comparison infographic for classification and
    regression experiment results.

    Args:
        classification_df: DataFrame with classification results (needs 'accuracy')
        regression_df: DataFrame with regression results (needs 'r2_score')
        title: Main title
        theme: 'dark' or 'light'

    Returns:
        matplotlib Figure
    """
    if theme == 'dark':
        _apply_dark_theme()
    else:
        _apply_light_theme()

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')

    fig = plt.figure(figsize=(20, 16))
    gs = gridspec.GridSpec(3, 2, height_ratios=[0.5, 2, 2],
                           hspace=0.30, wspace=0.25,
                           left=0.06, right=0.94, top=0.96, bottom=0.05)

    # Hero
    ax_hero = fig.add_subplot(gs[0, :])
    subtitle = (f'Classification: {len(classification_df)} experiments  •  '
                f'Regression: {len(regression_df)} experiments')
    _render_hero_banner(ax_hero, title, subtitle, None, classification_df, timestamp)

    fig.add_artist(plt.Line2D([0.06, 0.94], [0.78, 0.78],
                              color=DIVIDER, linewidth=0.8,
                              transform=fig.transFigure))

    # Classification
    ax_clf_bar = fig.add_subplot(gs[1, 0])
    clf_metric = _detect_metric(classification_df, 'accuracy')
    if clf_metric:
        _render_bar_ranking(ax_clf_bar, classification_df, clf_metric,
                            PALETTES['ocean'])
        ax_clf_bar.set_title(f'Classification — {clf_metric.title()}',
                             fontsize=13, fontweight='bold', pad=10)

    ax_clf_dist = fig.add_subplot(gs[2, 0])
    if clf_metric:
        _render_distribution(ax_clf_dist, classification_df, clf_metric)

    # Regression
    ax_reg_bar = fig.add_subplot(gs[1, 1])
    reg_metric = _detect_metric(regression_df, 'r2_score')
    if reg_metric:
        _render_bar_ranking(ax_reg_bar, regression_df, reg_metric,
                            PALETTES['sunset'])
        ax_reg_bar.set_title(f'Regression — {reg_metric.title()}',
                             fontsize=13, fontweight='bold', pad=10)

    ax_reg_dist = fig.add_subplot(gs[2, 1])
    if reg_metric:
        _render_distribution(ax_reg_dist, regression_df, reg_metric)

    return fig


def create_mini_infographic(df, metric=None, title='Quick Results',
                             theme='dark'):
    """
    Create a compact single-page infographic (good for embedding in reports).

    Args:
        df: DataFrame with experiment results
        metric: Primary metric (auto-detected if None)
        title: Title text
        theme: 'dark' or 'light'

    Returns:
        matplotlib Figure
    """
    if theme == 'dark':
        _apply_dark_theme()
    else:
        _apply_light_theme()

    if metric is None:
        metric = _detect_metric(df)

    fig = plt.figure(figsize=(12, 8))
    gs = gridspec.GridSpec(1, 2, wspace=0.25,
                           left=0.08, right=0.92, top=0.88, bottom=0.10)

    fig.suptitle(title, fontsize=18, fontweight='bold',
                 color=TEXT_PRIMARY, y=0.96)
    fig.text(0.5, 0.91, datetime.now().strftime('%Y-%m-%d %H:%M'),
             fontsize=8, color=TEXT_SECONDARY, ha='center', style='italic')

    ax_bars = fig.add_subplot(gs[0, 0])
    _render_bar_ranking(ax_bars, df, metric, PALETTES['ocean'])

    ax_dist = fig.add_subplot(gs[0, 1])
    _render_distribution(ax_dist, df, metric)

    return fig


# ---------------------------------------------------------------------------
# Export Utilities
# ---------------------------------------------------------------------------

def export_infographic(fig, output_path, dpi=300):
    """
    Export infographic to a file (PNG, PDF, SVG, etc.).

    Args:
        fig: matplotlib Figure
        output_path: Path to save file (extension determines format)
        dpi: Resolution (default: 300 for print quality)

    Returns:
        str: Absolute path where saved
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    fig.savefig(output_path, dpi=dpi, bbox_inches='tight',
                facecolor=fig.get_facecolor(), edgecolor='none')
    print(f"✅ Infographic saved to: {output_path}")
    return os.path.abspath(output_path)


def export_multi_format(fig, base_path, dpi=300):
    """
    Export infographic in PNG and PDF formats.

    Args:
        fig: matplotlib Figure
        base_path: Base path without extension (e.g., 'output/infographic')
        dpi: Resolution

    Returns:
        dict: {'png': path, 'pdf': path}
    """
    paths = {}
    for ext in ['png', 'pdf']:
        path = f"{base_path}.{ext}"
        export_infographic(fig, path, dpi)
        paths[ext] = os.path.abspath(path)
    return paths


# ---------------------------------------------------------------------------
# Convenience / Quick Functions
# ---------------------------------------------------------------------------

def quick_infographic(csv_path, output_path='images/infographic.png',
                       title='Experiment Results', metric=None, theme='dark'):
    """
    One-liner: load CSV → create infographic → save to file.

    Args:
        csv_path: Path to CSV file with experiment results
        output_path: Path to save the infographic image
        title: Title for the infographic
        metric: Primary metric (auto-detected if None)
        theme: 'dark' or 'light'

    Returns:
        str: Path where infographic was saved
    """
    df = pd.read_csv(csv_path)
    fig = create_experiment_infographic(df, title=title, metric=metric,
                                         theme=theme)
    path = export_infographic(fig, output_path)
    plt.close(fig)
    return path


def quick_comparison(clf_csv, reg_csv, output_path='images/comparison.png',
                      title='Classification vs Regression', theme='dark'):
    """
    One-liner: load two CSVs → create comparison infographic → save.

    Args:
        clf_csv: Path to classification results CSV
        reg_csv: Path to regression results CSV
        output_path: Path to save the infographic image
        title: Title
        theme: 'dark' or 'light'

    Returns:
        str: Path where infographic was saved
    """
    clf_df = pd.read_csv(clf_csv)
    reg_df = pd.read_csv(reg_csv)
    fig = create_comparison_infographic(clf_df, reg_df, title=title, theme=theme)
    path = export_infographic(fig, output_path)
    plt.close(fig)
    return path


def create_nlp_infographic(topic_counts, keywords_df=None, title='NLP Analysis Results', theme='dark'):
    """
    Create an infographic specifically for NLP tasks like topic modeling and keyword extraction.
    
    Args:
        topic_counts: DataFrame from analyze_text_topics
        keywords_df: DataFrame with 'word' and 'score' for top keywords (optional)
        title: Title
        theme: 'dark' or 'light'
        
    Returns:
        matplotlib Figure
    """
    if theme == 'dark':
        _apply_dark_theme()
    else:
        _apply_light_theme()

    fig = plt.figure(figsize=(14, 8))
    
    # Decide layout based on whether we have keywords
    if keywords_df is not None:
        gs = gridspec.GridSpec(1, 2, width_ratios=[1.2, 1], wspace=0.3, 
                               left=0.08, right=0.92, top=0.88, bottom=0.10)
    else:
        gs = gridspec.GridSpec(1, 1, left=0.1, right=0.9, top=0.88, bottom=0.10)

    # Title
    fig.suptitle(title, fontsize=20, fontweight='bold', color=TEXT_PRIMARY, y=0.96)
    fig.text(0.5, 0.91, datetime.now().strftime('%Y-%m-%d %H:%M'), 
             fontsize=10, color=TEXT_SECONDARY, ha='center', style='italic')

    # Topic Distribution Subplot
    ax_topics = fig.add_subplot(gs[0, 0])
    sns.barplot(data=topic_counts, x='Percentage', y='Topic', palette=PALETTES['ocean'], ax=ax_topics)
    ax_topics.set_title('Topic Distribution (%)', fontsize=14, fontweight='bold', pad=15)
    ax_topics.set_xlabel('Percentage (%)', fontsize=12)
    ax_topics.set_ylabel('')
    
    # Annotate bars
    for i, p in enumerate(ax_topics.patches):
        width = p.get_width()
        ax_topics.text(width + 1, p.get_y() + p.get_height() / 2, f"{width:.1f}%", 
                       ha='left', va='center', color=TEXT_PRIMARY, fontweight='bold')

    # Keywords Subplot
    if keywords_df is not None:
        ax_kw = fig.add_subplot(gs[0, 1])
        top_kw = keywords_df.sort_values(by='score', ascending=False).head(15)
        sns.barplot(data=top_kw, x='score', y='word', palette=PALETTES['purple'], ax=ax_kw)
        ax_kw.set_title('Top Keywords / Features', fontsize=14, fontweight='bold', pad=15)
        ax_kw.set_xlabel('Importance Score', fontsize=12)
        ax_kw.set_ylabel('')

    return fig

