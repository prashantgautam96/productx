#!/usr/bin/env python3
"""
Example: Using ResumeOS with AI Agent
=====================================
Demonstrates AI-powered bullet rewriting
"""

import json
import os
from resume_compiler import ResumeCompiler
from ai_agent import create_ai_agent
from latex_renderer import render_resume
from example_job_descriptions import AI_ENGINEER_JD


def example_with_ai():
    """Example using AI agent"""
    
    print("=" * 80)
    print("ResumeOS with AI Agent - Example")
    print("=" * 80)
    
    # Check for API key
    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
    provider = "openai" if os.getenv("OPENAI_API_KEY") else "anthropic"
    
    if not api_key:
        print("\n⚠️  No API key found. Using rule-based rewriting.")
        print("Set OPENAI_API_KEY or ANTHROPIC_API_KEY to enable AI.")
        ai_agent = None
    else:
        print(f"\n✅ Creating AI agent with {provider}...")
        try:
            ai_agent = create_ai_agent(provider=provider, api_key=api_key, enabled=True)
            print("✅ AI Agent ready!")
        except Exception as e:
            print(f"⚠️  AI Agent failed: {e}. Using rule-based.")
            ai_agent = None
    
    # Initialize compiler
    compiler = ResumeCompiler(ai_agent=ai_agent)
    
    # Load master resume
    print("\n📄 Loading master resume...")
    with open('example_master_resume.json', 'r') as f:
        master_resume = json.load(f)
    
    print(f"  Skills: {len(master_resume['skills'])}")
    print(f"  Experience entries: {len(master_resume['experience'])}")
    print(f"  Projects: {len(master_resume['projects'])}")
    
    # Show original bullets
    print("\n📝 Original Bullets (first experience):")
    first_exp = master_resume['experience'][0]
    for i, bullet in enumerate(first_exp['bullets'][:2], 1):
        print(f"  {i}. {bullet['text']}")
    
    # Compile with AI
    print("\n🤖 Compiling with AI agent...")
    tailored = compiler.compile(master_resume, AI_ENGINEER_JD)
    
    # Show rewritten bullets
    print("\n✨ AI-Rewritten Bullets (if AI enabled):")
    if tailored.get('experience'):
        first_tailored = tailored['experience'][0]
        for i, bullet in enumerate(first_tailored['bullets'][:2], 1):
            print(f"  {i}. {bullet}")
    
    # Show match score
    print(f"\n📊 Match Score: {tailored['match_score']*100:.1f}%")
    print(f"   Target Role: {tailored['target_role']}")
    
    # Render to LaTeX
    print("\n📄 Rendering to LaTeX...")
    render_resume(tailored, 'resume_ai_enhanced.tex')
    print("✅ Saved to: resume_ai_enhanced.tex")
    
    print("\n" + "=" * 80)
    print("Comparison:")
    print("=" * 80)
    print("\nOriginal vs AI-Enhanced:")
    print(f"\nOriginal: {first_exp['bullets'][0]['text']}")
    if tailored.get('experience') and tailored['experience'][0].get('bullets'):
        print(f"AI-Enhanced: {tailored['experience'][0]['bullets'][0]}")
    
    if ai_agent:
        print("\n✅ AI rewriting was applied!")
    else:
        print("\nℹ️  Using rule-based rewriting (no AI)")


if __name__ == '__main__':
    example_with_ai()
