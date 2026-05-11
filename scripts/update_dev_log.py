#!/usr/bin/env python3
"""Create/update a daily engineering log check-in.

The script supports multiple legitimate check-ins per day. Each run creates the
next missing check-in file for the current UTC day:

1. morning-plan
2. afternoon-progress
3. evening-summary

It avoids fake random content. The generated files are structured prompts for
real work notes that you can fill in after each check-in.
"""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOG_DIR = ROOT / "logs"
INDEX = ROOT / "logs" / "README.md"

CHECKINS = [
    (
        "morning-plan",
        "Morning Plan",
        [
            "Top priority for today",
            "Implementation plan",
            "Risks or unknowns",
            "Definition of done",
        ],
    ),
    (
        "afternoon-progress",
        "Afternoon Progress",
        [
            "Progress made so far",
            "Code, docs, or research touched",
            "Blockers discovered",
            "Adjustment for the rest of the day",
        ],
    ),
    (
        "evening-summary",
        "Evening Summary",
        [
            "What shipped or improved",
            "What I learned",
            "Open follow-ups",
            "Next concrete step",
        ],
    ),
]


def next_missing_entry(day_dir: Path, day: str) -> tuple[str, str, list[str], Path] | None:
    for slug, title, prompts in CHECKINS:
        path = day_dir / f"{day}-{slug}.md"
        if not path.exists():
            return slug, title, prompts, path
    return None


def write_entry(path: Path, day: str, title: str, prompts: list[str], now: datetime) -> None:
    body = [
        f"# {title}: {day}",
        "",
        f"Generated at: `{now.strftime('%Y-%m-%d %H:%M:%S UTC')}`",
        "",
        "## Summary",
        "",
        "TODO: replace this with real engineering progress.",
        "",
        "## Notes",
        "",
    ]
    for prompt in prompts:
        body.extend([f"### {prompt}", "", "- TODO", ""])
    body.extend([
        "## Commit hygiene",
        "",
        "- Keep commits small and descriptive",
        "- Link related issues or PRs when available",
        "- Prefer real project work over vanity activity",
        "",
    ])
    path.write_text("\n".join(body), encoding="utf-8")


def update_index() -> None:
    entries = sorted(LOG_DIR.glob("**/[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]-*.md"), reverse=True)
    lines = ["# Log Index", "", "Recent daily engineering check-ins.", ""]
    for p in entries[:120]:
        rel = p.relative_to(LOG_DIR)
        label = p.stem.replace("-", " ").title()
        lines.append(f"- [{label}]({rel.as_posix()})")
    INDEX.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    now = datetime.now(timezone.utc)
    day = now.strftime("%Y-%m-%d")
    year_month = now.strftime("%Y/%m")
    day_dir = LOG_DIR / year_month
    day_dir.mkdir(parents=True, exist_ok=True)

    item = next_missing_entry(day_dir, day)
    if item is not None:
        _slug, title, prompts, path = item
        write_entry(path, day, title, prompts, now)

    update_index()


if __name__ == "__main__":
    main()
