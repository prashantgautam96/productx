"""
Authentication helpers
======================
Password hashing + JWT utilities.
"""

from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from config import get_config
from db import get_db
from models import User


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
oauth2_scheme_optional = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, password_hash: str) -> bool:
    return pwd_context.verify(plain_password, password_hash)


def create_access_token(subject: str, expires_minutes: Optional[int] = None) -> str:
    config = get_config()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes or config.jwt_expires_minutes)
    to_encode = {"sub": subject, "exp": expire}
    return jwt.encode(to_encode, config.jwt_secret, algorithm=config.jwt_algorithm)


def _get_user_from_token(token: str, db: Session) -> User:
    config = get_config()
    try:
        payload = jwt.decode(token, config.jwt_secret, algorithms=[config.jwt_algorithm])
        subject = payload.get("sub")
        if subject is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except JWTError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc

    user = db.query(User).filter(User.email == subject).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    return _get_user_from_token(token, db)


def get_optional_user(
    token: Optional[str] = Depends(oauth2_scheme_optional),
    db: Session = Depends(get_db)
) -> Optional[User]:
    if not token:
        return None
    return _get_user_from_token(token, db)
