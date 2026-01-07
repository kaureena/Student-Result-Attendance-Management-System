# ETL Design

Pipeline:
1. Extract from OLTP (SQLite by default) and optional SharePoint inputs (template only).
2. Transform: clean, standardise, dedupe, validate types.
3. Load: build dimensions and facts.
4. Logs: run_id, row counts, timings.

Run: `python v2_analytics_modernisation/etl/run_etl.py --generate-samples`
