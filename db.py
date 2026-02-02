"""
Database setup
==============
SQLAlchemy engine/session helpers for Postgres.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import get_config


def _get_database_url() -> str:
    config = get_config()
    return config.database_url


engine = create_engine(
    _get_database_url(),
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    from models import Base
    Base.metadata.create_all(bind=engine)
