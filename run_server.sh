#!/bin/bash
# Convenience script to start the ResumeOS server

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Running setup..."
    ./setup.sh
fi

# Activate venv and start server
source venv/bin/activate
python3 start_ui.py
