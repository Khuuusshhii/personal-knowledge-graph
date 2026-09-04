# backend/crud.py
# Database helper functions — all database reads and writes live here.
# Route handlers call these functions instead of talking to the DB directly,
# which keeps the routes thin and easy to test.

import re
from sqlalchemy.orm import Session

import models
import schemas


# ---------------------------------------------------------------------------
# Tag normalisation
# ---------------------------------------------------------------------------
# TAG NORMALISATION EXPLAINED:
#   The challenge requires tags to be normalised so that 'Python', ' python ',
#   and 'PYTHON' all map to the same tag row.  We normalise every tag before
#   saving it and before querying by tag.  This means the unique constraint on
#   tags.name works reliably regardless of how the user types the tag.

def normalize_tag(raw_name: str) -> str:
    """
    Normalise a tag name:
      1. strip()  — remove leading and trailing whitespace.
      2. lower()  — convert to lowercase.

    Examples:
      '  Python  '  ->  'python'
      'MACHINE-LEARNING'  ->  'machine-learning'
      'database '  ->  'database'
    """
    return raw_name.strip().lower()


def get_or_create_tag(db: Session, raw_name: str) -> models.Tag:
    """
    Look up a Tag by its normalised name.  If no Tag exists yet, create one.

    The get-or-create pattern guarantees we never insert two rows with the
    same normalised name (which would violate the unique constraint on tags.name).
    We use db.flush() after creating a new tag so that SQLAlchemy assigns it
    an ID immediately — the ID is needed when we attach the tag to a note
    within the same transaction.
    """
    name = normalize_tag(raw_name)

    # Try to find an existing tag with this exact normalised name.
    tag = db.query(models.Tag).filter(models.Tag.name == name).first()

    if tag is None:
        # Tag does not exist yet — create it.
        tag = models.Tag(name=name)
        db.add(tag)
        # flush() writes the INSERT to the DB within the current transaction
        # so the tag gets a primary-key ID before we return it.
        db.flush()

    return tag


def get_all_tags(db: Session) -> list[models.Tag]:
    """Return every tag in alphabetical order.  Used by the frontend for tag suggestions."""
    return db.query(models.Tag).order_by(models.Tag.name).all()


# ---------------------------------------------------------------------------
# Automatic [[wiki link]] resolution
# ---------------------------------------------------------------------------
# WIKI-LINK EXPLAINED:
#   When a note is created, its content is scanned for patterns like:
#     [[Python Programming]]
#   If a note titled "Python Programming" exists, a directed link is automatically
#   created from the new note to that note.  This mirrors how Obsidian and
#   Roam Research work.
#
#   The regex used is:  \[\[([^\]\n]+)\]\]
#     \[\[         — literal opening [[
#     ([^\]\n]+)   — capture group: one or more chars that are not ] or newline
#     \]\]         — literal closing ]]
#
#   This is called inside create_note(), after the note has been flushed to the
#   DB so it already has an ID (required before creating links).

def resolve_wiki_links(db: Session, note: models.Note) -> None:
    """
    Scan note.content for [[Title]] patterns and auto-create links.

    For each matched title:
      - Query the DB for a note whose title matches exactly.
      - If found, try to create a link via _create_link_if_valid().
        That helper handles self-links and duplicates silently.
      - If no matching note is found, the [[Title]] is left in the content as-is.

    This function only creates links; it never modifies the note content.
    """
    # Compile the regex once (could be extracted to a module-level constant,
    # but keeping it here makes this function self-contained and easy to read).
    wiki_pattern = re.compile(r"\[\[([^\]\n]+)\]\]")

    # findall() returns a list of captured group strings, e.g. ['Python Programming', 'Data Structures']
    matched_titles = wiki_pattern.findall(note.content)

    for title in matched_titles:
        # Strip any accidental whitespace inside the brackets.
        title = title.strip()

        # Look for a note whose title exactly matches.  Case-sensitive, because
        # note titles are user-defined and [[Python]] and [[python]] could be
        # intentionally different.
        target = db.query(models.Note).filter(models.Note.title == title).first()

        if target is not None:
            # A matching note exists — create the link (if valid).
            _create_link_if_valid(db, source_id=note.id, target_id=target.id)
        # If no matching note is found, we silently skip — no error raised.


# ---------------------------------------------------------------------------
# Link creation — shared by automatic resolution and manual linking
# ---------------------------------------------------------------------------
# SELF-LINK AND DUPLICATE PREVENTION EXPLAINED:
#
#   Self-link prevention:
#     A note linking to itself would create a meaningless loop.  We check
#     source_id == target_id and return None immediately if true.
#     The PATCH route handler also checks this before calling crud, so the
#     user receives a clear 400 error message rather than a silent skip.
#
#   Duplicate-link prevention:
#     The `links` table uses (source_id, target_id) as a composite primary key,
#     so the database itself would reject a duplicate INSERT with an IntegrityError.
#     We do an explicit SELECT first so we can return None gracefully instead of
#     letting an exception bubble up.  This makes the PATCH endpoint idempotent:
#     calling it twice with the same pair simply returns the note unchanged.

def _create_link_if_valid(db: Session, source_id: int, target_id: int) -> models.NoteLink | None:
    """
    Try to create a directed link (source_id -> target_id).

    Returns the new NoteLink object if successful.
    Returns None (without raising) if:
      - source_id == target_id  (self-link — a note must not link to itself)
      - the link already exists  (duplicate — idempotent behaviour)

    NOTE: This function does NOT commit the transaction.  The caller is
    responsible for calling db.commit() after all operations are complete.
    """
    # --- Self-link check ---
    # A note linking to itself would create an infinite loop in the graph.
    if source_id == target_id:
        return None  # Silently skip self-links.

    # --- Duplicate check ---
    # Query for an existing row with the same (source_id, target_id) pair.
    existing = (
        db.query(models.NoteLink)
        .filter(
            models.NoteLink.source_id == source_id,
            models.NoteLink.target_id == target_id,
        )
        .first()
    )
    if existing is not None:
        return None  # Link already exists — silently skip.

    # Both checks passed: create and stage the new link row.
    link = models.NoteLink(source_id=source_id, target_id=target_id)
    db.add(link)
    # Flush immediately so the next call to _create_link_if_valid within the
    # same session can find this row in the duplicate check query above.
    # Without flush(), the row only lives in the ORM identity map and is
    # invisible to a subsequent SELECT in the same transaction.
    db.flush()
    return link


# ---------------------------------------------------------------------------
# Note CRUD
# ---------------------------------------------------------------------------

def create_note(db: Session, note_data: schemas.NoteCreate) -> models.Note:
    """
    Create a new note with tags and automatic wiki-link resolution.

    Transaction steps (all in one commit):
      1. Create the Note row and flush to get its ID.
      2. Normalise each tag string and attach it to the note via get_or_create_tag().
      3. Scan the content for [[Title]] patterns and create links to matching notes.
      4. Commit everything — notes, tags, note_tags rows, and link rows — in one go.
    """
    # Step 1: create the note and flush so it gets a primary-key ID.
    # We need the ID before creating links or attaching tags.
    note = models.Note(title=note_data.title, content=note_data.content)
    db.add(note)
    db.flush()

    # Step 2: normalise and attach tags.
    # get_or_create_tag handles the case where a tag already exists.
    # The `if tag not in note.tags` guard prevents the same tag being
    # appended twice if the caller sends duplicate strings in the list.
    for raw_tag in note_data.tags:
        tag = get_or_create_tag(db, raw_tag)
        if tag not in note.tags:
            note.tags.append(tag)

    # Step 3: auto-resolve [[wiki links]] found in the note content.
    resolve_wiki_links(db, note)

    # Step 4: commit everything and refresh the note so its relationships
    # (tags, links) are available on the returned object.
    db.commit()
    db.refresh(note)
    return note


def get_notes(
    db: Session,
    tag: str | None = None,
    keyword: str | None = None,
) -> list[models.Note]:
    """
    Return all notes, newest first, with optional filters.

    tag filter:
      Normalise the requested tag name, then join notes -> note_tags -> tags
      and filter by tags.name.  Normalising the query value ensures
      ?tag=Python matches the stored 'python' row.

    keyword filter:
      Use SQLAlchemy's ilike() (case-insensitive LIKE) to search both the
      title and content columns.  The % wildcards match any surrounding text.

    Both filters can be combined (AND logic — both must match).
    """
    query = db.query(models.Note)

    if tag:
        # Normalise the tag query the same way tags are normalised on creation.
        normalised = normalize_tag(tag)
        query = (
            query
            # Join through the note_tags association table.
            .join(models.note_tags, models.Note.id == models.note_tags.c.note_id)
            .join(models.Tag, models.Tag.id == models.note_tags.c.tag_id)
            .filter(models.Tag.name == normalised)
        )

    if keyword:
        like_pattern = f"%{keyword}%"
        # ilike() is case-insensitive — works for ASCII on SQLite.
        query = query.filter(
            models.Note.title.ilike(like_pattern)
            | models.Note.content.ilike(like_pattern)
        )

    return query.order_by(models.Note.created_at.desc()).all()


def get_note_by_id(db: Session, note_id: int) -> models.Note | None:
    """
    Return a single note by its primary key, or None if not found.
    SQLAlchemy lazily loads the related tags and links when they are first
    accessed (e.g. in the route handler when building the response).
    """
    return db.query(models.Note).filter(models.Note.id == note_id).first()


# ---------------------------------------------------------------------------
# Backlink lookup
# ---------------------------------------------------------------------------
# BACKLINKS EXPLAINED:
#   A backlink of note B is any note A that has an outgoing link pointing TO B.
#   In the `links` table this means: find all rows where target_id = B,
#   then return the notes whose IDs appear in the source_id column.
#
#   Example:
#     links table contains: (source_id=2, target_id=1)
#     This means note 2 links to note 1.
#     So note 2 is a *backlink* of note 1.
#
#   The query joins notes ON links.source_id = notes.id, then filters
#   WHERE links.target_id = note_id.  This gives us all notes that point at
#   the requested note.

def get_backlinks(db: Session, note_id: int) -> list[models.Note]:
    """
    Return all notes that contain an outgoing link pointing TO note_id.

    These are the backlinks of note_id — notes that reference it.
    """
    return (
        db.query(models.Note)
        # Join the links table: we want notes where the note is the SOURCE
        # of a link that targets note_id.
        .join(models.NoteLink, models.NoteLink.source_id == models.Note.id)
        .filter(models.NoteLink.target_id == note_id)
        .all()
    )


# ---------------------------------------------------------------------------
# Manual link creation (called from PATCH /notes/{id}/link)
# ---------------------------------------------------------------------------

def create_manual_link(
    db: Session,
    source_id: int,
    target_id: int,
) -> models.NoteLink | None:
    """
    Create a directed link from source_id to target_id.

    Validates that both notes exist first (raises ValueError if not).
    Then delegates to _create_link_if_valid() which handles:
      - self-link prevention  (source_id == target_id  ->  returns None)
      - duplicate prevention  (link already exists  ->  returns None)

    The route handler (PATCH /notes/{id}/link) raises HTTP 400 for self-links
    before this function is called, but _create_link_if_valid is a second safety net.
    """
    # Verify the source note exists.
    source = db.query(models.Note).filter(models.Note.id == source_id).first()
    if source is None:
        raise ValueError(f"Source note with id={source_id} not found.")

    # Verify the target note exists.
    target = db.query(models.Note).filter(models.Note.id == target_id).first()
    if target is None:
        raise ValueError(f"Target note with id={target_id} not found.")

    # Attempt to create the link (handles duplicates and self-links silently).
    link = _create_link_if_valid(db, source_id=source_id, target_id=target_id)
    db.commit()
    return link


# ---------------------------------------------------------------------------
# Graph
# ---------------------------------------------------------------------------

def get_graph(db: Session) -> schemas.GraphResponse:
    """
    Assemble the full knowledge graph for the GET /graph/ endpoint.

    - nodes: all notes, each represented as { id, title }
    - edges: all rows in the `links` table, each as { source_id, target_id }

    The frontend renders this as a text-based or visual graph map.
    """
    all_notes = db.query(models.Note).all()
    all_links = db.query(models.NoteLink).all()

    nodes = [schemas.GraphNode(id=n.id, title=n.title) for n in all_notes]
    edges = [
        schemas.GraphEdge(source_id=lnk.source_id, target_id=lnk.target_id)
        for lnk in all_links
    ]

    return schemas.GraphResponse(nodes=nodes, edges=edges)
