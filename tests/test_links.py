# backend/tests/test_links.py
import pytest

def test_manual_linking(client):
    """Test that manually linking two notes creates a link."""
    # Create source and target notes
    resp1 = client.post("/notes/", json={"title": "Source Note", "content": "...", "tags": []})
    source_id = resp1.json()["id"]
    
    resp2 = client.post("/notes/", json={"title": "Target Note", "content": "...", "tags": []})
    target_id = resp2.json()["id"]
    
    # Create a link
    link_resp = client.patch(f"/notes/{source_id}/link", json={"target_id": target_id})
    assert link_resp.status_code == 200
    
    # Verify link was created
    note_detail = link_resp.json()
    assert len(note_detail["outgoing_links"]) == 1
    assert note_detail["outgoing_links"][0]["title"] == "Target Note"

def test_link_to_nonexistent_note(client):
    """Test that linking to a non-existent note returns 404."""
    resp1 = client.post("/notes/", json={"title": "Source Note", "content": "...", "tags": []})
    source_id = resp1.json()["id"]
    
    link_resp = client.patch(f"/notes/{source_id}/link", json={"target_id": 9999})
    assert link_resp.status_code == 404

def test_duplicate_links_rejected(client):
    """Test that duplicate links are ignored (idempotent response)."""
    resp1 = client.post("/notes/", json={"title": "Source Note", "content": "...", "tags": []})
    source_id = resp1.json()["id"]
    
    resp2 = client.post("/notes/", json={"title": "Target Note", "content": "...", "tags": []})
    target_id = resp2.json()["id"]
    
    # Create the link once
    client.patch(f"/notes/{source_id}/link", json={"target_id": target_id})
    
    # Attempt to create it again
    link_resp = client.patch(f"/notes/{source_id}/link", json={"target_id": target_id})
    assert link_resp.status_code == 200
    
    # Verify only one link exists
    note_detail = link_resp.json()
    assert len(note_detail["outgoing_links"]) == 1

def test_self_link_prevention(client):
    """Test that a note cannot link to itself."""
    resp1 = client.post("/notes/", json={"title": "Self Note", "content": "...", "tags": []})
    source_id = resp1.json()["id"]
    
    link_resp = client.patch(f"/notes/{source_id}/link", json={"target_id": source_id})
    assert link_resp.status_code == 400
    assert "cannot link to itself" in link_resp.json()["detail"]

def test_graph_endpoint(client):
    """Test that the graph endpoint returns all notes as nodes and links as edges."""
    resp1 = client.post("/notes/", json={"title": "Node A", "content": "...", "tags": []})
    id_a = resp1.json()["id"]
    
    resp2 = client.post("/notes/", json={"title": "Node B", "content": "...", "tags": []})
    id_b = resp2.json()["id"]
    
    # Create link from A -> B
    client.patch(f"/notes/{id_a}/link", json={"target_id": id_b})
    
    graph_resp = client.get("/graph/")
    assert graph_resp.status_code == 200
    data = graph_resp.json()
    
    # Ensure nodes A and B are in the graph
    node_ids = [node["id"] for node in data["nodes"]]
    assert id_a in node_ids
    assert id_b in node_ids
    
    # Ensure edge A -> B is in the graph
    edges = data["edges"]
    assert {"source_id": id_a, "target_id": id_b} in edges
