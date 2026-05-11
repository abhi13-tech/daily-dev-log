#!/usr/bin/env python3
"""Create retrospective daily engineering log files for a month.

Default: previous UTC month.
This creates dated files like logs/YYYY/MM/YYYY-MM-DD.md for honest retrospective notes.
It does not rewrite git history or fake commit dates.
"""
from __future__ import annotations

import argparse
import calendar
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOG_DIR = ROOT / "logs"
INDEX = LOG_DIR / "README.md"


def previous_month(today: date) -> tuple[int, int]:
    if today.month == 1:
        return today.year - 1, 12
    return today.year, today.month - 1


def write_day(path: Path, day: date) -> bool:
    if path.exists():
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    path.write_text(
        "\n".join([
            f"# Daily Dev Log: {day.isoformat()}",
            "",
            f"Retrospective file generated at: `{now}`",
            "",
            "> Fill this with real notes from that day. Do not use this as fake work history.",
            "",
            "## Summary",
            "",
            "- TODO: real work summary",
            "",
            "## Work completed",
            "",
            "- TODO",
            "",
            "## What I learned",
            "",
            "- TODO",
            "",
            "## Next step",
            "",
            "- TODO",
            "",
        ]),
        encoding="utf-8",
    )
    return True


def update_index() -> None:
    entries = sorted(LOG_DIR.glob("**/[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]*.md"), reverse=True)
    lines = ["# Log Index", "", "Recent daily engineering notes and check-ins.", ""]
    for p in entries[:180]:
        rel = p.relative_to(LOG_DIR)
        label = p.stem.replace("-", " ").title()
        lines.append(f"- [{label}]({rel.as_posix()})")
    INDEX.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", type=int)
    parser.add_argument("--month", type=int, choices=range(1, 13))
    args = parser.parse_args()

    year, month = (args.year, args.month) if args.year and args.month else previous_month(date.today())
    _, days = calendar.monthrange(year, month)
    created = 0
    for d in range(1, days + 1):
        day = date(year, month, d)
        path = LOG_DIR / f"{year:04d}" / f"{month:02d}" / f"{day.isoformat()}.md"
        created += int(write_day(path, day))
    update_index()
    print(f"Created {created} retrospective log file(s) for {year:04d}-{month:02d}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
