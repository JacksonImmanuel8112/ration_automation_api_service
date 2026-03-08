"""
Database engine, session factory, and Base declarative class.
All models should inherit from Base so Alembic can detect them.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from dotenv import load_dotenv
import os

load_dotenv()


# Create the SQLAlchemy engine
engine = create_engine(
    os.getenv('DATABASE_URL'),
    pool_pre_ping=True,      # Verify connections before use
    pool_size=10,
    max_overflow=20,
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Base class shared by all ORM models."""
    pass


def get_db():
    """
    FastAPI dependency that yields a database session and
    ensures it is closed after the request is complete.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
