"""UI component for previewing and downloading generated artifacts."""

from __future__ import annotations

import streamlit as st


def render_output_links(job_status: dict) -> None:
    """Render output download links and inline media previews."""
    st.subheader("Outputs")

    audio_url = job_status.get("audio_download_url")
    description_url = job_status.get("description_download_url")
    video_url = job_status.get("video_download_url")

    if audio_url:
        st.markdown(f"- [Download mixtape audio]({audio_url})")
        st.audio(audio_url)

    if description_url:
        st.markdown(f"- [Download description]({description_url})")

    if video_url:
        st.markdown(f"- [Download mixtape video]({video_url})")
        st.video(video_url)
