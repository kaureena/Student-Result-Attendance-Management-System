# v2 Logbook — Modernisation

Window (tentative): 05 Dec 2025 → 14 Jan 2026

| Date | What was done | Category | Why it mattered | Evidence (paths) |
|---|---|---|---|---|
| 05 Dec 2025 | Created v2 scaffold; defined OLTP vs warehouse separation. | PLAN,WARE | Sets modernisation story and supports BI modelling. | v2_analytics_modernisation/warehouse/; docs/03_data_model_warehouse.md |
| 12 Dec 2025 | ETL runner skeleton and data zones created. | ETL | Core pipeline capability. | v2_analytics_modernisation/etl/run_etl.py; data/raw|staged|curated |
| 18 Dec 2025 | DQ rules and sample outputs prepared. | DQ,OPS | Data trust and governance proof. | dq_data_quality/rules; reports/dq_report.html |
| 25 Dec 2025 | Star schema refined; dims/facts clarified. | WARE | Enables clean Power BI relationships. | warehouse/*.sql |
| 02 Jan 2026 | Run register + sample runtime logs added. | OPS,DOCS | Operational evidence trail. | docs/logs/v2_run_register.csv; logs/sample_logs_only/ |
| 14 Jan 2026 | Docs and mermaid dashboards polished. | DOCS,QA | Interview-ready narrative. | docs/mermaid/; docs/screenshots/ |

### Category key
PLAN: planning/scope
DEV: baseline development (v1)
DATA: schema/seed/exports
ETL: pipeline work (v2)
DQ: data quality (v2)
WARE: warehouse/star schema (v2)
BI: dashboards/screenshots (v2)
API: API/tests (v2)
DOCS: documentation/diagrams/mermaid
QA: validation/bug fixes
OPS: CI/release/registers

