// frontend/src/components/NoteList.jsx
import React, { useState, useEffect } from "react";
import { getNotes, getTags } from "../api";
import ReactMarkdown from "react-markdown";

export default function NoteList({ onViewNote }) {
  const [notes, setNotes] = useState([]);
  const [tags, setTags] = useState([]);
  const [keyword, setKeyword] = useState("");
  const [selectedTag, setSelectedTag] = useState("");
  const [loading, setLoading] = useState(true);

  // Fetch tags for the filter dropdown
  useEffect(() => {
    getTags()
      .then(setTags)
      .catch((err) => console.error("Failed to load tags", err));
  }, []);

  // Fetch notes whenever the keyword or tag filter changes
  useEffect(() => {
    setLoading(true);
    // Use a small delay/debounce for the keyword search in a real app,
    // but for this simple challenge, fetching directly on change is fine.
    const fetchNotes = async () => {
      try {
        const data = await getNotes(selectedTag, keyword);
        setNotes(data);
      } catch (err) {
        console.error("Failed to load notes", err);
      } finally {
        setLoading(false);
      }
    };
    
    // We add a tiny artificial debounce to avoid spamming the backend while typing
    const timeoutId = setTimeout(() => {
      fetchNotes();
    }, 300);
    
    return () => clearTimeout(timeoutId);
  }, [keyword, selectedTag]);

  return (
    <div className="animate-fade-in">
      <div className="glass-panel" style={{ marginBottom: "2rem" }}>
        <div className="flex-row">
          <div style={{ flex: 1 }}>
            <label className="form-label">Search Notes</label>
            <input
              type="text"
              className="form-input"
              placeholder="Search by keyword..."
              value={keyword}
              onChange={(e) => setKeyword(e.target.value)}
            />
          </div>
          <div style={{ flex: 1 }}>
            <label className="form-label">Filter by Tag</label>
            <select
              className="form-select"
              value={selectedTag}
              onChange={(e) => setSelectedTag(e.target.value)}
            >
              <option value="">All Tags</option>
              {tags.map((tag) => (
                <option key={tag.id} value={tag.name}>
                  {tag.name}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {loading ? (
        <p>Loading notes...</p>
      ) : notes.length === 0 ? (
        <p style={{ color: "var(--text-secondary)" }}>No notes found matching your criteria.</p>
      ) : (
        <div className="notes-grid">
          {notes.map((note) => (
            <div
              key={note.id}
              className="card"
              onClick={() => onViewNote(note.id)}
            >
              <h3>{note.title}</h3>
              <p style={{ color: "var(--text-secondary)", fontSize: "0.9rem", marginBottom: "1rem" }}>
                {new Date(note.created_at).toLocaleDateString()}
              </p>
              
              {/* Note preview (first 100 characters) */}
              <div style={{ marginBottom: "1.5rem", fontSize: "0.95rem" }} className="markdown-preview">
                <ReactMarkdown>
                  {note.content.length > 100 
                    ? note.content.substring(0, 100) + "..." 
                    : note.content}
                </ReactMarkdown>
              </div>

              <div className="tags-container">
                {note.tags.map((tag) => (
                  <span key={tag.id} className="tag">
                    #{tag.name}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
