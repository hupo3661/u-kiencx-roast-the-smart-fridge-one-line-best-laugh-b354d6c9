#!/usr/bin/env python3
"""Roast the Smart Fridge: One Line, Best Laugh Wins — one-line entry.

The entry is a single deterministic line: no randomness, no network, no
clock. It is printed to stdout and written verbatim to the entry file.
"""

import os
from pathlib import Path

MAX_LENGTH = 160

LINE = 'My smart fridge diagnosed my midnight snacking, emailed my doctor, then locked the cheese drawer until I subscribed to premium cold.'


def _fail(message: str) -> None:
    raise SystemExit(message)


def _checks(line: str):
    """Yield (passed, message) for every rule the line must satisfy."""
    yield bool(line.strip()), "Invalid line: entry must be non-empty."
    yield line == line.strip(), (
        "Invalid line: entry must not have leading or trailing whitespace."
    )
    yield len(line) <= MAX_LENGTH, (
        f"Invalid line: {len(line)} characters, over the {MAX_LENGTH} limit."
    )
    yield "\n" not in line and "\r" not in line, (
        "Invalid line: entry must be a single line with no newline characters."
    )


def validate(line: str) -> None:
    for passed, message in _checks(line):
        if not passed:
            _fail(message)


def _output_path() -> Path:
    return Path(os.environ.get("OUTPUT_PATH", "/output/entry.txt"))


def _write_entry(path: Path, line: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(line, encoding="utf-8")
    if path.read_text(encoding="utf-8") != line:
        _fail(
            "Write verification failed: entry file content does not match the line."
        )


def main() -> int:
    validate(LINE)
    _write_entry(_output_path(), LINE)
    print(LINE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
