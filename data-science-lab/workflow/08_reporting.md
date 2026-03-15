# Step 10: Report Generation

For presentation-style reports (like lab presentations), use LaTeX Beamer. This skill includes support for creating professional slide decks.

## Prerequisites

LaTeX compilation requires either:
- **Local installation**: TeX Live or MiKTeX
- **Docker**: Use the official TeX Live Docker image

```bash
# Pull the Docker image (one-time setup)
docker pull registry.gitlab.com/islandoftex/images/texlive:latest
```

## Creating a Beamer Presentation

Create your presentation in the `reports/` directory with `.tex` extension:

```latex
\documentclass[12pt,aspectratio=169]{beamer}

% Theme settings
\usetheme{Madrid}
\usecolortheme{whale}

% Title
\title{Your Presentation Title}
\author{Your Name}
\date{\today}

\begin{document}
\frame{\titlepage}

% Sections
\section{Introduction}
\begin{frame}{Introduction}
Your content here...
\end{frame}

\section{Results}
\begin{frame}{Results}
\begin{table}[htbp]
\centering
\caption{Your Table}
\begin{tabular}{lcc}
\toprule
Model & Accuracy & F1-Score \\
\midrule
A & 0.95 & 0.94\\
B & 0.97 & 0.96\\
\bottomrule
\end{tabular}
\end{table}
\end{frame}

\end{document}
```

## Compiling with Docker

```bash
# From your project root
docker run --rm -v "//$(pwd):/workdir" -w //workdir \
  registry.gitlab.com/islandoftex/images/texlive:latest \
  pdflatex labs/lab1/reports/main.tex
```

Or for non-stop compilation:
```bash
docker run --rm -v "//$(pwd):/workdir" -w //workdir \
  registry.gitlab.com/islandoftex/images/texlive:latest \
  pdflatex -interaction=nonstopmode main.tex
```

## Common Beamer Elements

| Element | Code | Description |
|---------|------|-------------|
| Title Slide | `\frame{\titlepage}` | Standard title |
| Section | `\section{Name}` | Navigation section |
| Block | `\begin{block}{Title}...\end{block}` | Colored box |
| Two Columns | `\begin{columns}...\end{columns}` | Split slide |
| Image | `\includegraphics[width=0.8\textwidth]{path}` | Include figure |
| Table | `\begin{table}...\end{table}` | Table with caption |
| Itemize | `\begin{itemize}...\end{itemize}` | Bullet points |
| Equation | `$...$` | LaTeX math |

## Common LaTeX Errors and Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `Undefined control sequence` | Typo in command name | Use `inserttotalframenumber` (NOT `inserttotalframerumber` - common typo!) |
| `There's no line here to end` | Empty line after `\\` | Remove empty line breaks before line endings |
| `Missing $ inserted` | Special characters in text mode | Use `\textit{}` or `\textbf{}` for italic/bold |
| `Package xcolor Error` | Missing table support | Use `\usepackage[table]{xcolor}` |
| `Extra alignment tab` | Too many columns in table | Add more `&` to match column count |

## Best Practices for Lab Reports

- **Verify CSV values match report**: Always cross-check numbers in LaTeX tables against the actual CSV results
- **Use consistent decimal places**: Round to 2-4 decimal places for readability
- **Include all experiment variants**: Document baseline, regularized (Ridge/Lasso), scaled, and feature selection experiments
- **Add visualization captions**: Every plot should have a descriptive caption
- **Use professional themes**: `Madrid` + `whale` or `Berlin` + `whale` work well for presentations

## Report Structure Template

See the complete example template at: `examples/report_example.tex`

### Quick Checklist for Good Reports

| Item | Description |
|------|-------------|
| [ ] Title slide | Author, course, date clearly shown |
| [ ] Outline | Table of contents with sections |
| [ ] EDA section | At least 2-3 slides with visualizations |
| [ ] Data prep | Document all preprocessing steps |
| [ ] Model sections | Each model: setup + results + analysis |
| [ ] Comparison | Side-by-side model comparison |
| [ ] Discussion | Insights and lessons learned |
| [ ] Conclusion | Summary and recommendations |
| [ ] Tables | Have captions, consistent formatting |
| [ ] Images | Have descriptive captions |
| [ ] Consistency | Same style throughout |
