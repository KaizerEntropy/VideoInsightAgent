
from modules.llm import ask_llm


MAX_CONTEXT_CHUNKS = 8


def build_context(chunks: list[str]) -> str:
    selected_chunks = chunks[:MAX_CONTEXT_CHUNKS]
    context_lines = []

    for index, chunk in enumerate(selected_chunks, start=1):
        parts = [part.strip() for part in chunk.split("|", 2)]
        if len(parts) == 3:
            context_lines.append(
                f"[{index}] Source: {parts[0]} | Timestamp: {parts[1]} | Text: {parts[2]}"
            )
        else:
            context_lines.append(f"[{index}] {chunk}")

    return "\n".join(context_lines)


def answer_question(question: str, chunks: list[str]) -> str:
    """
    Answer a question using retrieved transcript chunks.
    Limits context size to avoid token overflow.
    """

    if not chunks:
        return "I could not find relevant transcript context to answer that question."

    context = build_context(chunks)

    prompt = f"""
Answer the question using only the provided transcript context.

Question:
{question}

Context:
{context}

Rules:
- Synthesize across multiple context lines when helpful
- If the answer is uncertain or missing, say so plainly
- Keep the answer concise but informative
- Prefer precise details over vague wording
- Do not invent facts beyond the context
- When possible, mention the most relevant timestamped source naturally in the answer
- Treat the video transcript as the authoritative source over outside assumptions

Answer:
"""

    return ask_llm(prompt)
