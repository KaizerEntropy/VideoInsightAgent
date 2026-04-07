from moviepy import VideoFileClip
import os

from modules.errors import ProcessingError


def extract_audio(video_path: str) -> str:
    """
    Extract audio from a video file.

    If the input is already an audio file (.mp3/.wav),
    return it directly without processing.
    """

    if not os.path.exists(video_path):
        raise ProcessingError(f"Input file not found: {video_path}")

    if video_path.endswith((".mp3", ".wav")):
        return video_path

    audio_path = video_path + ".wav"

    # Avoid re-extracting if file already exists
    if os.path.exists(audio_path):
        return audio_path

    video = None

    try:
        video = VideoFileClip(video_path)
        audio = video.audio

        if audio is None:
            raise ProcessingError(f"No audio track found in file: {video_path}")

        audio.write_audiofile(audio_path)
    except ProcessingError:
        raise
    except Exception as exc:
        raise ProcessingError(f"Unable to extract audio from '{video_path}': {exc}") from exc
    finally:
        if video is not None:
            video.close()

    return audio_path
