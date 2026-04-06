import streamlit as st

from modules.qa_agent import answer_question
from modules.vector_store import retrieve
from services.video_pipeline import process_video_inputs
from ui.parsers import parse_timeline
from ui.renderers import (
    estimate_text_height,
    load_css,
    render_ask_intro,
    render_ask_messages,
    render_copy_section,
    render_download_button,
    render_empty_ask_state,
    render_empty_state,
    render_flashcards,
    render_hero,
    render_panel,
    render_search_insight,
    render_search_result_card,
    render_source_overview,
    render_stats,
    render_timeline_section,
    render_timeline_copy_controls,
)
from ui.sidebar import render_sidebar_inputs
from ui.state import initialize_session_state


st.set_page_config(
    page_title="Video Insight Agent",
    page_icon="🎥",
    layout="wide",
)

load_css("assets/styles.css")
initialize_session_state()
render_hero()
youtube_urls, uploaded_files, process_button = render_sidebar_inputs()


if process_button:
    if not youtube_urls and not uploaded_files:
        st.warning("Add at least one YouTube link or uploaded video before processing.")
    else:
        processed_data = process_video_inputs(youtube_urls, uploaded_files)

        for key, value in processed_data.items():
            st.session_state[key] = value

        st.success("Processing complete")


if st.session_state.transcript:
    render_panel(
        "Analysis workspace",
        "Browse the translated English transcript, review generated study material, search concepts, or ask questions with cited timestamps.",
    )
    with st.expander("Workspace Details", expanded=False):
        render_stats(st.session_state)
        render_source_overview(st.session_state)

    tab = st.radio(
        "",
        ["Transcript", "Summary", "Flashcards", "Timeline", "Semantic Search", "Ask"],
        horizontal=True,
        key="main_tabs",
    )

    if tab == "Transcript":
        render_panel(
            "Full transcript",
            "Read the combined English transcript from every processed source in a single scrollable view.",
            label="Transcript",
        )
        render_download_button(
            "Download Transcript",
            st.session_state.transcript or "",
            "video_insight_transcript.txt",
        )
        st.text_area(
            "Transcript",
            st.session_state.transcript,
            height=estimate_text_height(
                st.session_state.transcript or "",
                minimum=420,
                maximum=1100,
            ),
        )
        render_copy_section(
            "Copy Transcript",
            st.session_state.transcript or "",
            key="copy_transcript",
            height=estimate_text_height(
                st.session_state.transcript or "",
                minimum=220,
                maximum=800,
            ),
        )

    elif tab == "Summary":
        render_panel(
            "Condensed overview",
            "A single AI summary stitched from the processed English transcript chunks.",
            label="Summary",
        )
        render_download_button(
            "Download Summary",
            st.session_state.summary or "",
            "video_insight_summary.txt",
        )
        st.text_area(
            "Summary",
            st.session_state.summary or "",
            height=estimate_text_height(
                st.session_state.summary or "",
                minimum=260,
                maximum=700,
            ),
            key="summary_view",
        )
        render_copy_section(
            "Copy Summary",
            st.session_state.summary or "",
            key="copy_summary",
            height=estimate_text_height(
                st.session_state.summary or "",
                minimum=220,
                maximum=600,
            ),
        )

    elif tab == "Flashcards":
        render_panel(
            "Study flashcards",
            "Quick question-answer pairs generated from the transcript, laid out as readable study cards with clear answer separation.",
            label="Flashcards",
        )
        render_download_button(
            "Download Flashcards",
            st.session_state.flashcards or "",
            "video_insight_flashcards.txt",
        )
        render_flashcards(st.session_state.flashcards)
        render_copy_section(
            "Copy Flashcards",
            st.session_state.flashcards or "",
            key="copy_flashcards",
            height=estimate_text_height(
                st.session_state.flashcards or "",
                minimum=260,
                maximum=700,
            ),
        )

    elif tab == "Timeline":
        render_panel(
            "Timeline view",
            "Each video gets a smarter sequence of timestamped moments based on transcript progression and topic shifts.",
            label="Timeline",
        )
        st.subheader("Video Timelines")

        for video_name, timeline_text in st.session_state.timelines.items():
            render_timeline_section(video_name, timeline_text)

        timeline_export_lines = []
        for video_name, timeline_text in st.session_state.timelines.items():
            timeline_export_lines.append(video_name)
            for timestamp, description in parse_timeline(timeline_text):
                timeline_export_lines.append(f"{timestamp} - {description}")
            timeline_export_lines.append("")

        timeline_export = "\n".join(timeline_export_lines).strip()

        if timeline_export:
            render_timeline_copy_controls(timeline_export)

    elif tab == "Semantic Search":
        render_panel(
            "Semantic search",
            "Search by meaning, not just exact wording. Results are reranked using both semantic similarity and keyword overlap.",
            label="Search",
        )

        query = st.text_input("Search topic")

        if query:
            if not st.session_state.index or not st.session_state.chunks:
                st.info("Search is unavailable until searchable transcript chunks are created.")
                results = []
            else:
                results = retrieve(query, st.session_state.index, st.session_state.chunks, k=8)

            if results:
                formatted_results = []

                for rank, result in enumerate(results, start=1):
                    parts = [part.strip() for part in result.split("|", 2)]
                    if len(parts) < 3:
                        continue

                    formatted_results.append(
                        f"Match {rank}: {parts[0]} | {parts[1]}\n{parts[2]}"
                    )
                    render_search_result_card(rank, parts[0], parts[1], parts[2])

                search_answer = answer_question(query, results)
                search_output = f"{search_answer}\n\nMatches:\n" + "\n\n".join(formatted_results)
                st.session_state.last_search_result = search_output

                render_search_insight(search_answer)
                render_download_button(
                    "Download Search Answer",
                    search_output,
                    "video_insight_search_answer.txt",
                )
                render_copy_section(
                    "Copy Search Answer",
                    search_output,
                    key="copy_search_answer",
                    height=estimate_text_height(
                        search_output,
                        minimum=220,
                        maximum=650,
                    ),
                )
            else:
                st.info("No relevant matches were found for that search.")

    elif tab == "Ask":
        render_panel(
            "Conversational QA",
            "Ask about concepts, examples, or moments in the videos and get grounded English answers with source timestamps.",
            label="Ask",
        )
        render_ask_intro()

        with st.form("ask_form", clear_on_submit=True):
            question = st.text_input(
                "Your question",
                placeholder="Ask something about the videos...",
            )
            ask_clicked = st.form_submit_button("Ask")

        if ask_clicked and question:
            if not st.session_state.index or not st.session_state.chunks:
                st.info("Q&A is unavailable until searchable transcript chunks are created.")
                relevant_chunks = []
                answer = "No searchable transcript context is available yet."
            else:
                relevant_chunks = retrieve(
                    question,
                    st.session_state.index,
                    st.session_state.chunks,
                    k=8,
                )
                answer = answer_question(question, relevant_chunks)

            sources = []
            for chunk in relevant_chunks:
                parts = chunk.split("|")
                if len(parts) >= 2:
                    sources.append((parts[0], parts[1]))

            source_text = "\n".join([f"{video} — {timestamp}" for video, timestamp in sources])
            final_answer = f"{answer}\n\nSources:\n{source_text}"

            st.session_state.chat_history.append(
                {
                    "question": question,
                    "answer": final_answer,
                }
            )

        if st.session_state.chat_history:
            render_ask_messages(st.session_state.chat_history)
        else:
            render_empty_ask_state()
else:
    render_empty_state()
