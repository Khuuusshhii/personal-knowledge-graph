// frontend/src/api.js
// Centralised Axios instance and API helper functions.

import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

/**
 * Fetch all notes, optionally filtered by tag or keyword.
 * @param {string} tag
 * @param {string} keyword
 */
export const getNotes = async (tag = "", keyword = "") => {
  const params = {};
  if (tag) params.tag = tag;
  if (keyword) params.keyword = keyword;
  const response = await api.get("/notes/", { params });
  return response.data;
};

/**
 * Fetch a single note by ID, including its links and backlinks.
 * @param {number} id
 */
export const getNote = async (id) => {
  const response = await api.get(`/notes/${id}`);
  return response.data;
};

/**
 * Create a new note.
 * @param {object} data - { title, content, tags }
 */
export const createNote = async (data) => {
  const response = await api.post("/notes/", data);
  return response.data;
};

/**
 * Manually link one note to another.
 * @param {number} sourceId
 * @param {number} targetId
 */
export const linkNotes = async (sourceId, targetId) => {
  const response = await api.patch(`/notes/${sourceId}/link`, {
    target_id: targetId,
  });
  return response.data;
};

/**
 * Fetch all available tags (for suggestions).
 */
export const getTags = async () => {
  const response = await api.get("/notes/tags/all");
  return response.data;
};

/**
 * Fetch the entire note graph (nodes and edges).
 */
export const getGraph = async () => {
  const response = await api.get("/graph/");
  return response.data;
};

export default api;
