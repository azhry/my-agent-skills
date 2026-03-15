# Step 6b: Modeling

## Interpreting User Goals

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

## Dynamic Model Selection

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

## Running Experiments with Multiple Models

```python
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, f1_score

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

## User-Provided Goal Examples

| User Prompt | Interpreted Goal | Task Type |
|-------------|-----------------|----------|
| "Predict house prices" | regression on price column | regression |
| "Detect fraud transactions" | binary classification | classification |
| "Customer segmentation" | group similar customers | clustering |
| "What factors influence sales?" | feature importance analysis | regression/classification |
| "Sentiment analysis on reviews" | classify positive/negative | NLP classification |
| "Recommend products" | collaborative filtering | recommendation |
| "Detect anomalies" | outlier/anomaly detection | unsupervised |

## Use Case Examples

For complete code examples, see:
- Classification/Regression → `examples/lab1_supervised_learning.ipynb`
- Clustering → `examples/use_case_clustering.ipynb`
- Anomaly Detection → `examples/use_case_anomaly.md`
- Time Series → `examples/use_case_forecasting.md`
- NLP Sentiment → `examples/use_case_nlp_sentiment.ipynb`
- NLP Topics → `examples/use_case_nlp_topic.md`
- Recommendation → `examples/use_case_recommendation.md`
