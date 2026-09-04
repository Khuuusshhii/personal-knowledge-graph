// frontend/src/components/GraphView.jsx
import React, { useState, useEffect } from "react";
import { getGraph } from "../api";

export default function GraphView({ onNavigate }) {
  const [graphData, setGraphData] = useState({ nodes: [], edges: [] });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    getGraph()
      .then((data) => {
        setGraphData(data);
        setError(null);
      })
      .catch((err) => {
        console.error(err);
        setError("Failed to load graph data.");
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="animate-fade-in"><p>Loading graph map...</p></div>;
  if (error) return <div className="animate-fade-in"><p style={{ color: "var(--danger)" }}>{error}</p></div>;

  // Build a lookup map for faster title retrieval
  const nodeMap = {};
  graphData.nodes.forEach((n) => {
    nodeMap[n.id] = n.title;
  });

  return (
    <div className="glass-panel animate-fade-in" style={{ maxWidth: "1000px", margin: "0 auto" }}>
      <h2>Knowledge Graph Map</h2>
      <p style={{ color: "var(--text-secondary)", marginBottom: "2rem" }}>
        Total Nodes: {graphData.nodes.length} | Total Links: {graphData.edges.length}
      </p>

      <div className="flex-row" style={{ alignItems: "flex-start", gap: "2rem" }}>
        {/* Nodes List */}
        <div style={{ flex: 1 }}>
          <h3 style={{ borderBottom: "1px solid var(--border-color)", paddingBottom: "0.5rem" }}>
            All Nodes
          </h3>
          <ul className="link-list" style={{ marginTop: "1rem" }}>
            {graphData.nodes.map((node) => (
              <li 
                key={node.id} 
                className="link-item" 
                onClick={() => onNavigate(node.id)}
                title="Click to view details"
              >
                <span style={{ 
                  display: "inline-block", 
                  width: "24px", 
                  height: "24px", 
                  background: "var(--accent-primary)", 
                  borderRadius: "50%",
                  textAlign: "center",
                  lineHeight: "24px",
                  fontSize: "0.75rem",
                  marginRight: "0.75rem"
                }}>
                  {node.id}
                </span>
                {node.title}
              </li>
            ))}
          </ul>
        </div>

        {/* Edges List (Text Map) */}
        <div style={{ flex: 1 }}>
          <h3 style={{ borderBottom: "1px solid var(--border-color)", paddingBottom: "0.5rem" }}>
            Connections
          </h3>
          <ul className="link-list" style={{ marginTop: "1rem" }}>
            {graphData.edges.map((edge, idx) => (
              <li key={idx} className="link-item" style={{ cursor: "default" }}>
                <span style={{ color: "var(--accent-secondary)" }}>
                  {nodeMap[edge.source_id]}
                </span>
                <span style={{ margin: "0 0.5rem", color: "var(--text-secondary)" }}>
                  &rarr;
                </span>
                <span style={{ color: "var(--success)" }}>
                  {nodeMap[edge.target_id]}
                </span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
