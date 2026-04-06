import streamlit as st


DEFAULT_SESSION_STATE = {
    "transcript": None,
    "summary": None,
    "flashcards": None,
    "timelines": {},
    "index": None,
    "chunks": None,
    "chat_history": [],
    "source_labels": [],
    "source_details": [],
    "last_search_result": "",
    "youtube_link_count": 1,
    "video_input_count": 1,
}


def initialize_session_state():
    for key, value in DEFAULT_SESSION_STATE.items():
        if key not in st.session_state:
            st.session_state[key] = value
