
from modules.llm import ask_llm


MAX_CONTEXT_CHUNKS = 5


def answer_question(question: str, chunks: list[str]) -> str:
    """
    Answer a question using retrieved transcript chunks.
    Limits context size to avoid token overflow.
    """

    # Limit number of chunks sent to the LLM
    selected_chunks = chunks[:MAX_CONTEXT_CHUNKS]

    context = "\n".join(selected_chunks)

    prompt = f"""
Answer the question using the provided transcript context.

Question:
{question}

Context:
{context}

Answer clearly and concisely.
"""

    return ask_llm(prompt)
