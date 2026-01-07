from __future__ import annotations
from pathlib import Path
import pandas as pd

def extract_sharepoint_csv(attendance_csv: Path, results_csv: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Template only: in real usage this would connect to SharePoint.
    For portfolio demo, we treat local CSVs as a SharePoint export.
    """
    attendance = pd.read_csv(attendance_csv)
    results = pd.read_csv(results_csv)
    return attendance, results
