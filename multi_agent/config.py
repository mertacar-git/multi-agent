from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass
class Settings:
    provider: str = "lmstudio"
    openai_api_key: str = ""
    openai_base_url: str = "http://localhost:1234/v1"
    openai_model: str = "local-model"
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.1"
    timeout_seconds: int = 90


def load_settings() -> Settings:
    load_dotenv()
    return Settings(
        provider=os.getenv("PROVIDER", "lmstudio").strip().lower(),
        openai_api_key=os.getenv("OPENAI_API_KEY", "").strip(),
        openai_base_url=os.getenv("OPENAI_BASE_URL", "http://localhost:1234/v1").strip(),
        openai_model=os.getenv("OPENAI_MODEL", "local-model").strip(),
        ollama_base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").strip(),
        ollama_model=os.getenv("OLLAMA_MODEL", "llama3.1").strip(),
        timeout_seconds=int(os.getenv("TIMEOUT_SECONDS", "90")),
    )

