# LaTeX in SVG - How It Works

## Auto-Detection

The `MarkdownRenderer.astro` component automatically detects LaTeX in SVG `<text>` elements by checking for these characters: `_`, `^`, `{`, `}`, `\\`, `σ`, `⊕`.

If detected, the `<text>` element is replaced with a `<foreignObject>` containing KaTeX-rendered HTML.

## What This Means for You

1. **Simple text labels** (e.g., "Input", "Output", "LSTM") → rendered as normal SVG `<text>`
2. **Math-containing labels** (e.g., `h_i^{(l)}`, `W_Q`, `α_{i,j}`) → auto-converted to KaTeX

## Safe Patterns

```html
<!-- Plain text - stays as SVG text -->
<text x="100" y="50" text-anchor="middle" font-size="14"
  fill="#1d4ed8">Input Layer</text>

<!-- Math notation - auto-converted to KaTeX -->
<text x="100" y="50" text-anchor="middle" font-size="14"
  fill="#1d4ed8">h_i^{(l)}</text>

<!-- Subscript notation - auto-converted -->
<text x="100" y="50" text-anchor="middle" font-size="14"
  fill="#1d4ed8">W_{K,e}</text>
```

## Known Gotchas

1. **Unicode math symbols** (`σ`, `⊕`) trigger auto-detection even in plain labels. Use UTF-8 text like `Σ` carefully - it may get mangled by KaTeX.

2. **Underscores in plain text** (e.g., `no_relation`) will trigger LaTeX mode. Avoid underscores in non-math SVG text labels. Use hyphens or spaces instead.

3. **Width estimation**: The `foreignObject` defaults to `width=400`. Very long formulas may need manual adjustment. For short labels, this is fine.

4. **Alignment**: The renderer maps `text-anchor="middle"` to `text-align: center` in the foreignObject. `x` and `y` coordinates are preserved.

## Display Math in Article Body

For display-mode formulas outside SVG, use double dollar signs:

```markdown
$$K_j = h_j W_K + e_{i,j} W_{K_e}$$
```

Or wrap in a centered div:

```html
<div class="my-4 text-center">
$$\alpha_{i,j} = \text{softmax}\left(\frac{Q_i \cdot K_j^T}{\sqrt{d_k}}\right)$$
</div>
```

## Inline Math

Use single dollar signs for inline:

```markdown
The hidden state $h_i \in \mathbb{R}^{200}$ is computed by the BiLSTM.
```
