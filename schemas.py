"""
API schemas
===========
"""

from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
    email: str = Field(..., min_length=3)
    password: str = Field(..., min_length=8)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: int
    email: str
    created_at: datetime


class MasterResumeCreateResponse(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime
    master_resume: Dict[str, Any]


class MasterResumeListItem(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime


class MasterResumeFromLatexRequest(BaseModel):
    latex_resume: str
