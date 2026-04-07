import re
from youtube_transcript_api import YouTubeTranscriptApi

from modules.cache import build_cache_key, load_json_cache, save_json_cache
from modules.errors import ExternalServiceError, ProcessingError
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

    raise ProcessingError("Invalid YouTube URL.")


def fetch_youtube_transcript(url: str):
    """
    Fetch transcript and timestamps from YouTube
    """
    video_id = extract_video_id(url)
    cache_key = build_cache_key("youtube_transcript", video_id)
    cached_transcript = load_json_cache("youtube_transcript", cache_key)

    if cached_transcript:
        return (
            cached_transcript["transcript_text"],
            cached_transcript["segments"],
            cached_transcript["metadata"],
        )

    try:
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
    except ProcessingError:
        raise
    except Exception as exc:
        raise ExternalServiceError(
            f"Unable to fetch YouTube transcript for video '{video_id}': {exc}"
        ) from exc

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

    save_json_cache(
        "youtube_transcript",
        cache_key,
        {
            "transcript_text": transcript_text,
            "segments": segments,
            "metadata": metadata,
        },
    )

    return transcript_text, segments, metadata
