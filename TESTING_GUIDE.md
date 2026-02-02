# Testing Guide for ResumeOS Compiler Engine

This guide explains how to test the ResumeOS Compiler Engine application.

## Quick Start

### Option 1: Run All Tests (Recommended)

```bash
python3 run_tests.py
```

This will:
- Check dependencies
- Verify required files exist
- Run all unit tests
- Run the complete demo
- Generate a summary report

### Option 2: Run Individual Tests

```bash
# Test the compiler engine
python3 test_compiler.py

# Test the LaTeX renderer
python3 test_renderer.py

# Run the complete pipeline demo
python3 complete_demo.py
```

## Prerequisites

### Install Dependencies

```bash
pip install -r requirements.txt
```

Required packages:
- `jinja2` - For LaTeX template rendering
- `fastapi` (optional) - For API example
- `pydantic` (optional) - For API example

### Required Files

Make sure these files exist:
- `example_master_resume.json` - Sample master resume data
- `example_job_descriptions.py` - Sample job descriptions
- `resume_compiler.py` - Core compiler engine
- `latex_renderer.py` - LaTeX renderer

## Test Descriptions

### 1. Compiler Tests (`test_compiler.py`)

**What it tests:**
- Keyword extraction from job descriptions
- Role lens selection (AI Engineer, Backend, DevOps)
- Relevance scoring and ranking
- Skills prioritization
- Project highlighting
- Match score calculation
- Gap analysis

**Expected output:**
- Three tailored resume JSON files:
  - `tailored_ai_engineer.json`
  - `tailored_backend_engineer.json`
  - `tailored_devops_engineer.json`

**What to verify:**
- Match scores are calculated (0-100%)
- Skills are reordered by role relevance
- Different projects are highlighted for different roles
- Experience bullets are ranked by relevance

### 2. LaTeX Renderer Tests (`test_renderer.py`)

**What it tests:**
- LaTeX template rendering
- JSON to LaTeX conversion
- Template formatting

**Expected output:**
- Three LaTeX files:
  - `resume_ai_engineer.tex`
  - `resume_backend_engineer.tex`
  - `resume_devops_engineer.tex`

**What to verify:**
- LaTeX files are generated without errors
- Files contain proper LaTeX syntax
- All resume sections are included

**Note:** This test requires the compiler tests to run first (needs the tailored JSON files).

### 3. Complete Pipeline Demo (`complete_demo.py`)

**What it demonstrates:**
- Full end-to-end workflow
- Master resume loading
- Job description parsing
- Compilation process
- LaTeX rendering
- Gap analysis

**Expected output:**
- `tailored_ai_engineer_demo.json`
- `resume_ai_engineer_demo.tex`

**What to verify:**
- All pipeline steps complete successfully
- Output files are generated
- Match scores are reasonable
- Gap analysis provides useful insights

## Understanding Test Results

### Match Scores

Match scores indicate how well the master resume matches the job description:
- **80-100%**: Excellent match, highly qualified
- **60-79%**: Good match, well qualified
- **40-59%**: Moderate match, some gaps
- **0-39%**: Poor match, significant gaps

### Gap Analysis

The gap analysis shows:
- **Matched Skills**: Skills from master resume that match JD requirements
- **Missing Skills**: Required skills not in master resume
- **Recommendations**: Suggestions to improve match score

### Output Files

After running tests, you'll find:

**JSON Files:**
- `tailored_*.json` - Role-optimized resume data
- Contains ranked bullets, prioritized skills, match scores

**LaTeX Files:**
- `resume_*.tex` - LaTeX source documents
- Can be compiled to PDF using `pdflatex`

## Troubleshooting

### Import Errors

If you see `ModuleNotFoundError`:
```bash
pip install jinja2
```

### File Not Found Errors

Make sure you're running tests from the project root directory:
```bash
cd /path/to/files
python3 test_compiler.py
```

### LaTeX Renderer Fails

If `test_renderer.py` fails, make sure `test_compiler.py` ran successfully first. The renderer needs the tailored JSON files.

### Low Match Scores

Low match scores are expected if:
- Master resume doesn't have many matching skills
- Job description requires very specific technologies
- Role lens doesn't match well

This is normal and helps identify resume gaps.

## Advanced Testing

### Test with Custom Resume

1. Create your own `master_resume.json` following the format in `example_master_resume.json`
2. Modify test files to use your resume:
   ```python
   with open('your_master_resume.json', 'r') as f:
       master_resume = json.load(f)
   ```

### Test with Custom Job Description

1. Add your job description to `example_job_descriptions.py`
2. Use it in tests:
   ```python
   from example_job_descriptions import YOUR_JD
   tailored = compiler.compile(master_resume, YOUR_JD)
   ```

### Compile LaTeX to PDF

To generate PDFs from LaTeX files:
```bash
# Install LaTeX (macOS)
brew install --cask mactex

# Or use Docker
docker run --rm -v $(pwd):/data texlive/texlive:latest pdflatex resume_ai_engineer.tex

# Or use online service like Overleaf
# Upload .tex file to overleaf.com
```

## Test Coverage

Current test coverage:
- ✅ Keyword extraction
- ✅ Role lens selection
- ✅ Relevance scoring
- ✅ Skills ranking
- ✅ Project ranking
- ✅ Match score calculation
- ✅ Gap analysis
- ✅ LaTeX rendering
- ✅ Template formatting

Not yet tested:
- ⏳ AI bullet rewriting (Pass 4 - TODO)
- ⏳ API endpoints (if FastAPI backend exists)
- ⏳ PDF compilation
- ⏳ Error handling edge cases

## Next Steps

After running tests successfully:
1. Review generated tailored resumes
2. Check match scores and gap analysis
3. Compile LaTeX files to PDF to see final output
4. Customize master resume with your own data
5. Test with real job descriptions

## Getting Help

If tests fail:
1. Check error messages carefully
2. Verify all dependencies are installed
3. Ensure all required files exist
4. Check Python version (3.7+ required)
5. Review the README.md for architecture details

---

**Happy Testing! 🚀**
