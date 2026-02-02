#!/bin/bash
# Stop ResumeOS server

echo "🛑 Stopping ResumeOS server..."

# Find and kill uvicorn processes
pkill -f "uvicorn.*api_example"
pkill -f "start_ui.py"

# Wait a moment
sleep 1

# Check if still running
if pgrep -f "api_example" > /dev/null; then
    echo "⚠️  Some processes still running. Force killing..."
    pkill -9 -f "uvicorn.*api_example"
    pkill -9 -f "start_ui.py"
fi

echo "✅ Server stopped"
