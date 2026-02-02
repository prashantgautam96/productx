# ✅ API Key Setup Instructions

Your API key has been provided! Here's how to set it up:

## Quick Setup (Choose One Method)

### Method 1: Run Setup Script (Easiest)

```bash
./setup_your_key.sh
```

This will:
- Save your API key to `.env` file
- Test that it's loaded correctly
- Show you how to start the server

### Method 2: Manual Setup

**Create `.env` file:**
```bash
echo 'export OPENAI_API_KEY="your-api-key-here"' > .env
```

**Load it:**
```bash
source .env
```

**Verify:**
```bash
echo $OPENAI_API_KEY  # Should show your key
```

### Method 3: Add to Shell Profile (Permanent)

**For macOS/Linux (zsh):**
```bash
echo 'export OPENAI_API_KEY="your-api-key-here"' >> ~/.zshrc
source ~/.zshrc
```

## Start the Server

Once the key is set:

```bash
python3 start_ui.py
```

You should see:
```
🤖 AI Agent: ✅ Enabled (OpenAI)
```

## Test It Works

1. Open http://localhost:8000/
2. Check header - should show "🤖 AI: Enabled"
3. Paste your LaTeX resume
4. Add a job description
5. Click "Compile Resume"
6. Bullets should be AI-rewritten!

## Security Reminders

⚠️ **Important:**
- Your `.env` file is in `.gitignore` (won't be committed)
- Never share your API key publicly
- If key is exposed, regenerate it at https://platform.openai.com/api-keys
- Monitor usage at https://platform.openai.com/usage

## Troubleshooting

**"API key not found"**
- Make sure `.env` file exists
- Run `source .env` to load it
- Or add to your shell profile

**"AI Agent failed"**
- Check key is valid: https://platform.openai.com/api-keys
- Make sure you have credits: https://platform.openai.com/account/billing
- Install OpenAI: `pip install openai`

**"Module not found: openai"**
```bash
pip install openai
```

---

**Your API key is ready! Run `./setup_your_key.sh` to get started! 🚀**
