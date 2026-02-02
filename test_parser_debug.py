#!/usr/bin/env python3
"""
Test parser with user's exact LaTeX format
"""

from latex_parser import parse_latex_resume

# User's exact LaTeX format
user_latex = r"""
\documentclass[11pt,a4paper]{article}
\usepackage[margin=1in]{geometry}
\usepackage{enumitem}
\usepackage[hidelinks]{hyperref}
\usepackage{titlesec}
\usepackage{setspace}
\setstretch{1.05}
\pagenumbering{gobble}

\titleformat{\section}
 {\large\bfseries}
 {}
 {0pt}
 {}
 [\titlerule]

\begin{document}

\begin{center}
{\LARGE \textbf{Prashant Gautam}}\\
Software Engineer (Backend)\\
Mau, Uttar Pradesh, India\\
Phone: +91-9219313040 \\
Email: prashantgautam.275101@gmail.com \\
LinkedIn: \url{https://www.linkedin.com/in/prashantgautamiit/}
\end{center}

\section{Professional Summary}
Backend Software Engineer with 2+ years of experience...

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
  \item Optimized PostgreSQL queries and database indexes, reducing API response latency by 25--35\%.
  \item Implemented event-driven communication using Apache Kafka to ensure reliable asynchronous processing.
  \item Integrated Redis caching to reduce database load and improve system performance.
  \item Containerized services using Docker and deployed applications on AWS infrastructure.
  \item Implemented application monitoring using Micrometer and centralized logging with Kibana, reducing production issues by 85\%.
\end{itemize}

\textbf{Software Engineer Intern} \\
Zuci Systems, India \hfill July 2024 -- February 2025
\begin{itemize}[leftmargin=*]
  \item Developed backend services using Java, Spring Boot, and PostgreSQL in a microservices architecture.
  \item Implemented RESTful APIs and handled data persistence using Hibernate ORM.
  \item Assisted in database schema design and data migration between PostgreSQL schemas.
  \item Collaborated with senior engineers to debug production issues and improve system stability.
  \item Gained hands-on experience with AWS services and container-based deployment using Docker.
\end{itemize}

\section{Projects}
\textbf{Legal Instrument Management System}
\begin{itemize}[leftmargin=*]
  \item Developed a backend system using Java, Spring Boot, and PostgreSQL to manage legal instrument metadata.
  \item Designed REST APIs for document ingestion, validation, and retrieval.
  \item Improved query performance through indexing and optimized SQL queries.
\end{itemize}

\textbf{Real-Time Notification Service}
\begin{itemize}[leftmargin=*]
  \item Built a scalable notification service using Node.js, Express.js, and Apache Kafka.
  \item Implemented event-driven messaging for real-time updates across multiple services.
  \item Ensured high availability and fault tolerance in a distributed system environment.
\end{itemize}

\section{Education}
\textbf{Indian Institute of Technology (IIT)} \\
Bachelor of Technology (B.Tech)

\end{document}
"""

if __name__ == '__main__':
    print("=" * 60)
    print("Testing LaTeX Parser with User's Exact Format")
    print("=" * 60)
    
    parsed = parse_latex_resume(user_latex)
    
    print(f"\n✓ Profile: {parsed.get('profile', {}).get('name', 'Not found')}")
    print(f"✓ Skills: {len(parsed.get('skills', []))} found")
    
    print(f"\n✓ Experience: {len(parsed.get('experience', []))} entries")
    for i, exp in enumerate(parsed.get('experience', []), 1):
        print(f"  {i}. {exp.get('role')} at {exp.get('company')} ({exp.get('duration')})")
        print(f"     Bullets: {len(exp.get('bullets', []))}")
        for j, bullet in enumerate(exp.get('bullets', [])[:2], 1):
            print(f"       {j}. {bullet.get('text', '')[:60]}...")
    
    print(f"\n✓ Projects: {len(parsed.get('projects', []))} found")
    for i, proj in enumerate(parsed.get('projects', []), 1):
        print(f"  {i}. {proj.get('name')} ({len(proj.get('bullets', []))} bullets)")
    
    print("\n" + "=" * 60)
    if len(parsed.get('experience', [])) == 2 and len(parsed.get('projects', [])) == 2:
        print("✅ Parser working correctly - both experiences and projects found!")
    else:
        print("❌ Parser issue - missing experiences or projects")
        print(f"   Expected: 2 experiences, 2 projects")
        print(f"   Got: {len(parsed.get('experience', []))} experiences, {len(parsed.get('projects', []))} projects")
