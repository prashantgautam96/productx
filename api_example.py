"""
ResumeOS FastAPI Backend (MVP Example)
=======================================
Shows how the compiler engine would be wrapped in a REST API

To run:
    pip install fastapi uvicorn
    python api_example.py
    
Then visit: http://localhost:8000/docs
"""

import json
import os
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator

# Import configuration and services
from config import get_config
from services import ResumeService, FileService
from exceptions import (
    CompilationError,
    ParsingError,
    RenderingError,
    ValidationError,
    ResumeOSError
)
from ai_agent import create_ai_agent
from resume_compiler import ResumeCompiler

# Configure logging from config
config = get_config()
logging.basicConfig(
    level=getattr(logging, config.log_level.upper()),
    format=config.log_format
)
logger = logging.getLogger(__name__)


# ========== Pydantic Models ==========

class ProfileModel(BaseModel):
    name: str
    headline: str
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None


class SkillModel(BaseModel):
    name: str
    tags: List[str] = []


class BulletModel(BaseModel):
    id: str
    text: str
    tags: List[str] = []


class ExperienceModel(BaseModel):
    company: str
    role: str
    duration: str
    bullets: List[BulletModel]


class ProjectModel(BaseModel):
    id: str
    name: str
    description: Optional[str] = ""
    tags: List[str] = []
    technologies: List[str] = []
    bullets: List[str]


class MasterResumeModel(BaseModel):
    profile: ProfileModel
    skills: List[SkillModel]
    experience: List[ExperienceModel]
    projects: List[ProjectModel]


class TailorRequest(BaseModel):
    master_resume: Optional[MasterResumeModel] = None  # JSON format
    latex_resume: Optional[str] = None  # LaTeX format
    job_description: str
    role_override: Optional[str] = None  # 'ai_engineer', 'backend_engineer', etc.
    enable_ai: Optional[bool] = True  # Enable/disable AI rewriting


class TailorResponse(BaseModel):
    target_role: str
    match_score: float
    tailored_resume: Dict[str, Any]
    latex_file: str
    latex_content: Optional[str] = None  # LaTeX content as string
    gap_analysis: Dict[str, Any]


class AnalyzeRequest(BaseModel):
    master_resume: Optional[MasterResumeModel] = None
    latex_resume: Optional[str] = None
    job_description: str


# ========== FastAPI App ==========

app = FastAPI(
    title="ResumeOS API",
    description="Resume Compiler as a Service",
    version="2.1.0"
)

# CORS middleware for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
static_dir = config.static_dir
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Initialize services (dependency injection)
resume_service = ResumeService()
file_service = FileService()


# ========== Endpoints ==========

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the UI"""
    index_path = static_dir / "index.html"
    if index_path.exists():
        with open(index_path, "r", encoding="utf-8") as f:
            return f.read()
    return """
    <html>
        <body>
            <h1>ResumeOS Compiler API</h1>
            <p>Status: operational</p>
            <p><a href="/docs">API Documentation</a></p>
        </body>
    </html>
    """


@app.get("/api/status")
async def api_status():
    """API status"""
    return {
        "message": "ResumeOS Compiler API",
        "status": "operational",
        "version": "0.1.0",
        "ai_enabled": ai_agent is not None and ai_agent.enabled if 'ai_agent' in globals() else False,
        "ai_provider": ai_agent.config.provider if 'ai_agent' in globals() and ai_agent else None
    }


@app.get("/roles")
async def get_available_roles():
    """Get list of available role lenses"""
    return {
        "roles": [role.value for role in RoleType],
        "role_details": {
            role.value: {
                "priority_tags": lens.priority_tags,
                "rewrite_style": lens.rewrite_style
            }
            for role in RoleType
        }
    }


@app.post("/resume/tailor")
async def tailor_resume(request: TailorRequest) -> TailorResponse:
    """
    Compile master resume for specific job description
    
    Accepts either JSON master_resume or latex_resume (LaTeX format)
    
    Returns tailored resume JSON + LaTeX file
    """
    try:
        # Parse input (LaTeX or JSON)
        if request.latex_resume:
            master_resume_dict = resume_service.parse_latex_resume(request.latex_resume)
        elif request.master_resume:
            master_resume_dict = request.master_resume.model_dump()
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Either master_resume (JSON) or latex_resume (LaTeX) must be provided"
            )
        
        # Handle role override
        role_override = None
        if request.role_override:
            try:
                from resume_compiler import RoleType
                role_override = RoleType(request.role_override)
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid role. Must be one of: {[r.value for r in RoleType]}"
                )
        
        # Compile tailored resume
        tailored = resume_service.compile_resume(
            master_resume_dict,
            request.job_description,
            enable_ai=request.enable_ai
        )
        
        # Generate gap analysis
        gaps = resume_service.analyze_match(master_resume_dict, tailored)
        
        # Render to LaTeX
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        latex_filename = f"resume_{tailored['target_role']}_{timestamp}.tex"
        latex_path = file_service.output_dir / latex_filename
        
        latex_content = resume_service.render_latex(tailored, latex_path)
        
        return TailorResponse(
            target_role=tailored['target_role'],
            match_score=tailored['match_score'],
            tailored_resume=tailored,
            latex_file=latex_filename,
            latex_content=latex_content,
            gap_analysis=gaps
        )
    
    except (ValidationError, ParsingError) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except CompilationError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Compilation failed: {str(e)}"
        )
    except RenderingError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Rendering failed: {str(e)}"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Tailor resume failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@app.get("/resume/download/{filename}")
async def download_resume(filename: str):
    """Download generated LaTeX file"""
    if file_service.file_exists(filename):
        file_path = file_service.output_dir / filename
        return FileResponse(
            str(file_path),
            media_type="application/x-tex",
            filename=filename
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )


@app.post("/resume/parse-latex")
async def parse_latex(latex_content: str):
    """
    Parse LaTeX resume to JSON format
    
    Useful for preview/debugging LaTeX parsing
    """
    try:
        parsed = parse_latex_resume(latex_content)
        
        # Add parsing diagnostics
        diagnostics = {
            "parsed": parsed,
            "diagnostics": {
                "has_profile": bool(parsed.get('profile')),
                "profile_name": parsed.get('profile', {}).get('name', 'Not found'),
                "skills_count": len(parsed.get('skills', [])),
                "experience_count": len(parsed.get('experience', [])),
                "projects_count": len(parsed.get('projects', [])),
                "total_bullets": sum(
                    len(exp.get('bullets', [])) 
                    for exp in parsed.get('experience', [])
                ),
                "sample_skills": [s.get('name') for s in parsed.get('skills', [])[:5]],
                "sample_companies": [exp.get('company') for exp in parsed.get('experience', [])[:3]]
            }
        }
        
        return diagnostics
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Parsing error: {str(e)}")


@app.post("/keywords/extract")
async def extract_keywords(job_description: str):
    """
    Extract keywords from job description
    
    Useful for preview/debugging
    """
    try:
        keywords = resume_service.compiler.extract_keywords_from_jd(job_description)
        
        return {
            "detected_role": keywords.role.value,
            "required_skills": keywords.required_skills,
            "preferred_skills": keywords.preferred_skills,
            "tools": keywords.tools,
            "concepts": keywords.concepts
        }
    
    except Exception as e:
        logger.error(f"Keyword extraction failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Keyword extraction failed"
        )


@app.post("/resume/analyze")
async def analyze_match(request: AnalyzeRequest):
    """
    Analyze how well master resume matches JD
    
    Accepts either JSON master_resume or latex_resume (LaTeX format)
    Returns match score and gaps without generating full resume
    """
    try:
        if request.latex_resume:
            master_resume_dict = parse_latex_resume(request.latex_resume)
        elif request.master_resume:
            master_resume_dict = request.master_resume.model_dump()
        else:
            raise HTTPException(
                status_code=400,
                detail="Either master_resume (JSON) or latex_resume (LaTeX) must be provided"
            )
        
        # Quick compile
        tailored = resume_service.compile_resume(
            master_resume_dict,
            request.job_description,
            enable_ai=False
        )
        
        # Gap analysis
        gaps = resume_service.analyze_match(master_resume_dict, tailored)
        
        return {
            "match_score": tailored['match_score'],
            "target_role": tailored['target_role'],
            "matched_skills": gaps['matched_skills'],
            "missing_skills": gaps['missing_required_skills'],
            "recommendations": gaps['recommendations'],
            "keywords_matched": tailored['metadata']['total_keywords_matched']
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ========== Run Server ==========

if __name__ == "__main__":
    import uvicorn
    
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║              ResumeOS API Server Starting                 ║
    ╚═══════════════════════════════════════════════════════════╝
    
    🌐 Web UI: http://localhost:8000/
    📚 API Docs: http://localhost:8000/docs
    📖 ReDoc: http://localhost:8000/redoc
    
    Endpoints:
    • GET  /                    - Web UI
    • GET  /api/status          - API status
    • GET  /roles               - Available role lenses
    • POST /resume/tailor       - Compile tailored resume
    • POST /keywords/extract    - Extract JD keywords
    • POST /resume/analyze      - Quick match analysis
    • GET  /resume/download/{filename} - Download LaTeX
    """)
    
    config = get_config()
    uvicorn.run(
        app,
        host=config.api_host,
        port=config.api_port,
        reload=config.api_reload
    )
