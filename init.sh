#!/usr/bin/env bash

# Find the Python executable
PYTHON_EXEC=$(which python3)

echo $PYTHON_EXEC
# Check if Python is installed
if [ -z "$PYTHON_EXEC" ]; then
    echo "Error: Python not found. Please install Python."
    exit 1
fi


# Create virtual environment
$PYTHON_EXEC -m venv __vt_env__

# Activate virtual environment
source __vt_env__/Scripts/activate

# Install requirements
# pip install -r vt/requirements.txt

# Add virtual environment to .gitignore
echo "__vt_env__/" >> .gitignore

echo ""
echo "[VT:INFO]: Virtual environment setup completed."
