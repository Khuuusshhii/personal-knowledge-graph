# backend/schemas.py
# Pydantic schemas define the shape of API request bodies and response payloads.
# They are separate from SQLAlchemy models so the API contract is independent
# of the database layer.

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


# ---------------------------------------------------------------------------
# Tag schemas
# ---------------------------------------------------------------------------

class TagResponse(BaseModel):
    """A tag as returned in API responses."""
    id: int
    name: str

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Note summary  (used inside link lists to avoid deep nesting)
# ---------------------------------------------------------------------------

class NoteSummary(BaseModel):
    """Minimal note info — used when listing outgoing links or backlinks."""
    id: int
    title: str

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Note request schemas  (what the client sends)
# ---------------------------------------------------------------------------

class NoteCreate(BaseModel):
    """Body for POST /notes/"""
    title: str
    content: str = ""
    # Tags are sent as plain strings; the backend normalises them before saving.
    tags: List[str] = []


class LinkCreate(BaseModel):
    """Body for PATCH /notes/{note_id}/link"""
    # The ID of the note that the source note should link to.
    target_id: int


# ---------------------------------------------------------------------------
# Note response schemas  (what the server returns)
# ---------------------------------------------------------------------------

class NoteResponse(BaseModel):
    """Note as returned by POST /notes/ and GET /notes/"""
    id: int
    title: str
    content: str
    created_at: datetime
    tags: List[TagResponse]

    model_config = {"from_attributes": True}


class NoteDetailResponse(BaseModel):
    """
    Full note detail as returned by GET /notes/{note_id}.
    Includes both outgoing links (notes this note points to)
    and backlinks (notes that point to this note).
    """
    id: int
    title: str
    content: str
    created_at: datetime
    tags: List[TagResponse]
    outgoing_links: List[NoteSummary]
    backlinks: List[NoteSummary]

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Graph schemas  (returned by GET /graph/)
# ---------------------------------------------------------------------------

class GraphNode(BaseModel):
    """A note represented as a node in the graph."""
    id: int
    title: str


class GraphEdge(BaseModel):
    """A directed link between two notes."""
    source_id: int
    target_id: int


class GraphResponse(BaseModel):
    """All notes as nodes and all links as directed edges."""
    nodes: List[GraphNode]
    edges: List[GraphEdge]
