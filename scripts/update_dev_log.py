#!/usr/bin/env python3
"""Create/update a dated daily engineering log entry.

This script intentionally creates a meaningful work journal template instead of
random fake content. Edit each generated entry with real work before using it as
portfolio evidence.
"""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOG_DIR = ROOT / "logs"
INDEX = ROOT / "logs" / "README.md"

PROMPTS = [
    "Project / focus area",
    "What I built or improved",
    "What I learned",
    "Bug, blocker, or design decision",
    "Next concrete step",
]


def main() -> None:
    now = datetime.now(timezone.utc)
    day = now.strftime("%Y-%m-%d")
    year_month = now.strftime("%Y/%m")
    entry_dir = LOG_DIR / year_month
    entry_dir.mkdir(parents=True, exist_ok=True)
    entry = entry_dir / f"{day}.md"

    if not entry.exists():
        body = [
            f"# Daily Dev Log: {day}",
            "",
            f"Generated at: `{now.strftime('%Y-%m-%d %H:%M:%S UTC')}`",
            "",
            "## Summary",
            "",
            "Today I made progress on engineering practice and project tracking.",
            "",
            "## Notes",
            "",
        ]
        for prompt in PROMPTS:
            body.extend([f"### {prompt}", "", "- TODO: replace with real detail", ""])
        body.extend([
            "## Commit hygiene",
            "",
            "- Keep commits small and descriptive",
            "- Link related issues or PRs when available",
            "- Prefer real project work over vanity activity",
            "",
        ])
        entry.write_text("\n".join(body), encoding="utf-8")

    entries = sorted(LOG_DIR.glob("**/[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9].md"), reverse=True)
    lines = ["# Log Index", "", "Recent daily engineering notes.", ""]
    for p in entries[:60]:
        rel = p.relative_to(LOG_DIR)
        lines.append(f"- [{p.stem}]({rel.as_posix()})")
    INDEX.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
