# GitClaude
[![CI](https://github.com/BeckettFrey/GitClaude/actions/workflows/ci.yml/badge.svg)](https://github.com/BeckettFrey/GitClaude/actions/workflows/ci.yml)

**GitClaude** is a lightweight, AI-powered Git automation tool. Built on Anthropic Claude and LangGraph, it brings intelligent assistance to your local development workflow—starting with commit message generation and expanding toward deeper code context, changelogs, etc.

> ✨ Ideal for developers who want to automate Git workflows and integrate AI into their local dev loop—starting with clean commits.

---

## 🔧 Features

- 🧠 Analyzes your Git diffs and stages
- ✍️ Generates concise commit messages like:
  ```
  feat: add user authentication system
  fix: resolve memory leak in data processor
  refactor: simplify API response handling
  ```
- 🧼 Supports `--staged`, `--all`, or custom file inputs
- ✅ Confirms the message before running `git commit`
- 🧪 Test suite with pytest

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

1. Clone this repo:
```bash
git clone https://github.com/BeckettFrey/GitClaude.git
cd GitClaude
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your API key and configuration:
```bash
cp .env.example .env
# Edit .env and add your Anthropic API key
# Optionally customize config.json for prompt styles and validation settings
```

4. Update script paths and make executable:
```bash
# Update the GIT_CLAUDE_PATH variable in scripts to match your installation directory
# Or move the scripts to your PATH for global access
chmod +x scripts/git-claude.sh
chmod +x scripts/test.sh
```

---

## 🚀 Usage

# Use staged changes only
./scripts/git-claude.sh --staged

# Stage all files and generate commit message
./scripts/git-claude.sh --all

# Add specific files before generating commit message
./scripts/git-claude.sh -e file1.py file2.js


### Running Tests

To run the test suite:
```bash
# Make the test script executable
chmod +x scripts/test.sh

# Run all tests
./scripts/test.sh --staged
``` 

### Example workflows:

**Auto-staging all changes:**
```bash
❯ ls
config.py        main.py          requirements.txt tests            venv
❯ git-claude --all
🔧 Running git add for all files
🔍 Analyzing staged changes...
-------------------- M --------------------
docs: add readme and files
-------------------------------------------
❓ Proceed with this commit message? (y/n):
```

run:
```bash
./scripts/git-claude.sh
```

---

## 📦 Dependencies

- anthropic
- langgraph
- python-dotenv
- pydantic

See requirements.txt for full dependency list, scripts automatically install them.

---

## 🔮 Roadmap

GitClaude is just getting started. Planned features include:

- 🧾 `--explain`: Natural language summary of the diff
- ✍️ `--interactive`: Edit Claude's message before committing
- 🔁 Pull request changelogs from branch history
- 📜 Configurable prompt + commit styles (JSON-based)

---

## 🤝 Contributing

Ideas, PRs, and feature requests welcome.

---

## 📄 License

MIT License