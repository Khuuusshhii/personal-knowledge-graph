# Personal Knowledge Graph System

A full-stack web application for creating, connecting, and exploring personal notes as a knowledge graph. Notes can be linked automatically using `[[Note Title]]` references or connected manually through the UI.

---------------------------------------------------------------------------------------------------------

## What the Project Does

- **Write notes** with a title, body, and optional tags.
- **Link notes automatically** by writing `[[Note Title]]` anywhere in note content. On creation, the backend scans for these patterns and creates directed links to matching notes.
- **Browse backlinks** — every note shows which other notes point to it.
- **Search and filter** notes by keyword or tag.
- **View the knowledge graph** as a text-based node and edge map.
- **Toggle between light and dark mode.**

---------------------------------------------------------------------------------------------------------

## Main Features

|               Feature                 |                 Description                              |
|---------------------------------------|----------------------------------------------------------|
| Create notes                          | Title, markdown body, and optional tags                  |
| Tag normalization                     | Tags are lowercased and stripped before saving           |
| Keyword search                        | Case-insensitive search across title and content         |
| Tag filter                            | Filter the note list by a specific tag                   |
| Note detail view                      | Full content, outgoing links, and backlinks              |
| Auto `[[Note Title]]` linking         | Wiki-style references auto-create links on note creation |
| Manual linking                        | Link any two notes from the detail page                  |
| Self-link prevention                  | A note cannot link to itself (HTTP 400)                  |
| Duplicate link prevention             | Creating the same link twice is silently ignored         |
| Graph view                            | Text-based map of all notes and connections              |
| Markdown rendering                    | Note bodies rendered via react-markdown                  |
| Light/Dark mode                       | One-click toggle, persisted to localStorage              |
| Unique note titles                    | Duplicate titles rejected with HTTP 400                  |
| Tag suggestions                       | Tag dropdown populated from all existing tags            |

--------------------------------------------------------------------------------------------------------

## Technology Stack

| Component                 | Technology                  |
|---------------------------|-----------------------------|
| Backend language          | Python 3.10+                |
| API framework             | FastAPI                     |
| ORM                       | SQLAlchemy 2.x              |
| Database                  | SQLite                      |
| Migrations                | Alembic                     |
| Validation                | Pydantic 2.x                |
| ASGI server               | Uvicorn                     |
| Testing                   | Pytest + FastAPI TestClient |
| Frontend                  | React 19, Vite              |
| HTTP client               | Axios                       |
| Markdown                  | react-markdown              |
| Styling                   | Vanilla CSS + CSS Variables |
| SDK generation            | OpenAPI Generator CLI       |

--------------------------------------------------------------------------------------------------------

## Project Structure

All backend files live at the project root alongside `frontend/` and `knowledge_sdk/`.

```
personal-knowledge-graph/
├── alembic/                    # Alembic migration environment
│   └── versions/               # Migration scripts
├── routers/
│   ├── notes.py                # Route handlers for /notes/
│   └── graph.py                # Route handler for /graph/
├── tests/
│   ├── conftest.py             # Pytest fixtures (in-memory DB + TestClient)
│   ├── test_notes.py           # Note creation, retrieval, tags, auto-linking
│   └── test_links.py           # Manual linking, self-links, duplicates, graph
├── frontend/                   # React frontend (Vite)
│   ├── src/
│   │   ├── components/
│   │   │   ├── NoteList.jsx
│   │   │   ├── NoteForm.jsx
│   │   │   ├── NoteDetail.jsx
│   │   │   ├── LinkForm.jsx
│   │   │   └── GraphView.jsx
│   │   ├── api.js
│   │   ├── App.jsx
│   │   └── index.css
│   └── package.json
├── knowledge_sdk/              # Auto-generated Python SDK
│   ├── openapi_client/         # Generated SDK package
│   └── sample_usage.py         # Sample script demonstrating SDK usage
├── main.py                     # FastAPI application entry point
├── database.py                 # SQLAlchemy engine and session setup
├── models.py                   # SQLAlchemy ORM models
├── schemas.py                  # Pydantic request/response schemas
├── crud.py                     # All database logic
├── requirements.txt            # Python dependencies
├── alembic.ini                 # Alembic configuration
├── seed_data.sql               # Example data for the SQLite database
├── setupdev.bat                # One-time setup script
├── runapplication.bat          # Start both servers
└── README.md
```

-----------------------------------------------------------------------------------------------

## Database Design

Four tables:

```
notes
  id          INTEGER  PRIMARY KEY AUTOINCREMENT
  title       TEXT     NOT NULL UNIQUE
  content     TEXT
  created_at  DATETIME DEFAULT CURRENT_TIMESTAMP

tags
  id          INTEGER  PRIMARY KEY AUTOINCREMENT
  name        TEXT     NOT NULL UNIQUE   (always stored lowercase, stripped)

note_tags  (many-to-many join)
  note_id     INTEGER  FK → notes.id  ┐ composite primary key
  tag_id      INTEGER  FK → tags.id   ┘

links  (directed graph edges)
  source_id   INTEGER  FK → notes.id  ┐ composite primary key
  target_id   INTEGER  FK → notes.id  ┘
```

------------------------------------------------------------------------------------------------------------

## Setup Instructions

### Option 1 — Automated (Recommended)

Run from the project root:

```bat
setupdev.bat
```

This creates the Python virtual environment (`env\`), installs backend and frontend dependencies, and runs Alembic migrations.

### Option 2 — Manual

**Backend** (run from the project root):
```bat
python -m venv env
call env\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
```

**Frontend:**
```bat
cd frontend
npm install
cd ..
```

---

## Running the Application

### Option 1 — Automated (Recommended)

```bat
runapplication.bat
```

Starts the backend on `http://localhost:8000` and the frontend on `http://localhost:5173`.

### Option 2 — Manual

**Backend** (from project root):
```bat
call env\Scripts\activate
python main.py
```

**Frontend:**
```bat
cd frontend
npm start
```

### URLs

| URL | Description |
|---|---|
| `http://localhost:5173` | React frontend |
| `http://localhost:8000` | FastAPI backend |
| `http://localhost:8000/docs` | Swagger UI |
| `http://localhost:8000/openapi.json` | Raw OpenAPI schema |

---

## API Endpoints

| Method    | Endpoint               | Description                                       |
|-----------|------------------------|---------------------------------------------------|
| `POST`    | `/notes/`              | Create a note. Returns HTTP 201.                  |
| `GET`     | `/notes/`              | List all notes. Supports `?tag=` and `?keyword=`. |
| `GET`     | `/notes/{note_id}`     | Get a note with outgoing links and backlinks.     |
| `PATCH`   | `/notes/{note_id}/link`| Create a directed link from this note to another. |
| `GET`     | `/notes/tags/all`      | Return all tags alphabetically.                   |
| `GET`     | `/graph/`              | Return all notes as nodes and all links as edges. |
| `GET`     | `/`                    | Health-check endpoint.                            |

---------------------------------------------------------------------------------------------

## Database Migrations and Seed Data

### Apply Migrations

From the project root:
```bat
call env\Scripts\activate
alembic upgrade head
```

### Load Seed Data

Load example notes, tags, and links into a fresh database (run migrations first):
```bat
sqlite3 knowledge_graph.db < seed_data.sql
```

---

## Running Tests

The test suite uses an isolated in-memory SQLite database. The development database (`knowledge_graph.db`) is never touched.

From the project root:
```bat
call env\Scripts\activate
pytest tests/ -v
```

**Current result: 13 passed, 0 failed.**

| File            | Tests | What is covered                                                                                       |
|-----------------|-------|-------------------------------------------------------------------------------------------------------|
| `test_notes.py` | 8     | Note creation, retrieval, keyword search, tag filter, tag normalization, auto-linking, duplicate link prevention, missing reference handling |
| `test_links.py` | 5     | Manual linking, 404 on nonexistent note, duplicate link idempotence, self-link prevention, graph endpoint |

--------------------------------------------------------------------------------------------

## Python SDK

The SDK is auto-generated from the live FastAPI OpenAPI schema using [OpenAPI Generator CLI](https://openapi-generator.tech/).

### Step 1 — Install OpenAPI Generator CLI

```bash
npm install -g @openapitools/openapi-generator-cli
```

Java (JRE 11+) must be installed and on your PATH.

### Step 2 — Start the Backend

The backend must be running before generating the SDK. Start it with `runapplication.bat` or manually as shown above.

### Step 3 — Generate the SDK

Run this exact command from the project root:

```bash
openapi-generator-cli generate -i http://localhost:8000/openapi.json -g python -o knowledge_sdk
```

This creates a complete Python SDK in `knowledge_sdk/`. The generator places the importable Python package under the name `openapi_client` by default. The `-o knowledge_sdk` flag sets the output *folder*, not the Python package name.

### Step 4 — Install SDK Dependencies

```bat
python -m venv knowledge_sdk\venv
knowledge_sdk\venv\Scripts\pip install -r knowledge_sdk\requirements.txt
knowledge_sdk\venv\Scripts\pip install -e knowledge_sdk
```

### Step 5 — Run the Sample Script

```bat
knowledge_sdk\venv\Scripts\python knowledge_sdk\sample_usage.py
```

### Sample Usage

```python
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from openapi_client.api.notes_api import NotesApi
from openapi_client import ApiClient, Configuration

configuration = Configuration(host="http://localhost:8000")

with ApiClient(configuration) as client:
    api = NotesApi(client)

    # Get all notes (generated method name: list_notes_notes_get)
    notes = api.list_notes_notes_get()
    print(notes)
```

----------------------------------------------------------------------------------------------------------------------------

## Assessment Requirements Checklist

| Requirement                                            | Location                                             | Status   |
|--------------------------------------------------------|------------------------------------------------------|--------  |
| FastAPI backend                                        | `main.py`, `routers/`                                | ✅      |
| SQLite database                                        | `database.py` → `knowledge_graph.db`                 | ✅      |
| POST /notes/                                           | `routers/notes.py`                                   | ✅      |
| GET /notes/ with tag + keyword filters                 | `routers/notes.py`, `crud.py`                        | ✅      |
| GET /notes/{note_id} with outgoing links + backlinks   | `routers/notes.py`, `crud.py`                        | ✅      |
| PATCH /notes/{note_id}/link                            | `routers/notes.py`                                   | ✅      |
| GET /notes/tags/all                                    | `routers/notes.py`                                   | ✅      |
| GET /graph/                                            | `routers/graph.py`                                   | ✅      |
| Auto `[[Note Title]]` link resolution on creation      | `crud.py` → `resolve_wiki_links()`                   | ✅      |
| Tag normalization                                      | `crud.py` → `normalize_tag()`                        | ✅      |
| Duplicate link prevention                              | `crud.py`                                            | ✅      |
| Self-link prevention                                   | `routers/notes.py` (HTTP 400)                        | ✅      |
| Unique note titles                                     | `models.py` (UNIQUE constraint)                      | ✅      |
| Alembic migrations                                     | `alembic/versions/`                                  | ✅      |
| Seed data                                              | `seed_data.sql`                                      | ✅      |
| React + Vite frontend                                  | `frontend/`                                          | ✅      |
| Axios for API calls                                    | `frontend/src/api.js`                                | ✅      |
| Markdown rendering                                     | `NoteDetail.jsx` (react-markdown)                    | ✅      |
| Light/Dark mode toggle                                 | `App.jsx`, `index.css`                               | ✅      |
| Unit tests (13 passing)                                | `tests/`                                             | ✅      |
| `setupdev.bat`                                         | Project root                                         | ✅      |
| `runapplication.bat`                                   | Project root                                         | ✅      |
| SDK generated with exact command                       | `knowledge_sdk/`                                     | ✅      |
| `sample_usage.py` demonstrating SDK                    | `knowledge_sdk/sample_usage.py`                      | ✅      |
| README                                                 | `README.md`                                          | ✅      |
