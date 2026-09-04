import sys
import os

# Ensure the generated openapi_client package is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from openapi_client.api.notes_api import NotesApi
from openapi_client import ApiClient, Configuration

# Configure the client to point to the local backend
configuration = Configuration(host="http://localhost:8000")

with ApiClient(configuration) as client:
    api = NotesApi(client)
    
    # Get all notes
    notes = api.list_notes_notes_get()
    print("Notes retrieved:")
    print(notes)
