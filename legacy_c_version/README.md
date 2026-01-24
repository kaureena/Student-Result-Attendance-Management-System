# Legacy C draft (historic)

This folder contains an older **C-based draft** of the Student Result & Attendance system.

It is **not** part of the current portfolio story.
The active implementation is:

- **v1 (baseline app):** `v1_bca_basic_system/` (Python + SQLite demo)
- **v2 (modernisation):** `v2_analytics_modernisation/` (ETL + DQ + warehouse + BI)

Why keep this?
- It shows early experimentation, but moving it here avoids confusing reviewers
  about the main technology stack.

What to do:
- Move the old root `src/` folder (C files) into `legacy_c_version/c_src/`
  OR delete it if you don't need it.
