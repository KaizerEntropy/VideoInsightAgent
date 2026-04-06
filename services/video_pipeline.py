import os

import streamlit as st

from modules.audio_extractor import extract_audio
from modules.flashcards import generate_flashcards
from modules.summarizer import summarize_transcript
from modules.timeline_generator import generate_timeline
from modules.transcriber import transcribe_audio
from modules.vector_store import create_vector_store
from modules.youtube_transcript import fetch_youtube_transcript
from ui.parsers import format_language_name, seconds_to_timestamp


def _process_youtube_sources(urls: list[str], progress_bar, start_step: int):
    transcripts = []
    chunks = []
    labels = []
    timelines = {}
    source_details = []
    step = start_step

    for index, url in enumerate(urls):
        transcript, segments, metadata = fetch_youtube_transcript(url)
        label = f"YouTube Video {index + 1}"

        transcripts.append(transcript)
        labels.append(label)
        source_details.append(
            {
                "label": label,
                "language": metadata["source_language"],
                "translated": metadata["translated_to_english"],
            }
        )

        for segment in segments:
            timestamp = seconds_to_timestamp(segment["start"])
            chunks.append(f"{label} | {timestamp} | {segment['text']}")

        timelines[label] = generate_timeline(transcript, segments)
        step += 1
        progress_bar.progress(min(step * 20, 60))

    return transcripts, chunks, labels, timelines, source_details, step


def _process_uploaded_sources(uploaded_files, progress_bar, start_step: int):
    transcripts = []
    chunks = []
    labels = []
    timelines = {}
    source_details = []
    step = start_step

    if uploaded_files:
        os.makedirs("downloads", exist_ok=True)

    for index, uploaded_file in enumerate(uploaded_files or []):
        file_path = os.path.join("downloads", uploaded_file.name)

        with open(file_path, "wb") as output_file:
            output_file.write(uploaded_file.read())

        audio_path = extract_audio(file_path)
        transcript, segments, detected_language = transcribe_audio(audio_path)
        label = f"Uploaded Video {index + 1}"

        transcripts.append(transcript)
        labels.append(label)
        source_details.append(
            {
                "label": label,
                "language": format_language_name(detected_language),
                "translated": detected_language in {"hi", "bn"},
            }
        )

        for segment in segments:
            timestamp = seconds_to_timestamp(segment["start"])
            chunks.append(f"{label} | {timestamp} | {segment['text']}")

        timelines[label] = generate_timeline(transcript, segments)
        step += 1
        progress_bar.progress(min(step * 20, 60))

    return transcripts, chunks, labels, timelines, source_details, step


def process_video_inputs(youtube_urls: list[str], uploaded_files):
    progress_bar = st.progress(0)

    transcripts = []
    chunks = []
    labels = []
    timelines = {}
    source_details = []
    step = 0

    urls = [url.strip() for url in youtube_urls if url and url.strip()]

    if not urls and not uploaded_files:
        progress_bar.empty()
        return {
            "transcript": None,
            "summary": None,
            "flashcards": None,
            "timelines": {},
            "index": None,
            "chunks": None,
            "source_labels": [],
            "source_details": [],
            "last_search_result": "",
        }

    (
        yt_transcripts,
        yt_chunks,
        yt_labels,
        yt_timelines,
        yt_source_details,
        step,
    ) = _process_youtube_sources(urls, progress_bar, step)

    transcripts.extend(yt_transcripts)
    chunks.extend(yt_chunks)
    labels.extend(yt_labels)
    timelines.update(yt_timelines)
    source_details.extend(yt_source_details)

    (
        uploaded_transcripts,
        uploaded_chunks,
        uploaded_labels,
        uploaded_timelines,
        uploaded_source_details,
        step,
    ) = _process_uploaded_sources(uploaded_files, progress_bar, step)

    transcripts.extend(uploaded_transcripts)
    chunks.extend(uploaded_chunks)
    labels.extend(uploaded_labels)
    timelines.update(uploaded_timelines)
    source_details.extend(uploaded_source_details)

    combined_transcript = "\n\n".join(transcripts)
    summary = summarize_transcript(combined_transcript)
    flashcards = generate_flashcards(combined_transcript)
    index, indexed_chunks = create_vector_store(chunks) if chunks else (None, [])

    progress_bar.progress(100)

    return {
        "transcript": combined_transcript,
        "summary": summary,
        "flashcards": flashcards,
        "timelines": timelines,
        "index": index,
        "chunks": indexed_chunks,
        "source_labels": labels,
        "source_details": source_details,
        "last_search_result": "",
    }
