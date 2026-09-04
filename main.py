# backend/main.py
# Entry point for the FastAPI application.
# Registers all routers and configures CORS so the React frontend
# (running on a different port) can talk to the API.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import notes, graph

app = FastAPI(
    title="Personal Knowledge Graph API",
    description="A note-based knowledge graph with bi-directional links and tags.",
    version="1.0.0",
)

# Allow the React dev server (port 5173 by default with Vite) to call the API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers — each router handles a group of related endpoints.
app.include_router(notes.router)
app.include_router(graph.router)


@app.get("/")
def root():
    """Health-check endpoint."""
    return {"status": "ok", "message": "Personal Knowledge Graph API is running."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)