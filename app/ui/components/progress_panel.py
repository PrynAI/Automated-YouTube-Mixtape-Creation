"""UI component for rendering job progress, errors, and track timings."""

from __future__ import annotations

import streamlit as st


def render_job_status(job_status: dict) -> None:
    """Display job status payload details in a readable panel."""
    st.subheader("Job Status")
    st.write(f"Job ID: `{job_status.get('job_id', '')}`")
    st.write(f"Status: **{job_status.get('status', '').upper()}**")
    st.write(f"Message: {job_status.get('message', '')}")

    error = job_status.get("error")
    if error:
        st.error(error)

    tracks = job_status.get("tracks", [])
    if tracks:
        st.caption("Track timing")
        st.table(tracks)
