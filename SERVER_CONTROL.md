# Server Control Guide

## 🛑 Stop the Server

### Method 1: Keyboard Interrupt (Easiest)
In the terminal where the server is running:
- Press `Ctrl+C` (or `Cmd+C` on Mac)
- Wait for it to stop

### Method 2: Use Stop Script
```bash
./stop_server.sh
```

### Method 3: Manual Kill
```bash
# Find the process
ps aux | grep "uvicorn\|start_ui"

# Kill it (replace PID with actual process ID)
kill <PID>

# Or force kill
pkill -f "uvicorn.*api_example"
```

## 🚀 Start the Server

### Step 1: Set Up API Key (If Not Done)
```bash
./setup_your_key.sh
```

Or manually:
```bash
source .env  # If .env exists
```

### Step 2: Start Server
```bash
python3 start_ui.py
```

You should see:
```
🤖 AI Agent: ✅ Enabled (OpenAI)
🌐 Web UI:    http://localhost:8000/
```

## 🔄 Restart Server

### Quick Restart
```bash
# Stop
./stop_server.sh

# Start
python3 start_ui.py
```

### Or in One Command
```bash
./stop_server.sh && python3 start_ui.py
```

## ✅ Verify Server is Running

1. **Check Process:**
   ```bash
   ps aux | grep "uvicorn\|start_ui"
   ```

2. **Check Port:**
   ```bash
   lsof -i :8000
   ```

3. **Test in Browser:**
   - Open: http://localhost:8000/
   - Should see the ResumeOS UI

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Find what's using port 8000
lsof -i :8000

# Kill it
kill <PID>

# Or use different port
# Edit start_ui.py and change port=8000 to port=8001
```

### Server Won't Stop
```bash
# Force kill all Python processes (be careful!)
pkill -9 python3

# Or kill specific process
pkill -9 -f "api_example"
```

### Server Won't Start
```bash
# Check if port is free
lsof -i :8000

# Check dependencies
pip install -r requirements.txt

# Check for errors
python3 start_ui.py
```

## 📝 Quick Reference

| Action | Command |
|--------|---------|
| Stop server | `Ctrl+C` or `./stop_server.sh` |
| Start server | `python3 start_ui.py` |
| Restart server | `./stop_server.sh && python3 start_ui.py` |
| Check if running | `ps aux \| grep uvicorn` |
| Check port | `lsof -i :8000` |

---

**That's it! You're in control! 🎮**
