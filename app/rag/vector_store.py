from __future__ import annotations

import json
import math
import re
from collections import Counter
from pathlib import Path

from app.rag.models import Chunk

TOKEN_RE = re.compile(r"[\w\u4e00-\u9fff]+")
VECTOR_SIZE = 512


def tokenize(text: str) -> list[str]:
    words = TOKEN_RE.findall(text.lower())
    grams: list[str] = []
    for word in words:
        if re.fullmatch(r"[\u4e00-\u9fff]+", word) and len(word) > 1:
            grams.extend(word[i : i + 2] for i in range(len(word) - 1))
        grams.append(word)
    return grams


def local_embedding(text: str) -> list[float]:
    vec = [0.0] * VECTOR_SIZE
    for token, count in Counter(tokenize(text)).items():
        vec[hash(token) % VECTOR_SIZE] += 1.0 + math.log(count)
    norm = math.sqrt(sum(v * v for v in vec)) or 1.0
    return [v / norm for v in vec]


def cosine(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b)) if a and b else 0.0


class VectorStore:
    def __init__(self, index_path: Path):
        self.index_path = index_path
        self.chunks: list[Chunk] = []

    def load(self) -> None:
        self.chunks = []
        if not self.index_path.exists():
            return
        with self.index_path.open("r", encoding="utf-8") as handle:
            for line in handle:
                if line.strip():
                    self.chunks.append(Chunk.from_dict(json.loads(line)))

    def save(self, chunks: list[Chunk]) -> None:
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        with self.index_path.open("w", encoding="utf-8") as handle:
            for chunk in chunks:
                if not chunk.embedding:
                    chunk.embedding = local_embedding(f"{chunk.title}\n{chunk.section_path}\n{chunk.content}")
                handle.write(json.dumps(chunk.to_dict(), ensure_ascii=False) + "\n")
        self.chunks = chunks

    def search(self, query: str, preferred: list[str], limit: int = 8) -> list[dict]:
        self.load()
        query_vec = local_embedding(query)
        query_tokens = set(tokenize(query))
        results = []
        for chunk in self.chunks:
            semantic = cosine(query_vec, chunk.embedding or local_embedding(chunk.content))
            lexical = len(query_tokens & set(tokenize(chunk.content))) / max(len(query_tokens), 1)
            type_boost = 0.25 if chunk.type in preferred else 0.0
            score = semantic * 0.7 + lexical * 0.3 + type_boost
            results.append({"score": score, "chunk": chunk.to_dict()})
        results.sort(key=lambda item: item["score"], reverse=True)
        return results[:limit]
