-- seed_data.sql
-- Example data for the Personal Knowledge Graph.
-- Run AFTER Alembic migrations have been applied.
--
-- Usage (from the backend directory):
--   sqlite3 knowledge_graph.db < seed_data.sql
--
-- The seed creates 8 interconnected notes, 6 tags, and several manual links.
-- Wiki-link resolution ([[Note Title]]) cannot run through SQL alone,
-- so links referenced in content are also inserted explicitly here.


-- ────────────────────────────────────────────────────────────────────────────
-- NOTES
-- ────────────────────────────────────────────────────────────────────────────
INSERT INTO notes (id, title, content, created_at) VALUES
  (1, 'Python Programming',
   'Python is a high-level, general-purpose programming language. It is widely used in web development, data science, and automation. See also [[Machine Learning]] and [[FastAPI Tutorial]].',
   datetime('now', '-7 days')),

  (2, 'Machine Learning',
   'Machine learning is a branch of artificial intelligence. It relies heavily on [[Python Programming]] for data processing. Key concepts include neural networks — see [[Neural Networks]].',
   datetime('now', '-6 days')),

  (3, 'Data Structures',
   'Data structures are ways of organising data so that algorithms can operate on it efficiently. Common examples include arrays, linked lists, stacks, queues, and trees.',
   datetime('now', '-5 days')),

  (4, 'Algorithms',
   'Algorithms are step-by-step procedures for solving problems. They operate on [[Data Structures]]. Good algorithm design is fundamental to computer science.',
   datetime('now', '-4 days')),

  (5, 'Neural Networks',
   'Neural networks are a type of machine learning model inspired by the human brain. They are a core technique in deep learning. Understanding [[Machine Learning]] is a prerequisite.',
   datetime('now', '-3 days')),

  (6, 'Database Design',
   'Database design involves defining the structure of a database. Key concepts include normalisation, relationships (one-to-many, many-to-many), and indexing. Relevant to [[FastAPI Tutorial]].',
   datetime('now', '-2 days')),

  (7, 'FastAPI Tutorial',
   'FastAPI is a modern Python web framework for building APIs. It uses [[Python Programming]] and integrates seamlessly with [[Database Design]] via SQLAlchemy.',
   datetime('now', '-1 day')),

  (8, 'Knowledge Graphs',
   'A knowledge graph is a network of real-world entities and their relationships. This very application is a personal knowledge graph. It connects concepts from [[Neural Networks]] and [[Database Design]].',
   datetime('now'));


-- ────────────────────────────────────────────────────────────────────────────
-- TAGS  (all names pre-normalised to lowercase)
-- ────────────────────────────────────────────────────────────────────────────
INSERT INTO tags (id, name) VALUES
  (1, 'python'),
  (2, 'programming'),
  (3, 'machine-learning'),
  (4, 'computer-science'),
  (5, 'artificial-intelligence'),
  (6, 'database');


-- ────────────────────────────────────────────────────────────────────────────
-- NOTE ↔ TAG  (many-to-many)
-- ────────────────────────────────────────────────────────────────────────────
INSERT INTO note_tags (note_id, tag_id) VALUES
  (1, 1), (1, 2),          -- Python Programming: python, programming
  (2, 1), (2, 3),          -- Machine Learning: python, machine-learning
  (3, 2), (3, 4),          -- Data Structures: programming, computer-science
  (4, 2), (4, 4),          -- Algorithms: programming, computer-science
  (5, 3), (5, 5),          -- Neural Networks: machine-learning, artificial-intelligence
  (6, 6), (6, 4),          -- Database Design: database, computer-science
  (7, 1), (7, 6),          -- FastAPI Tutorial: python, database
  (8, 5), (8, 6);          -- Knowledge Graphs: artificial-intelligence, database


-- ────────────────────────────────────────────────────────────────────────────
-- LINKS  (directed edges — matching the [[wiki links]] in the content above,
--          plus a couple of extra manual links)
-- Table name: 'links'  (composite primary key: source_id + target_id)
-- ────────────────────────────────────────────────────────────────────────────
-- source_id → target_id  (no duplicates: composite PK enforces uniqueness)
INSERT INTO links (source_id, target_id) VALUES
  (1, 2),   -- Python Programming → Machine Learning
  (1, 7),   -- Python Programming → FastAPI Tutorial
  (2, 1),   -- Machine Learning → Python Programming
  (2, 5),   -- Machine Learning → Neural Networks
  (4, 3),   -- Algorithms → Data Structures
  (5, 2),   -- Neural Networks → Machine Learning
  (6, 7),   -- Database Design → FastAPI Tutorial (manual extra link)
  (7, 1),   -- FastAPI Tutorial → Python Programming
  (7, 6),   -- FastAPI Tutorial → Database Design
  (8, 5),   -- Knowledge Graphs → Neural Networks
  (8, 6);   -- Knowledge Graphs → Database Design
