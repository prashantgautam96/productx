#!/bin/bash
# Setup script for ResumeOS Web UI

echo "🚀 Setting up ResumeOS Web UI..."
echo ""

# Check Python version
python3 --version

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start the server, run:"
echo "  source venv/bin/activate"
echo "  python3 start_ui.py"
echo ""
echo "Or use the convenience script:"
echo "  ./run_server.sh"
