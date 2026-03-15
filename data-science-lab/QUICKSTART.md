# Data Science Lab — Quickstart

The fastest path from CSV to results. Copy this pattern into a Jupyter notebook:

```python
import pandas as pd
import sys
sys.path.insert(0, '/path/to/data-science-lab/scripts')

from run_eda import run_full_eda
from run_data_prep import run_full_data_prep

# 1. Load
df = pd.read_csv('data/my_dataset.csv')

# 2. EDA
eda = run_full_eda(df, title='My EDA', output_dir='images', target_col='target_column')

# 3. Data Prep
result = run_full_data_prep(
    df, target_col='target_column', task_type='classification',  # or 'regression'
    output_dir='data/prepared', images_dir='images',
)

# 4. Model
X_train, y_train = result['split']['X_train'], result['split']['y_train']
X_test, y_test = result['split']['X_test'], result['split']['y_test']

from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# 5. Evaluate
from sklearn.metrics import accuracy_score, classification_report
print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
print(classification_report(y_test, y_pred))

# 6. Visualize
from create_infographics import create_experiment_infographic, export_infographic
results_df = pd.DataFrame([{'model': 'Random Forest', 'accuracy': accuracy_score(y_test, y_pred)}])
fig = create_experiment_infographic(results_df, title='Results', metric='accuracy')
export_infographic(fig, 'images/infographic.png')
```

For the full workflow, see [SKILL.md](SKILL.md).
