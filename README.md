# 🧊 My Agent Skills

<div align="center">
  <img src="assets/icon.png" width="100" alt="Agent Skills Icon" />
  <p align="center">
    <strong>Efficient AI workflows created with high-end models, executed by fast ones.</strong>
  </p>
  <p align="center">
    <img src="https://img.shields.io/badge/Status-Tested%20%26%20Ready-success" alt="Status" />
    <img src="https://img.shields.io/badge/Speed-Fast-sky" alt="Speed" />
    <img src="https://img.shields.io/badge/Efficiency-High-emerald" alt="Efficiency" />
  </p>
</div>

---

## 🛠 What is this?

This is a collection of AI agent skills I've built and tested. 

The idea is simple:
1.  **I use a smart model** (like Claude Opus) to design and test the complex logic of a skill.
2.  **I save that logic** into a `SKILL.md` file.
3.  **A faster, cheaper model** (like Gemini Flash) can then follow these instructions to do the heavy lifting.

This makes the agent's work fast and cheap without losing the quality of a much smarter model.

---

## 📂 Available Skills

### 📝 [Research Article Writing](./article-writings/SKILL.md)
A skill for turning papers into well-structured articles with diagrams.
- **What it does**: Extracts text from PDFs, generates SVG diagrams, and handles LaTeX math.
- **How it works**: It follows an 8-step process I've refined to ensure everything renders correctly in dark mode and mobile.
- **⚠️ Important**: This skill specifically targets my personal website's custom renderer and database schema. It is not currently standalone.

---

## 📖 How to use

If you're using an AI agent:

1.  Show it the `SKILL.md` file you want to use.
2.  Give it the file or data you want it to work on.
3.  The agent will follow the step-by-step instructions in the skill file.

