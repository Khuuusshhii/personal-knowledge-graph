# backend/database.py
# Sets up the SQLAlchemy engine and session factory.
# All other modules import `SessionLocal` and `Base` from here.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite database file will be created in the backend directory.
DATABASE_URL = "sqlite:///./knowledge_graph.db"

# `connect_args` is required for SQLite so the same connection can be
# used across multiple threads (FastAPI runs request handlers concurrently).
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# Each request will get its own database session via this factory.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# All SQLAlchemy models inherit from this base class.
Base = declarative_base()


def get_db():
    """
    FastAPI dependency that provides a database session per request.
    The session is always closed after the request finishes, even on error.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
