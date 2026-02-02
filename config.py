"""
Configuration Management
=======================
Centralized configuration using environment variables with sensible defaults.
Follows 12-factor app principles.
"""

import os
from typing import Optional
from dataclasses import dataclass
from pathlib import Path


@dataclass
class AppConfig:
    """Application configuration"""
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = False
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # File Paths
    output_dir: Path = Path("output")
    static_dir: Path = Path("static")
    
    # AI Configuration
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    ai_provider: str = "openai"  # "openai" or "anthropic"
    ai_model: str = "gpt-4o-mini"
    ai_enabled: bool = True
    ai_max_tokens: int = 200
    ai_temperature: float = 0.3
    
    # Compiler Configuration
    max_bullets_per_experience: int = 6
    max_skills: int = 20
    min_match_score_threshold: float = 0.0

    # Database Configuration
    database_url: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/resumeos"

    # Auth / JWT
    jwt_secret: str = "change-me"
    jwt_algorithm: str = "HS256"
    jwt_expires_minutes: int = 60
    
    @classmethod
    def from_env(cls) -> "AppConfig":
        """Load configuration from environment variables"""
        # Load .env file if it exists
        env_file = Path(".env")
        if env_file.exists():
            cls._load_env_file(env_file)
        
        return cls(
            # API
            api_host=os.getenv("API_HOST", "0.0.0.0"),
            api_port=int(os.getenv("API_PORT", "8000")),
            api_reload=os.getenv("API_RELOAD", "false").lower() == "true",
            
            # Logging
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            log_format=os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"),
            
            # Paths
            output_dir=Path(os.getenv("OUTPUT_DIR", "output")),
            static_dir=Path(os.getenv("STATIC_DIR", "static")),
            
            # AI
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
            ai_provider=os.getenv("AI_PROVIDER", "openai"),
            ai_model=os.getenv("AI_MODEL", "gpt-4o-mini"),
            ai_enabled=os.getenv("AI_ENABLED", "true").lower() == "true",
            ai_max_tokens=int(os.getenv("AI_MAX_TOKENS", "200")),
            ai_temperature=float(os.getenv("AI_TEMPERATURE", "0.3")),
            
            # Compiler
            max_bullets_per_experience=int(os.getenv("MAX_BULLETS_PER_EXPERIENCE", "6")),
            max_skills=int(os.getenv("MAX_SKILLS", "20")),
            min_match_score_threshold=float(os.getenv("MIN_MATCH_SCORE_THRESHOLD", "0.0")),

            # Database
            database_url=os.getenv(
                "DATABASE_URL",
                "postgresql+psycopg2://postgres:postgres@localhost:5432/resumeos"
            ),

            # Auth / JWT
            jwt_secret=os.getenv("JWT_SECRET", "change-me"),
            jwt_algorithm=os.getenv("JWT_ALGORITHM", "HS256"),
            jwt_expires_minutes=int(os.getenv("JWT_EXPIRES_MINUTES", "60")),
        )
    
    @staticmethod
    def _load_env_file(env_file: Path) -> None:
        """Load environment variables from .env file"""
        with open(env_file, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    # Handle both "export KEY=value" and "KEY=value" formats
                    if line.startswith("export "):
                        line = line[7:]  # Remove "export "
                    key, value = line.split("=", 1)
                    # Remove quotes if present
                    value = value.strip('"').strip("'")
                    os.environ[key.strip()] = value
    
    def get_ai_api_key(self) -> Optional[str]:
        """Get API key for configured AI provider"""
        if self.ai_provider == "openai":
            return self.openai_api_key
        elif self.ai_provider == "anthropic":
            return self.anthropic_api_key
        return None
    
    def is_ai_available(self) -> bool:
        """Check if AI is configured and available"""
        return self.ai_enabled and self.get_ai_api_key() is not None


# Global configuration instance
_config: Optional[AppConfig] = None


def get_config() -> AppConfig:
    """Get global configuration instance (singleton)"""
    global _config
    if _config is None:
        _config = AppConfig.from_env()
    return _config


def reset_config() -> None:
    """Reset configuration (useful for testing)"""
    global _config
    _config = None
