# Data Quality Rules

Attendance:
- Valid date format
- No duplicate (student_id, date)

Results:
- marks within bounds
- total = internal + external
- pass/fail consistent with threshold

DQ runner:
`python v2_analytics_modernisation/dq_data_quality/run_checks.py`
