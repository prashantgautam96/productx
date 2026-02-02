#!/usr/bin/env python3
"""
Start the ResumeOS Web UI Server
"""

import uvicorn
import sys
import os

# Load .env file if it exists
if os.path.exists(".env"):
    print("📄 Loading environment variables from .env file...")
    with open(".env", "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                # Handle both "export KEY=value" and "KEY=value" formats
                if line.startswith("export "):
                    line = line[7:]  # Remove "export "
                key, value = line.split("=", 1)
                # Remove quotes if present
                value = value.strip('"').strip("'")
                os.environ[key.strip()] = value
    print("✅ Environment variables loaded")

# Check if we're in the right directory
if not os.path.exists("resume_compiler.py"):
    print("Error: resume_compiler.py not found. Please run from the project root directory.")
    sys.exit(1)

# Check if static directory exists
if not os.path.exists("static"):
    print("Warning: static directory not found. Creating it...")
    os.makedirs("static", exist_ok=True)

# Check if output directory exists
if not os.path.exists("output"):
    os.makedirs("output", exist_ok=True)

if __name__ == "__main__":
    # Check for API keys
    has_openai = os.getenv("OPENAI_API_KEY") is not None
    has_anthropic = os.getenv("ANTHROPIC_API_KEY") is not None
    ai_status = "✅ Enabled" if (has_openai or has_anthropic) else "❌ Disabled (Rule-based)"
    ai_provider = "OpenAI" if has_openai else "Anthropic" if has_anthropic else "None"
    
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║              ResumeOS Compiler - Web UI                  ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    
    🚀 Starting server...
    🤖 AI Agent: {ai_status} ({ai_provider})
    
    🌐 Web UI:    http://localhost:8000/
    📚 API Docs:  http://localhost:8000/docs
    📖 ReDoc:     http://localhost:8000/redoc
    
    💡 To enable AI: Run ./setup_api_key.sh or set OPENAI_API_KEY/ANTHROPIC_API_KEY
    
    Press Ctrl+C to stop the server.
    """.format(ai_status=ai_status, ai_provider=ai_provider))
    
    try:
        uvicorn.run(
            "api_example:app",
            host="0.0.0.0",
            port=8000,
            reload=False,  # Disabled for restricted environments
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped. Goodbye!")
