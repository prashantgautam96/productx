#!/bin/bash
# Quick setup script for your API key

# IMPORTANT: Replace with your own API key
# Get your key from: https://platform.openai.com/api-keys
API_KEY="your-api-key-here"

echo "🔑 Setting up your OpenAI API key..."
echo ""

# Create .env file
cat > .env << EOF
export OPENAI_API_KEY="$API_KEY"
EOF

echo "✅ API key saved to .env file"
echo ""

# Check if openai is installed
echo "📦 Checking for openai package..."
if python3 -c "import openai" 2>/dev/null; then
    echo "✅ openai package already installed"
else
    echo "⚠️  openai package not found. Installing..."
    echo ""
    echo "Choose installation method:"
    echo "1. Install with --break-system-packages (quick)"
    echo "2. Use virtual environment (recommended)"
    echo ""
    read -p "Enter choice (1 or 2): " choice
    
    if [ "$choice" = "1" ]; then
        python3 -m pip install --break-system-packages openai
    elif [ "$choice" = "2" ]; then
        if [ ! -d "venv" ]; then
            echo "Creating virtual environment..."
            python3 -m venv venv
        fi
        echo "Activating virtual environment..."
        source venv/bin/activate
        pip install openai
        echo ""
        echo "⚠️  Remember to activate venv before starting server:"
        echo "   source venv/bin/activate"
        echo "   python3 start_ui.py"
    else
        echo "❌ Invalid choice. Please install manually:"
        echo "   python3 -m pip install --break-system-packages openai"
    fi
fi

echo ""
echo "🧪 Testing API key..."
source .env

if [ -n "$OPENAI_API_KEY" ]; then
    echo "✅ API key loaded: ${OPENAI_API_KEY:0:15}..."
    echo ""
    echo "🚀 You're all set! Start the server with:"
    if [ -d "venv" ]; then
        echo "   source venv/bin/activate"
    fi
    echo "   python3 start_ui.py"
    echo ""
    echo "You should see: ✅ AI Agent: Enabled"
else
    echo "❌ Failed to load API key"
    exit 1
fi
