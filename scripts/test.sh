#!/bin/bash

# GitClaude test runner
# Works locally and in GitHub Actions

set -e
python -m ensurepip --upgrade
python -m pip install --upgrade "pip==25.1.1"
echo "🔍 Checking environment..."

# Only try to activate virtualenv if it exists
if [[ -d ".venv" && -f ".venv/bin/activate" ]]; then
    echo "✅ Activating local virtual environment"
    source .venv/bin/activate
else
    echo "⚠️  No local virtual environment detected — assuming system Python"
fi

# Ensure pip is up-to-date
echo "⬆️  Updating pip (if needed)..."
python -m pip install --upgrade pip

# Install required packages
echo "📦 Installing test dependencies..."
pip install -r requirements.txt || {
    echo "❌ Failed to install from requirements.txt. Falling back to manual install."
    pip install pytest pytest-mock pydantic anthropic langgraph python-dotenv
}

# Make sure test packages are visible
export PYTHONPATH="$PYTHONPATH:$(pwd)"
echo "🔧 PYTHONPATH set to: $PYTHONPATH"

# Sanity check dirs
echo "📁 Verifying structure..."
for dir in graph utils tests; do
    if [[ ! -d "$dir" ]]; then
        echo "❌ Missing required directory: $dir"
        exit 1
    fi
    touch "$dir/__init__.py"
done

# Run tests
echo "🧪 Running pytest..."
pytest tests/ -v

echo "✅ All tests passed"
