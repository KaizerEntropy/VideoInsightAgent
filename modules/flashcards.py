
from modules.llm import ask_llm


MAX_CHUNK_WORDS = 1200


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
Create 8 concise, high-quality study flashcards from the following transcript section.

Format:
Q: question on one line
A: answer on the next line

Rules:
- Keep each question and answer clearly separate
- Make the answer directly respond to the question
- Avoid repeating the same fact across cards
- Prefer covering different sections, examples, and conclusions from the transcript
- Use clear English
- Output only flashcards in the exact format above

Transcript:
{chunk}
"""

        result = ask_llm(prompt)

        all_flashcards.append(result)

    return "\n\n".join(all_flashcards)
