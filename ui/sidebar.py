import streamlit as st


def _render_youtube_inputs() -> list[str]:
    st.markdown("### YouTube Sources")

    urls = []

    for index in range(st.session_state.youtube_link_count):
        url = st.text_input(
            f"Video Link {index + 1}",
            key=f"youtube_url_{index}",
            placeholder="Paste a YouTube video link",
        )
        if url.strip():
            urls.append(url.strip())

    if st.button("Add Link", use_container_width=True):
        st.session_state.youtube_link_count += 1
        st.rerun()

    return urls


def _render_video_inputs() -> list:
    st.markdown("### Uploaded Videos")

    uploaded_files = []

    for index in range(st.session_state.video_input_count):
        uploaded_file = st.file_uploader(
            f"Video File {index + 1}",
            type=["mp4", "mov", "mkv"],
            key=f"uploaded_video_{index}",
        )
        if uploaded_file is not None:
            uploaded_files.append(uploaded_file)

    if st.button("Add Video", use_container_width=True):
        st.session_state.video_input_count += 1
        st.rerun()

    return uploaded_files


def render_sidebar_inputs() -> tuple[list[str], list]:
    with st.sidebar:
        st.header("Videos")
        st.caption("Build a workspace source-by-source with individual link and upload slots.")

        youtube_urls = _render_youtube_inputs()
        st.divider()
        uploaded_files = _render_video_inputs()
        st.divider()
        process_button = st.button("Process Videos", use_container_width=True)

    return youtube_urls, uploaded_files, process_button
