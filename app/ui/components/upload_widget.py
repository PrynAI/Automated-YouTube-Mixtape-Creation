"""UI component for media file uploads and session-state persistence."""

from __future__ import annotations

import streamlit as st


def render_upload_widget() -> None:
    """Render upload inputs and store file bytes in Streamlit session state."""
    st.subheader("Upload Inputs")
    audio_files = st.file_uploader(
        "Select audio tracks (.mp3, .wav, .flac, .aac, .ogg, .m4a)",
        type=["mp3", "wav", "flac", "aac", "ogg", "m4a"],
        accept_multiple_files=True,
    )
    image_file = st.file_uploader(
        "Optional static image for video (.png, .jpg, .jpeg)",
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=False,
    )

    if audio_files:
        st.session_state.audio_payloads = [
            {
                "name": file.name,
                "type": file.type,
                "bytes": file.getvalue(),
            }
            for file in audio_files
        ]

    if image_file:
        st.session_state.image_payload = {
            "name": image_file.name,
            "type": image_file.type,
            "bytes": image_file.getvalue(),
        }

    if st.session_state.get("audio_payloads"):
        st.success(f"Audio files loaded: {len(st.session_state.audio_payloads)}")

    if st.session_state.get("image_payload"):
        st.success(f"Image loaded: {st.session_state.image_payload['name']}")
