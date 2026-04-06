import re

from modules.translator import SUPPORTED_TRANSLATION_LANGUAGES


def seconds_to_timestamp(seconds: float) -> str:
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes}:{secs:02d}"


def parse_timeline(text: str) -> list[tuple[str, str]]:
    timeline = []

    for line in text.split("\n"):
        cleaned = line.strip().replace("•", "").strip()
        match = re.match(r"(\d+:\d+(?::\d+)?)\s*[-–:]?\s*(.*)", cleaned)

        if match:
            timeline.append((match.group(1), match.group(2)))

    return timeline


def parse_flashcards(text: str) -> list[dict[str, str]]:
    flashcards = []
    current_question = None
    current_answer = []

    for raw_line in text.splitlines():
        line = raw_line.strip()

        if not line:
            continue

        if line.startswith("Q:"):
            if current_question and current_answer:
                flashcards.append(
                    {
                        "question": current_question,
                        "answer": "\n".join(current_answer).strip(),
                    }
                )

            current_question = line[2:].strip()
            current_answer = []
            continue

        if line.startswith("A:"):
            current_answer.append(line[2:].strip())
            continue

        if current_question:
            current_answer.append(line)

    if current_question and current_answer:
        flashcards.append(
            {
                "question": current_question,
                "answer": "\n".join(current_answer).strip(),
            }
        )

    return flashcards


def format_language_name(language_code: str) -> str:
    return SUPPORTED_TRANSLATION_LANGUAGES.get(language_code, language_code.upper())
