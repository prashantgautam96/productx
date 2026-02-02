#!/bin/bash
# Install OpenAI package

echo "📦 Installing OpenAI package..."
echo ""

# Method 1: Try with --break-system-packages
echo "Attempting installation with --break-system-packages..."
python3 -m pip install --break-system-packages openai 2>&1

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ OpenAI installed successfully!"
    exit 0
fi

# Method 2: Use virtual environment
echo ""
echo "⚠️  System installation failed. Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate
pip install openai

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ OpenAI installed in virtual environment!"
    echo ""
    echo "⚠️  Remember to activate venv before starting server:"
    echo "   source venv/bin/activate"
    echo "   python3 start_ui.py"
else
    echo ""
    echo "❌ Installation failed. Please install manually."
    exit 1
fi
