#!/usr/bin/env python3
"""Test API key setup"""

import os
import sys

# Load .env if exists
if os.path.exists(".env"):
    with open(".env", "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                value = value.strip('"').strip("'")
                os.environ[key.strip().replace("export ", "")] = value

# Check API key
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("❌ API key not found in environment")
    print("Make sure .env file exists and contains: export OPENAI_API_KEY=\"sk-...\"")
    sys.exit(1)

print(f"✅ API key found: {api_key[:15]}...")

# Test AI agent
try:
    from ai_agent import create_ai_agent
    
    print("🤖 Initializing AI agent...")
    agent = create_ai_agent(provider="openai", api_key=api_key, enabled=True)
    
    if agent and agent.enabled:
        print("✅ AI Agent initialized successfully!")
        print(f"   Provider: {agent.config.provider}")
        print(f"   Model: {agent.config.model}")
        print("\n🎉 Your API key is working! You can now use AI-powered features.")
    else:
        print("❌ AI Agent failed to initialize")
        sys.exit(1)
        
except ImportError as e:
    print(f"❌ Missing dependency: {e}")
    print("Install with: pip install openai")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    print("\nPossible issues:")
    print("1. API key might be invalid")
    print("2. OpenAI package not installed: pip install openai")
    print("3. No internet connection")
    sys.exit(1)
