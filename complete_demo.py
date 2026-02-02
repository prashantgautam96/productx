#!/usr/bin/env python3
"""
ResumeOS Complete Pipeline Demo
================================
Demonstrates the full compiler workflow:
    Master Resume → Tailored Resume → LaTeX → (PDF)
"""

import json
from resume_compiler import ResumeCompiler, generate_gap_analysis
from latex_renderer import render_resume
from example_job_descriptions import AI_ENGINEER_JD


def print_banner(text: str):
    """Print a fancy banner"""
    print("\n" + "=" * 80)
    print(f"  {text}")
    print("=" * 80 + "\n")


def complete_pipeline_demo():
    """Run complete pipeline"""
    
    print("""
    ╔══════════════════════════════════════════════════════════════════════════╗
    ║                                                                          ║
    ║                        ResumeOS Complete Pipeline                        ║
    ║                                                                          ║
    ║    Master Resume → Role-Tailored Resume → LaTeX Document → PDF          ║
    ║                                                                          ║
    ╚══════════════════════════════════════════════════════════════════════════╝
    """)
    
    # ========== STEP 1: Load Master Resume ==========
    print_banner("STEP 1: Loading Master Resume (Single Source of Truth)")
    
    with open('example_master_resume.json', 'r') as f:
        master_resume = json.load(f)
    
    print(f"✓ Loaded master resume for: {master_resume['profile']['name']}")
    print(f"  Skills: {len(master_resume['skills'])} skills")
    print(f"  Experience: {len(master_resume['experience'])} positions")
    print(f"  Projects: {len(master_resume['projects'])} projects")
    
    # ========== STEP 2: Initialize Compiler ==========
    print_banner("STEP 2: Initializing Resume Compiler")
    
    compiler = ResumeCompiler()
    
    print("✓ Compiler initialized with role lenses:")
    for role_type, role_lens in compiler.role_lenses.items():
        print(f"  • {role_type.value:20} → Priority tags: {', '.join(role_lens.priority_tags[:3])}")
    
    # ========== STEP 3: Extract Keywords from JD ==========
    print_banner("STEP 3: Extracting Keywords from Job Description")
    
    print("Job Description Preview:")
    print("-" * 80)
    print(AI_ENGINEER_JD[:300] + "...")
    print("-" * 80)
    
    keywords = compiler.extract_keywords_from_jd(AI_ENGINEER_JD)
    
    print(f"\n✓ Detected role: {keywords.role.value}")
    print(f"  Required skills: {', '.join(keywords.required_skills[:6])}")
    print(f"  Tools: {', '.join(keywords.tools)}")
    print(f"  Key concepts: {', '.join(keywords.concepts[:3])}")
    
    # ========== STEP 4: Compile Tailored Resume ==========
    print_banner("STEP 4: Compiling Tailored Resume")
    
    print("Running compiler passes:")
    print("  [1/5] Extracting JD keywords...")
    print("  [2/5] Selecting role lens...")
    print("  [3/5] Scoring & ranking bullets...")
    print("  [4/5] Scoring & ranking projects...")
    print("  [5/5] Generating tailored JSON...")
    
    tailored = compiler.compile(master_resume, AI_ENGINEER_JD)
    
    print(f"\n✓ Compilation complete!")
    print(f"  Target Role: {tailored['target_role']}")
    print(f"  Match Score: {tailored['match_score']*100:.1f}%")
    print(f"  Keywords Matched: {tailored['metadata']['total_keywords_matched']}")
    
    # ========== STEP 5: Show Optimization Results ==========
    print_banner("STEP 5: Optimization Results")
    
    print("Skills Reordering:")
    print(f"  Top 5: {', '.join(tailored['skills'][:5])}")
    print(f"  (Prioritized AI/ML skills to top)")
    
    print("\nExperience Ranking:")
    for i, exp in enumerate(tailored['experience'][:2], 1):
        print(f"  {i}. {exp['company']} (score: {exp['relevance_score']:.2f})")
        print(f"     → Top bullet: {exp['bullets'][0][:70]}...")
    
    print("\nProject Ranking:")
    for i, proj in enumerate(tailored['projects'][:3], 1):
        print(f"  {i}. {proj['name']} (score: {proj['relevance_score']:.2f})")
        print(f"     → Keywords: {', '.join(proj['matched_keywords'][:4])}")
    
    # ========== STEP 6: Gap Analysis ==========
    print_banner("STEP 6: Gap Analysis")
    
    gaps = generate_gap_analysis(master_resume, tailored)
    
    print(f"Match Score: {gaps['match_score']*100:.1f}%")
    print(f"\nMatched Required Skills:")
    for skill in gaps['matched_skills'][:8]:
        print(f"  ✓ {skill}")
    
    if gaps['missing_required_skills']:
        print(f"\n⚠️  Missing Required Skills:")
        for skill in gaps['missing_required_skills']:
            print(f"  ✗ {skill}")
        print(f"\n💡 Recommendations:")
        for rec in gaps['recommendations'][:3]:
            print(f"  • {rec}")
    else:
        print("\n✅ All required skills present!")
    
    # ========== STEP 7: Render to LaTeX ==========
    print_banner("STEP 7: Rendering LaTeX Document")
    
    latex_file = 'resume_ai_engineer_demo.tex'
    render_resume(tailored, latex_file)
    
    print(f"✓ LaTeX document generated: {latex_file}")
    
    # Show LaTeX preview
    with open(latex_file, 'r') as f:
        lines = f.readlines()
    
    print("\nLaTeX Preview (header section):")
    print("-" * 80)
    for line in lines[23:36]:  # Header section
        print(line.rstrip())
    print("-" * 80)
    
    # ========== STEP 8: Save Artifacts ==========
    print_banner("STEP 8: Saving Artifacts")
    
    # Save tailored JSON
    tailored_json_file = 'tailored_ai_engineer_demo.json'
    with open(tailored_json_file, 'w') as f:
        json.dump(tailored, f, indent=2)
    
    print("✓ Generated files:")
    print(f"  • {tailored_json_file} (tailored resume JSON)")
    print(f"  • {latex_file} (LaTeX document)")
    print(f"\n💡 To compile to PDF:")
    print(f"  pdflatex {latex_file}")
    
    # ========== SUMMARY ==========
    print_banner("PIPELINE COMPLETE! 🎉")
    
    print("""
    Summary of ResumeOS Compiler:
    ==============================
    
    ✅ Input: Master Resume (single source of truth) + Job Description
    ✅ Output: Role-optimized LaTeX resume ready for ATS
    
    Key Features Demonstrated:
    --------------------------
    1. Automatic keyword extraction from JD
    2. Role-specific lens selection (AI, Backend, DevOps, etc.)
    3. Intelligent bullet ranking by relevance score
    4. Skills prioritization by role requirements
    5. Project highlighting based on tag matching
    6. Match score calculation for ATS compatibility
    7. Gap analysis showing missing skills
    8. Deterministic LaTeX rendering (no AI-written LaTeX)
    
    Core Principles Maintained:
    ---------------------------
    ✓ Master resume is immutable truth
    ✓ Tailored resumes are projections, not edits
    ✓ AI cannot invent new skills
    ✓ Output is deterministic structure
    ✓ Tailoring improves ATS relevance
    
    Next Steps for Production:
    --------------------------
    1. Add AI bullet rewriting (Pass 4) with Claude API
    2. Build FastAPI backend wrapper
    3. Create database layer (Postgres)
    4. Build Next.js frontend
    5. Add version history tracking
    6. Implement PDF compilation
    7. Add authentication & payments
    
    The compiler ENGINE is complete and working! 🚀
    """)
    
    return tailored, latex_file


if __name__ == '__main__':
    complete_pipeline_demo()
