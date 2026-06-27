from __future__ import annotations

import shutil
from pathlib import Path

from app.rag.config import INDEX_PATH, KNOWLEDGE_DIR
from app.rag.markdown_loader import infer_type, parse_frontmatter, read_text, split_markdown
from app.rag.vector_store import VectorStore

CATEGORY_DIRS = {
    "persona": "01_persona",
    "original_quotes": "02_original_quotes",
    "meeting_summaries": "03_meeting_summaries",
    "company": "04_company",
    "products": "05_products",
    "cases": "06_cases",
    "sop": "07_sop",
    "sales_faq": "08_sales_faq",
}

REQUIRED_DIRS = [
    "01_persona",
    "02_original_quotes",
    "03_meeting_summaries",
    "04_company",
    "05_products",
    "06_cases",
    "07_sop",
    "08_sales_faq",
    "09_prompts",
    "10_evaluation",
]


def ensure_knowledge_dirs() -> None:
    for directory in REQUIRED_DIRS:
        (KNOWLEDGE_DIR / directory).mkdir(parents=True, exist_ok=True)


def import_markdown_files(source: Path) -> list[Path]:
    ensure_knowledge_dirs()
    copied: list[Path] = []
    for file in source.rglob("*.md"):
        metadata, _ = parse_frontmatter(read_text(file))
        doc_type = infer_type(file, metadata)
        target_dir = KNOWLEDGE_DIR / CATEGORY_DIRS.get(doc_type, "03_meeting_summaries")
        target_dir.mkdir(parents=True, exist_ok=True)
        target = target_dir / file.name
        if file.resolve() != target.resolve():
            shutil.copy2(file, target)
        copied.append(target)
    return copied


def build_index() -> list:
    ensure_knowledge_dirs()
    chunks = []
    for file in KNOWLEDGE_DIR.rglob("*.md"):
        chunks.extend(split_markdown(file, KNOWLEDGE_DIR))
    VectorStore(INDEX_PATH).save(chunks)
    return chunks
