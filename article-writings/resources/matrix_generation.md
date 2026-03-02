# Programmatic Matrix/Grid Generation

## When to Use

Use programmatic generation for any N×N grid where N ≥ 5. Writing 25+ SVG cells by hand is error-prone and hard to maintain.

## Template Script

```javascript
import Database from 'better-sqlite3';
import path from 'path';

const db = new Database(path.resolve('db/content.db'));
const slug = 'your-article-slug';
const res = db.prepare('SELECT content FROM articles WHERE slug=?').get(slug);
let content = res.content;

// ─── Configuration ───
const words = ['word1', 'word2', 'word3', /* ... */];
const N = words.length;
const cx = 70, cy = 45;   // Cell dimensions (minimum 70×45 for readability)
const ox = 100, oy = 55;  // Offset for headers
const fontSize = 14;       // Minimum 14 for cell text

// ─── Data Matrix ───
// Define your NxN data. Example for adjacency:
const matrix = [
  [1, 1, 0],
  [1, 1, 1],
  [0, 1, 1],
];

// ─── Color Logic ───
function getCellStyle(value, row, col) {
  if (row === col) return { fill: '#eef2ff', stroke: '#a5b4fc', sw: 1.5, textFill: '#6366f1' };
  if (value === 1)  return { fill: '#dbeafe', stroke: '#3b82f6', sw: 2, textFill: '#1d4ed8' };
  return { fill: '#f9fafb', stroke: '#e5e7eb', sw: 1, textFill: '#d1d5db' };
}

// ─── Generate SVG Cells ───
let cells = '';
for (let r = 0; r < N; r++) {
  for (let c = 0; c < N; c++) {
    const x = ox + c * cx, y = oy + r * cy;
    const v = matrix[r][c];
    const s = getCellStyle(v, r, c);
    cells += `<rect x="${x}" y="${y}" width="${cx}" height="${cy}" rx="4" fill="${s.fill}" class="dark:fill-gray-800" stroke="${s.stroke}" stroke-width="${s.sw}"/>`;
    cells += `<text x="${x+cx/2}" y="${y+cy/2+5}" text-anchor="middle" font-size="${fontSize}" font-weight="${v ? 'bold' : 'normal'}" fill="${s.textFill}">${v}</text>`;
  }
}

// ─── Generate Headers ───
let headers = '';
for (let i = 0; i < N; i++) {
  headers += `<text x="${ox + i*cx + cx/2}" y="${oy - 10}" text-anchor="middle" font-size="${fontSize}" font-weight="bold" fill="#374151" class="dark:fill-gray-300">${words[i]}</text>`;
  headers += `<text x="${ox - 10}" y="${oy + i*cy + cy/2 + 5}" text-anchor="end" font-size="${fontSize}" font-weight="bold" fill="#374151" class="dark:fill-gray-300">${words[i]}</text>`;
}

const totalW = ox + N * cx + 20;
const totalH = oy + N * cy + 20;

// ─── Compose Final SVG ───
const svgBlock = `<div class="my-8 flex flex-col items-center">
<div class="w-full overflow-x-auto flex justify-center">
<svg viewBox="0 0 ${totalW} ${totalH}" class="h-auto overflow-visible font-sans" style="min-width:700px;width:100%;max-width:900px;">
  <text x="${ox + N*cx/2}" y="25" text-anchor="middle" font-size="15" font-weight="bold" fill="#6b7280" class="dark:fill-gray-400">Matrix Title</text>
  ${headers}
  ${cells}
</svg>
</div>
<p class="text-[0.7rem] text-center mt-4 italic text-gray-600 dark:text-gray-400 max-w-2xl">*Figure N: Description.*</p>
</div>`;

// ─── Insert into Article ───
const insertBefore = '## Next Section Title';
const idx = content.indexOf(insertBefore);
if (idx === -1) { console.log('Marker not found'); process.exit(1); }
content = content.slice(0, idx) + svgBlock + '\n\n' + content.slice(idx);

db.prepare('UPDATE articles SET content = ? WHERE slug=?').run(content, slug);
console.log('Matrix inserted!');
db.close();
```

## Tips

- Use `overflow-x-auto` wrapper for mobile horizontal scroll
- Set `min-width: 700px` - prevents the SVG from becoming too tiny
- For relationship matrices with text labels (e.g., "nsubj", "det"), use smaller font (11-12px) and wider cells (80×45)
- Add a legend bar below the grid using simple `<rect>` + `<text>` elements
