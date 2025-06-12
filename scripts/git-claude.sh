#!/bin/bash
GIT_CLAUDE_PATH="/Users/beckettfrey/Desktop/code/projects/GitClaude"
FRESH=false

# Create the virtual environment if it doesn't exist
if [ ! -d "$GIT_CLAUDE_PATH/venv" ]; then
    FRESH=true
    echo "🔧 Creating virtual environment at $GIT_CLAUDE_PATH/venv"
    python3 -m venv $GIT_CLAUDE_PATH/venv
fi

# Activate the virtual environment
source $GIT_CLAUDE_PATH/venv/bin/activate
if [ $? -ne 0 ]; then
    echo "❌ Error: Could not activate virtual environment"
    exit 1
fi

# install dependencies
if [ "$FRESH" = true ]; then
    echo "🔧 Installing dependencies"
    pip install -r $GIT_CLAUDE_PATH/requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Error: Failed to install dependencies"
        exit 1
    fi
fi

# Handle CLI arguments
if [ "$1" == "-c" ]; then
    python $GIT_CLAUDE_PATH/main.py
else
    echo "Usage: ./scripts/git-claude.sh -c"
    echo "  -c   Run commit generation"
fi
