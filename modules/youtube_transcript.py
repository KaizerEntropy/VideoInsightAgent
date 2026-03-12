import re
from youtube_transcript_api import YouTubeTranscriptApi


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

    transcript = api.fetch(video_id)

    full_text = []
    segments = []

    for item in transcript:

        text = item["text"]
        start = item["start"]

        full_text.append(text)

        segments.append({
            "start": start,
            "text": text
        })

    return " ".join(full_text), segments