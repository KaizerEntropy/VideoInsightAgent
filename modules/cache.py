import hashlib
import json
from pathlib import Path
from typing import Any


CACHE_DIR = Path(".cache") / "video_insight_agent"


def _ensure_cache_dir() -> Path:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    return CACHE_DIR


def build_cache_key(*parts: Any) -> str:
    serialized = json.dumps(parts, sort_keys=True, default=str)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def load_json_cache(namespace: str, cache_key: str) -> dict[str, Any] | None:
    cache_path = _ensure_cache_dir() / f"{namespace}_{cache_key}.json"

    if not cache_path.exists():
        return None

    try:
        with cache_path.open("r", encoding="utf-8") as cache_file:
            return json.load(cache_file)
    except (OSError, json.JSONDecodeError):
        return None


def save_json_cache(namespace: str, cache_key: str, payload: dict[str, Any]) -> None:
    cache_path = _ensure_cache_dir() / f"{namespace}_{cache_key}.json"

    with cache_path.open("w", encoding="utf-8") as cache_file:
        json.dump(payload, cache_file, ensure_ascii=False, indent=2)
