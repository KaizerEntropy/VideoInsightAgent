import re
from youtube_transcript_api import YouTubeTranscriptApi

from modules.translator import (
    SUPPORTED_TRANSLATION_LANGUAGES,
    is_supported_non_english,
    normalize_language_code,
    translate_text_to_english,
)


def extract_video_id(url: str):
    """
    Extract YouTube video ID from URL
    """

    patterns = [
        r"v=([^&]+)",
        r"youtu\.be/([^?]+)",
        r"embed/([^?]+)"
    ]

    for pattern in patterns:
        match = re.search(pattern, url)

        if match:
            return match.group(1)

    raise ValueError("Invalid YouTube URL")


def fetch_youtube_transcript(url: str):
    """
    Fetch transcript and timestamps from YouTube
    """

    video_id = extract_video_id(url)

    api = YouTubeTranscriptApi()
    transcript_list = api.list(video_id)

    preferred_languages = ["en", "hi", "bn"]
    transcript = transcript_list.find_transcript(preferred_languages)
    source_language = normalize_language_code(transcript.language_code)
    translated = False

    if is_supported_non_english(source_language):
        translation_languages = {
            item["language_code"] for item in transcript.translation_languages
        }

        if "en" in translation_languages:
            transcript = transcript.translate("en")
            translated = True

    fetched_transcript = transcript.fetch()

    full_text = []
    segments = []

    for item in fetched_transcript:

        text = item.text
        start = item.start

        full_text.append(text)

        segments.append({
            "start": start,
            "text": text
        })

    transcript_text = " ".join(full_text)

    if is_supported_non_english(source_language) and not translated:
        transcript_text = translate_text_to_english(transcript_text, source_language)
        for segment in segments:
            segment["text"] = translate_text_to_english(segment["text"], source_language)
        translated = True

    metadata = {
        "source_language": SUPPORTED_TRANSLATION_LANGUAGES.get(
            source_language,
            source_language,
        ),
        "translated_to_english": translated,
    }

    return transcript_text, segments, metadata
