# LaTeX Input/Output Guide

The ResumeOS Compiler now supports **LaTeX input → LaTeX output** workflow!

## 🎯 New Workflow

```
LaTeX Resume → Parse to JSON → Compile → Tailored LaTeX Resume
```

Instead of requiring JSON input, you can now:
1. **Input**: Paste your LaTeX resume
2. **Process**: System parses LaTeX, compiles it for the job description
3. **Output**: Get a tailored LaTeX resume optimized for the role

## 🚀 Using the Web UI

### Step 1: Paste LaTeX Resume

In the web UI, paste your LaTeX resume in the "Master Resume (LaTeX)" field.

Example LaTeX format:
```latex
\documentclass[11pt,a4paper]{article}
\usepackage[margin=0.75in]{geometry}

\begin{document}
\begin{center}
    {\LARGE\textbf{Your Name}}\\[4pt]
    Software Engineer\\[4pt]
    email@example.com $|$ +1-234-567-8900
\end{center}

\section*{Technical Skills}
Python, JavaScript, React, FastAPI

\section*{Professional Experience}
\noindent\textbf{Company} \hfill Jan 2023 - Present\\
\textit{Engineer}
\begin{itemize}
    \item Built scalable API
\end{itemize}

\section*{Projects}
\noindent\textbf{Project} $|$ \textit{Python}
\begin{itemize}
    \item Developed feature X
\end{itemize}

\end{document}
```

### Step 2: Paste Job Description

Add the job description you want to tailor for.

### Step 3: Compile

Click "Compile Resume" and get your tailored LaTeX output!

## 📋 Supported LaTeX Structure

The parser recognizes these sections:

- **Header**: Name, headline, contact info (email, phone, location, LinkedIn, GitHub)
- **Technical Skills**: Comma-separated list of skills
- **Professional Experience**: 
  - Company name (in `\textbf{}`)
  - Duration (after `\hfill`)
  - Role (in `\textit{}`)
  - Bullet points (in `\item`)
- **Projects**:
  - Project name (in `\textbf{}`)
  - Technologies (in `\textit{}`)
  - Bullet points (in `\item`)
- **Education**: (optional)
  - Degree (in `\textbf{}`)
  - Institution, year, GPA

## 🔧 API Endpoints

### Compile Resume (LaTeX Input)

```bash
POST /resume/tailor
{
  "latex_resume": "\\documentclass{...}...",
  "job_description": "AI Engineer position...",
  "role_override": "ai_engineer"  # optional
}
```

### Parse LaTeX to JSON

```bash
POST /resume/parse-latex
{
  "latex_content": "\\documentclass{...}..."
}
```

Returns the parsed JSON structure.

### Analyze Match (LaTeX Input)

```bash
POST /resume/analyze
{
  "latex_resume": "\\documentclass{...}...",
  "job_description": "AI Engineer position..."
}
```

## 🎨 Example LaTeX Resume

Load the example LaTeX resume in the UI by clicking "Load Example LaTeX Resume" button.

Or use the sample file: `static/example_resume.tex`

## 🔍 How It Works

1. **LaTeX Parser** (`latex_parser.py`):
   - Extracts profile information from header
   - Parses skills from Technical Skills section
   - Extracts experience entries with company, role, duration, bullets
   - Parses projects with technologies and bullets
   - Infers tags automatically based on keywords

2. **Tag Inference**:
   - Skills: Analyzes skill names to infer tags (ai, backend, frontend, devops, etc.)
   - Bullets: Infers tags from bullet content
   - Projects: Infers tags from project name and technologies

3. **Compilation**:
   - Converts parsed JSON to master resume format
   - Runs through ResumeCompiler
   - Generates tailored resume
   - Outputs as LaTeX

## 💡 Tips

- **Format**: Use the standard LaTeX resume format shown in examples
- **Tags**: Tags are auto-inferred, but you can manually edit the JSON if needed
- **Skills**: List skills comma-separated in Technical Skills section
- **Bullets**: Use `\item` for bullet points in experience and projects
- **Technologies**: Include technologies in projects using `\textit{}`

## 🐛 Troubleshooting

**Parser not extracting data correctly?**
- Make sure your LaTeX follows the expected structure
- Check that sections use `\section*{}` format
- Verify company names are in `\textbf{}` and roles in `\textit{}`

**Missing tags?**
- Tags are inferred automatically
- You can manually add tags by editing the parsed JSON
- Or use the JSON input format if you need precise tag control

**Want more control?**
- Use JSON input format for precise control over tags and structure
- LaTeX input is convenient but JSON gives you full control

---

**Enjoy the LaTeX → LaTeX workflow! 🚀**
