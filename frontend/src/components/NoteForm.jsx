// frontend/src/components/NoteForm.jsx
import React, { useState } from "react";
import { createNote } from "../api";

export default function NoteForm({ onNoteCreated, onCancel }) {
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [tagInput, setTagInput] = useState("");
  const [tags, setTags] = useState([]);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);

  // Add a tag to the local state list when the user presses Enter or clicks Add
  const handleAddTag = (e) => {
    e.preventDefault();
    const trimmed = tagInput.trim();
    if (trimmed && !tags.includes(trimmed)) {
      setTags([...tags, trimmed]);
    }
    setTagInput("");
  };

  // Remove a tag from the local state list
  const handleRemoveTag = (tagToRemove) => {
    setTags(tags.filter((t) => t !== tagToRemove));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!title.trim()) {
      setError("Title is required.");
      return;
    }

    setSubmitting(true);
    setError(null);

    try {
      await createNote({
        title,
        content,
        tags,
      });
      onNoteCreated(); // Signal parent to switch view back to list
    } catch (err) {
      console.error(err);
      setError("Failed to create note. Please try again.");
      setSubmitting(false);
    }
  };

  return (
    <div className="glass-panel animate-fade-in" style={{ maxWidth: "800px", margin: "0 auto" }}>
      <h2>Create New Note</h2>
      
      {error && <div style={{ color: "var(--danger)", marginBottom: "1rem" }}>{error}</div>}

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label className="form-label">Title *</label>
          <input
            type="text"
            className="form-input"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="e.g. Project Ideas"
            required
          />
        </div>

        <div className="form-group">
          <label className="form-label">
            Content
            <span style={{ fontWeight: "normal", marginLeft: "0.5rem" }}>
              (Use [[Note Title]] to automatically link to another note)
            </span>
          </label>
          <textarea
            className="form-textarea"
            value={content}
            onChange={(e) => setContent(e.target.value)}
            placeholder="Write your note here..."
          />
        </div>

        <div className="form-group">
          <label className="form-label">Tags</label>
          <div className="flex-row">
            <input
              type="text"
              className="form-input"
              value={tagInput}
              onChange={(e) => setTagInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  e.preventDefault();
                  handleAddTag(e);
                }
              }}
              placeholder="Add a tag..."
            />
            <button className="btn" onClick={handleAddTag} type="button">
              Add
            </button>
          </div>
          
          {tags.length > 0 && (
            <div className="tags-container" style={{ marginTop: "1rem" }}>
              {tags.map((tag) => (
                <span
                  key={tag}
                  className="tag tag-removable"
                  onClick={() => handleRemoveTag(tag)}
                  title="Click to remove"
                >
                  #{tag} &times;
                </span>
              ))}
            </div>
          )}
        </div>

        <div className="flex-row" style={{ marginTop: "2rem", justifyContent: "flex-end" }}>
          <button type="button" className="btn" onClick={onCancel} disabled={submitting}>
            Cancel
          </button>
          <button type="submit" className="btn btn-primary" disabled={submitting}>
            {submitting ? "Saving..." : "Create Note"}
          </button>
        </div>
      </form>
    </div>
  );
}
