# File: scripts/test.sh
#!/bin/bash

# Script to run pytest tests for GitClaude project

# Exit on any error
set -e
# Project directory
GIT_CLAUDE_PATH="."

# Check if project directory exists
if [ ! -d "$GIT_CLAUDE_PATH" ]; then
    echo "Error: Project directory $GIT_CLAUDE_PATH not found!"
    exit 1
fi

cd "$GIT_CLAUDE_PATH" || {
    echo "Error: Could not change to $GIT_CLAUDE_PATH"
    exit 1
}

# Activate virtual environment
VENV_DIR="$GIT_CLAUDE_PATH/.venv"
if [ ! -d "$VENV_DIR" ]; then
    echo "Error: Virtual environment not found at $VENV_DIR"
    echo "Please create it with: python -m venv .venv"
    exit 1
fi

source "$VENV_DIR/bin/activate" || {
    echo "Error: Could not activate virtual environment"
    exit 1
}
echo "Virtual environment activated"

# Update pip to 25.1.1
echo "Checking pip version..."
pip_version=$(pip --version | grep -o 'pip [0-9.]*' | cut -d' ' -f2)
if [[ "$pip_version" != "25.1.1" ]]; then
    echo "Updating pip from $pip_version to 25.1.1..."
    python -m pip install --upgrade pip==25.1.1 || {
        echo "Error: Failed to update pip. Trying to force reinstall..."
        curl https://bootstrap.pypa.io/get-pip.py -o get_pip.py
        python get_pip.py
        rm -f get_pip.py
    }
fi
pip --version

# Install dependencies
echo "Installing dependencies..."
pip install pytest pytest-mock pydantic anthropic langgraph python-dotenv || {
    echo "Error: Failed to install dependencies"
    exit 1
}

# Create __init__.py files to make graph and utils Python packages
echo "Ensuring __init__.py files exist..."
touch graph/__init__.py
touch utils/__init__.py

# Verify directory structure
echo "Verifying directory structure..."
EXPECTED_DIRS=("graph" "utils" "tests")
for dir in "${EXPECTED_DIRS[@]}"; do
    if [ ! -d "$dir" ]; then
        echo "Error: Directory $dir not found!"
        exit 1
    fi
done

# Set PYTHONPATH
export PYTHONPATH="$PYTHONPATH:$GIT_CLAUDE_PATH"
echo "PYTHONPATH set to include $GIT_CLAUDE_PATH"

# Run pytest
echo "Running tests..."
pytest tests/ -v || {
    echo "Error: Tests failed"
    exit 1
}

echo "Tests completed successfully"
deactivate