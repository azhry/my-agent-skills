# Step 1-2: Task Planning & Execution

## Pre-Flight Check: Tool Availability

Before starting any experiment, **confirm tool availability** with the user:

### Required Tools (Check if installed)

```
Hi! Before we begin, let me check what tools are available:

1. **Python 3.8+** with `uv` - [ ] Available / [ ] Not installed
2. **Jupyter** (ipykernel) - [ ] Available / [ ] Not installed
3. **Data science packages** - [ ] All installed / [ ] Need to install

Optional:
4. **Linear App** (for task tracking) - [ ] Connected / [ ] Not set up

Should I proceed? Let me know if any tools need to be set up first.
```

### Tool Availability Response Handling

| User Response | Action |
|---------------|--------|
| "Yes, proceed" / "All good" | Continue with task planning |
| "Install packages" | Run: `uv pip install pandas numpy scikit-learn matplotlib seaborn plotly tabulate ipykernel` |
| "No Linear" | Use **Markdown-based task tracking** (see below) |
| "Set up Linear" | Guide user through Linear MCP setup |

## Step 1: Task Planning

- Analyze source documents (PDF, TXT, etc.)
- Break down into structured tasks
- Create todos in Linear App with `"Backlog"` status using `save_issue`
- Add appropriate labels (e.g., `"lab 1"`, `"lab 2"`, `"final project"`)

### Linear App (Task Management)

Linear is used for tracking lab tasks. The agent MUST use these **Linear MCP tools** directly and provide high-quality context for every task:

| Action | MCP Tool | Example |
|--------|----------|---------|
| Create a task | `save_issue` | `save_issue(title="[EDA] Analyze Census Data", description="# Objective\nPerform full EDA to find correlations.\n# Definition of Done\n- [ ] Missing values handled\n- [ ] Plots saved", team="XYZ", labels=["lab 1"])` |
| Update task status | `save_issue` | `save_issue(id="...", state="In Progress")` |
| List tasks | `list_issues` | `list_issues(project="ML Course")` |

**CRITICAL TASK REQUIREMENTS:**
1. **Title**: Concise but descriptive (e.g., `[EDA] Analyze Feature Correlations in Census Data`).
2. **Description**: Every task MUST include:
   - **Objective**: What are we trying to achieve?
   - **Reasoning**: Why is this step necessary for the overall goal?
   - **Definition of Done (DoD)**: A checklist of exactly what must be completed for this task to be considered finished.
3. **Labels**: Always include the project/lab label (e.g., `"lab 1"`).
4. **Lifecycle**: 
   - Move to `"In Progress"` when starting.
   - Attach a comment with initial thoughts/hypotheses using `save_comment`.
   - Move to `"Done"` (or `"In Review"`) only when DoD is fully met.

### Markdown-Based Task Tracking (Alternative to Linear)

If Linear is not available, use markdown files for task tracking:

1. **Create a TODO list** in `tasks.md`:
```markdown
# Lab Tasks: [Experiment Name]

- [ ] Step 1: Load and explore data
- [ ] Step 2: Data cleaning and preprocessing
- [ ] Step 3: Build and train model
- [ ] Step 4: Evaluate results
- [ ] Step 5: Generate visualizations
```

2. **Update progress** as tasks complete:
```markdown
- [x] Step 1: Load and explore data
- [x] Step 2: Data cleaning and preprocessing
- [ ] Step 3: Build and train model
```

3. **Create separate files** for:
   - `notebook.ipynb` - Main experiment notebook
   - `results.csv` - Experiment metrics
   - `notes.md` - Observations and insights

## Step 2: Task Execution

- Move todo to `"In Progress"` using `save_issue(id="...", state="In Progress")`
- Execute one task at a time
- Use clear metrics and goals
- Break long tasks into smaller composable steps
