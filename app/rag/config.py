from __future__ import annotations

import os
from pathlib import Path

try:
    from dotenv import load_dotenv
except ModuleNotFoundError:  # pragma: no cover - minimal Python env fallback.
    load_dotenv = None

if load_dotenv:
    load_dotenv()

ROOT_DIR = Path(__file__).resolve().parents[2]
KNOWLEDGE_DIR = ROOT_DIR / os.getenv("KNOWLEDGE_DIR", "knowledge")
VECTOR_DB_DIR = ROOT_DIR / os.getenv("VECTOR_DB_DIR", "storage/vector_db")
INDEX_PATH = VECTOR_DB_DIR / "chunks.jsonl"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
ENABLE_OPENAI_GENERATION = os.getenv("ENABLE_OPENAI_GENERATION", "false").lower() == "true"
