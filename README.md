# CodeLibre
[![CI](https://github.com/BeckettFrey/CodeLibre/actions/workflows/ci.yml/badge.svg)](https://github.com/BeckettFrey/CodeLibre/actions/workflows/ci.yml)

**CodeLibre** is an intelligent CLI tool that brings AI-powered automation to your Git workflow. Built with Claude and LangGraph, it analyzes your code changes and generates meaningful commit messages, helping you maintain clean Git history effortlessly.

> **Experimental**: Install in development mode and use at your own discretion.

---

## Features

- **Smart Analysis** - Analyzes Git diffs and staged changes with AI precision
- **Clean Commits** - Generates conventional commit messages:
  ```
  feat: add user authentication system
  fix: resolve memory leak in data processor  
  refactor: simplify API response handling
  docs: update README with usage examples
  ```
- **Flexible Staging** - Work with staged files, all changes, or specific files
- **Safe by Design** - Built-in validation and confirmation prompts
- **Fast & Local** - Token-efficient, no state tracking cloud infrastructure

---

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/BeckettFrey/CodeLibre.git
cd CodeLibre

# Install in development mode
pip install -e .
```

### Setup

1. **Configure your API key:**
   ```bash
   export ANTHROPIC_API_KEY=your_api_key_here
   ```

2. **Start using CodeLibre:**
   ```bash
   # Generate commit from staged changes
   codelibre --staged
   
   # Stage all files and generate commit
   codelibre --all
   
   # Add specific files and generate commit
   codelibre -e src/main.py README.md
   ```

---

## Usage Example

### Interactive Workflow
```bash
codelibre --all
-------------------------------------------
  CodeLibre - Smart Commit Generator
-------------------------------------------
Staging all files...
All files staged successfully
------------------------------
Analyzing staged changes...
Generating commit message...

Asking AI...
refactor: update app name and remove debug messages

INPUT REQUIRED 
-> Respond (or 'y' to continue, 'n' to exit): y
Continuing...

Proposed Commit Message: refactor: update app name and remove debug messages
------------------------------
What would you like to do?
  [y]es    -> Commit now
  [e]dit   -> Modify message  
  [n]o     -> Cancel

Your choice (y/e/n): y
Committing changes...
Successfully committed!
```

---

## Command Reference

| Command | Description |
|---------|-------------|
| `codelibre --staged` | Generate commit message from currently staged files |
| `codelibre --all` | Stage all changes and generate commit message |
| `codelibre -e <files...>` | Stage specific files and generate commit message |

### Options
- Interactive confirmation with edit capability
- Automatic staging and unstaging
- Color-coded output for better readability
- Graceful error handling with helpful messages

---

## Architecture

CodeLibre is built with modern Python tools:

- **Anthropic Claude** - AI-powered code analysis and message generation
- **LangGraph** - Modular workflow orchestration
- **Pydantic** - Type-safe configuration and validation
- **Rich CLI** - Beautiful terminal interface

---

## Roadmap June 2025

- **`--explain`** - Natural language summaries of code changes
- **`--interactive`** - Advanced editing mode with suggestions
- **`--changelog`** - Generate changelogs from commit history
- **Custom Templates** - Configurable commit message formats
- **GitHub Integration** - PR descriptions and release notes
- **Context Memory** - Learn from your commit patterns

---

## Contributing

We welcome contributions! Suggest changes freely.

### Development Setup
```bash
# Clone and install
git clone https://github.com/BeckettFrey/CodeLibre.git
cd CodeLibre
pip install -e .

# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest
```

### Current Status
- Core commit generation working
- Interactive CLI with confirmation
- Flexible file staging options
- Comprehensive test coverage expanding

---

## License

MIT License - see [LICENSE](LICENSE) for details.

---

*CodeLibre - Where AI meets Git (locally) and with a human in the loop.*
