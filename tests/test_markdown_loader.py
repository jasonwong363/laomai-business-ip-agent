from pathlib import Path

from app.rag.markdown_loader import split_markdown


def test_split_markdown_keeps_metadata(tmp_path: Path) -> None:
    file = tmp_path / "demo.md"
    file.write_text(
        """---
title: 测试文档
type: SOP
usage: 测试用途
speaker_scope: 不是原话
---

# 第一章

这是第一段。

## 小节

这是第二段。
""",
        encoding="utf-8",
    )
    chunks = split_markdown(file, tmp_path)
    assert chunks
    assert chunks[0].title == "测试文档"
    assert chunks[0].usage == "测试用途"
    assert chunks[0].speaker_scope == "不是原话"
    assert chunks[0].file_path == "demo.md"
