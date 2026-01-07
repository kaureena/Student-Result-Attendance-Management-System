# Staged outputs

This template uses **CSV** outputs by default.
When ETL runs, staged files will be generated here:

- `attendance_clean.csv`
- `results_clean.csv`

If you want Parquet, install `pyarrow` and update ETL accordingly.
