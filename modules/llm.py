import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq


load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")


def get_groq_client() -> Groq:
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is not set. Add it to the .env file or environment variables."
        )

    return Groq(api_key=api_key)


def ask_llm(prompt):
    client = get_groq_client()

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content
