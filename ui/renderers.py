import html

import streamlit as st

from ui.parsers import parse_flashcards, parse_timeline


def load_css(file_path: str):
    with open(file_path, encoding="utf-8") as css_file:
        st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)


def render_hero():
    st.markdown(
        """
        <section class="hero-shell">
            <div class="hero-badge">Multimodal Study Workspace</div>
            <h1 class="hero-title">Video Insight Agent</h1>
            <p class="hero-copy">
                Turn long-form video into a searchable knowledge base with transcripts,
                summaries, flashcards, semantic retrieval, and timestamped answers.
            </p>
            <div class="hero-grid">
                <div class="hero-card">
                    <div class="hero-kicker">Input</div>
                    <div class="hero-metric">Uploads + YouTube</div>
                    <div class="hero-note">Process one source or blend several into one workspace.</div>
                </div>
                <div class="hero-card">
                    <div class="hero-kicker">Output</div>
                    <div class="hero-metric">Summary + QA</div>
                    <div class="hero-note">Move from raw footage to study-ready insight in one pass.</div>
                </div>
                <div class="hero-card">
                    <div class="hero-kicker">Search</div>
                    <div class="hero-metric">Timestamped Retrieval</div>
                    <div class="hero-note">Ask targeted questions and jump to the relevant moment fast.</div>
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_panel(title: str, description: str, label: str = "Workspace"):
    st.markdown(
        f"""
        <section class="panel-card">
            <div class="panel-label">{label}</div>
            <div class="panel-title">{title}</div>
            <p class="panel-copy">{description}</p>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_stats(state):
    flashcards = parse_flashcards(state.flashcards or "")
    timeline_points = sum(
        len(parse_timeline(timeline_text))
        for timeline_text in state.timelines.values()
    )

    stats = [
        ("Sources", str(len(state.source_labels)), "Videos processed into one workspace"),
        ("Transcript Chunks", str(len(state.chunks or [])), "Searchable timestamped units"),
        ("Flashcards", str(len(flashcards)), "Question and answer study cards"),
        ("Timeline Points", str(timeline_points), "Moments extracted across videos"),
    ]

    columns = st.columns(len(stats))

    for column, (label, value, note) in zip(columns, stats):
        with column:
            st.markdown(
                f"""
                <div class="stat-card">
                    <div class="stat-label">{html.escape(label)}</div>
                    <div class="stat-value">{html.escape(value)}</div>
                    <div class="stat-note">{html.escape(note)}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_source_overview(state):
    if not state.source_details:
        return

    cards = []

    for source in state.source_details:
        translation_note = (
            "Translated to English" if source["translated"] else "Processed directly in English"
        )
        cards.append(
            f"""
            <div class="source-card">
                <div class="source-title">{html.escape(source['label'])}</div>
                <div class="source-meta">{html.escape(source['language'])}</div>
                <div class="source-note">{html.escape(translation_note)}</div>
            </div>
            """
        )

    st.markdown(f'<div class="source-grid">{"".join(cards)}</div>', unsafe_allow_html=True)


def render_empty_state():
    st.markdown(
        """
        <section class="empty-card">
            <div class="panel-label">Ready To Process</div>
            <div class="empty-title">Start with a video or a YouTube link</div>
            <p class="empty-copy">
                Add one or more sources from the sidebar, then run processing to unlock the
                transcript, summary, flashcards, semantic search, and question answering tabs.
            </p>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_flashcards(flashcards_text: str):
    flashcards = parse_flashcards(flashcards_text)

    if not flashcards:
        st.write(flashcards_text)
        return

    for start_index in range(0, len(flashcards), 2):
        columns = st.columns(2)
        current_cards = flashcards[start_index:start_index + 2]

        for offset, item in enumerate(current_cards):
            with columns[offset]:
                with st.container(border=True):
                    st.caption(f"Flashcard {start_index + offset + 1}")
                    st.markdown(f"**{item['question']}**")
                    st.divider()
                    st.markdown("`Answer`")
                    st.write(item["answer"])


def render_download_button(label: str, data: str, file_name: str):
    st.download_button(
        label,
        data=data,
        file_name=file_name,
        mime="text/plain",
        use_container_width=True,
    )


def estimate_text_height(
    value: str,
    minimum: int = 220,
    maximum: int = 900,
    line_height: int = 24,
) -> int:
    if not value:
        return minimum

    line_count = max(1, len(value.splitlines()))
    estimated = (line_count + 2) * line_height
    return max(minimum, min(maximum, estimated))


def render_copy_box(label: str, value: str, key: str, height: int = 180):
    st.text_area(label, value, height=height, key=key)


def render_copy_section(label: str, value: str, key: str, height: int = 180):
    with st.expander(label, expanded=False):
        render_copy_box("Select and copy", value, key=key, height=height)


def render_search_result_card(rank: int, source: str, timestamp: str, text: str):
    st.markdown(
        f"""
        <div class="search-card">
            <div class="panel-label">Match {rank}</div>
            <div class="panel-title">{html.escape(source)} | {html.escape(timestamp)}</div>
            <p class="panel-copy">{html.escape(text)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_search_insight(answer: str):
    st.markdown(
        f"""
        <div class="search-insight-card">
            <div class="panel-label">Search Insight</div>
            <div class="panel-title">What the best matches suggest</div>
            <p class="panel-copy">{html.escape(answer)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_timeline_section(video_name: str, timeline_text: str):
    st.markdown(f"### {video_name}")

    for timestamp, description in parse_timeline(timeline_text):
        st.markdown(
            f"""
            <section class="timeline-card">
                <div class="timeline-time">{html.escape(timestamp)}</div>
                <div class="timeline-desc">{html.escape(description)}</div>
            </section>
            """,
            unsafe_allow_html=True,
        )

    st.divider()


def render_timeline_copy_controls(timeline_export: str):
    render_download_button(
        "Download Timeline",
        timeline_export,
        "video_insight_timeline.txt",
    )
    render_copy_section(
        "Copy Timeline",
        timeline_export,
        key="copy_timeline",
        height=estimate_text_height(timeline_export, minimum=220, maximum=700),
    )


def render_ask_intro():
    st.markdown(
        """
        <div class="ask-shell">
            <div class="ask-title">Ask Questions About The Videos</div>
            <div class="ask-copy">
                Ask naturally and the app will answer from retrieved transcript evidence with timestamped sources.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_ask_messages(chat_history: list[dict[str, str]]):
    for index, chat in enumerate(reversed(chat_history), start=1):
        st.markdown(
            f"""
            <div class="message-shell">
                <div class="message-card message-user">
                    <div class="message-label">You Asked</div>
                    <div class="message-question">{html.escape(chat['question'])}</div>
                </div>
                <div class="message-card message-ai">
                    <div class="message-label">Answer</div>
                    <div class="message-answer">{html.escape(chat['answer'])}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        render_download_button(
            f"Download Answer {index}",
            chat["answer"],
            f"video_insight_answer_{index}.txt",
        )
        render_copy_section(
            f"Copy Answer {index}",
            chat["answer"],
            key=f"copy_answer_{index}",
            height=estimate_text_height(
                chat["answer"],
                minimum=200,
                maximum=650,
            ),
        )


def render_empty_ask_state():
    st.markdown(
        """
        <div class="empty-card">
            <div class="panel-label">No Questions Yet</div>
            <div class="empty-title">Your answers will appear here</div>
            <p class="empty-copy">
                Ask about a concept, example, or moment in the processed videos to start a clean Q&A thread.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
