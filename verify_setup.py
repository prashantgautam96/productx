#!/usr/bin/env python3
"""Verify API key setup"""

import os

# Load .env if exists
if os.path.exists(".env"):
    with open(".env", "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                if line.startswith("export "):
                    line = line[7:]
                key, value = line.split("=", 1)
                value = value.strip('"').strip("'")
                os.environ[key.strip()] = value

print("=" * 60)
print("API Key Setup Verification")
print("=" * 60)

# Check .env file
if os.path.exists(".env"):
    print("✅ .env file exists")
    with open(".env", "r") as f:
        content = f.read()
        if "OPENAI_API_KEY" in content:
            print("✅ OPENAI_API_KEY found in .env file")
        else:
            print("❌ OPENAI_API_KEY not found in .env file")
else:
    print("❌ .env file not found")

# Check environment variable
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    print(f"✅ OPENAI_API_KEY is set: {api_key[:20]}...")
else:
    print("❌ OPENAI_API_KEY not set in environment")

# Check OpenAI package
try:
    import openai
    print("✅ openai package installed")
except ImportError:
    print("❌ openai package not installed")
    print("   Install with: pip install openai")

# Test AI agent
if api_key:
    try:
        from ai_agent import create_ai_agent
        agent = create_ai_agent(provider="openai", api_key=api_key, enabled=True)
        if agent and agent.enabled:
            print("✅ AI Agent initialized successfully!")
            print(f"   Provider: {agent.config.provider}")
            print(f"   Model: {agent.config.model}")
        else:
            print("❌ AI Agent failed to initialize")
    except Exception as e:
        print(f"❌ AI Agent error: {e}")

print("=" * 60)
if api_key:
    print("🎉 Setup looks good! Restart your server to enable AI.")
else:
    print("⚠️  API key not set. Run: ./setup_your_key.sh")
