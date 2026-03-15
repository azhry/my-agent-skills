# Use Case: Topic Modeling (NLP)

This document shows how to use the data-science-lab skill for **topic modeling** tasks.

---

## User Prompt Example

```
Find topics in @[path/to/documents.csv] using LDA.
Export results and create visualizations.
Follow the data-science-lab skill.
```

---

## Goal Interpretation

| User Goal | Task Type | Recommended Models |
|-----------|-----------|-------------------|
| "find topics" / "topic modeling" | NLP unsupervised | LDA, NMF |

---

## Example: Document Topic Analysis

### Step 1: Load Data

```python
import pandas as pd
import numpy as np

# Sample documents
documents = [
    "machine learning deep neural networks artificial intelligence",
    "recipe cooking food ingredients chef kitchen",
    "stock market investment trading finance economy",
    "python programming software development code",
    "healthy diet nutrition exercise fitness wellness",
    "climate change environment pollution sustainability",
    "database sql queries data storage",
    "music band concert festival rock jazz",
    "photo camera photography lens aperture",
    "sports football basketball soccer game",
]

# Create more variations
np.random.seed(42)
docs = []
for doc in documents:
    for _ in range(20):
        words = doc.split()
        # Add random words from same topic
        new_doc = doc + " " + " ".join(np.random.choice(words, 2))
        docs.append(new_doc)

df = pd.DataFrame({'document': docs})
print(f"Number of documents: {len(df)}")
```

### Step 2: Text Preprocessing

```python
from sklearn.feature_extraction.text import CountVectorizer

# Create document-term matrix
vectorizer = CountVectorizer(
    max_df=0.95,  # Ignore terms in >95% of docs
    min_df=2,      # Ignore terms in <2 docs
    stop_words='english'
)

doc_term_matrix = vectorizer.fit_transform(df['document'])
feature_names = vectorizer.get_feature_names_out()

print(f"Vocabulary size: {len(feature_names)}")
print(f"Document-term matrix shape: {doc_term_matrix.shape}")
```

### Step 3: LDA Topic Modeling

```python
from sklearn.decomposition import LatentDirichletAllocation

# Fit LDA
n_topics = 5
lda = LatentDirichletAllocation(
    n_components=n_topics,
    random_state=42,
    max_iter=10
)

lda_topics = lda.fit_transform(doc_term_matrix)

print(f"LDA completed. Topics: {n_topics}")
```

### Step 4: Display Topics

```python
def display_topics(model, feature_names, n_top_words=10):
    for topic_idx, topic in enumerate(model.components_):
        top_words = [feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]]
        print(f"Topic {topic_idx}: {', '.join(top_words)}")

display_topics(lda, feature_names)
```

### Step 5: NMF Topic Modeling (Alternative)

```python
from sklearn.decomposition import NMF

# Fit NMF (often gives more interpretable topics)
nmf = NMF(n_components=n_topics, random_state=42, max_iter=200)
nmf_topics = nmf.fit_transform(doc_term_matrix)

print("\n=== NMF Topics ===")
display_topics(nmf, feature_names)
```

### Step 6: Document-Topic Distribution

```python
# Assign dominant topic to each document
df['dominant_topic'] = lda_topics.argmax(axis=1)

print("\nDocument distribution across topics:")
print(df['dominant_topic'].value_counts().sort_index())
```

### Step 7: Visualize Topics

```python
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

# Reduce to 2D for visualization
pca = PCA(n_components=2)
doc_2d = pca.fit_transform(lda_topics)

plt.figure(figsize=(10, 6))
scatter = plt.scatter(doc_2d[:, 0], doc_2d[:, 1], 
                     c=df['dominant_topic'], cmap='viridis', alpha=0.6)
plt.colorbar(scatter, label='Topic')
plt.title('Documents in Topic Space (LDA)')
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.savefig('images/topic_visualization.png', dpi=150)
plt.show()
```

### Step 8: Topic-Word Distribution

```python
# Visualize top words per topic
fig, axes = plt.subplots(1, n_topics, figsize=(15, 4))

for topic_idx, topic in enumerate(lda.components_):
    top_words_idx = topic.argsort()[:-6:-1]
    top_words = [feature_names[i] for i in top_words_idx]
    top_weights = [topic[i] for i in top_words_idx]
    
    axes[topic_idx].barh(top_words, top_weights)
    axes[topic_idx].set_title(f'Topic {topic_idx}')
    axes[topic_idx].invert_yaxis()

plt.tight_layout()
plt.savefig('images/topic_words.png', dpi=150)
plt.show()
```

### Step 9: Export Results

```python
# Export topic assignments
for i in range(n_topics):
    df[f'topic_{i}_weight'] = lda_topics[:, i]

df.to_csv('results/topic_assignments.csv', index=False)

# Export topic words
topic_words = []
for topic_idx, topic in enumerate(lda.components_):
    top_words = [feature_names[i] for i in topic.argsort()[:-11:-1]]
    topic_words.append({
        'topic': topic_idx,
        'top_words': ', '.join(top_words)
    })

topic_df = pd.DataFrame(topic_words)
topic_df.to_csv('results/topic_words.csv', index=False)

print("Results saved:")
print("  - results/topic_assignments.csv")
print("  - results/topic_words.csv")
```

---

## Summary

| Model | Pros | Cons |
|-------|------|------|
| LDA | Well-established, probabilistic | Can be slow, less interpretable |
| NMF | More interpretable topics, faster | Requires tuning |

### Key Parameters

- `n_topics`: Number of topics to extract
- `max_df`: Ignore very common words
- `min_df`: Ignore very rare words
- `max_iter`: Number of iterations for convergence
