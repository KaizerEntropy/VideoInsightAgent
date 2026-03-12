
from modules.llm import ask_llm


MAX_CHUNK_WORDS = 1500


def chunk_text(text, chunk_size=MAX_CHUNK_WORDS):
    """
    Split text into smaller chunks so we do not exceed
    Groq token limits.
    """

    words = text.split()

    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks


def generate_flashcards(transcript: str) -> str:
    """
    Generate flashcards from a long transcript using
    chunked processing.
    """

    chunks = chunk_text(transcript)

    all_flashcards = []

    for chunk in chunks:

        prompt = f"""
Create 5 concise flashcards from the following transcript section.

Format:
Q: question
A: answer

Transcript:
{chunk}
"""

        result = ask_llm(prompt)

        all_flashcards.append(result)

    return "\n\n".join(all_flashcards)

