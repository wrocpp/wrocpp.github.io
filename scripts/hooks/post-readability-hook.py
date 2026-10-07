#!/usr/bin/env python3
"""PostToolUse hook (Edit|Write|MultiEdit): advisory readability findings for post bodies.

Reads the tool JSON on stdin. For src/content/posts/*.mdx it runs
`prose-lint.py --file` and `readability-report.py --file` and returns their findings as
additionalContext. Never blocks: always exits 0, prints plain ASCII JSON (or nothing).
"""

import json
import re
import subprocess
import sys
from fnmatch import fnmatch
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent
REPO = SCRIPTS.parent
MAX_LINES = 40
ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")
LEGEND_MARKER = "budgets:"


def is_post(path):
    return fnmatch(Path(path).as_posix(), "*/src/content/posts/*.mdx") or fnmatch(path, "src/content/posts/*.mdx")


def run(script, path):
    r = subprocess.run([sys.executable, str(SCRIPTS / script), "--file", path],
                       capture_output=True, text=True, cwd=REPO, timeout=60)
    return ANSI_RE.sub("", r.stdout).strip()


def trim_lint(out):
    keep = []
    for line in out.splitlines():
        if LEGEND_MARKER in line or line.strip().startswith(("anaphora<=", "see docs/STYLE")):
            break
        if line.strip():
            keep.append(line)
    return keep


def build_message(path):
    lint = trim_lint(run("prose-lint.py", path))
    report = run("readability-report.py", path).splitlines()
    parts = ["Readability check for " + Path(path).name + " (advisory, see docs/STYLE.md Readability):"]
    parts += lint[:MAX_LINES]
    parts += report[:MAX_LINES]
    return "\n".join(parts)


def main():
    try:
        payload = json.load(sys.stdin)
        path = (payload.get("tool_input") or {}).get("file_path", "")
        if not path or not is_post(path):
            return
        msg = build_message(path)
        out = {"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": msg}}
        print(json.dumps(out))
    except Exception:
        return


if __name__ == "__main__":
    main()
    sys.exit(0)
