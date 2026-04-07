import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

from modules.cache import build_cache_key, load_json_cache, save_json_cache
from modules.errors import ConfigurationError, ExternalServiceError


load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")


def get_groq_client() -> Groq:
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ConfigurationError(
            "GROQ_API_KEY is not set. Add it to the .env file or environment variables."
        )

    return Groq(api_key=api_key)


def ask_llm(prompt: str, model: str = "llama-3.1-8b-instant", use_cache: bool = True) -> str:
    cache_key = build_cache_key("llm", model, prompt)

    if use_cache:
        cached_response = load_json_cache("llm", cache_key)
        if cached_response and cached_response.get("content"):
            return cached_response["content"]

    client = get_groq_client()

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
    except Exception as exc:
        raise ExternalServiceError(
            f"LLM request failed: {exc}"
        ) from exc

    content = response.choices[0].message.content

    if not content:
        raise ExternalServiceError("LLM request returned an empty response.")

    if use_cache:
        save_json_cache("llm", cache_key, {"content": content})

    return content
