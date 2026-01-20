# Install and Run (Local)

Prerequisites:
- Python 3.11+ recommended
- Optional: Docker Desktop (for v2 container runs)

v1 (Baseline):
```bash
cd v1_bca_basic_system
python -m pip install -r requirements.txt
python src/main.py
```

v2 (Modernisation):
```bash
cd v2_analytics_modernisation
python -m pip install -r requirements.txt
python etl/run_etl.py
python dq_data_quality/run_checks.py
```
