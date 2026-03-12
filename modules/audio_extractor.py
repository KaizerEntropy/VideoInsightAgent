from moviepy import VideoFileClip
import os


def extract_audio(video_path: str) -> str:
    """
    Extract audio from a video file.

    If the input is already an audio file (.mp3/.wav),
    return it directly without processing.
    """

    if video_path.endswith((".mp3", ".wav")):
        return video_path

    audio_path = video_path + ".wav"

    # Avoid re-extracting if file already exists
    if os.path.exists(audio_path):
        return audio_path

    video = VideoFileClip(video_path)

    audio = video.audio
    audio.write_audiofile(audio_path)

    video.close()

    return audio_path