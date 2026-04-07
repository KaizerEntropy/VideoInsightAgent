
from modules.llm import ask_llm


MAX_CHUNK_SIZE = 2000


def chunk_text(text, chunk_size=MAX_CHUNK_SIZE):
    """
    Split long text into smaller chunks
    to avoid token limits.
    """

    words = text.split()

    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks


def summarize_transcript(transcript: str) -> str:
    """
    Summarize long transcripts safely
    using chunk-based summarization.
    """

    if not transcript or not transcript.strip():
        return "No transcript was available to summarize."

    chunks = chunk_text(transcript)

    partial_summaries = []

    for chunk in chunks:

        prompt = f"""
Summarize the following transcript section clearly:

{chunk}
"""

        summary = ask_llm(prompt)

        partial_summaries.append(summary)

    combined = "\n".join(partial_summaries)

    final_prompt = f"""
Combine these summaries into a single clear summary:

{combined}
"""

    final_summary = ask_llm(final_prompt)

    return final_summary
