---
name: Data Science Lab
description: End-to-end data science lab workflow from task planning to result analysis. Uses Jupyter notebooks, Linear for task management (optional), and exports results for analysis.
---

# Data Science Lab Skill

> [!NOTE]
> This skill is designed for data science experiments using Jupyter notebooks. It handles the complete workflow from planning to result export, supporting Supervised Learning, Unsupervised Learning, and NLP (Topic Modeling, Sentiment Analysis, Text Classification).

## Pre-Flight Check: Tool Availability

Before starting any experiment, **confirm tool availability** with the user:

### Required Tools (Check if installed)

```
Hi! Before we begin, let me check what tools are available:

1. **Python 3.8+** with `uv` - [ ] Available / [ ] Not installed
2. **Jupyter** (ipykernel) - [ ] Available / [ ] Not installed
3. **Data science packages** - [ ] All installed / [ ] Need to install

Optional:
4. **Linear App** (for task tracking) - [ ] Connected / [ ] Not set up

Should I proceed? Let me know if any tools need to be set up first.
```

### Tool Availability Response Handling

| User Response | Action |
|---------------|--------|
| "Yes, proceed" / "All good" | Continue with Step 1 |
| "Install packages" | Run: `uv pip install pandas numpy scikit-learn matplotlib seaborn plotly tabulate ipykernel` |
| "No Linear" | Use **Markdown-based task tracking** (see below) |
| "Set up Linear" | Guide user through Linear MCP setup |

### Markdown-Based Task Tracking (Alternative to Linear)

If Linear is not available, use markdown files for task tracking:

1. **Create a TODO list** in `tasks.md`:
```markdown
# Lab Tasks: [Experiment Name]

- [ ] Step 1: Load and explore data
- [ ] Step 2: Data cleaning and preprocessing
- [ ] Step 3: Build and train model
- [ ] Step 4: Evaluate results
- [ ] Step 5: Generate visualizations
```

2. **Update progress** as tasks complete:
```markdown
# Lab Tasks: [Experiment Name]

- [x] Step 1: Load and explore data
- [x] Step 2: Data cleaning and preprocessing
- [ ] Step 3: Build and train model
- [ ] Step 4: Evaluate results
- [ ] Step 5: Generate visualizations
```

3. **Create separate files** for:
   - `notebook.ipynb` - Main experiment notebook
   - `results.csv` - Experiment metrics
   - `notes.md` - Observations and insights

## Overview

This skill guides you through a complete data science lab workflow:
1. Analyze requirements and create structured tasks
2. Create and edit Jupyter notebooks
3. Run experiments (Regression, Classification, NLP) and analyze results
4. Export results to CSV
5. Generate visualizations and infographics
6. Create reports with findings and insights

## How to Use This Skill

To start a new data science lab, provide the AI agent with:

### Example Prompts

**Starting a new lab:**
```
Create a new data science lab for [topic].
Follow the data-science-lab skill.
```

**Starting with a CSV/dataset only:**
```
Analyze the dataset at @[path/to/data.csv] and create a data science experiment.
Follow the data-science-lab skill.
```

**Starting with CSV and goal:**
```
I have a dataset at @[path/to/data.csv].
Goal: predict the [target_column] value.
Follow the data-science-lab skill.
```

**Starting with CSV for exploration:**
```
Explore @[path/to/data.csv] and find patterns/insights.
Use the data-science-lab skill.
```

**Analyzing requirements:**
```
Analyze @[path/to/lab-instructions.pdf] and create a plan.
Use the data-science-lab skill.
```

**Creating notebook:**
```
Create a Jupyter notebook for [experiment name].
Follow the data-science-lab skill.
```

**Exporting results:**
```
Add CSV export to the notebook at @[path/to/notebook.ipynb].
Follow the data-science-lab skill.
```

## Prerequisites

Before starting, ensure the following are available:

- **Python 3.8+** with `uv` for environment management
- **Jupyter** — `ipykernel` for notebook kernel
- **Linear account** (optional) — for task tracking via MCP; use Markdown if not available
- **Data science packages** — pandas, numpy, scikit-learn, matplotlib, seaborn, plotly, tabulate

### Quick Setup

```bash
# Create virtual environment
uv venv

# Install required packages
uv pip install pandas numpy scikit-learn matplotlib seaborn plotly tabulate ipykernel

# Register kernel for Jupyter
python -m ipykernel install --user --name=my-env
```

## Tool Setup

### Handling CSV/Dataset-Only Prompts

When the user provides **only a CSV or dataset** (without explicit task type), the agent should:

1. **Load and inspect the data** — Use EDA to understand structure, columns, data types
2. **Auto-detect task type** based on the target column:
   - If target column is **categorical** (few unique values, string or int with low cardinality) → `classification`
   - If target column is **continuous numerical** → `regression`
   - If no clear target → treat as **unsupervised** (clustering, PCA, etc.)
3. **Suggest experiment type** to user and proceed

```python
# Auto-detect task type example
def detect_task_type(df, target_col):
    if target_col not in df.columns:
        return 'unsupervised'
    
    unique_ratio = df[target_col].nunique() / len(df)
    
    if df[target_col].dtype in ['object', 'str'] or unique_ratio < 0.05:
        return 'classification'
    elif unique_ratio > 0.5 and df[target_col].dtype in ['int64', 'float64']:
        return 'regression'
    else:
        return 'classification'  # default
```

### Flexible Workflow Entry Points

The skill supports different starting points based on what user provides:

| User Input | Start at Step | Notes |
|------------|---------------|-------|
| Topic/Problem only | Step 1: Task Planning | Create experiment from scratch |
| CSV only | Step 4: Data Handling | Auto-detect task type |
| CSV + Goal | Step 4: Data Handling | Use specified target column |
| Existing notebook | Step 5: EDA | Continue from existing work |

### Linear App (Task Management)

Linear is used for tracking lab tasks. The agent should use these **Linear MCP tools** directly:

| Action | MCP Tool | Example |
|--------|----------|---------|
| Create a task | `save_issue` | `save_issue(title="Lab 1: Train classifier", team="...", labels=["lab 1"])` |
| Update task status | `save_issue` | `save_issue(id="...", state="In Progress")` |
| List tasks | `list_issues` | `list_issues(project="ML Course")` |
| Get task details | `get_issue` | `get_issue(id="...")` |

The agent should:
1. Create issues with proper labels (e.g., `"lab 1"`, `"lab 2"`, `"final project"`)
2. Move issues to `"In Progress"` when starting work
3. Move issues to `"In Review"` when complete

If the user has not set up Linear, use **Markdown-based task tracking** (see Pre-Flight Check section) and proceed with the experiment directly.

### Helper Scripts

> [!NOTE]
> This skill includes reusable scripts in the `scripts/` directory. Use these directly — do not recreate them.

| Script | Purpose | Key Functions |
|--------|---------|---------------|
| `scripts/run_eda.py` | **Generic EDA on any dataset** | `run_full_eda()`, `data_overview()`, `data_quality_report()`, `univariate_analysis()`, `bivariate_analysis()`, `outlier_detection()` |
| `scripts/run_data_prep.py` | **Generic data preparation pipeline** | `run_full_data_prep()`, `handle_missing_values()`, `encode_features()`, `scale_features()`, `handle_outliers()`, `select_features()`, `split_data()` |
| `scripts/analyze_results.py` | Analyze experiment results | `find_best_model()`, `compare_models()`, `generate_insights()`, `analyze_text_topics()` |
| `scripts/visualize.py` | Generate plots and charts | `plot_confusion_matrix()`, `plot_metric_comparison()`, `plot_topic_distribution()`, `plot_word_frequencies()` |
| `scripts/create_infographics.py` | Publication-quality infographics with dark/light themes | `create_experiment_infographic()`, `create_comparison_infographic()`, `create_nlp_infographic()`, `export_infographic()` |

**Usage in notebooks:**
```python
import sys
sys.path.insert(0, '/path/to/data-science-lab/scripts')

# EDA (always run first on any new dataset)
from run_eda import run_full_eda

# Data Preparation (run after EDA, before modeling)
from run_data_prep import run_full_data_prep

from analyze_results import find_best_model, compare_models, generate_insights
from visualize import plot_confusion_matrix, plot_metric_comparison
from create_infographics import create_experiment_infographic, export_infographic
```

## Workflow

### Step 1: Task Planning

- Analyze source documents (PDF, TXT, etc.)
- Break down into structured tasks
- Create todos in Linear App with `"Backlog"` status using `save_issue`
- Add appropriate labels (e.g., `"lab 1"`, `"lab 2"`, `"final project"`)

### Step 2: Task Execution

- Move todo to `"In Progress"` using `save_issue(id="...", state="In Progress")`
- Execute one task at a time
- Use clear metrics and goals
- Break long tasks into smaller composable steps

### Step 3: Notebook Creation

- Use `.ipynb` format for all experiments
- Create separate directories for each lab/experiment
- Use `uv` for Python environment management

### Step 4: Data Handling

- Load data from local files or remote sources
- Handle missing values appropriately
- Use proper path resolution (handle both script and notebook execution):

```python
import os

# Resolve base directory — works in both scripts and notebooks
try:
    base_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    base_dir = os.getcwd()

data_path = os.path.join(base_dir, '..', 'data', 'file.csv')
```

> [!WARNING]
> Use `__file__` (the Python variable), NOT `'__file__'` (a string literal). The string version resolves the literal filename `"__file__"` relative to cwd, which is incorrect.

### Step 5: Exploratory Data Analysis (EDA)

> [!IMPORTANT]
> **Always run EDA before any modeling or experiments.** This step helps you understand the dataset structure, quality, and distributions. Use the generic `run_eda.py` script — it works with **any** tabular dataset.

Run the full EDA pipeline:
```python
import sys
sys.path.insert(0, '/path/to/data-science-lab/scripts')

from run_eda import run_full_eda

# Basic usage — works with any DataFrame
eda_results = run_full_eda(df, output_dir='../images', title='My Dataset EDA')
```

Customization options:
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

The EDA module automatically:
- Classifies columns as numerical, categorical, datetime, or ID-like
- Generates missing-value reports and duplicate counts
- Creates distribution plots (histograms + KDE for numerical, pie/bar for categorical)
- Produces correlation heatmaps and scatter matrices
- Detects outliers via z-score or IQR methods
- Saves all figures to the specified `output_dir`

### Step 6: Data Preparation

> [!IMPORTANT]
> **Run data preparation after EDA and before modeling.** This step cleans, encodes, scales, and splits your data. Use the generic `run_data_prep.py` script — it works with **any** tabular dataset and produces **human-readable discussions** explaining every decision.

Run the full data preparation pipeline:
```python
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

### Step 6b: Modeling Based on User Goal

When user provides a goal, map it to the appropriate modeling approach:

| User Goal | Task Type | Recommended Models |
|-----------|-----------|-------------------|
| "predict X" / "forecast" | regression | Linear Regression, Random Forest, XGBoost, LSTM |
| "classify X" / "detect X" | classification | Logistic Regression, Random Forest, SVM, XGBoost |
| "segment X" / "group" | clustering | K-Means, DBSCAN, Hierarchical |
| "find patterns" | unsupervised | PCA, Association Rules, Anomaly Detection |
| "understand text" | NLP | TF-IDF + Classifier, BERT, Word2Vec |
| "sentiment analysis" | NLP | VADER, TextBlob, Transformer Models |

**Interpreting ambiguous goals:**
- If user says "analyze" or "find insights" → run EDA + suggest clustering/unsupervised
- If user says "predict" but target is categorical → use classification
- If user says "predict" but target is continuous → use regression
- If user says "improve" or "optimize" → treat as regression (e.g., optimize for metric)

**Dynamic model selection based on data:**
```python
def select_models(task_type, data_size):
    if task_type == 'classification':
        models = [
            ('Logistic Regression', LogisticRegression()),
            ('Random Forest', RandomForestClassifier(n_estimators=100)),
            ('XGBoost', XGBClassifier()),
        ]
    elif task_type == 'regression':
        models = [
            ('Linear Regression', LinearRegression()),
            ('Random Forest', RandomForestRegressor(n_estimators=100)),
            ('XGBoost', XGBRegressor()),
        ]
    elif task_type == 'clustering':
        models = [
            ('K-Means', KMeans(n_clusters=5)),
            ('DBSCAN', DBSCAN(eps=0.5)),
        ]
    
    # For small datasets, prefer simpler models
    if data_size < 1000:
        models = models[:2]  # Skip complex models
    
    return models
```

**User-provided goal examples:**

| User Prompt | Interpreted Goal | Task Type |
|-------------|-----------------|----------|
| "Predict house prices" | regression on price column | regression |
| "Detect fraud transactions" | binary classification | classification |
| "Customer segmentation" | group similar customers | clustering |
| "What factors influence sales?" | feature importance analysis | regression/classification |
| "Sentiment analysis on reviews" | classify positive/negative | NLP classification |
| "Recommend products" | collaborative filtering | recommendation |
| "Detect anomalies" | outlier/anomaly detection | unsupervised |

**Running experiments with multiple models:**
```python
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

# Select models based on task and data
models = select_models(task_type='classification', data_size=len(X_train))

results = []
for name, model in models:
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    results.append({
        'model': name,
        'accuracy': accuracy_score(y_test, y_pred),
        'f1': f1_score(y_test, y_pred, average='weighted'),
    })

# Compare results
results_df = pd.DataFrame(results)
print(results_df)
```

### Step 7: Results Export

- Save experiment results to CSV files
- Store in a `results/` subdirectory
- Include all parameters and metrics (accuracy, F1, MSE, R2, etc.)

```python
import os
import pandas as pd

results_dir = os.path.join(os.path.dirname(data_path), '..', 'results')
os.makedirs(results_dir, exist_ok=True)

results = []
for param in params:
    # run experiment...
    results.append({'model': model_name, 'param': param, 'accuracy': score})

df = pd.DataFrame(results)
df.to_csv(os.path.join(results_dir, 'results.csv'), index=False)
```

### Step 8: Analysis & Findings

After running experiments, use the helper scripts to analyze results:

```python
from analyze_results import find_best_model, compare_models, generate_insights, print_summary

# Load results
results_df = pd.read_csv('results/results.csv')

# Find best model
best = find_best_model(results_df, metric='accuracy')

# Compare all models
comparison = compare_models(results_df, metric='accuracy')

# Generate structured insights
insights = generate_insights(results_df, metric='accuracy')

# Print formatted summary
print_summary(results_df, metric='accuracy')
```

The agent should:
- **Analyze results**: Compare metrics across different models/parameters
- **Identify patterns**: Find what works best and why
- **Document findings**: Write clear summaries of what the experiments show
- **Generate insights**: Explain what the results mean for the problem

### Step 9: Visualizations

Use the helper scripts to generate plots:

```python
from visualize import plot_confusion_matrix, plot_metric_comparison, plot_parameter_sweep, save_all_plots

# Quick: save all standard plots at once
save_all_plots(results_df, results_dir='images', metric='accuracy')

# Or generate individual plots:
plot_metric_comparison(results_df, 'accuracy', save_path='images/model_comparison.png')
plot_parameter_sweep(results_df, 'alpha', 'accuracy', hue='model', save_path='images/param_sweep.png')
plot_confusion_matrix(cm, labels=['Class A', 'Class B'], save_path='images/confusion_matrix.png')
```

For infographics (supports `theme='dark'` or `'light'`, and palette options `'ocean'`, `'sunset'`, `'forest'`, `'purple'`, `'slate'`, `'candy'`):
```python
from create_infographics import (
    create_experiment_infographic,
    create_comparison_infographic,
    create_mini_infographic,
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
```

Save all visualizations to an `images/` or `figures/` directory.

### Step 10: Report Generation & Translation

For presentation-style reports (like lab presentations), use LaTeX Beamer. This skill includes support for creating professional slide decks.

#### Prerequisites

LaTeX compilation requires either:
- **Local installation**: TeX Live or MiKTeX
- **Docker**: Use the official TeX Live Docker image

```bash
# Pull the Docker image (one-time setup)
docker pull registry.gitlab.com/islandoftex/images/texlive:latest
```

#### Creating a Beamer Presentation

Create your presentation in the `reports/` directory with `.tex` extension:

```latex
\documentclass[12pt,aspectratio=169]{beamer}

% Theme settings
\usetheme{Madrid}
\usecolortheme{whale}

% Title
\title{Your Presentation Title}
\author{Your Name}
\date{\today}

\begin{document}
\frame{\titlepage}

% Sections
\section{Introduction}
\begin{frame}{Introduction}
Your content here...
\end{frame}

\section{Results}
\begin{frame}{Results}
\begin{table}[htbp]
\centering
\caption{Your Table}
\begin{tabular}{lcc}
\toprule
Model & Accuracy & F1-Score \\
\midrule
A & 0.95 & 0.94\\
B & 0.97 & 0.96\\
\bottomrule
\end{tabular}
\end{table}
\end{frame}

\end{document}
```

#### Compiling with Docker

```bash
# From your project root
docker run --rm -v "//$(pwd):/workdir" -w //workdir \
  registry.gitlab.com/islandoftex/images/texlive:latest \
  pdflatex labs/lab1/reports/main.tex
```

Or for continuous compilation:
```bash
# Watch mode (requires additional tools)
docker run --rm -v "//$(pwd):/workdir" -w //workdir \
  registry.gitlab.com/islandoftex/images/texlive:latest \
  pdflatex -interaction=nonstopmode main.tex
```

#### Common Beamer Elements

| Element | Code | Description |
|---------|------|-------------|
| Title Slide | `\frame{\titlepage}` | Standard title |
| Section | `\section{Name}` | Navigation section |
| Block | `\begin{block}{Title}...\end{block}` | Colored box |
| Two Columns | `\begin{columns}...\end{columns}` | Split slide |
| Image | `\includegraphics[width=0.8\textwidth]{path}` | Include figure |
| Table | `\begin{table}...\end{table}` | Table with caption |
| Itemize | `\begin{itemize}...\end{itemize}` | Bullet points |
| Equation | `$...$` | LaTeX math |

#### Common LaTeX Errors and Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `Undefined control sequence` | Typo in command name | Use `inserttotalframenumber` (NOT `inserttotalframerumber` - common typo!) |
| `There's no line here to end` | Empty line after `\\` | Remove empty line breaks before line endings |
| `Missing $ inserted` | Special characters in text mode | Use `\textit{}` or `\textbf{}` for italic/bold |
| `Package xcolor Error` | Missing table support | Use `\usepackage[table]{xcolor}` |
| `Extra alignment tab` | Too many columns in table | Add more `&` to match column count |

#### Best Practices for Lab Reports

- **Verify CSV values match report**: Always cross-check numbers in LaTeX tables against the actual CSV results
- **Use consistent decimal places**: Round to 2-4 decimal places for readability  
- **Include all experiment variants**: Document baseline, regularized (Ridge/Lasso), scaled, and feature selection experiments
- **Add visualization captions**: Every plot should have a descriptive caption
- **Use professional themes**: `Madrid` + `whale` or `Berlin` + `whale` work well for presentations
