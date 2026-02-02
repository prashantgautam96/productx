# How to Get Your API Key

## 🚀 Quick Setup Guide

### Option 1: OpenAI (Recommended - Cheaper & Fast)

1. **Sign up/Login:**
   - Go to: https://platform.openai.com/
   - Sign up or log in

2. **Get API Key:**
   - Go to: https://platform.openai.com/api-keys
   - Click "Create new secret key"
   - Copy the key (starts with `sk-`)
   - ⚠️ **Save it immediately** - you won't see it again!

3. **Add Credits:**
   - Go to: https://platform.openai.com/account/billing
   - Add payment method
   - Add credits ($5-10 is enough to start)

4. **Set Environment Variable:**
   ```bash
   export OPENAI_API_KEY="sk-your-key-here"
   ```

### Option 2: Anthropic Claude (High Quality)

1. **Sign up/Login:**
   - Go to: https://console.anthropic.com/
   - Sign up or log in

2. **Get API Key:**
   - Go to: https://console.anthropic.com/settings/keys
   - Click "Create Key"
   - Copy the key (starts with `sk-ant-`)
   - ⚠️ **Save it immediately**!

3. **Add Credits:**
   - Go to billing section
   - Add payment method
   - Add credits ($5-10 is enough to start)

4. **Set Environment Variable:**
   ```bash
   export ANTHROPIC_API_KEY="sk-ant-your-key-here"
   ```

## 🔧 Setup Methods

### Method 1: Using Setup Script (Easiest)

```bash
chmod +x setup_api_key.sh
./setup_api_key.sh
```

This will:
- Guide you through getting a key
- Save it to `.env` file
- Set it up automatically

### Method 2: Manual Setup

**For macOS/Linux:**
```bash
# Add to ~/.zshrc or ~/.bashrc
export OPENAI_API_KEY="sk-your-key-here"

# Then reload
source ~/.zshrc  # or source ~/.bashrc
```

**For Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY="sk-your-key-here"
```

**Or create `.env` file:**
```bash
echo 'export OPENAI_API_KEY="sk-your-key-here"' > .env
source .env
```

### Method 3: Temporary (Current Session Only)

```bash
export OPENAI_API_KEY="sk-your-key-here"
python3 start_ui.py
```

## ✅ Verify Setup

Check if your key is set:
```bash
echo $OPENAI_API_KEY  # Should show your key
```

Or test with Python:
```bash
python3 -c "import os; print('✅ Key set!' if os.getenv('OPENAI_API_KEY') else '❌ Key not set')"
```

## 💰 Pricing Comparison

### OpenAI GPT-4o-mini (Recommended)
- **Cost**: ~$0.01-0.02 per resume
- **Speed**: Very fast
- **Quality**: Good for resume rewriting
- **Best for**: Most users, cost-effective

### Anthropic Claude Haiku
- **Cost**: ~$0.02-0.03 per resume
- **Speed**: Fast
- **Quality**: Excellent
- **Best for**: High-quality output

### Rule-Based (Free)
- **Cost**: Free
- **Speed**: Instant
- **Quality**: Good ranking, no rewriting
- **Best for**: Testing, no API needed

## 🔒 Security Tips

1. **Never commit API keys to git**
   - Add `.env` to `.gitignore`
   - Never share keys publicly

2. **Use environment variables**
   - Don't hardcode in files
   - Use `.env` file (not committed)

3. **Rotate keys regularly**
   - Regenerate if exposed
   - Use different keys for dev/prod

4. **Set usage limits**
   - Set monthly limits in OpenAI/Anthropic dashboard
   - Monitor usage regularly

## 🐛 Troubleshooting

### "API key not found"
```bash
# Check if set
echo $OPENAI_API_KEY

# Set it
export OPENAI_API_KEY="sk-your-key-here"
```

### "Invalid API key"
- Check key format (should start with `sk-` for OpenAI)
- Verify key is active in dashboard
- Check for extra spaces when copying

### "Insufficient credits"
- Add credits to your account
- Check billing dashboard
- Verify payment method

### "Rate limit exceeded"
- Wait a few minutes
- Upgrade to higher tier
- Use rule-based fallback

## 📝 Example Usage

Once key is set:

```bash
# Start server
python3 start_ui.py

# You should see:
# ✅ AI Agent initialized with openai
```

## 🎯 Recommendation

**For most users**: Start with OpenAI GPT-4o-mini
- Cheapest option
- Fast and reliable
- Good quality for resume rewriting
- Easy to get started

**For best quality**: Use Anthropic Claude
- Higher quality output
- Better at following constraints
- Slightly more expensive

---

**Need help? Check the setup script: `./setup_api_key.sh`**
