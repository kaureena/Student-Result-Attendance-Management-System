# API models

This folder is intentionally lightweight.

**Why it exists**
- Keeps a clean, predictable FastAPI structure (`routes/`, `services/`, `utils/`, `models/`).
- Allows us to add request/response schemas later without moving files around.

**What to put here (future)**
- Pydantic schemas for API requests and responses
- (Optional) ORM / database models if the service moves beyond direct SQLite queries

At present, the route handlers return rows from SQLite directly, so these schemas are *not required* for runtime.
They are included as placeholders to meet the agreed repo structure.
