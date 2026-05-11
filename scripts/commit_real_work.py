#!/usr/bin/env python3
"""Create multiple commits from real working-tree changes grouped by folder.

This is a safe helper for legitimate development work. It does not generate fake
changes. It only commits files you already changed, grouped by top-level area,
and then optionally pushes.

Examples:
  python3 scripts/commit_real_work.py --dry-run
  python3 scripts/commit_real_work.py --push
  python3 scripts/commit_real_work.py --prefix "docs"
"""
from __future__ import annotations

import argparse
import subprocess
from collections import defaultdict
from pathlib import Path


def run(cmd: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=check)


def changed_files() -> list[str]:
    # Porcelain v1 format. Path starts at column 4 for normal entries.
    out = run(["git", "status", "--porcelain"], check=True).stdout.splitlines()
    files: list[str] = []
    for line in out:
        if not line.strip():
            continue
        path = line[3:]
        if " -> " in path:  # rename format
            path = path.split(" -> ", 1)[1]
        files.append(path)
    return files


def group_for(path: str) -> str:
    p = Path(path)
    if len(p.parts) == 1:
        return "root"
    first = p.parts[0]
    if first == ".github":
        return "ci"
    if first in {"docs", "logs", "README.md"}:
        return "docs"
    if first in {"scripts", "tools", "bin"}:
        return "tools"
    if first in {"src", "app", "lib", "api"}:
        return "code"
    if first in {"tests", "test", "spec"}:
        return "tests"
    return first.replace("_", "-")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--push", action="store_true", help="Push after committing")
    parser.add_argument("--dry-run", action="store_true", help="Show planned commits without changing anything")
    parser.add_argument("--prefix", default="work", help="Commit message prefix, e.g. docs, feat, chore")
    args = parser.parse_args()

    files = changed_files()
    if not files:
        print("No real working-tree changes found. Nothing to commit.")
        return 0

    groups: dict[str, list[str]] = defaultdict(list)
    for file in files:
        groups[group_for(file)].append(file)

    print("Planned commits:")
    for group, paths in sorted(groups.items()):
        print(f"- {args.prefix}: update {group} ({len(paths)} file(s))")
        for path in paths:
            print(f"  - {path}")

    if args.dry_run:
        return 0

    for group, paths in sorted(groups.items()):
        run(["git", "add", "--", *paths])
        diff = run(["git", "diff", "--cached", "--quiet"], check=False)
        if diff.returncode == 0:
            continue
        msg = f"{args.prefix}: update {group}"
        run(["git", "commit", "-m", msg])
        print(f"Committed: {msg}")

    if args.push:
        run(["git", "push"])
        print("Pushed commits.")
    else:
        print("Done. Review commits, then run: git push")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
