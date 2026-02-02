"""
Service Layer
=============
Business logic separated from API layer.
Follows Service-Oriented Architecture principles.
"""

import logging
from typing import Dict, Any, Optional, List
from pathlib import Path

from resume_compiler import ResumeCompiler, RoleType, generate_gap_analysis
from latex_renderer import render_resume
from latex_parser import parse_latex_resume
from ai_agent import create_ai_agent, AIAgent
from exceptions import (
    CompilationError,
    ParsingError,
    RenderingError,
    ValidationError,
    AIError
)
from config import get_config

logger = logging.getLogger(__name__)


class ResumeService:
    """Service for resume compilation and tailoring operations"""
    
    def __init__(self, ai_agent: Optional[AIAgent] = None):
        """
        Initialize resume service
        
        Args:
            ai_agent: Optional AI agent for enhancements
        """
        self.compiler = ResumeCompiler(ai_agent=ai_agent)
        self.config = get_config()
        logger.info("ResumeService initialized")
    
    def parse_latex_resume(self, latex_content: str) -> Dict[str, Any]:
        """
        Parse LaTeX resume to structured format
        
        Args:
            latex_content: LaTeX resume content
            
        Returns:
            Parsed resume dictionary
            
        Raises:
            ParsingError: If parsing fails
        """
        try:
            logger.debug("Parsing LaTeX resume")
            parsed = parse_latex_resume(latex_content)
            
            # Validate parsed data
            if not parsed.get('experience') and not parsed.get('projects'):
                raise ValidationError(
                    "LaTeX resume must contain at least Experience or Projects section with content."
                )
            
            logger.info(f"Parsed {len(parsed.get('experience', []))} experiences, "
                       f"{len(parsed.get('projects', []))} projects")
            return parsed
            
        except Exception as e:
            if isinstance(e, (ValidationError, ParsingError)):
                raise
            logger.error(f"LaTeX parsing failed: {e}", exc_info=True)
            raise ParsingError(f"Failed to parse LaTeX resume: {e}") from e
    
    def compile_resume(
        self,
        master_resume: Dict[str, Any],
        job_description: str,
        enable_ai: bool = False
    ) -> Dict[str, Any]:
        """
        Compile tailored resume from master resume and job description
        
        Args:
            master_resume: Master resume dictionary
            job_description: Job description text
            enable_ai: Whether to enable AI enhancements
            
        Returns:
            Tailored resume dictionary
            
        Raises:
            CompilationError: If compilation fails
        """
        try:
            logger.info(f"Compiling resume (AI enabled: {enable_ai})")
            
            # Handle AI agent
            original_ai_agent = self.compiler.ai_agent
            if enable_ai and not original_ai_agent:
                # Try to initialize AI agent
                ai_agent = self._create_ai_agent()
                if ai_agent:
                    self.compiler.ai_agent = ai_agent
            
            if not enable_ai:
                self.compiler.ai_agent = None
            
            try:
                # Compile
                tailored = self.compiler.compile(master_resume, job_description)
                
                # Validate output
                if not tailored.get('skills') and not tailored.get('experience') and not tailored.get('projects'):
                    raise CompilationError("Compilation produced empty resume")
                
                logger.info(f"Compilation complete: {len(tailored.get('experience', []))} experiences, "
                           f"{len(tailored.get('projects', []))} projects")
                return tailored
                
            finally:
                # Restore original AI agent
                self.compiler.ai_agent = original_ai_agent
                
        except Exception as e:
            if isinstance(e, CompilationError):
                raise
            logger.error(f"Compilation failed: {e}", exc_info=True)
            raise CompilationError(f"Failed to compile resume: {e}") from e
    
    def render_latex(
        self,
        tailored_resume: Dict[str, Any],
        output_path: Optional[Path] = None
    ) -> str:
        """
        Render tailored resume to LaTeX
        
        Args:
            tailored_resume: Tailored resume dictionary
            output_path: Optional output file path
            
        Returns:
            LaTeX content as string
            
        Raises:
            RenderingError: If rendering fails
        """
        try:
            logger.debug("Rendering LaTeX")
            latex_content = render_resume(tailored_resume)
            
            if output_path:
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(latex_content)
                logger.info(f"LaTeX rendered to {output_path}")
            
            return latex_content
            
        except Exception as e:
            logger.error(f"LaTeX rendering failed: {e}", exc_info=True)
            raise RenderingError(f"Failed to render LaTeX: {e}") from e
    
    def analyze_match(
        self,
        master_resume: Dict[str, Any],
        tailored_resume: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyze match between master resume and tailored resume
        
        Args:
            master_resume: Master resume dictionary
            tailored_resume: Tailored resume dictionary
            
        Returns:
            Gap analysis dictionary
        """
        try:
            logger.debug("Analyzing match")
            return generate_gap_analysis(master_resume, tailored_resume)
        except Exception as e:
            logger.error(f"Match analysis failed: {e}", exc_info=True)
            raise CompilationError(f"Failed to analyze match: {e}") from e
    
    def _create_ai_agent(self) -> Optional[AIAgent]:
        """Create AI agent from configuration"""
        try:
            config = get_config()
            if not config.is_ai_available():
                logger.warning("AI not available (no API key or disabled)")
                return None
            
            api_key = config.get_ai_api_key()
            if not api_key:
                logger.warning("No API key available for AI provider")
                return None
            
            agent = create_ai_agent(
                provider=config.ai_provider,
                api_key=api_key,
                enabled=True
            )
            logger.info(f"AI agent created with provider: {config.ai_provider}")
            return agent
            
        except Exception as e:
            logger.warning(f"Failed to create AI agent: {e}")
            return None


class FileService:
    """Service for file operations"""
    
    def __init__(self):
        self.config = get_config()
        self.output_dir = self.config.output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"FileService initialized (output_dir: {self.output_dir})")
    
    def save_latex(self, latex_content: str, filename: str) -> Path:
        """
        Save LaTeX content to file
        
        Args:
            latex_content: LaTeX content
            filename: Output filename
            
        Returns:
            Path to saved file
        """
        file_path = self.output_dir / filename
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(latex_content)
            logger.info(f"LaTeX saved to {file_path}")
            return file_path
        except Exception as e:
            logger.error(f"Failed to save LaTeX file: {e}", exc_info=True)
            raise
    
    def read_latex(self, file_path: Path) -> str:
        """
        Read LaTeX file
        
        Args:
            file_path: Path to LaTeX file
            
        Returns:
            LaTeX content
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Failed to read LaTeX file: {e}", exc_info=True)
            raise
    
    def file_exists(self, filename: str) -> bool:
        """Check if file exists in output directory"""
        return (self.output_dir / filename).exists()
