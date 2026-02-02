# Quick Start Guide - ResumeOS Web UI

## 🚀 Start Testing in 3 Steps

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Start the Server

```bash
python3 start_ui.py
```

You should see:
```
╔═══════════════════════════════════════════════════════════╗
║              ResumeOS Compiler - Web UI                  ║
╚═══════════════════════════════════════════════════════════╝

🌐 Web UI:    http://localhost:8000/
📚 API Docs:  http://localhost:8000/docs
```

### Step 3: Open Browser

Go to: **http://localhost:8000/**

## 🎯 Quick Test

1. Click **"Load Example Resume"** button
2. Click **"AI Engineer JD"** button  
3. Click **"Compile Resume"** button
4. View your match score and results!

## 📁 What Was Created

- `static/index.html` - Beautiful web UI
- `static/example_master_resume.json` - Example resume data
- `start_ui.py` - Easy startup script
- `output/` - Generated LaTeX files (created automatically)

## 🎨 UI Features

✅ Load example resume with one click  
✅ Load example job descriptions  
✅ Auto-detect role or manually select  
✅ Visual match score display  
✅ Skills matching analysis  
✅ Gap analysis with recommendations  
✅ Download LaTeX file  

## 📚 More Info

- **Full UI Guide**: See `UI_README.md`
- **Testing Guide**: See `TESTING_GUIDE.md`
- **API Docs**: http://localhost:8000/docs

---

**That's it! Start testing now! 🎉**
