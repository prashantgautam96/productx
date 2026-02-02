# AI Agent Integration Guide

ResumeOS now includes an AI agent for enhanced bullet rewriting, keyword extraction, and smart recommendations!

## 🚀 Features

### 1. **AI-Powered Bullet Rewriting**
- Rewrites bullets to better align with target roles
- Maintains truth boundaries (no fabrication)
- Emphasizes relevant keywords naturally
- Validates output to prevent hallucinations

### 2. **Enhanced Keyword Extraction**
- Identifies synonyms and related terms
- Finds domain-specific terminology
- Suggests missing critical skills

### 3. **Smart Recommendations**
- AI-generated actionable recommendations
- Context-aware suggestions
- Role-specific optimization tips

## 📦 Installation

### Option 1: OpenAI (Recommended)

```bash
pip install openai
export OPENAI_API_KEY="sk-your-key-here"
```

### Option 2: Anthropic Claude

```bash
pip install anthropic
export ANTHROPIC_API_KEY="sk-ant-your-key-here"
```

### Option 3: Both

```bash
pip install openai anthropic
# Set the one you want to use
export OPENAI_API_KEY="sk-your-key-here"
# OR
export ANTHROPIC_API_KEY="sk-ant-your-key-here"
```

## 🎯 Usage

### Basic Usage (Automatic)

The AI agent is automatically initialized if API keys are found:

```bash
# Set API key
export OPENAI_API_KEY="sk-your-key-here"

# Start server - AI will be enabled automatically
python3 start_ui.py
```

### Programmatic Usage

```python
from resume_compiler import ResumeCompiler
from ai_agent import create_ai_agent

# Create AI agent
ai_agent = create_ai_agent(
    provider="openai",  # or "anthropic"
    api_key="sk-your-key-here",
    enabled=True
)

# Initialize compiler with AI agent
compiler = ResumeCompiler(ai_agent=ai_agent)

# Compile resume - bullets will be AI-rewritten
tailored = compiler.compile(master_resume, job_description)
```

### Custom Configuration

```python
from ai_agent import AIAgent, AIConfig

config = AIConfig(
    provider="openai",
    model="gpt-4o-mini",  # or "gpt-4", "claude-3-haiku-20240307"
    api_key="sk-your-key-here",
    enabled=True,
    temperature=0.3,  # Lower = more consistent
    max_tokens=200
)

ai_agent = AIAgent(config)
compiler = ResumeCompiler(ai_agent=ai_agent)
```

## 🔒 Safety Features

### Truth Boundary Enforcement

The AI agent includes multiple safety mechanisms:

1. **Technology Validation**: Prevents adding technologies not in original
2. **Metric Validation**: Prevents adding numbers/metrics not in original
3. **Similarity Check**: Ensures rewrite maintains core meaning
4. **Fallback**: Automatically falls back to rule-based if AI fails

### Example Safety Check

```python
# Original: "Built REST API using Python"
# ❌ AI tries: "Built REST API using Python and increased performance by 50%"
# ✅ System detects fabricated metric and uses original

# Original: "Developed microservices with Spring Boot"
# ❌ AI tries: "Developed microservices with Spring Boot and Kubernetes"
# ✅ System detects new technology and uses original
```

## 📊 What Gets Enhanced

### With AI Enabled:
- ✅ Bullets rewritten for better role alignment
- ✅ Keywords naturally emphasized
- ✅ Professional phrasing optimized
- ✅ ATS-friendly language
- ✅ Smart recommendations

### Without AI (Fallback):
- ✅ Bullets ranked by relevance
- ✅ Original text preserved
- ✅ Rule-based recommendations
- ✅ Still fully functional

## 🎨 Example Output

### Original Bullet:
```
Built backend service using Java and Spring Boot
```

### AI-Rewritten (for AI Engineer role):
```
Developed scalable backend microservices using Java and Spring Boot, 
implementing RESTful APIs that processed high-volume requests with 
optimized performance for machine learning model inference pipelines.
```

### AI-Rewritten (for Backend Engineer role):
```
Architected and implemented production-grade backend services using 
Java and Spring Boot, designing RESTful APIs that handled millions of 
requests daily with sub-100ms latency through database optimization 
and caching strategies.
```

## ⚙️ Configuration

### Environment Variables

```bash
# OpenAI
export OPENAI_API_KEY="sk-your-key-here"

# Anthropic
export ANTHROPIC_API_KEY="sk-ant-your-key-here"

# Disable AI (use rule-based)
export RESUMEOS_AI_ENABLED="false"
```

### API Models

**OpenAI:**
- `gpt-4o-mini` (recommended, fast & cheap)
- `gpt-4o` (better quality, more expensive)
- `gpt-4-turbo` (balanced)

**Anthropic:**
- `claude-3-haiku-20240307` (fast & cheap)
- `claude-3-sonnet-20240229` (balanced)
- `claude-3-opus-20240229` (best quality)

## 💰 Cost Estimation

### OpenAI GPT-4o-mini
- ~$0.15 per 1M input tokens
- ~$0.60 per 1M output tokens
- **Estimated**: ~$0.01-0.02 per resume compilation

### Anthropic Claude Haiku
- ~$0.25 per 1M input tokens
- ~$1.25 per 1M output tokens
- **Estimated**: ~$0.02-0.03 per resume compilation

*Costs are approximate and depend on resume length and number of bullets*

## 🐛 Troubleshooting

### AI Not Working?

1. **Check API Key:**
   ```bash
   echo $OPENAI_API_KEY  # Should show your key
   ```

2. **Check Installation:**
   ```bash
   pip install openai  # or anthropic
   ```

3. **Check Logs:**
   - Server will show: `✅ AI Agent initialized with openai`
   - Or: `⚠️ AI Agent initialization failed`

4. **Fallback Mode:**
   - System automatically falls back to rule-based
   - Still fully functional without AI

### Common Issues

**"Module not found: openai"**
```bash
pip install openai
```

**"API key not found"**
```bash
export OPENAI_API_KEY="sk-your-key-here"
```

**"AI rewrite failed"**
- Check API key is valid
- Check you have API credits
- System will use rule-based fallback

## 🚀 Next Steps

1. **Get API Key:**
   - OpenAI: https://platform.openai.com/api-keys
   - Anthropic: https://console.anthropic.com/

2. **Set Environment Variable:**
   ```bash
   export OPENAI_API_KEY="sk-your-key-here"
   ```

3. **Restart Server:**
   ```bash
   python3 start_ui.py
   ```

4. **Test It:**
   - Paste your LaTeX resume
   - Add a job description
   - Compile and see AI-enhanced bullets!

## 📝 Notes

- AI is **optional** - system works without it
- AI rewrites are **validated** for truthfulness
- Falls back to **rule-based** if AI fails
- **No data storage** - API calls are stateless
- **Privacy-first** - data not used for training (OpenAI/Anthropic policies)

---

**Enjoy AI-powered resume optimization! 🚀**
