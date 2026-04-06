import whisper
from modules.translator import normalize_language_code

# Load Whisper model once
model = whisper.load_model("base")


def transcribe_audio(audio_path: str):
    """
    Transcribe audio using Whisper and return:
    - full transcript
    - timestamped segments
    """

    result = model.transcribe(audio_path)
    detected_language = normalize_language_code(result.get("language"))

    if detected_language in {"hi", "bn"}:
        result = model.transcribe(audio_path, task="translate")

    transcript = result["text"]

    segments = []

    for segment in result["segments"]:

        segments.append({
            "start": segment["start"],
            "end": segment["end"],
            "text": segment["text"].strip()
        })

    return transcript, segments, detected_language
