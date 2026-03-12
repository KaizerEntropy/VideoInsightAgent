import yt_dlp
import os
import uuid
import streamlit as st


DOWNLOAD_DIR = "downloads"


@st.cache_data(show_spinner=False)
def download_youtube_video(url: str) -> str:
    """
    Download audio from YouTube safely using browser cookies.
    This avoids YouTube bot detection.
    """

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    unique_id = str(uuid.uuid4())

    output_template = os.path.join(DOWNLOAD_DIR, f"youtube_{unique_id}.%(ext)s")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_template,
        "quiet": True,

        # IMPORTANT FIX
        "cookiesfrombrowser": ("chrome",),

        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192"
            }
        ]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:

        info = ydl.extract_info(url, download=True)

        filename = ydl.prepare_filename(info)

    base, _ = os.path.splitext(filename)

    final_path = base + ".mp3"

    if not os.path.exists(final_path):
        raise RuntimeError(f"Download failed. File not found: {final_path}")

    return final_path