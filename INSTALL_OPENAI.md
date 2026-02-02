# Install OpenAI Package

## Quick Install (Choose One Method)

### Method 1: System-wide Install (Quick)

```bash
python3 -m pip install --break-system-packages openai
```

### Method 2: Use Install Script

```bash
./install_openai.sh
```

### Method 3: Virtual Environment (Recommended)

```bash
# Create venv (if not exists)
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install
pip install openai

# Then start server
python3 start_ui.py
```

## Verify Installation

```bash
python3 -c "import openai; print('✅ OpenAI installed!')"
```

## After Installation

1. **Set up API key:**
   ```bash
   ./setup_your_key.sh
   ```

2. **Start server:**
   ```bash
   # If using venv:
   source venv/bin/activate
   
   python3 start_ui.py
   ```

## Troubleshooting

**"command not found: pip"**
- Use: `python3 -m pip` instead of `pip`

**"externally-managed-environment"**
- Use: `--break-system-packages` flag
- Or: Use virtual environment (recommended)

**"ModuleNotFoundError: openai"**
- Make sure you activated venv if using one
- Or install with `--break-system-packages`

---

**Run `./install_openai.sh` for automatic installation!**
