# v1 Logbook — Baseline

Window (tentative): 01 Feb 2009 → 15 Mar 2009

| Date | What was done | Category | Why it mattered | Evidence (paths) |
|---|---|---|---|---|
| 01 Feb 2009 | Defined baseline scope and file structure. | PLAN | Clarifies what v1 proves and sets success criteria. | v1_bca_basic_system/src/; v1_bca_basic_system/database/schema.sql |
| 15 Feb 2009 | Implemented Students CRUD + unique roll number rule. | DEV,DATA | Students table is the base for attendance and results. | src/student_module.py; database/schema.sql |
| 25 Feb 2009 | Implemented Attendance module + constraints. | DEV,DATA | Introduces realistic operational workflow + data integrity. | src/attendance_module.py; ui_04_attendance.png |
| 06 Mar 2009 | Implemented Results module + export format. | DEV,DATA | Shows calculations and reporting outputs. | src/result_module.py; export/result_report_sample.xlsx |
| 10 Mar 2009 | Captured UI screenshots for all key screens. | DOCS | Fast evidence for non-technical reviewers. | ui/screenshots/ |
| 15 Mar 2009 | Baseline freeze; final tidy; demo run-sheet prepared. | OPS,DOCS | Creates a stable v1 milestone supporting v2 story. | docs/logs/v1_run-sheet.md; docs/logs/v1_changelog.md |

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

