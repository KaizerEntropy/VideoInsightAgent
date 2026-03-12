from modules.llm import ask_llm


def generate_timeline(transcript: str) -> str:
    """
    Generate a structured timeline from a transcript.

    Output format:
    MM:SS - description
    """

    prompt = f"""
Create a concise timeline of the video.

Rules:
- 8 to 12 bullet points
- Format: MM:SS - description
- Keep descriptions short
- Chronological order
- Only output the timeline

Transcript:
{transcript[:4000]}
"""

    timeline = ask_llm(prompt)

    return timeline