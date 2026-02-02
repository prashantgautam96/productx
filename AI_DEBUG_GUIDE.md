# AI Debug Guide - Why AI Suggestions Are None

## 🔍 Debugging Steps

### 1. **Check Server Console Output**

When you compile, you should see:
```
[API DEBUG] Request enable_ai: True
[API DEBUG] Original AI agent: <ai_agent.AIAgent object>
[API DEBUG] AI agent enabled: True
[API DEBUG] OPENAI_API_KEY present: True
[AI DEBUG] AI agent enabled, calling _get_ai_suggested_skills...
[_get_ai_suggested_skills] Called with ai_agent=..., enabled=True
[_get_ai_suggested_skills] Calling AI with prompt length: ...
[_get_ai_suggested_skills] AI response received, length: ...
[_get_ai_suggested_skills] AI suggested 5 skills: [...]
```

### 2. **Check API Key**

Verify your `.env` file has:
```
OPENAI_API_KEY=sk-...
```

Or check environment:
```bash
echo $OPENAI_API_KEY
```

### 3. **Check AI Agent Initialization**

At server startup, you should see:
```
✅ AI Agent initialized with openai
```

If you see:
```
⚠️  AI Agent initialization failed: ...
```

Then the API key might be invalid or the package isn't installed.

### 4. **Common Issues**

#### Issue 1: API Key Not Loaded
**Symptom**: `[API DEBUG] OPENAI_API_KEY present: False`
**Fix**: 
- Check `.env` file exists
- Check `.env` has `OPENAI_API_KEY=sk-...`
- Restart server after adding key

#### Issue 2: AI Agent Not Initialized
**Symptom**: `[API DEBUG] Original AI agent: None`
**Fix**:
- Check API key is valid
- Check `openai` package is installed: `pip install openai`
- Check server startup logs

#### Issue 3: AI Call Failing
**Symptom**: `[_get_ai_suggested_skills] AI skill suggestion failed with exception: ...`
**Fix**:
- Check API key is valid and has credits
- Check network connection
- Check OpenAI API status

#### Issue 4: JSON Parsing Error
**Symptom**: `[_get_ai_suggested_skills] AI skill suggestion parsing failed: ...`
**Fix**:
- AI might be returning non-JSON response
- Check the raw response in logs
- The prompt might need adjustment

## 🚀 Quick Fixes

### Fix 1: Re-initialize AI Agent
The code now tries to re-initialize the AI agent if it's None but `enable_ai=True`.

### Fix 2: Check Enable AI Toggle
Make sure the "Enable AI Enhancement" checkbox is checked in the UI.

### Fix 3: Verify API Key
```bash
# Check if key is loaded
python3 -c "import os; from dotenv import load_dotenv; load_dotenv(); print('Key:', os.getenv('OPENAI_API_KEY')[:10] if os.getenv('OPENAI_API_KEY') else 'None')"
```

## 📊 Expected Console Output

### When AI Works:
```
[API DEBUG] Request enable_ai: True
[API DEBUG] Original AI agent: <ai_agent.AIAgent object at 0x...>
[API DEBUG] AI agent enabled: True
[AI DEBUG] AI agent enabled, calling _get_ai_suggested_skills...
[_get_ai_suggested_skills] Called with ai_agent=..., enabled=True
[_get_ai_suggested_skills] Calling AI with prompt length: 1234
[_get_ai_suggested_skills] AI response received, length: 234
[_get_ai_suggested_skills] Parsed successfully, type: <class 'list'>, value: ['MLOps', 'Model Serving', ...]
[_get_ai_suggested_skills] Filtered to 5 new skills: ['MLOps', 'Model Serving', ...]
[AI DEBUG] AI suggested 5 skills: ['MLOps', 'Model Serving', ...]
```

### When AI Doesn't Work:
```
[API DEBUG] Request enable_ai: True
[API DEBUG] Original AI agent: None
[API DEBUG] AI agent enabled: False
[API DEBUG] OPENAI_API_KEY present: False
[API DEBUG] AI requested but agent is None, attempting to initialize...
[API DEBUG] ⚠️  AI Agent initialization failed: ...
```

---

**Check your server console to see which scenario you're in!**
