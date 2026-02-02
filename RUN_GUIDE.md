# 🚀 How to Run ResumeOS

## Quick Start (3 Steps)

### Step 1: Activate Virtual Environment

```bash
# If you have a virtual environment
source venv/bin/activate

# If you don't have one, create it first:
python3 -m venv venv
source venv/bin/activate
```

### Step 2: Install Dependencies (if not already installed)

```bash
pip install -r requirements.txt
```

### Step 3: Start the Server

**Option A: Using the start script (Recommended)**
```bash
python3 start_ui.py
```

**Option B: Using the shell script**
```bash
./run_server.sh
```

**Option C: Direct uvicorn command**
```bash
uvicorn api_example:app --host 0.0.0.0 --port 8000 --reload
```

## ✅ What You Should See

When the server starts, you'll see:

```
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║              ResumeOS Compiler - Web UI                  ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝

🚀 Starting server...
🤖 AI Agent: ✅ Enabled (OpenAI) or ❌ Disabled (Rule-based)

🌐 Web UI:    http://localhost:8000/
📚 API Docs:  http://localhost:8000/docs
📖 ReDoc:     http://localhost:8000/redoc

Press Ctrl+C to stop the server.
```

## 🌐 Access the Application

1. **Web UI**: Open your browser and go to:
   ```
   http://localhost:8000/
   ```

2. **API Documentation**: 
   ```
   http://localhost:8000/docs
   ```

3. **Alternative API Docs**:
   ```
   http://localhost:8000/redoc
   ```

## 🎯 First Time Usage

1. **Open the Web UI** at http://localhost:8000/

2. **Load Example Data**:
   - Click "Load Example LaTeX Resume" button
   - Click "AI Engineer JD" (or any example JD)

3. **Compile Resume**:
   - Click "Compile Resume" button
   - Wait for compilation (loading spinner)
   - View your results!

## ⚙️ Configuration (Optional)

### Enable AI Features

If you want AI enhancements, set up your API key:

```bash
# Option 1: Use setup script
./setup_api_key.sh

# Option 2: Create .env file manually
echo "OPENAI_API_KEY=your-key-here" > .env
# OR
echo "ANTHROPIC_API_KEY=your-key-here" > .env
```

**Note**: AI features work without API key (uses rule-based fallback)

### Environment Variables

You can configure the server using environment variables:

```bash
# In .env file or export before running
export API_HOST=0.0.0.0
export API_PORT=8000
export LOG_LEVEL=INFO
export AI_ENABLED=true
```

## 🛑 Stop the Server

Press `Ctrl+C` in the terminal where the server is running.

## 🔧 Troubleshooting

### Port Already in Use

If port 8000 is already in use:

```bash
# Option 1: Kill the process using port 8000
lsof -ti:8000 | xargs kill -9

# Option 2: Use a different port
uvicorn api_example:app --port 8001
```

### Module Not Found Errors

```bash
# Make sure you're in the project directory
cd /Users/prashantgautam/Downloads/files

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Static Files Not Loading

Make sure the `static` directory exists with:
- `static/index.html`
- `static/css/styles.css`
- `static/js/app.js`

If missing, they should be created automatically, but you can verify:

```bash
ls -la static/
```

### CSS/JS Not Loading

1. Check browser console for 404 errors
2. Verify files exist in `static/css/` and `static/js/`
3. Clear browser cache (Cmd+Shift+R on Mac, Ctrl+Shift+R on Windows)

## 📁 Project Structure

```
files/
├── api_example.py          # FastAPI server
├── start_ui.py             # Startup script
├── resume_compiler.py      # Core compiler
├── latex_parser.py         # LaTeX parser
├── latex_renderer.py       # LaTeX renderer
├── ai_agent.py             # AI integration
├── services.py             # Service layer
├── config.py               # Configuration
├── exceptions.py           # Custom exceptions
├── static/
│   ├── index.html          # Web UI
│   ├── css/
│   │   └── styles.css      # Styles
│   └── js/
│       └── app.js          # JavaScript
├── output/                 # Generated files
└── requirements.txt        # Dependencies
```

## 🎉 You're Ready!

Once the server is running, open http://localhost:8000/ in your browser and start using ResumeOS!

---

**Need Help?**
- Check `QUICK_START.md` for more details
- See `UI_README.md` for UI usage
- Check `SYSTEM_DESIGN.md` for architecture info
