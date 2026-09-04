// frontend/src/components/NoteDetail.jsx
import React, { useState, useEffect } from "react";
import { getNote } from "../api";
import LinkForm from "./LinkForm";
import ReactMarkdown from "react-markdown";

export default function NoteDetail({ noteId, onBack, onNavigate }) {
  const [note, setNote] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchNoteDetail = async () => {
    try {
      setLoading(true);
      const data = await getNote(noteId);
      setNote(data);
      setError(null);
    } catch (err) {
      console.error(err);
      setError("Failed to load note details.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchNoteDetail();
  }, [noteId]);

  if (loading) return <div className="animate-fade-in"><p>Loading note...</p></div>;
  if (error) return <div className="animate-fade-in"><p style={{ color: "var(--danger)" }}>{error}</p><button className="btn" onClick={onBack}>Back to List</button></div>;
  if (!note) return null;

  // Extract IDs of existing outgoing links to pass to the LinkForm
  const existingLinkIds = note.outgoing_links.map((link) => link.id);

  return (
    <div className="glass-panel animate-fade-in" style={{ maxWidth: "900px", margin: "0 auto" }}>
      <button className="btn-nav" onClick={onBack} style={{ marginBottom: "1.5rem" }}>
        &larr; Back to Notes
      </button>

      <h1>{note.title}</h1>
      
      <div className="note-meta">
        <p>Created: {new Date(note.created_at).toLocaleString()}</p>
        <div className="tags-container">
          {note.tags.map((tag) => (
            <span key={tag.id} className="tag">#{tag.name}</span>
          ))}
        </div>
      </div>

      <div className="note-content-rendered">
        {note.content ? (
          <ReactMarkdown>{note.content}</ReactMarkdown>
        ) : (
          <span style={{ color: "var(--text-secondary)", fontStyle: "italic" }}>Empty note</span>
        )}
      </div>

      <div className="flex-row" style={{ alignItems: "flex-start", gap: "2rem" }}>
        {/* Outgoing Links Column */}
        <div style={{ flex: 1 }}>
          <h3>Outgoing Links</h3>
          <p style={{ fontSize: "0.85rem", color: "var(--text-secondary)", marginBottom: "1rem" }}>
            Notes referenced by this note.
          </p>
          
          {note.outgoing_links.length > 0 ? (
            <ul className="link-list">
              {note.outgoing_links.map((link) => (
                <li key={link.id} className="link-item" onClick={() => onNavigate(link.id)}>
                  <span style={{ color: "var(--accent-secondary)", marginRight: "0.5rem" }}>&#8627;</span>
                  {link.title}
                </li>
              ))}
            </ul>
          ) : (
            <p style={{ color: "var(--text-secondary)", fontSize: "0.9rem" }}>No outgoing links.</p>
          )}

          {/* Form to manually add a new link */}
          <LinkForm 
            sourceNoteId={note.id} 
            existingLinkIds={existingLinkIds} 
            onLinkCreated={fetchNoteDetail} 
          />
        </div>

        {/* Backlinks Column */}
        <div style={{ flex: 1 }}>
          <h3>Backlinks</h3>
          <p style={{ fontSize: "0.85rem", color: "var(--text-secondary)", marginBottom: "1rem" }}>
            Notes that link to this note.
          </p>

          {note.backlinks.length > 0 ? (
            <ul className="link-list">
              {note.backlinks.map((link) => (
                <li key={link.id} className="link-item" onClick={() => onNavigate(link.id)}>
                  <span style={{ color: "var(--success)", marginRight: "0.5rem" }}>&#8626;</span>
                  {link.title}
                </li>
              ))}
            </ul>
          ) : (
            <p style={{ color: "var(--text-secondary)", fontSize: "0.9rem" }}>No backlinks yet.</p>
          )}
        </div>
      </div>
    </div>
  );
}
