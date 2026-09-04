# backend/tests/test_notes.py
import pytest

def test_create_and_get_note(client):
    """Test creating a note successfully and retrieving it by ID."""
    response = client.post("/notes/", json={
        "title": "My First Note",
        "content": "This is a test note.",
        "tags": ["Testing"]
    })
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "My First Note"
    assert data["content"] == "This is a test note."
    assert len(data["tags"]) == 1
    assert data["tags"][0]["name"] == "testing" # Tag normalization

    note_id = data["id"]
    get_response = client.get(f"/notes/{note_id}")
    assert get_response.status_code == 200
    assert get_response.json()["id"] == note_id

def test_get_all_notes(client):
    """Test retrieving all notes."""
    client.post("/notes/", json={"title": "Note 1", "content": "Content 1", "tags": []})
    client.post("/notes/", json={"title": "Note 2", "content": "Content 2", "tags": []})
    
    response = client.get("/notes/")
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_search_notes_by_keyword(client):
    """Test searching notes using a keyword in title or content."""
    client.post("/notes/", json={"title": "Apple", "content": "A tasty fruit", "tags": []})
    client.post("/notes/", json={"title": "Banana", "content": "Another fruit", "tags": []})
    client.post("/notes/", json={"title": "Carrot", "content": "A vegetable", "tags": []})
    
    # Keyword 'fruit' should match Apple and Banana
    response = client.get("/notes/?keyword=fruit")
    assert response.status_code == 200
    assert len(response.json()) == 2
    
    # Keyword 'Carrot' should match Carrot
    response2 = client.get("/notes/?keyword=Carrot")
    assert response2.status_code == 200
    assert len(response2.json()) == 1

def test_filter_notes_by_tag(client):
    """Test filtering notes using a tag."""
    client.post("/notes/", json={"title": "Python Basics", "content": "...", "tags": ["python"]})
    client.post("/notes/", json={"title": "Java Basics", "content": "...", "tags": ["java"]})
    
    response = client.get("/notes/?tag=python")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Python Basics"

def test_tag_normalization_and_deduplication(client):
    """
    Test that tags are normalized (whitespace stripped, lowercased) and
    equivalent tags do not create duplicate records.
    """
    client.post("/notes/", json={
        "title": "Note A",
        "content": "...",
        "tags": ["  Python  ", "python", "PYTHON"]
    })
    
    tags_response = client.get("/notes/tags/all")
    assert tags_response.status_code == 200
    tags = tags_response.json()
    
    # Even though 3 variations were passed, only 1 unique tag should be created
    assert len(tags) == 1
    assert tags[0]["name"] == "python"

def test_automatic_linking(client):
    """
    Test that creating a note containing [[Existing Note Title]] creates a link,
    and a referenced note correctly shows the source note as a backlink.
    """
    # Create the target note
    resp1 = client.post("/notes/", json={"title": "Target Note", "content": "...", "tags": []})
    target_id = resp1.json()["id"]
    
    # Create the source note with a wiki-link
    resp2 = client.post("/notes/", json={"title": "Source Note", "content": "Check out [[Target Note]] for info.", "tags": []})
    source_id = resp2.json()["id"]
    
    # Check that source note has an outgoing link to target note
    source_detail = client.get(f"/notes/{source_id}").json()
    assert len(source_detail["outgoing_links"]) == 1
    assert source_detail["outgoing_links"][0]["title"] == "Target Note"
    
    # Check that target note has a backlink from source note
    target_detail = client.get(f"/notes/{target_id}").json()
    assert len(target_detail["backlinks"]) == 1
    assert target_detail["backlinks"][0]["title"] == "Source Note"

def test_repeated_references_do_not_duplicate_links(client):
    """Test that referencing the same [[Note Title]] multiple times does not create duplicate links."""
    client.post("/notes/", json={"title": "Target", "content": "...", "tags": []})
    
    resp = client.post("/notes/", json={
        "title": "Source",
        "content": "Link 1: [[Target]], Link 2: [[Target]]",
        "tags": []
    })
    source_id = resp.json()["id"]
    
    source_detail = client.get(f"/notes/{source_id}").json()
    # Should only have 1 outgoing link, not 2
    assert len(source_detail["outgoing_links"]) == 1

def test_missing_note_reference_does_not_crash(client):
    """Test that a [[Missing Note]] reference does not crash note creation."""
    resp = client.post("/notes/", json={
        "title": "Source",
        "content": "This links to a [[Ghost Note]] that doesn't exist.",
        "tags": []
    })
    assert resp.status_code == 201
    note_id = resp.json()["id"]
    
    # Retrieve detail to verify outgoing_links is empty
    detail_resp = client.get(f"/notes/{note_id}")
    assert len(detail_resp.json()["outgoing_links"]) == 0
