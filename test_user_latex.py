#!/usr/bin/env python3
"""Test parser with user's LaTeX format"""

from latex_parser import parse_latex_resume

user_latex = r"""
\documentclass[11pt,a4paper]{article}
\usepackage[margin=1in]{geometry}
\usepackage{enumitem}

\begin{document}

\begin{center}
{\LARGE \textbf{Prashant Gautam}}\\
Software Engineer (Backend)\\
Mau, Uttar Pradesh, India\\
Phone: +91-9219313040 \\
Email: prashantgautam.275101@gmail.com \\
LinkedIn: \url{https://www.linkedin.com/in/prashantgautamiit/}
\end{center}

\section{Technical Skills}
\textbf{Programming Languages:} Java, Python, JavaScript \\
\textbf{Backend Frameworks:} Spring Boot, Spring MVC, Spring Data JPA, Express.js, FeathersJS \\
\textbf{Databases:} PostgreSQL, MongoDB \\

\section{Professional Experience}

\textbf{Software Engineer} \\
Zuci Systems, India \hfill March 2025 -- Present
\begin{itemize}[leftmargin=*]
  \item Designed and developed backend microservices using Java and Spring Boot for enterprise-scale applications.
  \item Built and maintained REST APIs with Spring MVC and Spring Data JPA, serving high-volume client requests.
\end{itemize}

\section{Projects}

\textbf{Legal Instrument Management System}
\begin{itemize}[leftmargin=*]
  \item Developed a backend system using Java, Spring Boot, and PostgreSQL to manage legal instrument metadata.
  \item Designed REST APIs for document ingestion, validation, and retrieval.
\end{itemize}

\end{document}
"""

if __name__ == '__main__':
    print("Testing LaTeX parser with user's format...")
    parsed = parse_latex_resume(user_latex)
    
    print(f"\n✓ Profile: {parsed.get('profile', {}).get('name', 'Not found')}")
    print(f"✓ Skills: {len(parsed.get('skills', []))} found")
    print(f"  Sample: {[s.get('name') for s in parsed.get('skills', [])[:5]]}")
    print(f"✓ Experience: {len(parsed.get('experience', []))} entries")
    for exp in parsed.get('experience', [])[:2]:
        print(f"  - {exp.get('role')} at {exp.get('company')} ({len(exp.get('bullets', []))} bullets)")
    print(f"✓ Projects: {len(parsed.get('projects', []))} found")
    for proj in parsed.get('projects', [])[:2]:
        print(f"  - {proj.get('name')} ({len(proj.get('bullets', []))} bullets)")
    
    if parsed.get('skills') and parsed.get('experience'):
        print("\n✅ Parser working correctly!")
    else:
        print("\n❌ Parser needs fixes")
