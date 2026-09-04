"""Streamlit Cloud entry point for the retail dashboard.

The dashboard implementation lives in ``app.py``. Execute that file by its
resolved path so deployment cannot accidentally import an unrelated module
named ``app``.
"""

from pathlib import Path
import runpy


DASHBOARD_PATH = Path(__file__).resolve().with_name("app.py")

if not DASHBOARD_PATH.is_file():
    raise FileNotFoundError(f"Dashboard entrypoint not found: {DASHBOARD_PATH}")

runpy.run_path(str(DASHBOARD_PATH), run_name="__main__")
