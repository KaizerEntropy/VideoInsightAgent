from modules.llm import ask_llm


def seconds_to_timestamp(seconds: float) -> str:
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"


def select_representative_segments(segments: list[dict], target_count: int = 160) -> list[dict]:
    if len(segments) <= target_count:
        return segments

    stride = max(1, len(segments) // target_count)
    selected = segments[::stride]

    if selected[-1] != segments[-1]:
        selected.append(segments[-1])

    return selected[:target_count]


def build_timeline_context(segments: list[dict], max_segments: int = 160) -> str:
    if not segments:
        return ""

    sampled_segments = select_representative_segments(segments, max_segments)
    lines = []

    for segment in sampled_segments:
        lines.append(
            f"{seconds_to_timestamp(segment['start'])} - {segment['text']}"
        )

    return "\n".join(lines)


def generate_timeline(transcript: str, segments: list[dict] | None = None) -> str:
    """
    Generate a structured timeline from a transcript.

    Output format:
    MM:SS - description
    """

    if not transcript or not transcript.strip():
        return "Timeline unavailable because no transcript was produced."

    timestamped_context = build_timeline_context(segments or [])
    context = timestamped_context or transcript[:4000]

    prompt = f"""
Create a concise but intelligent timeline of the video.

Rules:
- 10 to 14 bullet points
- Format: MM:SS - description
- Keep descriptions short but specific
- Chronological order
- Focus on topic shifts, major examples, demonstrations, or conclusions
- Only output the timeline
- Use the supplied timestamps instead of inventing new moments
- Cover the beginning, middle, and ending of the full video

Transcript:
{context}
"""

    timeline = ask_llm(prompt)

    return timeline
