# Quick API Key Setup 🚀

## Fastest Way (3 Steps)

### Step 1: Get Your API Key

**OpenAI (Recommended):**
1. Go to: https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Copy the key (starts with `sk-`)

**OR Anthropic:**
1. Go to: https://console.anthropic.com/settings/keys
2. Click "Create Key"
3. Copy the key (starts with `sk-ant-`)

### Step 2: Run Setup Script

```bash
./setup_api_key.sh
```

Paste your key when prompted. It will be saved to `.env` file.

### Step 3: Start Server

```bash
python3 start_ui.py
```

You should see: `✅ AI Agent: Enabled`

## Alternative: Manual Setup

```bash
# Create .env file
echo 'export OPENAI_API_KEY="sk-your-key-here"' > .env

# Load it
source .env

# Start server
python3 start_ui.py
```

## Verify It Works

1. Open http://localhost:8000/
2. Check the header - should show "🤖 AI: Enabled"
3. Compile a resume - bullets should be AI-rewritten

## Need Credits?

**OpenAI:**
- Go to: https://platform.openai.com/account/billing
- Add $5-10 to start

**Anthropic:**
- Go to billing section
- Add $5-10 to start

## Cost

- **Per resume**: ~$0.01-0.02 (very cheap!)
- **$5 credit**: ~250-500 resumes
- **Free option**: Use rule-based (no API key needed)

---

**That's it! You're ready to use AI-powered resume optimization! 🎉**
