"""Compatibility entry point for Streamlit Cloud.

The dashboard implementation lives in ``app.py``. Streamlit Cloud currently
launches this filename, so importing ``app`` delegates execution to the single
dashboard application without duplicating its code.
"""

import streamlit as st

try:
    import app
except ImportError as error:
    st.error("The dashboard could not start because a required Python package is missing.")
    st.exception(error)
except (FileNotFoundError, ValueError) as error:
    st.error("The dashboard could not start because its data file is unavailable or invalid.")
    st.exception(error)
except Exception as error:
    st.error("The dashboard failed during startup.")
    st.exception(error)
