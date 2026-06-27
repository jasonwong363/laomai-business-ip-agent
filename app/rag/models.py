from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class Chunk:
    id: str
    title: str
    file_path: str
    section_path: str
    type: str
    usage: str
    speaker_scope: str
    content: str
    source: Any = ""
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    metadata: dict[str, Any] = field(default_factory=dict)
    embedding: list[float] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Chunk":
        return cls(**data)
