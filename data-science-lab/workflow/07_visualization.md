# Step 9: Visualizations

## Standard Plots

Use the helper scripts to generate plots:

```python
import sys
sys.path.insert(0, '/path/to/data-science-lab/scripts')

from visualize import plot_confusion_matrix, plot_metric_comparison, plot_parameter_sweep, save_all_plots

# Quick: save all standard plots at once
save_all_plots(results_df, results_dir='images', metric='accuracy')

# Or generate individual plots:
plot_metric_comparison(results_df, 'accuracy', save_path='images/model_comparison.png')
plot_parameter_sweep(results_df, 'alpha', 'accuracy', hue='model', save_path='images/param_sweep.png')
plot_confusion_matrix(cm, labels=['Class A', 'Class B'], save_path='images/confusion_matrix.png')
```

### Additional Plot Functions

```python
from visualize import plot_feature_importance, plot_learning_curve, plot_regression_results

# Feature importance (for tree-based models)
plot_feature_importance(feature_names, model.feature_importances_, save_path='images/fi.png')

# Learning curve
plot_learning_curve(train_sizes, train_scores, test_scores, save_path='images/learning.png')

# Regression: actual vs predicted
plot_regression_results(y_test, y_pred, save_path='images/actual_vs_predicted.png')
```

### NLP Visualization

```python
from visualize import plot_topic_distribution, plot_word_frequencies

# Topic distribution bar chart
plot_topic_distribution(topic_counts_df, save_path='images/topics.png')

# Top word frequencies
plot_word_frequencies(keywords_list, save_path='images/keywords.png')
```

## Infographics

## Custom Infographics (Not Hard-Coded!)

For publication-quality, strategic infographics, **DO NOT rely on hardcoded static templates**. You MUST dynamically design a bespoke HTML/TailwindCSS layout that perfectly fits the narrative, metrics, and evidence of your specific research.

### Step-by-Step Custom Infographic Generation

1. **Strategic Narrative First**: Identify your #1 Strategic Recommendation.
2. **Visual Evidence**: Create a specific, custom plot (e.g., `sns.barplot`) that visually proves your point and save it to `images/strategic_evidence.png`.
3. **Design the Custom HTML**: 
   - Write a custom HTML string using TailwindCSS framing it in a professional, modern structure.
   - Use the examples in `data-science-lab/examples/` (e.g., `infographics_example_1.html`, `infographics_example_2.html`, `infographics_example_3.html`, `infographics_example_4.html`) for inspiration on high-end, professional, data-rich layouts (dark modes, gradients, grid layouts).
   - Base the colors, headers, structure, and text around your exact findings.
   - Embed your visual evidence plots directly into the HTML using the `image_to_base64` helper.
5. **Export**: Use `export_infographic` to render your custom HTML into a high-res `.png` file.

> [!WARNING]
> **Infographic Layout & Color Traps (CRITICAL)**:
> 1. **Viewport Cutoffs**: Playwright renders a fixed 1920x1080 viewport. You MUST strictly control the bounding boxes.
>    - Set the body strictly: `<body style="overflow: hidden; height: 1080px; width: 1920px; box-sizing: border-box;">`
>    - Use exact container heights (e.g., `<main class="h-[1016px] flex flex-col justify-between">`) and tight paddings (e.g., `p-6` or `p-8` max) so the footer/bottom is NEVER cut off.
> 2. **Professional Aesthetics**: Do NOT use harsh colors (like `#cc0000`, pure red, or `#000000` pure black). Use modern, soft pastel palettes (e.g., Tailwind's `slate-800`, `blue-500`, soft corals like `#e05a5a`).
> 3. **Business Charts over Technical Plots**: Raw `matplotlib` or `seaborn` plots can look bulky and technical. Whenever possible, represent top-level metrics (like Feature Importances) using native HTML/Tailwind CSS progress bars. Only embed base64 plots if they are absolutely necessary and impossible to build natively in CSS.
> 4. **SVG for Precision & Sharpness**: 
>    - **Icons & Illustrations**: Always use inline SVGs for icons, arrows, and decorative elements to ensure they stay perfectly sharp at 1080p.
>    - **Strategic SVG Charts**: For high-impact visualizations that Tailwind cannot handle alone, build custom SVG charts. They are lighter and sharper than PNGs.
>    - **Python Plots as SVG**: If you MUST include a complex Python plot, save it as an SVG string and inline it into the HTML instead of using base64 PNGs. This prevents "blurry" charts and allows the browser to render text elements cleanly.

```python
from create_infographics import export_infographic, image_to_base64

# 1. Embed your specific EDA plots as base64
plot_1_b64 = image_to_base64('images/strategic_evidence.png')

# 2. DESIGN A BRAND NEW, HYPER-DENSE HTML LAYOUT FROM SCRATCH
# DO NOT just use BeautifulSoup to plug values into a template.
# Read `examples/*.html` for INSPIRATION on TailwindCSS aesthetics (colors, grids, glassmorphism).
# Then, write your OWN completely bespoke HTML string below.
html_content = f"""
<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>body {{ background: #0f172a; color: white; font-family: sans-serif; }}</style>
</head>
<body class="p-12 min-h-screen">
    <h1 class="text-6xl font-black mb-8">MY RESEARCH TITLE</h1>
    
    <!-- YOU MUST BUILD A COMPLEX GRID HERE. DO NOT MAKE IT SIMPLE. -->
    <!-- It MUST include: 
         1. <img src="{plot_1_b64}"> (Visual Evidence)
         2. Empirical Results (Your text/numbers)
         3. Key Insights (Your text)
         4. Strategic Recommendations (Your text) 
    -->
    
</body>
</html>
"""

# 3. Export to high-res PNG
export_infographic(html_content, 'images/custom_strategic_infographic.png')
```

### 🚨 Infographic Best Practices (CRITICAL)

1. **CONTENT DENSITY IS MANDATORY**: You MUST include the following specific sections in whatever HTML design you invent:
   - **Visual Evidence Matrix**: At least 2 custom plots (from `image_to_base64`).
   - **Empirical Results**: A list of 3-4 actual hard numbers from your data.
   - **Key Insights**: A list of what the data actually means.
   - **Strategic Recommendations**: Policy/Busines action items.
   - *If your layout is too simple and omits this complex coherence, you have failed the task.*
2. **Never Make Ugly/Basic Layouts**: The infographic MUST look professional, modern, and visually appealing (like your examples in `examples/`). Use proper layout structures, cohesive color themes, and appropriate spacing.
3. **Strategic Plot Coherence**: The embedded images must visually support the strategy, not just dump random heatmaps. 
4. **Business Strategy**: Focus on real-world impact. Bridge the gap: "Because [Data Point], we must [Action]."
5. **PNG Output**: You MUST verify the existence of the `.png` file. Use the **Playwright Fallback** tool below if needed.

### 🛠️ Playwright Fallback (Manual Image Capture)

If `export_infographic` fails to generate a PNG because Playwright is not installed or configured:

1. The script will save the output as an `.html` file (e.g., `images/strategic_infographic.html`).
2. **MANDATORY**: You MUST then use the `browser_subagent` tool to capture the screenshot:
   - **Task Name**: "Capture Infographic Screenshot"
   - **Task**: "Open the local file `file:///C:/path/to/your/images/strategic_infographic.html`. Set the viewport to 1920x1080. Wait 2 seconds for animations to finish. Take a screenshot and save it as `images/strategic_infographic.png`. Return once the file is saved."
3. Verify that the `.png` file exists.



