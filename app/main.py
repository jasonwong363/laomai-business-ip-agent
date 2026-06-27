from __future__ import annotations

import shutil
from pathlib import Path

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.prompts import load_system_prompt
from app.rag.config import INDEX_PATH, KNOWLEDGE_DIR, ROOT_DIR
from app.rag.generator import generate_answer
from app.rag.ingest import build_index, import_markdown_files
from app.rag.intent import classify_intent, preferred_types
from app.rag.vector_store import VectorStore

app = FastAPI(title="老麦商业 IP 智能体")
app.mount("/static", StaticFiles(directory=ROOT_DIR / "static"), name="static")


@app.get("/", response_class=HTMLResponse)
def home() -> str:
    return (ROOT_DIR / "static" / "index.html").read_text(encoding="utf-8")


@app.post("/api/upload")
async def upload(file: UploadFile = File(...)) -> dict:
    target = KNOWLEDGE_DIR / "03_meeting_summaries" / Path(file.filename or "upload.md").name
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("wb") as handle:
        shutil.copyfileobj(file.file, handle)
    chunks = build_index()
    return {"ok": True, "file": str(target.relative_to(ROOT_DIR)), "chunks": len(chunks)}


@app.post("/api/import")
def import_source(source: str = Form("私董会学员ai投喂资料")) -> dict:
    files = import_markdown_files(ROOT_DIR / source)
    chunks = build_index()
    return {"ok": True, "files": len(files), "chunks": len(chunks)}


@app.get("/api/documents")
def documents() -> dict:
    docs = [{"path": str(file.relative_to(ROOT_DIR)), "name": file.name} for file in KNOWLEDGE_DIR.rglob("*.md")]
    return {"documents": docs}


@app.post("/api/ask")
def ask(query: str = Form(...), mode: str = Form("topics"), limit: int = Form(8)) -> dict:
    intent = classify_intent(query, mode)
    sources = VectorStore(INDEX_PATH).search(query, preferred_types(intent), limit=limit)
    answer = generate_answer(query, intent, sources, load_system_prompt())
    return {"intent": intent, "sources": sources, "answer": answer}
