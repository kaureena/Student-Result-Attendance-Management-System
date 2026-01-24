# Contributing

Thanks for your interest in contributing!

This repository is a **portfolio project** and uses **synthetic data only**.

## Ways to contribute
- Report a bug (open an Issue with steps to reproduce)
- Improve documentation (README, diagrams, runbooks)
- Improve tests (API tests / ETL smoke / DQ rules)
- Suggest new features (open an Issue first)

## Local setup
1. Clone the repo
2. Create a virtual environment
3. Install dependencies:
   - v1: `pip install -r v1_bca_basic_system/requirements.txt`
   - v2: `pip install -r v2_analytics_modernisation/requirements.txt`

## Run checks
- API unit tests:
  `pytest v2_analytics_modernisation/api_service/tests -q`
- ETL smoke:
  `python v2_analytics_modernisation/etl/run_etl.py`
- Data-quality checks:
  `python v2_analytics_modernisation/dq_data_quality/run_checks.py`

## Pull requests
- Keep PRs small and focused
- Update docs/screenshots if behaviour changes
- Ensure tests pass before submitting

## Data safety
- Do **not** add real personal data.
- Keep samples synthetic and anonymised.
