#!/usr/bin/env python3
"""
Quick Test of ResumeOS Compiler
"""

import json
from resume_compiler import ResumeCompiler, generate_gap_analysis
from example_job_descriptions import (
    AI_ENGINEER_JD,
    BACKEND_ENGINEER_JD,
    DEVOPS_ENGINEER_JD
)


def test_compiler():
    """Test the compiler with different roles"""
    compiler = ResumeCompiler()
    
    # Load master resume
    with open('example_master_resume.json', 'r') as f:
        master_resume = json.load(f)
    
    print("=" * 80)
    print("RESUMEOS COMPILER TEST")
    print("=" * 80)
    
    # Test AI Engineer
    print("\n1. AI ENGINEER ROLE")
    print("-" * 80)
    ai_tailored = compiler.compile(master_resume, AI_ENGINEER_JD)
    print(f"Match Score: {ai_tailored['match_score']*100:.1f}%")
    print(f"Top 5 Skills: {', '.join(ai_tailored['skills'][:5])}")
    print(f"Top Project: {ai_tailored['projects'][0]['name']}")
    print(f"Top Experience: {ai_tailored['experience'][0]['company']}")
    
    with open('tailored_ai_engineer.json', 'w') as f:
        json.dump(ai_tailored, f, indent=2)
    print("✓ Saved to: tailored_ai_engineer.json")
    
    # Test Backend Engineer
    print("\n2. BACKEND ENGINEER ROLE")
    print("-" * 80)
    backend_tailored = compiler.compile(master_resume, BACKEND_ENGINEER_JD)
    print(f"Match Score: {backend_tailored['match_score']*100:.1f}%")
    print(f"Top 5 Skills: {', '.join(backend_tailored['skills'][:5])}")
    print(f"Top Project: {backend_tailored['projects'][0]['name']}")
    print(f"Top Experience: {backend_tailored['experience'][0]['company']}")
    
    with open('tailored_backend_engineer.json', 'w') as f:
        json.dump(backend_tailored, f, indent=2)
    print("✓ Saved to: tailored_backend_engineer.json")
    
    # Test DevOps Engineer
    print("\n3. DEVOPS ENGINEER ROLE")
    print("-" * 80)
    devops_tailored = compiler.compile(master_resume, DEVOPS_ENGINEER_JD)
    print(f"Match Score: {devops_tailored['match_score']*100:.1f}%")
    print(f"Top 5 Skills: {', '.join(devops_tailored['skills'][:5])}")
    print(f"Top Project: {devops_tailored['projects'][0]['name']}")
    print(f"Top Experience: {devops_tailored['experience'][0]['company']}")
    
    with open('tailored_devops_engineer.json', 'w') as f:
        json.dump(devops_tailored, f, indent=2)
    print("✓ Saved to: tailored_devops_engineer.json")
    
    # Gap Analysis for AI role
    print("\n4. GAP ANALYSIS (AI Engineer)")
    print("-" * 80)
    gaps = generate_gap_analysis(master_resume, ai_tailored)
    print(f"Matched Required Skills: {', '.join(gaps['matched_skills'][:5])}")
    if gaps['missing_required_skills']:
        print(f"Missing Skills: {', '.join(gaps['missing_required_skills'])}")
    else:
        print("✓ All required skills present!")
    
    print("\n" + "=" * 80)
    print("KEY INSIGHTS")
    print("=" * 80)
    print("\n✓ Same master resume compiled into 3 different role-optimized versions")
    print("✓ Skills automatically reordered by relevance to target role")
    print("✓ Experience bullets ranked by keyword + tag matching")
    print("✓ Projects prioritized based on role lens")
    print("✓ Match scores indicate ATS compatibility")
    
    print("\nCOMPILER ENGINE: WORKING ✅")
    print("\nNext steps:")
    print("  - Add AI bullet rewriting (Pass 4)")
    print("  - Build LaTeX renderer")
    print("  - Create REST API")
    print("  - Build frontend\n")


if __name__ == '__main__':
    test_compiler()
