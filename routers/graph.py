# backend/routers/graph.py
# Route handler for the knowledge graph endpoint.

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import crud
import schemas
from database import get_db

router = APIRouter(prefix="/graph", tags=["graph"])


# ---------------------------------------------------------------------------
# GET /graph/  — Return the full note-link graph
# ---------------------------------------------------------------------------
@router.get("/", response_model=schemas.GraphResponse)
def get_graph(db: Session = Depends(get_db)):
    """
    Return the entire knowledge graph as a set of nodes and edges.

    - nodes: every note, represented as { id, title }
    - edges: every link, represented as { source_id, target_id }

    The frontend uses this data to render a text-based graph map.
    Advanced visualisation libraries (e.g. D3, Cytoscape) can also
    consume this format.
    """
    return crud.get_graph(db)
