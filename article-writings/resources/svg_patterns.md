# SVG Visualization Patterns

## Pattern 1: Flow Diagram with Arrows

Use for showing data flow between components (e.g., attention mechanisms, encoder layers).

```html
<div class="my-8 flex flex-col items-center">
<svg viewBox="0 0 800 400" class="w-full h-auto overflow-visible font-sans max-w-3xl">
  <defs>
    <marker id="arrow-blue" viewBox="0 0 10 10" refX="9" refY="5"
      markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#3b82f6"/>
    </marker>
  </defs>

  <!-- Input box -->
  <rect x="50" y="50" width="200" height="50" rx="8"
    fill="#eff6ff" class="dark:fill-blue-900/40"
    stroke="#3b82f6" stroke-width="2"/>
  <text x="150" y="70" text-anchor="middle" font-size="14"
    font-weight="bold" fill="#1d4ed8" class="dark:fill-blue-400">
    Input Component
  </text>
  <text x="150" y="90" text-anchor="middle" font-size="11"
    fill="#6b7280" class="dark:fill-gray-400" font-family="monospace">
    [0.52, -0.31, ...] ∈ ℝ²⁰⁰
  </text>

  <!-- Arrow (label placed BESIDE, not on top) -->
  <line x1="150" y1="100" x2="150" y2="170"
    stroke="#3b82f6" stroke-width="2" marker-end="url(#arrow-blue)"/>
  <text x="165" y="140" text-anchor="start" font-size="11"
    fill="#3b82f6" font-weight="bold">W_Q projection</text>

  <!-- Output box -->
  <rect x="50" y="175" width="200" height="50" rx="8"
    fill="#dcfce7" class="dark:fill-emerald-900/40"
    stroke="#10b981" stroke-width="2"/>
  <text x="150" y="205" text-anchor="middle" font-size="14"
    font-weight="bold" fill="#059669" class="dark:fill-emerald-400">
    Output: Q_i
  </text>
</svg>
<p class="text-[0.7rem] text-center mt-4 italic text-gray-600 dark:text-gray-400 max-w-2xl">
  *Figure N: Description of the visualization.*
</p>
</div>
```

### Key Rules:
- Arrow labels go BESIDE the arrow (use `text-anchor="start"` with x offset)
- Include concrete values in monospace font
- Use `class="dark:fill-*"` for dark mode

## Pattern 2: Programmatic N×N Matrix Grid

Use for adjacency matrices, relationship matrices, word-pair tagging grids.

**IMPORTANT**: For 10×10+ grids, generate SVG cells programmatically in a Node.js script.

```javascript
const words = ['The','staff','was','very','court.','but','the','food','was','terr.'];
const cx = 70, cy = 45, ox = 100, oy = 55; // cell width, height, x-offset, y-offset

// Build cells
let cells = '';
for (let r = 0; r < 10; r++) {
  for (let c = 0; c < 10; c++) {
    const x = ox + c * cx, y = oy + r * cy;
    const value = matrix[r][c];
    // Choose colors based on value
    let fill, stroke, sw, textFill;
    if (value === 1) {
      fill = '#dbeafe'; stroke = '#3b82f6'; sw = 2; textFill = '#1d4ed8';
    } else {
      fill = '#f9fafb'; stroke = '#e5e7eb'; sw = 1; textFill = '#d1d5db';
    }
    cells += `<rect x="${x}" y="${y}" width="${cx}" height="${cy}" rx="4"
      fill="${fill}" class="dark:fill-gray-800"
      stroke="${stroke}" stroke-width="${sw}"/>`;
    cells += `<text x="${x+cx/2}" y="${y+cy/2+5}" text-anchor="middle"
      font-size="14" font-weight="bold" fill="${textFill}">${value}</text>`;
  }
}

// Column + row headers
let headers = '';
for (let i = 0; i < 10; i++) {
  headers += `<text x="${ox + i*cx + cx/2}" y="${oy - 10}"
    text-anchor="middle" font-size="14" font-weight="bold"
    fill="#374151" class="dark:fill-gray-300">${words[i]}</text>`;
  headers += `<text x="${ox - 10}" y="${oy + i*cy + cy/2 + 5}"
    text-anchor="end" font-size="14" font-weight="bold"
    fill="#374151" class="dark:fill-gray-300">${words[i]}</text>`;
}

const totalW = ox + 10 * cx + 20;
const totalH = oy + 10 * cy + 20;

const svg = `<svg viewBox="0 0 ${totalW} ${totalH}"
  class="h-auto overflow-visible font-sans"
  style="min-width:700px;width:100%;max-width:900px;">
  ${headers}${cells}
</svg>`;
```

### Sizing Rules:
- Minimum cell size: **70×45px** for readability
- Font size: **14px** minimum for cell values
- Use `min-width:700px` on the SVG and wrap in `overflow-x-auto` div
- Always include a legend below the grid

## Pattern 3: GCN / Neighbor Propagation Diagram

Use for showing how adjacent cells/nodes influence a target.

```html
<!-- Center target node -->
<rect x="250" y="100" width="200" height="55" rx="10"
  fill="#dcfce7" stroke="#10b981" stroke-width="3"/>
<text x="350" y="130" text-anchor="middle" font-size="13"
  font-weight="bold" fill="#059669">Target Cell</text>

<!-- Neighbor nodes (top, bottom, left, right) -->
<rect x="270" y="10" width="160" height="40" rx="6"
  fill="#f3f4f6" stroke="#d1d5db" stroke-width="1.5"/>
<text x="350" y="35" text-anchor="middle" font-size="11"
  fill="#6b7280">Top Neighbor</text>

<!-- Dashed arrows from neighbors to target -->
<line x1="350" y1="50" x2="350" y2="95"
  stroke="#ef4444" stroke-width="2" stroke-dasharray="4"
  marker-end="url(#arrow-red)"/>
```

## Pattern 4: BiLSTM Sequence Diagram

```html
<!-- Forward LSTM cells (blue) -->
<rect x="60" y="150" width="80" height="60" rx="8"
  fill="#eff6ff" class="dark:fill-blue-900/40"
  stroke="#3b82f6" stroke-width="2"/>
<text x="100" y="186" text-anchor="middle"
  font-weight="bold" fill="#2563eb">LSTM</text>

<!-- Backward LSTM cells (amber) -->
<rect x="60" y="70" width="80" height="60" rx="8"
  fill="#fffbeb" class="dark:fill-amber-900/40"
  stroke="#f59e0b" stroke-width="2"/>
<text x="100" y="106" text-anchor="middle"
  font-weight="bold" fill="#d97706">LSTM</text>

<!-- Forward arrows (blue, left-to-right) -->
<line x1="140" y1="180" x2="210" y2="180"
  stroke="#3b82f6" stroke-width="3" marker-end="url(#arrow-fwd)"/>

<!-- Backward arrows (amber, right-to-left) -->
<line x1="210" y1="100" x2="140" y2="100"
  stroke="#f59e0b" stroke-width="3" marker-end="url(#arrow-bwd)"/>

<!-- Concatenation node -->
<circle cx="100" cy="35" r="16" fill="#f3f4f6"
  stroke="#6b7280" stroke-width="2"/>
<text x="100" y="41" text-anchor="middle" font-size="16"
  font-weight="bold" fill="#4b5563">⊕</text>
```

## Color Palette Reference

| Purpose | Fill | Stroke | Text |
|---------|------|--------|------|
| Semantic/BiLSTM | `#eff6ff` | `#3b82f6` | `#1d4ed8` |
| Syntactic/AEA | `#ecfdf5` | `#10b981` | `#047857` |
| Projection/Transform | `#f5f3ff` | `#8b5cf6` | `#7c3aed` |
| Warning/Distance | `#fffbeb` | `#f59e0b` | `#d97706` |
| Negative/Blocked | `#fef2f2` | `#ef4444` | `#dc2626` |
| Neutral/No relation | `#f9fafb` | `#e5e7eb` | `#9ca3af` |
| Output/Result | `#eff6ff` | `#3b82f6` (thick) | `#1d4ed8` |

## Anti-Patterns (DO NOT DO)

1. **❌ Text on top of arrows** — Always place text labels BESIDE arrows
2. **❌ Small cells** — Never use cells smaller than 70×45px in grids
3. **❌ No concrete values** — Every visualization MUST show actual numbers
4. **❌ Inconsistent example** — ALL visualizations must use the SAME running example
5. **❌ Missing dark mode** — Always add `class="dark:fill-* dark:stroke-*"`
6. **❌ No caption** — Every figure needs a `<p>` caption with figure number
7. **❌ Hardcoded large SVGs** — For 10×10+ grids, generate cells in JS loops
