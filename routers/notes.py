# backend/routers/notes.py
# Route handlers for all note-related API endpoints.
# Each handler validates input, calls a crud function, and returns a response.

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

import crud
import schemas
from database import get_db

router = APIRouter(prefix="/notes", tags=["notes"])


# ---------------------------------------------------------------------------
# POST /notes/  — Create a note
# ---------------------------------------------------------------------------
@router.post("/", response_model=schemas.NoteResponse, status_code=status.HTTP_201_CREATED)
def create_note(note_data: schemas.NoteCreate, db: Session = Depends(get_db)):
    """
    Create a new note with a title, content, and optional tags.

    Business logic that runs automatically:
      - Tags are normalised (stripped and lowercased) before being saved.
      - The content is scanned for [[Note Title]] patterns; any titles that
        match an existing note are automatically turned into outgoing links.
    """
    try:
        new_note = crud.create_note(db, note_data)
        return new_note
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="A note with this title already exists."
        )


# ---------------------------------------------------------------------------
# GET /notes/tags/all  — Tag suggestions (used by the frontend)
# IMPORTANT: This STATIC route must be registered BEFORE GET /{note_id},
# otherwise FastAPI will try to cast the literal string "tags" as an integer
# and return a 422 Unprocessable Entity error instead of calling this handler.
# ---------------------------------------------------------------------------
@router.get("/tags/all", response_model=list[schemas.TagResponse], tags=["tags"])
def list_all_tags(db: Session = Depends(get_db)):
    """
    Return every existing tag, alphabetically sorted.
    Used by the frontend to populate the tag filter dropdown.
    """
    return crud.get_all_tags(db)


# ---------------------------------------------------------------------------
# GET /notes/  — List all notes (with optional filters)
# ---------------------------------------------------------------------------
@router.get("/", response_model=list[schemas.NoteResponse])
def list_notes(
    tag: str | None = Query(default=None, description="Filter notes by tag name"),
    keyword: str | None = Query(default=None, description="Filter notes by keyword in title or content"),
    db: Session = Depends(get_db),
):
    """
    Return all notes, newest first.

    Optional query parameters:
      - ?tag=python     → only notes tagged 'python'
      - ?keyword=graph  → only notes whose title or content contains 'graph'
      - Both filters can be combined (AND logic).
    """
    notes = crud.get_notes(db, tag=tag, keyword=keyword)
    return notes


# ---------------------------------------------------------------------------
# GET /notes/{note_id}  — Get a single note with links and backlinks
# ---------------------------------------------------------------------------
@router.get("/{note_id}", response_model=schemas.NoteDetailResponse)
def get_note(note_id: int, db: Session = Depends(get_db)):
    """
    Return full details for one note, including:
      - outgoing_links: notes that this note links to
      - backlinks:      notes that link TO this note

    Backlinks are computed by finding all NoteLinks where target_id == note_id.
    """
    note = crud.get_note_by_id(db, note_id)
    if note is None:
        raise HTTPException(status_code=404, detail=f"Note with id={note_id} not found.")

    # Build the outgoing links list from the note's relationship.
    outgoing = [schemas.NoteSummary(id=lnk.target.id, title=lnk.target.title)
                for lnk in note.outgoing_links]

    # Backlinks require a separate query (see crud.get_backlinks).
    backlink_notes = crud.get_backlinks(db, note_id)
    backlinks = [schemas.NoteSummary(id=n.id, title=n.title) for n in backlink_notes]

    return schemas.NoteDetailResponse(
        id=note.id,
        title=note.title,
        content=note.content,
        created_at=note.created_at,
        tags=[schemas.TagResponse(id=t.id, name=t.name) for t in note.tags],
        outgoing_links=outgoing,
        backlinks=backlinks,
    )


# ---------------------------------------------------------------------------
# PATCH /notes/{note_id}/link  — Manually link one note to another
# ---------------------------------------------------------------------------
@router.patch("/{note_id}/link", response_model=schemas.NoteDetailResponse)
def link_notes(
    note_id: int,
    link_data: schemas.LinkCreate,
    db: Session = Depends(get_db),
):
    """
    Create a manual directed link from note_id → link_data.target_id.

    Rules enforced:
      - A note cannot link to itself (self-link prevention).
      - Duplicate links are silently ignored (idempotent — returns the note
        unchanged rather than raising an error, which is friendlier for the UI).
      - Both notes must exist (404 if either is missing).
    """
    # Self-link check before hitting the database.
    if note_id == link_data.target_id:
        raise HTTPException(
            status_code=400,
            detail="A note cannot link to itself.",
        )

    try:
        crud.create_manual_link(db, source_id=note_id, target_id=link_data.target_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    # Return the updated note detail (same shape as GET /notes/{note_id}).
    note = crud.get_note_by_id(db, note_id)
    outgoing = [schemas.NoteSummary(id=lnk.target.id, title=lnk.target.title)
                for lnk in note.outgoing_links]
    backlink_notes = crud.get_backlinks(db, note_id)
    backlinks = [schemas.NoteSummary(id=n.id, title=n.title) for n in backlink_notes]

    return schemas.NoteDetailResponse(
        id=note.id,
        title=note.title,
        content=note.content,
        created_at=note.created_at,
        tags=[schemas.TagResponse(id=t.id, name=t.name) for t in note.tags],
        outgoing_links=outgoing,
        backlinks=backlinks,
    )
