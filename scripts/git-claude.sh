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
if [ "$1" == "--staged" ]; then
    python $GIT_CLAUDE_PATH/main.py

elif [ "$1" == "-e" ]; then
    echo "🔧 Running git add for specified files"
    git add "${@:2}"
    python $GIT_CLAUDE_PATH/main.py

elif [ "$1" == "--all" ]; then
    echo "🔧 Running git add for all files"
    git add .
    python $GIT_CLAUDE_PATH/main.py

else
    echo ""
    echo "Usage: git-claude.sh [option]"
    echo ""
    echo "  --staged    Generate message from staged changes"
    echo "  --all       Stage all files and generate message"
    echo "  -e <files>  Add specified files before generating message"
    echo ""
fi

