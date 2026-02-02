# ResumeOS Web UI

A minimal web interface for testing and interacting with the ResumeOS Compiler Engine.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the Server

```bash
python3 start_ui.py
```

Or directly:

```bash
python3 api_example.py
```

### 3. Open in Browser

Navigate to: **http://localhost:8000/**

## Features

### 🎯 Main Interface

- **Master Resume Input**: Paste your JSON resume or load the example
- **Job Description Input**: Paste any job description
- **Role Selection**: Auto-detect or manually select a role lens
- **One-Click Compilation**: Generate tailored resume instantly

### 📊 Results Display

- **Match Score**: Visual score circle (0-100%)
- **Target Role**: Detected role from job description
- **Matched Skills**: Skills that match the job requirements
- **Missing Skills**: Required skills not in your resume
- **Recommendations**: Suggestions to improve match score
- **Download LaTeX**: Download the generated LaTeX file

### 🎨 Example Data

The UI includes quick-load buttons for:
- Example master resume (from `example_master_resume.json`)
- AI Engineer job description
- Backend Engineer job description
- DevOps Engineer job description

## Usage Guide

### Step 1: Load Master Resume

1. Click "Load Example Resume" to use the sample data, OR
2. Paste your own master resume JSON in the textarea

**Master Resume Format:**
```json
{
  "profile": {
    "name": "Your Name",
    "headline": "Software Engineer",
    ...
  },
  "skills": [
    {"name": "Python", "tags": ["backend", "ai"]},
    ...
  ],
  "experience": [...],
  "projects": [...]
}
```

### Step 2: Add Job Description

1. Click one of the example JD buttons (AI/Backend/DevOps), OR
2. Paste your own job description

### Step 3: Compile

1. Optionally select a role override (or leave as "Auto-detect")
2. Click "Compile Resume"
3. Wait for results (usually 1-3 seconds)

### Step 4: Review Results

- Check your match score
- Review matched and missing skills
- Read recommendations
- Download the LaTeX file

## API Endpoints

The UI uses these API endpoints:

- `POST /resume/tailor` - Compile tailored resume
- `GET /resume/download/{filename}` - Download LaTeX file
- `GET /roles` - Get available role lenses
- `POST /keywords/extract` - Extract keywords from JD
- `POST /resume/analyze` - Quick match analysis

## Troubleshooting

### Server Won't Start

**Error: Module not found**
```bash
pip install -r requirements.txt
```

**Error: Port already in use**
- Change port in `start_ui.py` or `api_example.py`
- Or stop the process using port 8000

### UI Not Loading

- Make sure `static/index.html` exists
- Check browser console for errors
- Verify server is running on port 8000

### Compilation Fails

- Check that master resume JSON is valid
- Ensure job description is not empty
- Check server logs for detailed error messages

### Download Not Working

- LaTeX files are saved in `output/` directory
- Check that the file was generated
- Try refreshing the page

## File Structure

```
files/
├── api_example.py              # FastAPI server
├── start_ui.py                 # UI startup script
├── static/
│   ├── index.html              # Web UI
│   └── example_master_resume.json  # Example resume
├── output/                     # Generated LaTeX files (created automatically)
└── requirements.txt            # Python dependencies
```

## Development

### Making Changes

1. Edit `static/index.html` for UI changes
2. Edit `api_example.py` for API changes
3. Server auto-reloads on code changes (if using `start_ui.py`)

### Testing

1. Use example data to test compilation
2. Try different role lenses
3. Test with custom resumes and job descriptions
4. Verify LaTeX files are generated correctly

## Next Steps

After testing with the UI:

1. **Compile LaTeX to PDF**: Use `pdflatex` or upload to Overleaf
2. **Customize Resume**: Edit `example_master_resume.json` with your data
3. **Test Different Roles**: Try all 5 role lenses
4. **Review Match Scores**: Understand what improves your score
5. **Use Gap Analysis**: Identify skills to add to your resume

## API Documentation

Full API documentation available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

**Happy Testing! 🚀**
