from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.rag.config import ROOT_DIR
from app.rag.ingest import build_index, import_markdown_files


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default="私董会学员ai投喂资料", help="Markdown source folder")
    args = parser.parse_args()
    source = Path(args.source)
    if not source.is_absolute():
        source = ROOT_DIR / source
    files = import_markdown_files(source)
    chunks = build_index()
    print(f"Imported {len(files)} files, built {len(chunks)} chunks.")


if __name__ == "__main__":
    main()
