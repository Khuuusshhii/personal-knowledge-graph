# backend/models.py
# SQLAlchemy ORM models for the Personal Knowledge Graph.
# Each class maps directly to one table in the SQLite database.
#
# Schema (matching the coding challenge exactly):
#   notes     : id, title, content, created_at
#   tags      : id, name
#   note_tags : note_id, tag_id  (many-to-many join table, composite PK)
#   links     : source_id, target_id  (directed graph edges, composite PK)


from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


# ---------------------------------------------------------------------------
# Many-to-many join table: notes ↔ tags
# ---------------------------------------------------------------------------
# We use a plain Table() here instead of a separate class because this table
# only holds foreign keys with no extra columns of its own.
note_tags = Table(
    "note_tags",
    Base.metadata,
    Column("note_id", Integer, ForeignKey("notes.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)


# ---------------------------------------------------------------------------
# Note
# ---------------------------------------------------------------------------
class Note(Base):
    __tablename__ = "notes"
    __table_args__ = {'sqlite_autoincrement': True}

    id = Column(Integer, primary_key=True, index=True)
    title = Column(Text, unique=True, nullable=False)
    content = Column(Text, default="")
    # server_default=func.now() lets SQLite set the timestamp automatically.
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # A note can have many tags (and a tag can belong to many notes).
    tags = relationship("Tag", secondary=note_tags, back_populates="notes")

    # Links where this note is the source (it points to other notes).
    outgoing_links = relationship(
        "NoteLink",
        foreign_keys="NoteLink.source_id",
        back_populates="source",
        cascade="all, delete-orphan",
    )

    # Links where this note is the target (other notes point to it).
    incoming_links = relationship(
        "NoteLink",
        foreign_keys="NoteLink.target_id",
        back_populates="target",
        cascade="all, delete-orphan",
    )


# ---------------------------------------------------------------------------
# Tag
# ---------------------------------------------------------------------------
class Tag(Base):
    __tablename__ = "tags"
    __table_args__ = {'sqlite_autoincrement': True}

    id = Column(Integer, primary_key=True, index=True)
    # Tag names are always normalised (lowercase, stripped) before storage,
    # so the unique constraint works correctly across different spellings.
    name = Column(Text, unique=True, nullable=False)

    notes = relationship("Note", secondary=note_tags, back_populates="tags")


# ---------------------------------------------------------------------------
# NoteLink  (directed edge in the knowledge graph)
# ---------------------------------------------------------------------------
# The Python class is called NoteLink for readability.
# The actual database table is named 'links' to match the challenge schema.
class NoteLink(Base):
    __tablename__ = "links"

    # Composite primary key: (source_id, target_id).
    # This automatically prevents duplicate links at the database level.
    source_id = Column(Integer, ForeignKey("notes.id", ondelete="CASCADE"), primary_key=True)
    target_id = Column(Integer, ForeignKey("notes.id", ondelete="CASCADE"), primary_key=True)

    source = relationship("Note", foreign_keys=[source_id], back_populates="outgoing_links")
    target = relationship("Note", foreign_keys=[target_id], back_populates="incoming_links")
