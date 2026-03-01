/**
 * Article Database Helper Templates
 *
 * Copy and adapt these patterns for reading/writing articles.
 * All scripts use ESM (import) and better-sqlite3.
 *
 * Run with: node scripts/your_script.js
 */

// ─── READ: Dump article content to a file ───
/*
import Database from 'better-sqlite3';
import path from 'path';
import fs from 'fs';

const db = new Database(path.resolve('db/content.db'));
const slug = 'your-article-slug';
const res = db.prepare('SELECT content FROM articles WHERE slug=?').get(slug);
fs.writeFileSync('scripts/debug_content.md', res.content);
console.log('Dumped to scripts/debug_content.md');
db.close();
*/

// ─── CREATE: Insert a new article ───
/*
import Database from 'better-sqlite3';
import path from 'path';

const db = new Database(path.resolve('db/content.db'));

const title = 'My Research Article Title';
const slug = 'my-research-article';
const excerpt = 'A brief summary of the article.';
const tags = JSON.stringify(['nlp', 'transformer']);
const references = `
@article{key2024paper,
  author = {Author Name},
  year = {2024},
  title = {Paper Title},
  publisher = {Journal Name}
}
`;

const content = `
## 1. Introduction

Your markdown content here with $LaTeX$ support.

## 2. Next Section

More content...
`;

db.prepare(`
  INSERT INTO articles (title, slug, content, excerpt, status, tags, "references")
  VALUES (?, ?, ?, ?, 'published', ?, ?)
`).run(title, slug, content, excerpt, tags, references);

console.log('Article created!');
db.close();
*/

// ─── UPDATE: Replace a specific section ───
/*
import Database from 'better-sqlite3';
import path from 'path';

const db = new Database(path.resolve('db/content.db'));
const slug = 'your-article-slug';
const res = db.prepare('SELECT content FROM articles WHERE slug=?').get(slug);
let content = res.content;

// Find section boundaries
const sectionStart = content.indexOf('## 3. My Section');
const sectionEnd = content.indexOf('## 4. Next Section');

if (sectionStart === -1 || sectionEnd === -1) {
  console.log('Section markers not found!');
  process.exit(1);
}

const newSection = `## 3. My Section (Updated)

New content for this section...

---

`;

content = content.slice(0, sectionStart) + newSection + content.slice(sectionEnd);
db.prepare('UPDATE articles SET content = ? WHERE slug=?').run(content, slug);
console.log('Section updated!');
db.close();
*/

// ─── INSERT: Add content before a marker ───
/*
import Database from 'better-sqlite3';
import path from 'path';

const db = new Database(path.resolve('db/content.db'));
const slug = 'your-article-slug';
const res = db.prepare('SELECT content FROM articles WHERE slug=?').get(slug);
let content = res.content;

const marker = '## 5. Target Section';
const idx = content.indexOf(marker);
if (idx === -1) { console.log('Marker not found'); process.exit(1); }

const newBlock = `
<div class="my-8 flex flex-col items-center">
  <svg viewBox="0 0 800 400">
    <!-- Your SVG here -->
  </svg>
</div>

`;

content = content.slice(0, idx) + newBlock + content.slice(idx);
db.prepare('UPDATE articles SET content = ? WHERE slug=?').run(content, slug);
console.log('Content inserted!');
db.close();
*/
