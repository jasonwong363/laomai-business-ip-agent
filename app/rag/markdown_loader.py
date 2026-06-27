from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Any

from app.rag.models import Chunk

try:
    import yaml
except ModuleNotFoundError:  # pragma: no cover - exercised in minimal Python envs.
    yaml = None

FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n?", re.DOTALL)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
ENCODINGS = ("utf-8-sig", "utf-8", "gb18030")


def read_text(path: Path) -> str:
    for encoding in ENCODINGS:
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text(encoding="utf-8", errors="replace")


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, text
    raw = match.group(1)
    body = text[match.end() :]
    if yaml:
        try:
            metadata = yaml.safe_load(raw) or {}
        except yaml.YAMLError:
            metadata = {"frontmatter_error": raw}
    else:
        metadata = _parse_simple_yaml(raw)
    return metadata, body


def _parse_simple_yaml(raw: str) -> dict[str, Any]:
    data: dict[str, Any] = {}
    current_key = ""
    for line in raw.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("- ") and current_key:
            data.setdefault(current_key, []).append(stripped[2:].strip())
            continue
        if ":" in line:
            key, value = line.split(":", 1)
            current_key = key.strip()
            value = value.strip()
            data[current_key] = value if value else []
    return data


def infer_type(path: Path, metadata: dict[str, Any]) -> str:
    declared = str(metadata.get("type") or "")
    text = f"{path.as_posix()} {declared}".lower()
    if "原话" in text or "金句" in text:
        return "original_quotes"
    if "公司" in text or "介绍" in text:
        return "company"
    if "产品" in text or "服务" in text or "百问百答" in text:
        return "products"
    if "案例" in text:
        return "cases"
    if "sop" in text or "流程" in text or "执行" in text:
        return "sop"
    if "faq" in text or "销售" in text or "异议" in text or "话术" in text:
        return "sales_faq"
    if "风格" in text or "人设" in text:
        return "persona"
    if "会议" in text or "投喂" in text or "纪要" in text:
        return "meeting_summaries"
    return declared or "general"


def split_markdown(path: Path, root: Path) -> list[Chunk]:
    text = read_text(path)
    metadata, body = parse_frontmatter(text)
    title = str(metadata.get("title") or path.stem)
    doc_type = infer_type(path, metadata)
    usage = str(metadata.get("usage") or "")
    speaker_scope = str(metadata.get("speaker_scope") or "")
    source = metadata.get("source", "")

    sections: list[dict[str, str]] = []
    stack: list[tuple[int, str]] = []
    current_lines: list[str] = []
    current_path = title

    def flush() -> None:
        content = "\n".join(current_lines).strip()
        if content:
            sections.append({"section_path": current_path, "content": content})

    for line in body.splitlines():
        match = HEADING_RE.match(line)
        if match:
            flush()
            current_lines = [line]
            level = len(match.group(1))
            heading = match.group(2).strip()
            stack[:] = [item for item in stack if item[0] < level]
            stack.append((level, heading))
            current_path = " > ".join(item[1] for item in stack)
        else:
            current_lines.append(line)
    flush()

    chunks: list[Chunk] = []
    for section in sections:
        chunks.extend(_split_long_section(path, root, title, doc_type, usage, speaker_scope, source, metadata, section))
    return chunks


def _split_long_section(
    path: Path,
    root: Path,
    title: str,
    doc_type: str,
    usage: str,
    speaker_scope: str,
    source: Any,
    metadata: dict[str, Any],
    section: dict[str, str],
    max_chars: int = 1200,
) -> list[Chunk]:
    content = section["content"].strip()
    if len(content) <= max_chars:
        parts = [content]
    else:
        paragraphs = [p.strip() for p in re.split(r"\n\s*\n", content) if p.strip()]
        parts = []
        buffer = ""
        for paragraph in paragraphs:
            if len(buffer) + len(paragraph) > max_chars and buffer:
                parts.append(buffer.strip())
                buffer = paragraph
            else:
                buffer = f"{buffer}\n\n{paragraph}".strip()
        if buffer:
            parts.append(buffer.strip())

    rel_path = str(path.relative_to(root)) if path.is_relative_to(root) else str(path)
    chunks = []
    for index, part in enumerate(parts, start=1):
        section_path = section["section_path"]
        if len(parts) > 1:
            section_path = f"{section_path} > part {index}"
        digest = hashlib.sha1(f"{rel_path}:{section_path}:{part[:80]}".encode("utf-8")).hexdigest()[:16]
        chunks.append(
            Chunk(
                id=digest,
                title=title,
                file_path=rel_path,
                section_path=section_path,
                type=doc_type,
                usage=usage,
                speaker_scope=speaker_scope,
                content=part,
                source=source,
                metadata=metadata,
            )
        )
    return chunks
