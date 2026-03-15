# Data Science Lab — Usage Examples

This directory contains reference examples showing what inputs the agent receives and what outputs it produces.

## Files

| File | Description |
|------|-------------|
| `lab_instructions.md` | Example lab assignment from a professor — this is the kind of input the agent analyzes in Step 1 |
| `lab1_supervised_learning.ipynb` | Complete example notebook — shows the expected structure and output of the skill workflow |
| `usage.md` | This file — overview of how to use the skill |

## Quick Start

### Prompt 1: Start from lab instructions

```
Here are my lab instructions:
@[path/to/lab_instructions.md]

Create the notebook and run all experiments.
Follow the data-science-lab skill.
```

### Prompt 2: Start from scratch

```
Create a data science lab for classification using the Iris dataset.
Compare Logistic Regression, SVM, and Random Forest.
Export results to CSV and generate an infographic.
Follow the data-science-lab skill.
```

### Prompt 3: Generate infographic from existing results

```
Generate an infographic from these experiment results:
@[path/to/results.csv]

Use the create_infographics.py script from the data-science-lab skill.
Save to images/infographic.png with dark theme.
```

### Prompt 4: Add analysis to existing notebook

```
Analyze the results in @[path/to/notebook.ipynb].
Use the analyze_results.py and generate the report.
Follow the data-science-lab skill.
```

## Expected Output Structure

After the skill completes, the project directory should look like:

```
lab1/
├── notebooks/
│   └── lab1_supervised_learning.ipynb
├── data/                              (if external data needed)
├── results/
│   ├── classification_results.csv
│   └── regression_results.csv
├── images/
│   ├── clf_infographic.png
│   ├── reg_infographic.png
│   ├── lab1_infographic.png           (comparison)
│   ├── clf_confusion_matrix.png
│   ├── clf_model_comparison.png
│   ├── reg_actual_vs_predicted.png
│   └── reg_r2_comparison.png
└── reports/
    ├── experiment_report.md
    └── experiment_report.tex
```
