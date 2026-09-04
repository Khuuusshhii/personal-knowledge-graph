// frontend/src/components/LinkForm.jsx
import React, { useState, useEffect } from "react";
import { getNotes, linkNotes } from "../api";

export default function LinkForm({ sourceNoteId, existingLinkIds = [], onLinkCreated }) {
  const [availableNotes, setAvailableNotes] = useState([]);
  const [targetId, setTargetId] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Fetch all notes to populate the dropdown
    getNotes().then((notes) => {
      // Filter out the current note (no self-links) and any notes we already link to
      const filtered = notes.filter(
        (n) => n.id !== sourceNoteId && !existingLinkIds.includes(n.id)
      );
      setAvailableNotes(filtered);
    }).catch(console.error);
  }, [sourceNoteId, existingLinkIds]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!targetId) return;

    setLoading(true);
    setError(null);

    try {
      await linkNotes(sourceNoteId, parseInt(targetId, 10));
      setTargetId(""); // Reset selection
      onLinkCreated(); // Tell parent to refresh
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || "Failed to create link.");
    } finally {
      setLoading(false);
    }
  };

  if (availableNotes.length === 0) {
    return <p style={{ color: "var(--text-secondary)", fontSize: "0.9rem" }}>No other notes available to link.</p>;
  }

  return (
    <div style={{ marginTop: "1.5rem", padding: "1rem", background: "rgba(0,0,0,0.1)", borderRadius: "var(--radius-md)" }}>
      <h4 style={{ fontSize: "1rem", marginBottom: "0.75rem" }}>Add Manual Link</h4>
      {error && <div style={{ color: "var(--danger)", marginBottom: "0.5rem", fontSize: "0.9rem" }}>{error}</div>}
      
      <form onSubmit={handleSubmit} className="flex-row">
        <select
          className="form-select"
          value={targetId}
          onChange={(e) => setTargetId(e.target.value)}
          required
        >
          <option value="" disabled>Select a note to link to...</option>
          {availableNotes.map((note) => (
            <option key={note.id} value={note.id}>
              {note.title}
            </option>
          ))}
        </select>
        
        <button type="submit" className="btn btn-primary" disabled={loading || !targetId}>
          {loading ? "Linking..." : "Create Link"}
        </button>
      </form>
    </div>
  );
}
