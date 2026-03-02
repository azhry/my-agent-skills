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
// Fetch specific language version
const res = db.prepare('SELECT content_id, content_en FROM articles WHERE slug=?').get(slug);
fs.writeFileSync('scripts/debug_id.md', res.content_id);
fs.writeFileSync('scripts/debug_en.md', res.content_en);
console.log('Dumped content to scripts/debug_*.md');
db.close();
*/

// ─── CREATE: Insert a new article ───
/*
import Database from 'better-sqlite3';
import path from 'path';

const db = new Database(path.resolve('db/content.db'));

const title_en = 'My Research Article Title';
const title_id = 'Judul Artikel Riset Saya';
const slug = 'my-research-article';
const excerpt_en = 'A brief summary of the article.';
const excerpt_id = 'Ringkasan singkat artikel.';
const tags = JSON.stringify(['nlp', 'transformer']);
const references = `...`;

const content_en = `## 1. Introduction (EN) ...`;
const content_id = `## 1. Pendahuluan (ID) ...`;

db.prepare(`
  INSERT INTO articles (
    title, slug, content,
    title_id, content_id, excerpt_id,
    title_en, content_en, excerpt_en,
    status, tags, "references"
  )
  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'published', ?, ?)
`).run(
  title_en, slug, content_en,
  title_id, content_id, excerpt_id,
  title_en, content_en, excerpt_en,
  tags, references
);

console.log('I18n Article created!');
db.close();
*/

// ─── UPDATE: Replace a specific section ───
/*
import Database from 'better-sqlite3';
import path from 'path';

const db = new Database(path.resolve('db/content.db'));
const slug = 'your-article-slug';
const field = 'content_id'; // or 'content_en'

const res = db.prepare(`SELECT ${field} as content FROM articles WHERE slug=?`).get(slug);
let content = res.content;

// Find section boundaries
const sectionStart = content.indexOf('## 3. My Section');
const sectionEnd = content.indexOf('## 4. Next Section');

if (sectionStart === -1 || sectionEnd === -1) {
  console.log('Section markers not found!');
  process.exit(1);
}

const newSection = `## 3. My Section (Updated) ...`;

content = content.slice(0, sectionStart) + newSection + content.slice(sectionEnd);
db.prepare(`UPDATE articles SET ${field} = ? WHERE slug=?`).run(content, slug);
console.log(`Section in ${field} updated!`);
db.close();
*/

// ─── INSERT: Add content before a marker ───
/*
import Database from 'better-sqlite3';
import path from 'path';

const db = new Database(path.resolve('db/content.db'));
const slug = 'your-article-slug';
const field = 'content_id';
const res = db.prepare(`SELECT ${field} as content FROM articles WHERE slug=?`).get(slug);
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
db.prepare(`UPDATE articles SET ${field} = ? WHERE slug=?`).run(content, slug);
console.log(`Content inserted into ${field}!`);
db.close();
*/
