import streamlit as st
import os
import re

from modules.audio_extractor import extract_audio
from modules.transcriber import transcribe_audio
from modules.summarizer import summarize_transcript
from modules.vector_store import create_vector_store, retrieve
from modules.qa_agent import answer_question
from modules.flashcards import generate_flashcards
from modules.timeline_generator import generate_timeline
from modules.youtube_transcript import fetch_youtube_transcript


# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------

st.set_page_config(
    page_title="Video Insight Agent",
    page_icon="🎥",
    layout="wide"
)

st.title("🎥 Video Insight Agent")
st.caption("Analyze videos and ask questions with timestamp citations.")


# ------------------------------------------------
# SESSION STATE
# ------------------------------------------------

defaults = {
    "transcript": None,
    "summary": None,
    "flashcards": None,
    "timelines": {},
    "index": None,
    "chunks": None,
    "chat_history": []
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ------------------------------------------------
# HELPERS
# ------------------------------------------------

def seconds_to_timestamp(sec):
    m = int(sec // 60)
    s = int(sec % 60)
    return f"{m}:{s:02d}"


def parse_timeline(text):

    timeline = []

    for line in text.split("\n"):

        line = line.strip()
        line = line.replace("•", "").strip()

        match = re.match(r"(\d+:\d+(?::\d+)?)\s*[-–:]?\s*(.*)", line)

        if match:
            timeline.append((match.group(1), match.group(2)))

    return timeline


# ------------------------------------------------
# SIDEBAR
# ------------------------------------------------

with st.sidebar:

    st.header("📂 Videos")

    youtube_urls = st.text_area(
        "Paste YouTube links (one per line)"
    )

    uploaded_files = st.file_uploader(
        "Upload videos",
        type=["mp4","mov","mkv"],
        accept_multiple_files=True
    )

    st.divider()

    process_button = st.button("🚀 Process Videos")


# ------------------------------------------------
# PROCESS VIDEOS
# ------------------------------------------------

if process_button:

    transcripts = []
    all_chunks = []
    video_labels = []
    video_timelines = {}

    progress = st.progress(0)
    step = 0


    # ----------------------------------------------
    # YOUTUBE VIDEOS
    # ----------------------------------------------

    if youtube_urls:

        urls = [u.strip() for u in youtube_urls.split("\n") if u.strip()]

        for i, url in enumerate(urls):

            transcript, segments = fetch_youtube_transcript(url)

            transcripts.append(transcript)

            label = f"YouTube Video {i+1}"
            video_labels.append(label)

            for seg in segments:

                ts = seconds_to_timestamp(seg["start"])
                chunk = f"{label} | {ts} | {seg['text']}"

                all_chunks.append(chunk)

            timeline = generate_timeline(transcript)
            video_timelines[label] = timeline

            step += 1
            progress.progress(min(step*20,60))


    # ----------------------------------------------
    # UPLOADED VIDEOS
    # ----------------------------------------------

    if uploaded_files:

        os.makedirs("downloads", exist_ok=True)

        for i, file in enumerate(uploaded_files):

            path = os.path.join("downloads", file.name)

            with open(path,"wb") as f:
                f.write(file.read())

            audio_path = extract_audio(path)

            transcript, segments = transcribe_audio(audio_path)

            transcripts.append(transcript)

            label = f"Uploaded Video {i+1}"
            video_labels.append(label)

            for seg in segments:

                ts = seconds_to_timestamp(seg["start"])
                chunk = f"{label} | {ts} | {seg['text']}"

                all_chunks.append(chunk)

            timeline = generate_timeline(transcript)
            video_timelines[label] = timeline

            step += 1
            progress.progress(min(step*20,60))


    combined = "\n\n".join(transcripts)

    summary = summarize_transcript(combined)
    flashcards = generate_flashcards(combined)

    index, chunks = create_vector_store(all_chunks)

    st.session_state.transcript = combined
    st.session_state.summary = summary
    st.session_state.flashcards = flashcards
    st.session_state.timelines = video_timelines
    st.session_state.index = index
    st.session_state.chunks = chunks

    progress.progress(100)
    st.success("Processing complete")


# ------------------------------------------------
# MAIN TABS
# ------------------------------------------------

if st.session_state.transcript:

    tab = st.radio(
        "",
        ["Transcript","Summary","Flashcards","Timeline","Semantic Search","Ask"],
        horizontal=True,
        key="main_tabs"
    )


# ------------------------------------------------
# TRANSCRIPT
# ------------------------------------------------

    if tab == "Transcript":

        st.text_area(
            "",
            st.session_state.transcript,
            height=400
        )


# ------------------------------------------------
# SUMMARY
# ------------------------------------------------

    elif tab == "Summary":

        st.write(st.session_state.summary)


# ------------------------------------------------
# FLASHCARDS
# ------------------------------------------------

    elif tab == "Flashcards":

        st.write(st.session_state.flashcards)


# ------------------------------------------------
# TIMELINE
# ------------------------------------------------

    elif tab == "Timeline":

        st.subheader("Video Timelines")

        for video_name, timeline_text in st.session_state.timelines.items():

            st.markdown(f"### {video_name}")

            timeline_items = parse_timeline(timeline_text)

            for timestamp, desc in timeline_items:

                col1, col2 = st.columns([1,5])

                with col1:
                    st.markdown(f"**{timestamp}**")

                with col2:
                    st.write(desc)

            st.divider()


# ------------------------------------------------
# SEMANTIC SEARCH
# ------------------------------------------------

    elif tab == "Semantic Search":

        query = st.text_input("Search topic")

        if query:

            results = retrieve(
                query,
                st.session_state.index,
                st.session_state.chunks
            )

            best = results[0]

            parts = best.split("|")

            st.success(f"{parts[0]} — {parts[1]}")
            st.write(parts[2])


# ------------------------------------------------
# ASK TAB
# ------------------------------------------------

    elif tab == "Ask":

        st.subheader("Ask Questions")

        col1, col2 = st.columns([8,1])

        with col1:
            question = st.text_input(
                "",
                placeholder="Ask something about the videos..."
            )

        with col2:
            ask_clicked = st.button("Ask")

        if ask_clicked and question:

            relevant_chunks = retrieve(
                question,
                st.session_state.index,
                st.session_state.chunks
            )

            answer = answer_question(question,relevant_chunks)

            sources = []

            for chunk in relevant_chunks:

                parts = chunk.split("|")

                if len(parts) >= 2:
                    sources.append((parts[0],parts[1]))

            source_text = "\n".join(
                [f"{v} — {t}" for v,t in sources]
            )

            final_answer = f"{answer}\n\nSources:\n{source_text}"

            st.session_state.chat_history.append({
                "question":question,
                "answer":final_answer
            })

        st.divider()

        for chat in reversed(st.session_state.chat_history):

            st.markdown(f"**You:** {chat['question']}")
            st.markdown(f"**AI:** {chat['answer']}")
            st.divider()