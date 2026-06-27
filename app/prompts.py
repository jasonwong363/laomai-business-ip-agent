from __future__ import annotations

from app.rag.config import ROOT_DIR


def load_system_prompt() -> str:
    path = ROOT_DIR / "prompts" / "laomai_system_prompt.md"
    if path.exists():
        return path.read_text(encoding="utf-8")
    return "你是老麦商业 IP 智能体，回答必须基于知识库资料并标注来源。"
