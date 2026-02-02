"""
ResumeOS LaTeX Renderer
=======================
Converts tailored resume JSON → LaTeX document

Key Principle: DO NOT let AI write LaTeX
Instead: Use templates + Jinja2 for deterministic rendering
"""

from typing import Dict, Any
from jinja2 import Template
import os


class LaTeXRenderer:
    """
    Renders tailored resume JSON into LaTeX document
    
    Uses template-based approach for consistent, clean output
    """
    
    def __init__(self, template_dir: str = "templates"):
        self.template_dir = template_dir
        self.templates = {}
        self._load_templates()
    
    def _load_templates(self):
        """Load LaTeX templates"""
        # For now, we'll define templates inline
        # In production, these would be separate .tex files
        
        self.templates['base'] = self._get_base_template()
        self.templates['ai_engineer'] = self._get_ai_engineer_template()
        self.templates['backend_engineer'] = self._get_backend_engineer_template()
        self.templates['devops_engineer'] = self._get_devops_engineer_template()
    
    def _get_base_template(self) -> str:
        """Base LaTeX template - clean, ATS-friendly format"""
        return r"""% ResumeOS Generated Resume
% Target Role: {{ target_role }}
% Match Score: {{ match_score }}%
% Version: v2.2.0 (AI Skills Enhancement + Market Standards 2025) - {{ compile_timestamp }}

\documentclass[11pt,a4paper]{article}
\usepackage[margin=0.75in]{geometry}
\usepackage{enumitem}
\usepackage{hyperref}
\usepackage{titlesec}

% Remove page numbers
\pagestyle{empty}

% Section formatting
\titleformat{\section}{\large\bfseries}{}{0em}{}[\titlerule]
\titlespacing*{\section}{0pt}{12pt}{6pt}

% Compact lists
\setlist[itemize]{leftmargin=*, noitemsep, topsep=0pt}

\begin{document}

% ============= HEADER =============
\begin{center}
    {\LARGE\textbf{ {{- profile.name -}} }}\\[4pt]
    {{- profile.headline -}}\\[4pt]
    {% if profile.email %}{{ profile.email }} $|$ {% endif %}
    {% if profile.phone %}{{ profile.phone }} $|$ {% endif %}
    {% if profile.location %}{{ profile.location }}{% endif %}\\
    {% if profile.linkedin %}{{ profile.linkedin }} $|$ {% endif %}
    {% if profile.github %}{{ profile.github }}{% endif %}
\end{center}

% ============= SUMMARY =============
{% if summary and summary|trim %}
\section*{Professional Summary}
{{ summary }}
{% endif %}

% ============= SKILLS =============
{% if skills %}
\section*{Technical Skills}
{% for skill in skills %}{{ skill }}{% if not loop.last %}, {% endif %}{% endfor %}
{% endif %}

% ============= EXPERIENCE =============
{% if experience %}
\section*{Professional Experience}
{% for exp in experience %}
{% if exp.company or exp.role %}
\noindent\textbf{ {{- exp.company -}} }{% if exp.duration %} \hfill {{ exp.duration }}{% endif %}\\
{% if exp.role %}\textit{ {{- exp.role -}} }{% endif %}
{% if exp.bullets %}
\begin{itemize}
{% for bullet in exp.bullets %}
    \item {{ bullet }}
{% endfor %}
\end{itemize}
{% endif %}
\vspace{4pt}
{% endif %}
{% endfor %}
{% endif %}

% ============= PROJECTS =============
{% if projects %}
\section*{Projects}
{% for proj in projects %}
{% if proj.name %}
\noindent\textbf{ {{- proj.name -}} }{% if proj.technologies %} $|$ \textit{ {{- proj.technologies | join(', ') -}} }{% endif %}
{% if proj.bullets %}
\begin{itemize}
{% for bullet in proj.bullets %}
    \item {{ bullet }}
{% endfor %}
\end{itemize}
{% endif %}
\vspace{4pt}
{% endif %}
{% endfor %}
{% endif %}

% ============= EDUCATION =============
{% if education and education|length > 0 %}
\section*{Education}
{% for edu in education %}
{% if edu.degree or edu.institution %}
{% if edu.institution %}
\noindent\textbf{ {{- edu.institution -}} }{% if edu.degree %} \\
{{ edu.degree }}{% endif %}{% if edu.year %}, {{ edu.year }}{% endif %}{% if edu.gpa %} $|$ GPA: {{ edu.gpa }}{% endif %}
{% else %}
\noindent\textbf{ {{- edu.degree -}} }\\
{{ edu.institution }}{% if edu.year %}, {{ edu.year }}{% endif %}{% if edu.gpa %} $|$ GPA: {{ edu.gpa }}{% endif %}
{% endif %}
\vspace{4pt}
{% endif %}
{% endfor %}
{% endif %}

\end{document}
"""
    
    def _get_ai_engineer_template(self) -> str:
        """AI Engineer specific template - emphasizes ML projects"""
        # Could have role-specific styling, for now uses base
        return self._get_base_template()
    
    def _get_backend_engineer_template(self) -> str:
        """Backend Engineer specific template"""
        return self._get_base_template()
    
    def _get_devops_engineer_template(self) -> str:
        """DevOps Engineer specific template"""
        return self._get_base_template()
    
    def render(
        self,
        tailored_resume: Dict[str, Any],
        template_name: str = "base"
    ) -> str:
        """
        Render tailored resume JSON to LaTeX
        
        Args:
            tailored_resume: Output from ResumeCompiler.compile()
            template_name: Template to use (base, ai_engineer, etc.)
        
        Returns:
            LaTeX document as string
        """
        
        # Select template based on role if not specified
        if template_name == "base":
            role = tailored_resume.get('target_role', 'backend_engineer')
            template_name = role if role in self.templates else 'base'
        
        template_str = self.templates.get(template_name, self.templates['base'])
        template = Template(template_str)
        
        # Prepare data for template
        from datetime import datetime
        render_data = {
            'target_role': tailored_resume.get('target_role', '').replace('_', ' ').title(),
            'match_score': int(tailored_resume.get('match_score', 0) * 100),
            'compile_timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'profile': tailored_resume.get('profile', {}),
            'summary': tailored_resume.get('summary', ''),  # CRITICAL: Include summary to prevent data loss
            'skills': tailored_resume.get('skills', []),
            'experience': tailored_resume.get('experience', []),
            'projects': tailored_resume.get('projects', []),
            'education': tailored_resume.get('education', [])  # CRITICAL: Include education to prevent data loss
        }
        
        # Render template
        latex_output = template.render(**render_data)
        
        return latex_output
    
    def render_to_file(
        self,
        tailored_resume: Dict[str, Any],
        output_path: str,
        template_name: str = "base"
    ) -> str:
        """
        Render and save to file
        
        Returns:
            Path to saved file
        """
        latex_content = self.render(tailored_resume, template_name)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(latex_content)
        
        return output_path
    
    def escape_latex_special_chars(self, text: str) -> str:
        """
        Escape special LaTeX characters
        
        Important for user-provided content
        """
        replacements = {
            '&': r'\&',
            '%': r'\%',
            '$': r'\$',
            '#': r'\#',
            '_': r'\_',
            '{': r'\{',
            '}': r'\}',
            '~': r'\textasciitilde{}',
            '^': r'\textasciicircum{}',
            '\\': r'\textbackslash{}',
        }
        
        for char, escaped in replacements.items():
            text = text.replace(char, escaped)
        
        return text


# ============= CONVENIENCE FUNCTIONS =============

def render_resume(tailored_resume: Dict[str, Any], output_file: str = None) -> str:
    """
    Quick function to render tailored resume to LaTeX
    
    Usage:
        tailored = compiler.compile(master_resume, jd)
        latex = render_resume(tailored, 'resume_ai.tex')
    """
    renderer = LaTeXRenderer()
    
    if output_file:
        renderer.render_to_file(tailored_resume, output_file)
        return output_file
    else:
        return renderer.render(tailored_resume)


def compile_latex_to_pdf(tex_file: str, output_dir: str = ".") -> str:
    """
    Compile LaTeX to PDF using pdflatex
    
    Returns path to PDF file
    
    Note: Requires pdflatex installed on system
    """
    import subprocess
    
    try:
        # Run pdflatex
        result = subprocess.run(
            ['pdflatex', '-interaction=nonstopmode', '-output-directory', output_dir, tex_file],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            pdf_file = tex_file.replace('.tex', '.pdf')
            return pdf_file
        else:
            raise Exception(f"pdflatex failed: {result.stderr}")
    
    except FileNotFoundError:
        raise Exception("pdflatex not found. Install texlive: apt-get install texlive-latex-base")
    except subprocess.TimeoutExpired:
        raise Exception("pdflatex timed out")
