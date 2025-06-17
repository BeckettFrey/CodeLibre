# GitClaude
[![CI](https://github.com/BeckettFrey/GitClaude/actions/workflows/ci.yml/badge.svg)](https://github.com/BeckettFrey/GitClaude/actions/workflows/ci.yml)

**GitClaude** is an experimental AI-powered Git automation tool. Built on Anthropic Claude and LangGraph, it brings intelligent assistance to your local development workflow—starting with commit message generation and expanding toward deeper code context, changelogs, etc.

> ⚠️ **Early Development**: This project is in active development. Use at your own risk and install in editable mode.

> ✨ Ideal for developers who want to automate Git workflows and integrate AI into their local dev loop—starting with clean commits.

---
## 🔧 Features

- 🧠 Analyzes your Git diffs and stages
- ✅ Generates concise commit messages like:
  ```
  feat: add user authentication system
  fix: resolve memory leak in data processor
  refactor: simplify API response handling
  docs: update README with usage examples
  ```
- ...

---

## 💡 Why GitClaude?

GitClaude gives you **Claude-powered Git automation** in a local-first, developer-friendly package.

> ⚡ It's a lightweight, open alternative to Anthropic's **CODE CLI**.

- 💸 Designed for **token-efficient local use** — lower cost than CODE CLI
- ✅ No cloud infra or backend setup required
- 🧩 Easily extendable: add RAG, custom prompts, or GitHub integration
- 🧠 Built on Claude + LangGraph = modular, powerful, cheap
- 🔒 Built-in validation safety to prevent malicious commits

---

## ⚙️ Setup

### Installation (Development Mode)

⚠️ **Important**: GitClaude is in early development. Install in editable mode for testing:

```bash
# Clone the repository
git clone https://github.com/BeckettFrey/GitClaude.git
cd GitClaude

# Install in editable development mode
pip install -e .
```

### Configuration

1. Set up your API key:
```bash
# Create a .env file in your working directory or set environment variable
export ANTHROPIC_API_KEY=your_api_key_here
```

2. Optional: Customize configuration by adjusting the `src/config.json` for prompt styles and validation settings.

---

## 🚀 Usage

⚠️ **Note**: Basic commit message generation is working. Other features are experimental.

After installation, use the `git-claude` command from anywhere:

```bash
# Use staged changes only (EXPERIMENTAL)
git-claude --staged

# Stage all files and generate commit message (EXPERIMENTAL)
git-claude --all

# Add specific files before generating commit message (EXPERIMENTAL)
git-claude -e file1.py file2.js
```

### Example workflows:

**Auto-staging all changes:**
```bash
❯ git-claude --all
🔧 Running git add for all files
🔍 Analyzing staged changes...
-------------------- M --------------------
docs: add readme and files
-------------------------------------------
❓ Proceed with this commit message? (y/n):
```

**Using only staged changes:**
```bash
❯ git add src/main.py
❯ git-claude --staged
🔍 Analyzing staged changes...
-------------------- M --------------------
feat: implement core functionality in main module
-------------------------------------------
❓ Proceed with this commit message? (y/n):
```

---

## 📦 Dependencies

GitClaude is built with:
- anthropic
- langgraph
- python-dotenv
- pydantic

All dependencies are automatically installed when you install via pip.

---

## 🔮 Roadmap

GitClaude is just getting started. Planned features include:

- 🧾 `--explain`: Natural language summary of the diff
- ✍️ `--interactive`: Edit Claude's message before committing
- 🔁 Pull request changelogs from branch history
- 📜 Configurable prompt + commit styles (JSON-based)
- ...

---

## 🤝 Contributing

Ideas, PRs, and feature requests welcome! This project is in early development.

**Current Status**: Core commit message generation is functional, but many features are still being developed and layered tests are continually being added as my knowledge of best practices expands.

For development:

```bash
# Clone the repository
git clone https://github.com/BeckettFrey/GitClaude.git
cd GitClaude

# Install in editable development mode
pip install -e .

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest
```

---

## 📄 License

MIT License