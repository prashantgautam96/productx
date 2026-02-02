"""
Custom Exceptions
================
Domain-specific exceptions for better error handling and separation of concerns.
"""


class ResumeOSError(Exception):
    """Base exception for all ResumeOS errors"""
    pass


class CompilationError(ResumeOSError):
    """Error during resume compilation"""
    pass


class ParsingError(ResumeOSError):
    """Error parsing input data (LaTeX, JSON, etc.)"""
    pass


class RenderingError(ResumeOSError):
    """Error rendering output (LaTeX, PDF, etc.)"""
    pass


class ValidationError(ResumeOSError):
    """Input validation error"""
    pass


class AIError(ResumeOSError):
    """AI-related error (quota, API, etc.)"""
    pass


class ConfigurationError(ResumeOSError):
    """Configuration error"""
    pass


class FileOperationError(ResumeOSError):
    """File operation error"""
    pass
