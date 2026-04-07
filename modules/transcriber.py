from functools import lru_cache
from pathlib import Path

import whisper

from modules.cache import build_cache_key, load_json_cache, save_json_cache
from modules.errors import ProcessingError
from modules.translator import normalize_language_code


@lru_cache(maxsize=1)
def get_whisper_model():
    try:
        return whisper.load_model("base")
    except Exception as exc:
        raise ProcessingError(f"Unable to load Whisper model: {exc}") from exc


def _audio_cache_key(audio_path: str) -> str:
    file_path = Path(audio_path)

    if not file_path.exists():
        raise ProcessingError(f"Audio file not found: {audio_path}")

    stats = file_path.stat()
    return build_cache_key(
        "transcription",
        str(file_path.resolve()),
        stats.st_size,
        stats.st_mtime_ns,
    )


def transcribe_audio(audio_path: str):
    """
    Transcribe audio using Whisper and return:
    - full transcript
    - timestamped segments
    """
    cache_key = _audio_cache_key(audio_path)
    cached_transcript = load_json_cache("transcription", cache_key)

    if cached_transcript:
        return (
            cached_transcript["transcript"],
            cached_transcript["segments"],
            cached_transcript["detected_language"],
        )

    model = get_whisper_model()

    try:
        result = model.transcribe(audio_path)
    except Exception as exc:
        raise ProcessingError(f"Unable to transcribe audio '{audio_path}': {exc}") from exc

    detected_language = normalize_language_code(result.get("language"))

    if detected_language in {"hi", "bn"}:
        try:
            result = model.transcribe(audio_path, task="translate")
        except Exception as exc:
            raise ProcessingError(
                f"Unable to translate audio '{audio_path}' to English: {exc}"
            ) from exc

    transcript = result["text"]

    segments = []

    for segment in result["segments"]:

        segments.append({
            "start": segment["start"],
            "end": segment["end"],
            "text": segment["text"].strip()
        })

    save_json_cache(
        "transcription",
        cache_key,
        {
            "transcript": transcript,
            "segments": segments,
            "detected_language": detected_language,
        },
    )

    return transcript, segments, detected_language
