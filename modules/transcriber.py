import whisper

# Load Whisper model once
model = whisper.load_model("base")


def transcribe_audio(audio_path: str):
    """
    Transcribe audio using Whisper and return:
    - full transcript
    - timestamped segments
    """

    result = model.transcribe(audio_path)

    transcript = result["text"]

    segments = []

    for segment in result["segments"]:

        segments.append({
            "start": segment["start"],
            "end": segment["end"],
            "text": segment["text"].strip()
        })

    return transcript, segments