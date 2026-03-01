# Example Article: SA-Transformer for ASTE

This document shows the actual structure used in the SA-Transformer article as a reference for writing future articles.

## Article Metadata

```
title: "Encoding Syntactic Information into Transformers for ASTE"
slug: "sa-transformer-aste-research"
tags: ["nlp", "transformer", "sentiment-analysis"]
category: "article"
status: "published"
```

## Section Flow & Running Example

**Running example sentence**: *"The staff was very courteous but the food was terrible"*

This sentence was chosen because it contains:
- Two aspect terms: "staff", "food"
- Two opinion terms: "courteous", "terrible"
- Two sentiments: POS, NEG
- A conjunction "but" that creates structural ambiguity

### Section Outline

| # | Title | Input | Output | Visualization |
|---|-------|-------|--------|---------------|
| 1 | Introduction | — | — | Architecture overview SVG |
| 2 | GloVe Embedding | Raw words | Vectors ∈ ℝ¹⁰⁰ | Embedding lookup table |
| 3 | BiLSTM | GloVe vectors | Hidden states ∈ ℝ²⁰⁰ | LSTM cell + sequence diagram |
| 4 | Dependency Parsing | Sentence | Adj. matrix + Rel. matrix | Tree SVG + 10×10 grids |
| 5 | AEA (Edge Attention) | Matrices | Edge representations | Edge embedding flow |
| 6 | Syntactic Distance | Dep. tree | BFS hop counts | BFS path diagram |
| 7 | SA-Transformer | BiLSTM + edges | Syntax-enhanced states | Attention flow diagram |
| 8 | Adjacent Inference | Pair representations | Tag predictions | GCN + tagging grid |
| 9 | Experimental Results | — | F1 scores | Results table |

### Value Chain (Coherence Example)

```
Section 2: GloVe("staff") → e₂ = [0.287, -0.156, 0.418, ...] ∈ ℝ¹⁰⁰
    ↓
Section 3: BiLSTM(e₂) → h₂ = [0.52, -0.31, 0.74, ...] ∈ ℝ²⁰⁰
    ↓
Section 4: DepTree → A₂,₃ = 1 (nsubj edge), R₂,₃ = "nsubj"
    ↓
Section 5: AEA(R₂,₃) → edge₂,₃ = [0.15, 0.28, ...] ∈ ℝ²⁰⁰
    ↓
Section 6: BFS(2→5) → dist = 2 hops → f^d(2,5) = [0.12, -0.34, ...] ∈ ℝ¹⁰⁰
    ↓
Section 7: SA-Attention(h₂, edge) → S₂ = [0.41, -0.18, 0.63, ...] ∈ ℝ²⁰⁰
    ↓
Section 8: MLP([S₂; S₅; f^d]) → y₂,₅ = POS (p=0.89)
```

Each section's output becomes the next section's input. This creates a seamless, traceable calculation chain.

## Key Takeaways for New Articles

1. **Choose the running example carefully** — it should exercise all model features
2. **Plan the value chain before writing** — sketch which numbers flow where
3. **Make dimensions explicit** — always state `∈ ℝⁿ` for vectors
4. **Number all figures sequentially** — Figure 1, 2, 3...
5. **Use consistent notation** — define symbols once, reuse everywhere
