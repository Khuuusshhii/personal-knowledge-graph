# backend/tests/conftest.py
# Shared pytest fixtures.
# An in-memory SQLite database is used for tests so they never
# touch the real database file.

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, pool
from sqlalchemy.orm import sessionmaker

import sys
import os
# Ensure backend directory is in the path to import main and database
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database import Base, get_db
from main import app

# Use an in-memory SQLite database. StaticPool ensures FastAPI threads share the connection.
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=pool.StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database for each test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    """Provide a TestClient that overrides the get_db dependency to use the test session."""
    def override_get_db():
        yield db_session
            
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
