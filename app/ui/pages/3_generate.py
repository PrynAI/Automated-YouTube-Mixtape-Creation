"""Step 3 page: submit generation jobs and poll job status."""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

# Ensure absolute imports (`from app...`) work when Streamlit executes this page directly.
PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.ui.api_client import ApiClientError, create_job, get_job_status
from app.ui.components.progress_panel import render_job_status

st.title("Step 3: Generate")

if not st.session_state.get("audio_payloads"):
    st.warning("Upload at least one audio file in Step 1.")
else:
    if st.button("Start generation", type="primary"):
        try:
            create_response = create_job(
                audio_payloads=st.session_state.audio_payloads,
                image_payload=st.session_state.get("image_payload"),
                transition_ms=int(st.session_state.get("transition_ms", 6000)),
                mixtape_name=st.session_state.get("mixtape_name", "Pryn House Mixtape"),
                genre=st.session_state.get("genre", "Pryn House"),
            )
            st.session_state.job_id = create_response["job_id"]
            st.session_state.job_status = None
            st.success(f"Job submitted: {st.session_state.job_id}")
        except ApiClientError as exc:
            st.error(f"Failed to create job: {exc}")

job_id = st.session_state.get("job_id")
if job_id:
    col1, col2 = st.columns([1, 3])
    with col1:
        refresh = st.button("Refresh status")
    with col2:
        st.caption("Use refresh until status is COMPLETED or FAILED.")

    if refresh or st.session_state.get("job_status") is None:
        try:
            st.session_state.job_status = get_job_status(job_id)
        except ApiClientError as exc:
            st.error(f"Failed to fetch status: {exc}")

    if st.session_state.get("job_status"):
        render_job_status(st.session_state.job_status)
