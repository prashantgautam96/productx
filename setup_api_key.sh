#!/bin/bash
# Setup script for API keys

echo "🔑 ResumeOS API Key Setup"
echo "========================="
echo ""

# Check if .env file exists
if [ -f ".env" ]; then
    echo "📄 Found existing .env file"
    source .env
fi

# Function to set OpenAI key
setup_openai() {
    echo ""
    echo "Setting up OpenAI API Key..."
    echo "Get your key from: https://platform.openai.com/api-keys"
    echo ""
    read -p "Enter your OpenAI API key (starts with sk-): " api_key
    
    if [[ $api_key == sk-* ]]; then
        echo "export OPENAI_API_KEY=\"$api_key\"" >> .env
        export OPENAI_API_KEY="$api_key"
        echo "✅ OpenAI API key saved to .env file"
        return 0
    else
        echo "❌ Invalid API key format (should start with sk-)"
        return 1
    fi
}

# Function to set Anthropic key
setup_anthropic() {
    echo ""
    echo "Setting up Anthropic API Key..."
    echo "Get your key from: https://console.anthropic.com/"
    echo ""
    read -p "Enter your Anthropic API key (starts with sk-ant-): " api_key
    
    if [[ $api_key == sk-ant-* ]]; then
        echo "export ANTHROPIC_API_KEY=\"$api_key\"" >> .env
        export ANTHROPIC_API_KEY="$api_key"
        echo "✅ Anthropic API key saved to .env file"
        return 0
    else
        echo "❌ Invalid API key format (should start with sk-ant-)"
        return 1
    fi
}

# Main menu
echo "Which AI provider would you like to use?"
echo "1. OpenAI (GPT-4) - Recommended, cheaper"
echo "2. Anthropic (Claude) - High quality"
echo "3. Skip (use rule-based only)"
echo ""
read -p "Enter choice (1-3): " choice

case $choice in
    1)
        setup_openai
        ;;
    2)
        setup_anthropic
        ;;
    3)
        echo "ℹ️  Skipping AI setup. System will use rule-based rewriting."
        ;;
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "✅ Setup complete!"
echo ""
echo "To use the API key, run:"
echo "  source .env"
echo "  python3 start_ui.py"
echo ""
echo "Or add to your shell profile (~/.zshrc or ~/.bashrc):"
echo "  source $(pwd)/.env"
