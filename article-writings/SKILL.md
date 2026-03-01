---
name: Research Article Writing
description: Write research articles with SVG visualizations, LaTeX math, citations, and end-to-end calculation traces. Articles are stored in SQLite and rendered via Astro + KaTeX.
---

# Research Article Writing Skill

> [!WARNING]
> This skill is specifically designed to work with a custom SQLite schema and a React/Astro renderer. It is optimized for my personal website's architecture and may not work as-is in other environments.

## Overview

This skill guides you through writing a research article for the personal website. Articles are stored in a SQLite database (`db/content.db`) and rendered by `src/components/MarkdownRenderer.astro` which supports Markdown, LaTeX (KaTeX), inline SVG visualizations, and BibTeX citations.

## How to Use This Skill

To write a new research article, provide the AI agent with:

1. **A source file** — PDF or TXT of the research paper
2. **A reference to this skill** — so the agent knows to follow it

### Example Prompts

**From a PDF:**
```
Write a research article based on this paper:
@[path/to/paper.pdf]

Use the article-writing skill at @[.agent/skills/article-writings]
```

**From a TXT file:**
```
Write a research article about this paper's methodology:
@[path/to/extracted_text.txt]

Follow the article-writing skill at @[.agent/skills/article-writings]
```

**Adding visualizations to an existing article:**
```
Add SVG visualizations for Section 5 of the article "my-article-slug"
in @[db/content.db]. Follow the article-writing skill.
```

**Completing an article:**
```
Complete the remaining sections of @[db/content.db] article "my-slug"
based on @[path/to/source.txt]. Follow the article-writing skill.
```

### What the Agent Will Do

When the agent reads this skill, it follows an 8-phase workflow:

| Phase | What Happens |
|-------|-------------|
| 1. Source Extraction | Extract text from PDF/TXT |
| 2. Plan Structure | Outline sections, pick a running example |
| 3. Database Setup | Create or update the article in SQLite |
| 4. Write Content | Markdown + LaTeX + citations + colored text |
| 5. Visualizations | SVG diagrams with concrete values, no overlaps |
| 6. Calculation Coherence | End-to-end value chain across all sections |
| 7. Content Updates | Small per-section scripts (never one giant write) |
| 8. Verification | Check rendering on localhost |

## Prerequisites

- Node.js with `better-sqlite3` (ESM)
- Python 3 with `PyPDF2` for PDF extraction
- The dev server: `npm run dev` (runs on `http://localhost:4321`)

## Step-by-Step Workflow

### Phase 1: Source Extraction

Extract text from the research paper PDF or TXT:

```bash
# PDF extraction
python scripts/extract.py "<path-to-pdf>" scripts/extracted_source.txt

# Or if already a .txt file, just copy it
cp <source.txt> scripts/extracted_source.txt
```

Read the extracted text to understand the paper's structure, key contributions, formulas, and architecture. 

**⚠️ CRITICAL RULE for Long Content:** If the source document is extremely long, DO NOT attempt to read, analyze, or write it all in one single massive action. Break the content down into smaller, logical pieces (e.g., processing Introduction, then Architecture, then Results) and build the article sequentially.

### Phase 2: Plan the Article Structure

Before writing, plan the sections to match the paper's architecture flow. A typical research article follows this pattern:

1. **Introduction** — Problem statement, motivation, key contributions
2. **Input Processing** — How raw data enters the model (embeddings, tokenization)
3. **Core Components** — Each architectural component gets its own section
4. **Inference/Output** — How the model produces final predictions
5. **Experimental Results** — Benchmark comparisons

**Critical Rule**: Pick ONE running example sentence and use it consistently throughout ALL sections. Every visualization and calculation must trace back to this same example.

### Phase 3: Database Operations

Use the helper scripts in `scripts/` to read/write articles. See `scripts/` directory for patterns.

**Schema** (table `articles`):
```sql
CREATE TABLE articles (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  slug TEXT NOT NULL UNIQUE,
  content TEXT NOT NULL,        -- Markdown content (main body)
  excerpt TEXT,
  published_at DATETIME,
  status TEXT DEFAULT 'draft',  -- 'draft', 'published', 'archived'
  tags TEXT,                    -- JSON array: '["nlp","transformer"]'
  category TEXT DEFAULT 'article',
  cover_image TEXT,
  "references" TEXT             -- BibTeX string for citations
);
```

**Reading content:**
```javascript
import Database from 'better-sqlite3';
const db = new Database('db/content.db');
const article = db.prepare('SELECT content, "references" FROM articles WHERE slug=?').get('my-article-slug');
```

**Writing content:**
```javascript
db.prepare('UPDATE articles SET content = ? WHERE slug = ?').run(newContent, slug);
```

**Inserting a new article:**
```javascript
db.prepare(`INSERT INTO articles (title, slug, content, excerpt, status, tags, "references")
  VALUES (?, ?, ?, ?, 'published', ?, ?)`).run(title, slug, content, excerpt, tagsJson, bibtexStr);
```

### Phase 4: Writing Content

The article content is **Markdown** with these special features:

#### 4a. LaTeX Math

- **Inline**: `$E = mc^2$` renders inline
- **Display block**: `$$F = ma$$` renders centered on its own line
- **In SVG**: Any `<text>` element containing `_`, `^`, `{`, `}`, or `\\` is auto-converted to KaTeX via `foreignObject`. See `resources/latex_in_svg.md`.

#### 4b. Citations

Use `[@cite:keyname]` in the article body. The `keyname` must match an entry in the `references` column (BibTeX format).

Example body text:
```
The SA-Transformer [@cite:yuan2024encoding] outperforms prior methods.
```

Example references column (BibTeX):
```bibtex
@article{yuan2024encoding,
  author = {Li Yuan and Jin Wang and Liang-Chih Yu and Xuejie Zhang},
  year = {2024},
  title = {Encoding Syntactic Information into Transformers for ASTE},
  publisher = {IEEE Transactions on Affective Computing}
}
```

#### 4c. Colored Text

Use `[color:text]` syntax for inline colored highlights:
- `[red:error text]`, `[blue:model name]`, `[emerald:positive result]`, `[sky:term]`, `[amber:warning]`, `[purple:component]`

#### 4d. SVG Visualizations

See `resources/svg_patterns.md` for complete SVG pattern examples. Key rules:
- All SVGs must be wrapped in a `<div class="my-8 flex flex-col items-center">`
- Use `viewBox` for responsive sizing
- **NEVER** overlap text labels with arrows — place labels adjacent to arrows
- Use `class="dark:fill-*"` for dark mode support
- Add a caption: `<p class="text-[0.7rem] text-center mt-4 italic ...">*Figure N: ...*</p>`

### Phase 5: Visualization Guidelines

See `resources/svg_patterns.md` for full SVG code patterns. Summary of rules:

1. **No overlapping elements** — Text labels must sit BESIDE arrows, not on top
2. **Show concrete values** — Every visualization must show actual numeric I/O values from the running example
3. **Use the running example** — All visuals must use the SAME example sentence/data throughout
4. **Arrow markers** — Define `<marker>` elements in `<defs>` for arrowheads
5. **No Tailwind for Base Colors** — ⚠️ CRITICAL: Database content is not scanned by Tailwind CSS during build! Do NOT use Tailwind classes (like `fill-blue-500` or `stroke-red-400`) for base colors. ALWAYS use explicit inline hex codes (e.g., `fill="#eff6ff" stroke="#3b82f6"`). You may include `class="dark:fill-*"` for dark mode support, but the base rendering must rely on inline hex colors.
6. **Programmatic grids** — For N×N matrices, generate SVG cells programmatically in a JS script (see `resources/matrix_generation.md`)
7. **Cell sizing** — For matrix grids, use minimum 70×45px cells with 14px+ font for readability
8. **Color coding** — Use consistent colors: blue for semantic, green for syntactic, red for negative/blocked, amber for warnings/distances, purple for projections

### Phase 6: Calculation Coherence

**Every section must show end-to-end calculation steps with concrete values:**

1. **Input** — Show what enters the component (with actual vector values from the running example)
2. **Formula** — Show the mathematical formula in LaTeX
3. **Worked example** — Trace through the formula with specific numbers
4. **Output** — Show the result that feeds into the next section

**Values must be coherent across sections.** If Section 2 outputs `e₂ = [0.287, -0.156, ...]`, then Section 3 must use that SAME vector as input.

### Phase 7: Content Update Strategy

When updating large articles, break changes into small scripts:

```javascript
// Pattern: Find a section marker, replace just that section
const content = db.prepare('SELECT content FROM articles WHERE slug=?').get(slug).content;
const sectionStart = content.indexOf('## 5. My Section');
const sectionEnd = content.indexOf('## 6. Next Section');
const newContent = content.slice(0, sectionStart) + newSectionText + content.slice(sectionEnd);
db.prepare('UPDATE articles SET content = ? WHERE slug=?').run(newContent, slug);
```

**NEVER** try to write the entire article content in one script if it's large. Break it into per-section scripts.

### Phase 8: Verification

After writing, verify the article renders correctly:

1. Run `npm run dev` if not already running
2. Visit `http://localhost:4321/articles/<slug>`
3. Check: LaTeX renders, SVGs display without overlaps, citations link correctly, dark mode works
