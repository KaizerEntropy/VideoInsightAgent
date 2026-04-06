from modules.llm import ask_llm


SUPPORTED_TRANSLATION_LANGUAGES = {
    "en": "English",
    "hi": "Hindi",
    "bn": "Bengali",
}


MAX_TRANSLATION_CHUNK_WORDS = 1200


def normalize_language_code(language_code: str | None) -> str:
    if not language_code:
        return "unknown"

    return language_code.split("-")[0].lower()


def is_supported_non_english(language_code: str | None) -> bool:
    normalized = normalize_language_code(language_code)
    return normalized in {"hi", "bn"}


def chunk_text(text: str, chunk_size: int = MAX_TRANSLATION_CHUNK_WORDS) -> list[str]:
    words = text.split()
    chunks = []

    for index in range(0, len(words), chunk_size):
        chunks.append(" ".join(words[index:index + chunk_size]))

    return chunks


def translate_text_to_english(text: str, source_language: str) -> str:
    chunks = chunk_text(text)
    translated_chunks = []
    language_name = SUPPORTED_TRANSLATION_LANGUAGES.get(
        normalize_language_code(source_language),
        "the source language",
    )

    for chunk in chunks:
        prompt = f"""
Translate the following {language_name} transcript into fluent English.

Rules:
- Preserve meaning faithfully
- Do not summarize
- Do not add commentary
- Output only the English translation

Transcript:
{chunk}
"""
        translated_chunks.append(ask_llm(prompt).strip())

    return "\n".join(translated_chunks).strip()
