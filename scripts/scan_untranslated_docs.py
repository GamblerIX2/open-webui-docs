#!/usr/bin/env python3
"""Heuristically find docs files that still look mostly untranslated."""
from __future__ import annotations

import argparse
import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCAN_ROOTS = [
    REPO_ROOT / "docs",
    REPO_ROOT / "README.md",
    REPO_ROOT / "docusaurus.config.ts",
    REPO_ROOT / "src/components",
    REPO_ROOT / "src/theme",
]
TEXT_SUFFIXES = {".md", ".mdx", ".json", ".ts", ".tsx"}
ASCII_LETTER_RE = re.compile(r"[A-Za-z]")
CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")


def iter_files() -> list[Path]:
    files: list[Path] = []
    for root in SCAN_ROOTS:
        if root.is_file():
            files.append(root)
            continue
        for path in root.rglob("*"):
            if path.is_file() and path.suffix in TEXT_SUFFIXES:
                files.append(path)
    return sorted(files)


def classify(text: str) -> tuple[int, int]:
    return len(ASCII_LETTER_RE.findall(text)), len(CJK_RE.findall(text))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", type=Path, help="Write flagged file paths to this file.")
    args = parser.parse_args()

    flagged: list[str] = []
    for path in iter_files():
        text = path.read_text(encoding="utf-8", errors="ignore")
        ascii_letters, cjk = classify(text)
        if ascii_letters < 80:
            continue
        if cjk == 0 or cjk * 6 < ascii_letters:
            flagged.append(str(path.relative_to(REPO_ROOT)))

    output = "\n".join(flagged)
    if args.write:
        args.write.write_text(output + ("\n" if output else ""), encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
