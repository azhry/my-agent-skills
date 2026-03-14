# Use Case: Recommendation Systems

This document shows how to use the data-science-lab skill for **product recommendation** tasks.

---

## User Prompt Example

```
Build a product recommendation system using @[path/to/user_ratings.csv].
Use collaborative filtering.
Export results and create visualizations.
Follow the data-science-lab skill.
```

---

## Goal Interpretation

| User Goal | Task Type | Recommended Models |
|-----------|-----------|-------------------|
| "Recommend products" | recommendation | Collaborative Filtering, Matrix Factorization, KNN |

---

## Example: Product Recommendations

### Step 1: Load Data

```python
import pandas as pd
import numpy as np

np.random.seed(42)

n_users = 50
n_products = 20
n_ratings = 200

# Generate sample ratings data
users = np.random.randint(1, n_users + 1, n_ratings)
products = np.random.randint(1, n_products + 1, n_ratings)
ratings = np.random.randint(1, 6, n_ratings)

df = pd.DataFrame({
    'user_id': users,
    'product_id': products,
    'rating': ratings
})

# Remove duplicates (keep first)
df = df.drop_duplicates(subset=['user_id', 'product_id'])

print(f"Users: {df['user_id'].nunique()}")
print(f"Products: {df['product_id'].nunique()}")
print(f"Ratings: {len(df)}")
print(df.head(10))
```

### Step 2: Create User-Item Matrix

```python
# Pivot to create user-item matrix
user_item_matrix = df.pivot_table(
    index='user_id', 
    columns='product_id', 
    values='rating'
).fillna(0)

print(f"User-Item Matrix shape: {user_item_matrix.shape}")
print(user_item_matrix.head())
```

### Step 3: Method 1 - KNN-Based Collaborative Filtering

```python
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix

# Convert to sparse matrix
sparse_matrix = csr_matrix(user_item_matrix.values)

# Fit KNN model
knn_model = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=5)
knn_model.fit(sparse_matrix)

def get_knn_recommendations(user_id, n_recommendations=5):
    user_idx = user_item_matrix.index.get_loc(user_id)
    user_vector = sparse_matrix[user_idx]
    
    distances, indices = knn_model.kneighbors(user_vector, n_neighbors=n_recommendations+1)
    
    # Get similar users (exclude self)
    similar_users = indices.flatten()[1:]
    
    # Get products those users rated highly but current user hasn't
    user_ratings = user_item_matrix.iloc[user_idx]
    recommendations = []
    
    for sim_user in similar_users:
        sim_user_ratings = user_item_matrix.iloc[sim_user]
        for product_id, rating in sim_user_ratings.items():
            if user_ratings[product_id] == 0 and rating >= 4:
                recommendations.append((product_id, rating))
    
    # Sort and return top products
    recommendations = sorted(recommendations, key=lambda x: x[1], reverse=True)
    return recommendations[:n_recommendations]

# Test for user 1
recs = get_knn_recommendations(1)
print(f"Recommendations for User 1: {recs}")
```

### Step 4: Method 2 - Matrix Factorization (SVD)

```python
from scipy.sparse.linalg import svds

# Normalize by subtracting mean
user_ratings_mean = np.mean(user_item_matrix.values, axis=1)
matrix_normalized = user_item_matrix.values - user_ratings_mean.reshape(-1, 1)

# Apply SVD
k = 10  # Number of latent factors
U, sigma, Vt = svds(matrix_normalized, k=k)

# Convert sigma to diagonal matrix
sigma = np.diag(sigma)

# Predicted ratings
predicted_ratings = np.dot(np.dot(U, sigma), Vt) + user_ratings_mean.reshape(-1, 1)
predictions_df = pd.DataFrame(predicted_ratings, 
                               index=user_item_matrix.index,
                               columns=user_item_matrix.columns)

def get_svd_recommendations(user_id, n_recommendations=5):
    user_predictions = predictions_df.loc[user_id]
    user_ratings = user_item_matrix.loc[user_id]
    
    # Recommend products not yet rated
    recommendations = []
    for product_id, pred_rating in user_predictions.items():
        if user_ratings[product_id] == 0:
            recommendations.append((product_id, pred_rating))
    
    # Sort by predicted rating
    recommendations = sorted(recommendations, key=lambda x: x[1], reverse=True)
    return recommendations[:n_recommendations]

# Test for user 1
svd_recs = get_svd_recommendations(1)
print(f"SVD Recommendations for User 1: {svd_recs}")
```

### Step 5: Evaluate Model

```python
from sklearn.metrics import mean_squared_error

# Simple evaluation: RMSE on known ratings
def evaluate_model(predictions, actual):
    # Only evaluate on known ratings
    mask = actual > 0
    return np.sqrt(mean_squared_error(actual[mask], predictions[mask]))

rmse_knn = evaluate_model(predictions_df.values, user_item_matrix.values)
print(f"SVD RMSE: {rmse_knn:.4f}")
```

### Step 6: Visualize

```python
import matplotlib.pyplot as plt
import seaborn as sns

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Rating distribution
axes[0].hist(df['rating'], bins=5, edgecolor='black', alpha=0.7)
axes[0].set_xlabel('Rating')
axes[0].set_ylabel('Count')
axes[0].set_title('Rating Distribution')

# User activity
user_activity = df.groupby('user_id').size()
axes[1].hist(user_activity, bins=20, edgecolor='black', alpha=0.7, color='orange')
axes[1].set_xlabel('Number of Ratings')
axes[1].set_ylabel('Number of Users')
axes[1].set_title('User Activity Distribution')

plt.tight_layout()
plt.savefig('images/recommendation_analysis.png', dpi=150)
plt.show()
```

### Step 7: Export Results

```python
# Generate recommendations for all users
all_recommendations = []
for user_id in user_item_matrix.index:
    recs = get_svd_recommendations(user_id, n_recommendations=5)
    for product_id, rating in recs:
        all_recommendations.append({
            'user_id': user_id,
            'product_id': product_id,
            'predicted_rating': rating
        })

recommendations_df = pd.DataFrame(all_recommendations)
recommendations_df.to_csv('results/product_recommendations.csv', index=False)

print("Results saved to results/product_recommendations.csv")
print(f"\nSample recommendations:")
print(recommendations_df.head(10))
```

---

## Summary

| Method | Pros | Cons |
|--------|------|------|
| KNN | Simple, interpretable | Slow for large datasets |
| SVD/Matrix Factorization | Handles sparsity well | Requires tuning k |
| Neural Collaborative Filtering | Can capture complex patterns | Needs more data |

### Key Parameters

- `n_neighbors`: Number of similar users (KNN)
- `k`: Number of latent factors (SVD)
- `metric`: Distance metric (cosine, pearson)
