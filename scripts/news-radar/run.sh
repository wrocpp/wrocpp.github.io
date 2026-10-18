#!/usr/bin/env bash
# Weekly C++ news radar: one headless Claude session (read-only: it has no write access) whose final
# message is the note; this script saves it as .notes/radar-YYYY-MM-DD.md.
# Runs under the private Scudo account (Max subscription), not the default Siili account.
# Usage: scripts/news-radar/run.sh [--dry-run]
set -euo pipefail

REPO="$(cd "$(dirname "$0")/../.." && pwd)"
PROMPT_FILE="$REPO/scripts/news-radar/prompt.md"
NOTE_DIR="$REPO/.notes"
RADAR_MODEL="sonnet"
RADAR_BUDGET_USD="6"   # ceiling per weekly run; the 2026-10-18 trial hit a 3 USD ceiling before it read 15 sources
# The session reads untrusted web pages and can reach the network, so it must hold no private data.
# It runs from an empty temp directory (the one place it may read by default), Read is limited to the
# published posts and earlier radar notes by absolute path, there is no Glob or Grep (coverage.py searches
# the posts), and probe.py takes inline code, never a file path. The repo's .env is out of reach.
ALLOWED_TOOLS="WebFetch WebSearch Read(/$REPO/src/content/posts/**) Read(/$REPO/.notes/radar-*.md) Bash(python3 $REPO/scripts/news-radar/coverage.py *) Bash(python3 $REPO/scripts/news-radar/probe.py *)"
TODAY="$(date -u +%F)"
NOTE="$NOTE_DIR/radar-$TODAY.md"

export CLAUDE_CONFIG_DIR="$HOME/.claude-scudo"
mkdir -p "$NOTE_DIR"
SANDBOX="$(mktemp -d)"
trap 'rmdir "$SANDBOX"' EXIT
cd "$SANDBOX"

PROMPT="Today is $TODAY (UTC). The note is dated $TODAY.

$(sed "s#{{REPO}}#$REPO#g" "$PROMPT_FILE")"

CMD=(claude -p "$PROMPT" --model "$RADAR_MODEL" --max-budget-usd "$RADAR_BUDGET_USD"
     --permission-mode dontAsk --allowedTools "$ALLOWED_TOOLS" --no-session-persistence
     --output-format json)

if [[ "${1:-}" == "--dry-run" ]]; then
  echo "cwd:      a fresh empty temp dir (repo at $REPO)"
  echo "config:   CLAUDE_CONFIG_DIR=$CLAUDE_CONFIG_DIR"
  echo "note:     $NOTE"
  echo "tools:    $ALLOWED_TOOLS"
  echo "model:    $RADAR_MODEL, budget \$$RADAR_BUDGET_USD"
  echo "prompt:   $(wc -c < "$PROMPT_FILE") bytes from $PROMPT_FILE"
  exit 0
fi

RAW="$("${CMD[@]}" || true)"
if [[ -z "$RAW" ]]; then
  echo "radar: claude printed nothing (login, network or budget); no note written" >&2
  exit 1
fi
# The JSON envelope carries the reply, the cost and how the session ended.
OUTPUT="$(python3 -c 'import json,sys; print(json.load(sys.stdin).get("result",""))' <<<"$RAW")"
python3 -c 'import json,sys; d=json.load(sys.stdin); print("radar: cost=%.2f USD turns=%s ended=%s" % (d.get("total_cost_usd",0), d.get("num_turns"), d.get("subtype")))' <<<"$RAW"

if ! grep -q '^# C++ news radar' <<<"$OUTPUT"; then
  echo "radar: reply is not a note; first 400 bytes follow" >&2
  head -c 400 <<<"$OUTPUT" >&2
  exit 1
fi
# Drop anything the model put before the heading.
awk '/^# C\+\+ news radar/{p=1} p' <<<"$OUTPUT" > "$NOTE"

CANDIDATES="$(grep -c '^### Candidate' "$NOTE" || true)"
echo "radar: $CANDIDATES candidate(s) in $NOTE"
if [[ "$CANDIDATES" -ge 1 ]]; then
  osascript -e "display notification \"$CANDIDATES candidate(s): radar-$TODAY.md\" with title \"wro.cpp news radar\""
fi
