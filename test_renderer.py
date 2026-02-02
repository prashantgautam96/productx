#!/usr/bin/env python3
"""
Test LaTeX Renderer
"""

import json
from latex_renderer import LaTeXRenderer, render_resume


def test_renderer():
    """Test LaTeX rendering"""
    print("=" * 80)
    print("TESTING LATEX RENDERER")
    print("=" * 80)
    
    # Load tailored resumes
    roles = [
        ('tailored_ai_engineer.json', 'resume_ai_engineer.tex'),
        ('tailored_backend_engineer.json', 'resume_backend_engineer.tex'),
        ('tailored_devops_engineer.json', 'resume_devops_engineer.tex')
    ]
    
    renderer = LaTeXRenderer()
    
    for tailored_file, output_file in roles:
        print(f"\n📄 Rendering {tailored_file}...")
        
        with open(tailored_file, 'r') as f:
            tailored_resume = json.load(f)
        
        # Render to LaTeX
        latex_output = render_resume(tailored_resume, output_file)
        
        print(f"   ✓ Generated: {output_file}")
        
        # Show preview
        with open(output_file, 'r') as f:
            content = f.read()
            lines = content.split('\n')
            
            # Show header section
            print(f"   Preview (first 15 lines):")
            for line in lines[5:20]:  # Skip preamble
                if line.strip():
                    print(f"     {line[:70]}")
    
    print("\n" + "=" * 80)
    print("LATEX FILES GENERATED ✅")
    print("=" * 80)
    print("\nGenerated files:")
    for _, output_file in roles:
        print(f"  • {output_file}")
    
    print("\n💡 To compile to PDF (requires pdflatex):")
    print("   pdflatex resume_ai_engineer.tex")
    print("\n📦 Or use the compile_latex_to_pdf() function in latex_renderer.py")


if __name__ == '__main__':
    test_renderer()
