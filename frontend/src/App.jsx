// frontend/src/App.jsx
import React, { useState, useEffect } from "react";
import NoteList from "./components/NoteList";
import NoteForm from "./components/NoteForm";
import NoteDetail from "./components/NoteDetail";
import GraphView from "./components/GraphView";

function App() {
  // Simple state-based routing: 'list', 'create', 'detail', 'graph'
  const [currentView, setCurrentView] = useState("list");
  // The ID of the note to show when currentView === 'detail'
  const [selectedNoteId, setSelectedNoteId] = useState(null);

  // Theme state: defaults to light mode, remembers user's choice
  const [theme, setTheme] = useState(() => {
    return localStorage.getItem("theme") || "light";
  });

  // Apply theme to the document and save to localStorage
  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("theme", theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme((prev) => (prev === "light" ? "dark" : "light"));
  };

  const navigateTo = (view, id = null) => {
    setCurrentView(view);
    if (id !== null) {
      setSelectedNoteId(id);
    }
  };

  return (
    <div className="app-container">
      <header className="nav-bar">
        <h1 style={{ margin: 0, marginRight: "auto" }}>Personal Knowledge Graph</h1>
        <button 
          className="btn-nav"
          onClick={toggleTheme}
          style={{ marginRight: "1rem" }}
          title="Toggle Theme"
        >
          {theme === "light" ? "🌙 Dark" : "☀️ Light"}
        </button>
        <button 
          className={`btn-nav ${currentView === "list" ? "active" : ""}`}
          onClick={() => navigateTo("list")}
        >
          All Notes
        </button>
        <button 
          className={`btn-nav ${currentView === "graph" ? "active" : ""}`}
          onClick={() => navigateTo("graph")}
        >
          Graph Map
        </button>
        <button 
          className="btn btn-primary"
          onClick={() => navigateTo("create")}
          style={{ marginLeft: "1rem" }}
        >
          + New Note
        </button>
      </header>

      <main>
        {currentView === "list" && (
          <NoteList 
            onViewNote={(id) => navigateTo("detail", id)} 
          />
        )}
        
        {currentView === "create" && (
          <NoteForm 
            onNoteCreated={() => navigateTo("list")}
            onCancel={() => navigateTo("list")}
          />
        )}
        
        {currentView === "detail" && selectedNoteId && (
          <NoteDetail 
            noteId={selectedNoteId} 
            onBack={() => navigateTo("list")}
            onNavigate={(id) => navigateTo("detail", id)}
          />
        )}
        
        {currentView === "graph" && (
          <GraphView 
            onNavigate={(id) => navigateTo("detail", id)}
          />
        )}
      </main>
    </div>
  );
}

export default App;
