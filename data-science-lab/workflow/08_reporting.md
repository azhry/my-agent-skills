# Step 8: MANDATORY Report Generation

Generating a comprehensive presentation-style report using LaTeX Beamer is a **MANDATORY** final step of any analysis. The report must NOT be short or superficial. It must be highly detailed, visually appealing, and filled with deep discussions, findings, insights, and evaluations.

## Prerequisites

LaTeX compilation requires either:
- **Local installation**: TeX Live or MiKTeX
- **Docker**: Use the official TeX Live Docker image

```bash
# Pull the Docker image (one-time setup)
docker pull registry.gitlab.com/islandoftex/images/texlive:latest
```

## 🚨 CRITICAL REPORT REQUIREMENTS 🚨

Your report must be mathematically rigorous, visually beautiful, and deeply analytical. Do not output a short 4-slide presentation. A good report should have at least 15-20 frames and follow the advanced AWS-styled template.

**You MUST use the exact styling, color palette, and structural depth found in:**
`c:\Users\Lyrid\Documents\Projects\my-agent-skills\data-science-lab\examples\report_example.tex`

1. **Title Page**: Use custom colors and a professional layout. **Set the Author to the User, not the AI agent.**
2. **Introduction, Objectives & Methodology**: Clearly state what you are doing and why. **CRITICAL**: You must include a "Methodology & Agent Actions" slide detailing exactly what actions you took to process the data, your rationale behind those steps, and the analytical framework you chose.
3. **Exploratory Data Analysis (EDA)**: Do not just show plots. Dedicate one slide per major finding (Distributions, Correlations, Box Plots). Add a side-by-side analysis explaining *what the data means*, *why it looks that way*, and the decisions it led you to make.
4. **Data Preparation & Structural Reasoning**: Document missing value strategies, encoding, scaling, and feature selection. Add the *reasoning* behind why specific columns were dropped or algorithms chosen based on the EDA phase.
5. **Experiments (Per Model)**:
   - Setup & Hyperparameters tested.
   - Tabular Results (Accuracy/F1 or MSE/R2).
   - Confusion Matrices or Actual vs Predicted plots.
   - **Crucial**: "Why did this model work / fail?" slide evaluating the math behind the outcome.
6. **Model Comparison**: Side-by-side tabular comparison of all models. State the definitive winner.
7. **Discussion & Strategic Findings**: Deep analysis. What were the lessons learned? Were there unexpected patterns? What does this mean in the real world?
8. **Conclusion & Recommendations**: Actionable insights based purely on data.

## Creating the Presentation

1. Copy the contents of `examples/report_example.tex` as your starting skeleton.
2. Replace the Palmer Penguins content with the insights from your actual dataset.
3. **MANDATORY**: You must include a slide or a footer in the conclusion with the following disclaimer exactly: "Disclaimer: The insights and recommendations presented herein may contain inaccuracies. Please use these findings as preliminary guidance rather than definitive conclusions. All strategic decisions should be independently verified and consulted with domain experts."
4. Save it to `reports/report.tex`.

## Compiling the Report (MANDATORY DOCKER USAGE)

You **MUST** compile using Docker. Do not attempt to run `pdflatex` directly unless you have 100% explicitly verified it exists on the system (which is unlikely). Attempting to use `pdflatex` directly will cause your pipeline to fail.

### Step-by-Step Compilation

Ensure you are located in the directory containing `reports/report.tex`. Then run the following Docker command exactly:

```bash
powershell -Command "docker run --rm -v ${PWD}:/workdir -w /workdir/reports registry.gitlab.com/islandoftex/images/texlive:latest pdflatex -interaction=nonstopmode report.tex"
```

> [!IMPORTANT]
> **Always compile TWICE** so that the Table of Contents and Navigation symbols render correctly!

## Best Practices for Lab Reports

- **Verify Numbers**: Cross-check numbers in LaTeX tables against the actual CSV results.
- **Deep Insights**: *Never* just paste a chart. Provide a `\begin{block}` explaining the implication of the chart.
- **Color Coding**: Use the custom AWS colors defined in the template (`\hl`, `\hlb`, `\hlg`) to highlight key metrics or words.
- **Interpretations**: Include an "Evaluation" slide that interprets the R2 score / Accuracy in the context of the real world.

## 🚨 CRITICAL LATEX WARNINGS & TROUBLESHOOTING 🚨

1. **Escaping Underscores (`_`)**: One of the most common causes of compilation failure is unescaped underscores in variable or dataset names (e.g., `exp_percap`). Unless you are inside a verbatim environment or math mode, you **MUST** escape all underscores like this: `exp\_percap` or wrap them in `\texttt{exp_percap}` depending on the context. If the report fails to compile, check your variable names first.
2. **Table Overflows**: Do NOT use standard `l` or `c` columns (`\begin{tabular}{llc}`) if a column contains long sentences or paragraphs (e.g., a "Reasoning" or "Insight" column). The text will not wrap and will shoot off the edge of the slide, resulting in cut-off text.
   - **MANDATORY FIX**: Always use the paragraph column type `p{...}` for text-heavy columns to force wrapping. Example: `\begin{tabular}{ll p{0.5\textwidth}}`.
3. **Missing Images**: Ensure all `\includegraphics` paths are correct and the images actually exist in the `images/` directory before compiling.
