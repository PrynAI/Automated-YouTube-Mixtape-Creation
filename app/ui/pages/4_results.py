"""Step 4 page: load completed job outputs and present downloads/previews."""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

# Ensure absolute imports (`from app...`) work when Streamlit executes this page directly.
PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.ui.api_client import ApiClientError, fetch_text_file, get_job_status
from app.ui.components.output_preview import render_output_links

st.title("Step 4: Results")

job_id = st.session_state.get("job_id")
if not job_id:
    st.warning("No job available yet. Generate one in Step 3.")
else:
    if st.button("Load latest results"):
        try:
            st.session_state.job_status = get_job_status(job_id)
        except ApiClientError as exc:
            st.error(f"Failed to load results: {exc}")

    job_status = st.session_state.get("job_status")
    if not job_status:
        st.info("Click 'Load latest results' to fetch job outputs.")
    elif job_status.get("status") != "completed":
        st.info(f"Job status is {job_status.get('status')}. Wait until it completes.")
    else:
        render_output_links(job_status)

        description_url = job_status.get("description_download_url")
        if description_url:
            try:
                description_text = fetch_text_file(description_url)
                st.subheader("Generated Description")
                st.text_area("Description", value=description_text, height=240)
            except ApiClientError as exc:
                st.error(f"Failed to load description text: {exc}")
