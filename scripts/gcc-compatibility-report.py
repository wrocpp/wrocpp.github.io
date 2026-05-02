#!/usr/bin/env python3
"""
GCC 16.1 compatibility audit for the wro.cpp C++26 reflection series.

Walks every `posts/<NN>-<slug>/examples/*.cpp` in the cpp26 examples repo,
applies the GCC source rewrites from `COMPILER_PROFILES["gcc"]` in
scripts/shorten-examples.py, and POSTs to godbolt.org's compile API for
g161 with `-std=c++26 -freflection` and `filters.execute=true`.

For each example, classify against the existing clang `expected_output`
captured in src/data/godbolt-permalinks.yml:

  OK              -- compile + exec OK; stdout matches clang's expected output
  OUTPUT_DRIFT    -- compile + exec OK but stdout differs from clang's
  EXEC_FAIL       -- compile OK; program exit != 0
  COMPILE_FAIL    -- compile.code != 0
  NETWORK_ERR     -- HTTP / timeout error (one retry)

Outputs:
  docs/gcc-16-1-compatibility.md   -- full matrix + per-failure stderr
  src/data/godbolt-permalinks.yml  -- gcc_id / gcc_url / gcc_expected_output
                                      populated for OK + OUTPUT_DRIFT (idempotent)

Run:
    scripts/gcc-compatibility-report.py
    scripts/gcc-compatibility-report.py --dry-run     # no YAML / md write
    scripts/gcc-compatibility-report.py --no-shorten  # md only
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ANSI_RE = re.compile(r"\x1b\[[0-9;?]*[a-zA-Z]")


def strip_ansi(s: str) -> str:
    return ANSI_RE.sub("", s)

try:
    import yaml
except ImportError:
    sys.exit("error: PyYAML not installed. run: pip3 install pyyaml")

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

# Reuse helpers + profiles from the existing shortener script so the
# rewrite list and compile profile stay in one place.
import importlib.util  # noqa: E402

_spec = importlib.util.spec_from_file_location(
    "shorten_examples", REPO_ROOT / "scripts" / "shorten-examples.py"
)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

COMPILER_PROFILES = _mod.COMPILER_PROFILES
apply_rewrites = _mod.apply_rewrites
compile_and_run = _mod.compile_and_run
shorten = _mod.shorten

YAML_PATH = REPO_ROOT / "src" / "data" / "godbolt-permalinks.yml"
DOC_PATH = REPO_ROOT / "docs" / "gcc-16-1-compatibility.md"
CPP26_ROOT = Path("/Users/filipsajdak/dev/c++26")

# Folder NN-slug -> mdx slug (which is the YAML key).
SLUG_MAP = {
    "01-why-it-matters": "why-cpp26-reflection-matters",
    "02-first-reflection": "first-reflection",
    "03-splicing": "splicing",
    "04-expansion-statements": "template-for-expansion-statements",
    "05-enum-to-string": "enum-to-string",
    "06-auto-formatter": "auto-formatter",
    "07-derive-eq-hash": "derive-eq-hash",
    "08-json-naive": "json-naive",
    "09-annotations": "annotations",
    "10-json-deserialize": "json-deserialize",
    "11-json-schema-yaml-toml": "one-codegen-many-formats",
    "12-clap-for-cpp": "clap-for-cpp",
    "13-tiny-orm": "tiny-orm",
    "14-dependency-injection": "dependency-injection",
    "15-auto-mocks": "auto-mocks",
    "16-define-aggregate": "define-aggregate",
    "17-qt-moc-replacement": "qt-moc-replacement",
    "18-cross-language-comparison": "cross-language-comparison",
    "19-reflect-llmschema": "reflect-llmschema",
    "20-reflect-arbitrary": "reflect-arbitrary",
    "21-reflect-optics": "reflect-optics",
    "22-reflect-dx": "reflect-dx",
    "23-reflect-telemetry": "reflect-telemetry",
    "24-reflect-tracing": "reflect-tracing",
    "25-reflect-soa": "reflect-soa",
}


def compile_url(profile: dict) -> str:
    return f"https://godbolt.org/api/compiler/{profile['id']}/compile"


def compile_and_run_with_retry(source: str, profile: dict) -> dict:
    """Single-pass compile+execute against godbolt; retries once on
    network error. Returns a structured dict with raw fields so the
    caller can classify (compile_fail vs exec_fail vs ok).
    """
    payload = {
        "source": source,
        "options": {
            "userArguments": profile["options"],
            "filters": {"execute": True},
        },
    }
    last_err = None
    for attempt in (1, 2):
        req = urllib.request.Request(
            compile_url(profile),
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                body = json.loads(resp.read().decode("utf-8"))
            compile_code = body.get("code", -1)
            compile_stderr = strip_ansi("\n".join(
                x.get("text", "") for x in body.get("stderr", [])
            ))
            exec_result = body.get("execResult") or {}
            exec_code = exec_result.get("code")
            exec_stdout = "\n".join(
                x.get("text", "") for x in exec_result.get("stdout", [])
            )
            exec_stderr = strip_ansi("\n".join(
                x.get("text", "") for x in exec_result.get("stderr", [])
            ))
            return {
                "network_ok": True,
                "compile_code": compile_code,
                "compile_stderr": compile_stderr,
                "exec_code": exec_code,
                "exec_stdout": exec_stdout,
                "exec_stderr": exec_stderr,
            }
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            last_err = e
            if attempt == 1:
                time.sleep(2)
                continue
    return {
        "network_ok": False,
        "error": f"{type(last_err).__name__}: {last_err}",
    }


def load_yaml() -> dict:
    if not YAML_PATH.exists():
        return {}
    with YAML_PATH.open() as f:
        return yaml.safe_load(f) or {}


def write_yaml(data: dict) -> None:
    header = []
    for line in YAML_PATH.read_text().splitlines(keepends=True):
        if line.startswith("#") or line.strip() == "":
            header.append(line)
        else:
            break
    body = yaml.safe_dump(data, sort_keys=False, allow_unicode=False, width=120)
    YAML_PATH.write_text("".join(header) + body)


def classify(result: dict, expected_output: str | None) -> tuple[str, str]:
    """Return (status, category). Category is a one-word bucket used for
    the at-a-glance column: ok / api-name-diff / consteval-strict /
    missing-feature / runtime-diff / unknown.
    """
    if not result["network_ok"]:
        return "NETWORK_ERR", "unknown"
    if result["compile_code"] != 0:
        stderr = result["compile_stderr"].lower()
        if (
            "no member named" in stderr
            or "no template named" in stderr
            or "has not been declared" in stderr
            or "is not a member of" in stderr
            or "no matching function for call" in stderr
        ):
            cat = "api-name-diff"
        elif "not a constant expression" in stderr or "is not constexpr" in stderr or "consteval" in stderr or "non-constant condition" in stderr:
            cat = "consteval-strict"
        elif "expansion-statement" in stderr or "template for" in stderr or "define_aggregate" in stderr or "annotations_of" in stderr or "data_member_spec" in stderr:
            cat = "missing-feature"
        else:
            cat = "unknown"
        return "COMPILE_FAIL", cat
    if result["exec_code"] not in (0, None):
        return "EXEC_FAIL", "runtime-diff"
    if expected_output is not None and result["exec_stdout"].strip() != expected_output.strip():
        return "OUTPUT_DRIFT", "runtime-diff"
    return "OK", "ok"


def render_md(rows: list[dict], gcc_options: str, rewrites: list[tuple[str, str]]) -> str:
    counts = {"OK": 0, "OUTPUT_DRIFT": 0, "COMPILE_FAIL": 0, "EXEC_FAIL": 0, "NETWORK_ERR": 0}
    for r in rows:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    total = len(rows)

    rewrite_lines = "\n".join(f"- `{a}` -> `{b}`" for a, b in rewrites) or "- (none)"

    lines = [
        "# GCC 16.1 compatibility matrix",
        "",
        f"_Generated 2026-05-01 by `scripts/gcc-compatibility-report.py`._",
        "",
        "Compiler: GCC 16.1 on Compiler Explorer (id `g161`), released April 2026.",
        f"Flags: `{gcc_options}`",
        "",
        "## Source rewrites applied",
        "",
        "The .cpp on disk targets clang-p2996 (uses `<experimental/meta>`); the",
        "audit applies these rewrites in-memory before sending to GCC:",
        "",
        rewrite_lines,
        "",
        "## Summary",
        "",
        f"**{counts['OK']} / {total} OK; {counts['OUTPUT_DRIFT']} output-drift; "
        f"{counts['COMPILE_FAIL']} compile-fail; {counts['EXEC_FAIL']} exec-fail"
        + (f"; {counts['NETWORK_ERR']} network-err" if counts.get('NETWORK_ERR') else "")
        + "**",
        "",
        "## Per-example matrix",
        "",
        "| # | Slug | Variant | Status | Category | Notes |",
        "|---|------|---------|--------|----------|-------|",
    ]
    for r in rows:
        notes = r["notes"].replace("|", "\\|").replace("\n", " ")[:120]
        lines.append(
            f"| {r['nn']} | `{r['slug']}` | `{r['variant']}` | "
            f"{r['status']} | {r['category']} | {notes} |"
        )

    failure_rows = [r for r in rows if r["status"] not in ("OK",)]
    if failure_rows:
        lines += ["", "## Failure detail", ""]
        for r in failure_rows:
            lines += [
                f"### {r['nn']:02d} `{r['slug']}` / `{r['variant']}` -- {r['status']}",
                "",
                f"Category: **{r['category']}**",
                "",
                "```",
                r["detail"][:400] or "(no stderr captured)",
                "```",
                "",
            ]

    # Footer: which posts ship with both badges vs clang-only.
    by_slug: dict[str, list[dict]] = {}
    for r in rows:
        by_slug.setdefault(r["slug"], []).append(r)
    both, clang_only = [], []
    for slug, group in by_slug.items():
        if all(g["status"] in ("OK", "OUTPUT_DRIFT") for g in group):
            both.append(slug)
        else:
            clang_only.append(slug)

    lines += [
        "## Compiler-support footer",
        "",
        "Posts confirmed to run on **clang-p2996 + GCC 16.1**:",
        "",
    ]
    lines += [f"- `{s}`" for s in sorted(both)] or ["- (none)"]
    lines += [
        "",
        "Posts that currently ship as **clang-p2996 only**:",
        "",
    ]
    lines += [f"- `{s}`" for s in sorted(clang_only)] or ["- (none)"]
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--dry-run", action="store_true",
                   help="don't write the .md or YAML")
    p.add_argument("--no-shorten", action="store_true",
                   help="skip godbolt /api/shortener calls (write only the .md)")
    args = p.parse_args()

    profile = COMPILER_PROFILES["gcc"]
    yaml_data = load_yaml()
    rows: list[dict] = []
    yaml_changed = False

    folders = sorted(SLUG_MAP.keys())
    for nn_slug in folders:
        slug = SLUG_MAP[nn_slug]
        nn = int(nn_slug.split("-", 1)[0])
        examples_dir = CPP26_ROOT / "posts" / nn_slug / "examples"
        if not examples_dir.is_dir():
            print(f"warn: missing {examples_dir}", file=sys.stderr)
            continue
        sources = sorted(examples_dir.glob("*.cpp"))
        for src in sources:
            variant = src.stem
            label = f"{nn:02d} {slug}.{variant}"
            print(f"audit  {label} ...", flush=True)
            source_text = src.read_text()
            rewritten = apply_rewrites(source_text, profile)

            existing = (yaml_data.get(slug) or {}).get(variant) or {}
            expected = existing.get("expected_output")

            result = compile_and_run_with_retry(rewritten, profile)
            status, category = classify(result, expected)

            notes = ""
            detail = ""
            if status == "COMPILE_FAIL":
                detail = result["compile_stderr"]
                # Prefer the first line containing 'error:' for the table cell.
                err_line = next(
                    (ln for ln in detail.splitlines() if "error:" in ln),
                    (detail.splitlines() or [""])[0],
                )
                # Strip the leading "<source>:NN:CC: error: " prefix for brevity.
                err_msg = re.sub(r"^.*?error:\s*", "", err_line)
                notes = err_msg[:100]
            elif status == "EXEC_FAIL":
                detail = result["exec_stderr"] or f"exit code {result['exec_code']}"
                notes = f"exec exit {result['exec_code']}"
            elif status == "OUTPUT_DRIFT":
                clang_one = (expected or "").splitlines()[0] if expected else ""
                gcc_one = (result["exec_stdout"] or "").splitlines()[0]
                notes = f"clang first line: {clang_one[:40]!r}; gcc: {gcc_one[:40]!r}"
                detail = (
                    f"--- clang expected ---\n{expected}\n"
                    f"--- gcc actual ---\n{result['exec_stdout']}"
                )
            elif status == "NETWORK_ERR":
                detail = result.get("error", "")
                notes = detail[:80]
            elif status == "OK":
                notes = "matches clang stdout" if expected else "ran cleanly (no clang baseline)"

            print(f"       -> {status} ({category})")
            rows.append({
                "nn": nn,
                "slug": slug,
                "variant": variant,
                "status": status,
                "category": category,
                "notes": notes,
                "detail": detail,
            })

            # YAML population for OK / OUTPUT_DRIFT (ran cleanly on g161).
            if status in ("OK", "OUTPUT_DRIFT") and not args.no_shorten:
                yaml_data.setdefault(slug, {})
                entry = dict(yaml_data[slug].get(variant) or {})
                if entry.get("gcc_id"):
                    pass  # idempotent: already shortened
                else:
                    title = entry.get("title") or variant.replace("_", " ").capitalize()
                    try:
                        result_short = shorten(rewritten, title, profile)
                        entry.setdefault("title", title)
                        entry["gcc_id"] = result_short["id"]
                        entry["gcc_url"] = result_short["url"]
                        entry["gcc_expected_output"] = result["exec_stdout"]
                        yaml_data[slug][variant] = entry
                        yaml_changed = True
                        print(f"       shortened -> {result_short['url']}")
                    except Exception as e:
                        print(f"       shorten FAILED: {e}", file=sys.stderr)

    md = render_md(rows, profile["options"], profile["source_rewrites"])
    if args.dry_run:
        print("\n--- DRY RUN: matrix would be ---\n")
        print(md)
        return 0

    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)
    DOC_PATH.write_text(md)
    print(f"\nwrote {DOC_PATH.relative_to(REPO_ROOT)}")

    if yaml_changed:
        write_yaml(yaml_data)
        print(f"wrote {YAML_PATH.relative_to(REPO_ROOT)}")
    else:
        print("YAML unchanged")
    return 0


if __name__ == "__main__":
    sys.exit(main())
