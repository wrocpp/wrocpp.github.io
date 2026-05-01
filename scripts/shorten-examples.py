#!/usr/bin/env python3
"""
Generate Compiler Explorer permalinks for a post's example sources.

For every `posts/<NN>-<slug>/examples/*.cpp` in the cpp26 examples repo,
POST the source to https://godbolt.org/api/shortener with the pinned
Bloomberg clang-p2996 compiler id and the series flags, then merge the
returned shortlink into src/data/godbolt-permalinks.yml.

Idempotent: skips variants that already have an `id` set, unless --force.

Usage:
    scripts/shorten-examples.py --post 02-first-reflection
    scripts/shorten-examples.py --post 02-first-reflection --force
    scripts/shorten-examples.py --post 02-first-reflection --dry-run
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.request
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("error: PyYAML not installed. run: pip3 install pyyaml")

REPO_ROOT = Path(__file__).resolve().parent.parent
YAML_PATH = REPO_ROOT / "src" / "data" / "godbolt-permalinks.yml"
CPP26_ROOT = Path("/Users/filipsajdak/dev/c++26")
SHORTENER_URL = "https://godbolt.org/api/shortener"

# Per-toolchain compile/shorten profile. Two compilers ship C++26 reflection
# as of 2026-05-01: the Bloomberg clang-p2996 fork (the series's reference
# container) and GCC 16.1 (released April 2026, hosted on Compiler Explorer
# as `g161`). Posts gain parallel godbolt links so readers can pick either.
COMPILER_PROFILES = {
    "clang": {
        "id": "clang_bb_p2996",
        "options": "-std=c++26 -freflection-latest -stdlib=libc++",
        "yaml_id_key": "id",
        "yaml_url_key": "url",
        "yaml_output_key": "expected_output",
        # No source rewrite needed -- clang-p2996 ships <experimental/meta>.
        "source_rewrites": [],
    },
    "gcc": {
        "id": "g161",
        "options": "-std=c++26 -freflection",
        "yaml_id_key": "gcc_id",
        "yaml_url_key": "gcc_url",
        "yaml_output_key": "gcc_expected_output",
        # GCC 16.1 ships only <meta>, not the <experimental/meta> alias.
        # Header shim: rewrite the include line on the fly so the same
        # source compiles against both toolchains. Authoritative .cpp on
        # disk stays clang-shaped (uses <experimental/meta>).
        "source_rewrites": [("<experimental/meta>", "<meta>")],
    },
}


def compile_url(profile: dict) -> str:
    return f"https://godbolt.org/api/compiler/{profile['id']}/compile"


def apply_rewrites(source: str, profile: dict) -> str:
    out = source
    for old, new in profile["source_rewrites"]:
        out = out.replace(old, new)
    return out


def slug_from_post(post_arg: str) -> tuple[str, str]:
    """Resolve `02-first-reflection` -> (NN-slug folder, mdx slug).

    The mdx slug is whatever the matching post's frontmatter `slug:` field
    says -- NOT just the folder name minus the NN- prefix. Post 1's folder
    is `01-why-it-matters` but its mdx slug is `why-cpp26-reflection-matters`,
    so a naive split would write the wrong YAML key.
    """
    parts = post_arg.split("-", 1)
    if len(parts) != 2 or not parts[0].isdigit():
        sys.exit(f"error: --post expects NN-slug form, got {post_arg!r}")
    nn = int(parts[0])

    # Find the mdx post whose series_order matches NN.
    posts_dir = REPO_ROOT / "src" / "content" / "posts"
    for mdx in sorted(posts_dir.glob("*.mdx")):
        text = mdx.read_text()
        if not text.startswith("---"):
            continue
        # Frontmatter: read until the closing ---
        end = text.find("\n---", 3)
        if end < 0:
            continue
        fm = yaml.safe_load(text[3:end])
        if fm and fm.get("series_order") == nn and fm.get("series") == "cpp26-reflection":
            return post_arg, fm["slug"]
    sys.exit(f"error: no mdx post with series_order={nn} found in {posts_dir}")


def shorten(source: str, title: str, profile: dict) -> dict:
    """Hit godbolt's shortener with one source file under the given
    compiler profile. Returns the parsed {id, url, title}."""
    payload = {
        "sessions": [
            {
                "id": 1,
                "language": "c++",
                "source": source,
                "compilers": [
                    {"id": profile["id"], "options": profile["options"]}
                ],
            }
        ]
    }
    req = urllib.request.Request(
        SHORTENER_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        body = json.loads(resp.read().decode("utf-8"))
    url = body.get("url")
    if not url:
        sys.exit(f"error: shortener returned no url: {body}")
    short_id = url.rsplit("/", 1)[-1]
    return {"id": short_id, "url": url, "title": title}


def compile_and_run(source: str, profile: dict) -> tuple[bool, str, str]:
    """Compile + execute the source via godbolt's API under the given
    compiler profile.

    Returns (ok, stdout, stderr_or_compile_log). `ok` is True only if the
    compiler exited 0 AND the program exited 0. Used as a gate BEFORE
    creating the shortlink: if the code doesn't actually run on Compiler
    Explorer, the published post would lie to readers.
    """
    payload = {
        "source": source,
        "options": {
            "userArguments": profile["options"],
            "filters": {"execute": True},
        },
    }
    req = urllib.request.Request(
        compile_url(profile),
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return False, "", f"godbolt http {e.code}: {e.read().decode(errors='replace')[:300]}"
    compile_code = body.get("code", -1)
    compile_stderr = "\n".join(x.get("text", "") for x in body.get("stderr", []))
    if compile_code != 0:
        return False, "", f"compile failed (code={compile_code}):\n{compile_stderr[:600]}"
    exec_result = body.get("execResult") or {}
    exec_code = exec_result.get("code", -1)
    exec_stdout = "\n".join(x.get("text", "") for x in exec_result.get("stdout", []))
    exec_stderr = "\n".join(x.get("text", "") for x in exec_result.get("stderr", []))
    if exec_code != 0:
        return False, exec_stdout, f"program exited {exec_code}:\n{exec_stderr[:600]}"
    return True, exec_stdout, ""


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--post", required=True, help="post folder (e.g. 02-first-reflection)")
    p.add_argument("--force", action="store_true", help="overwrite existing entries")
    p.add_argument("--dry-run", action="store_true", help="print what would change")
    p.add_argument("--no-run-verify", action="store_true",
                   help="skip the godbolt API compile+execute gate (NOT RECOMMENDED)")
    p.add_argument("--compiler", choices=["clang", "gcc", "both"], default="both",
                   help="which compiler profile(s) to shorten + verify against (default: both)")
    args = p.parse_args()

    profiles_to_run = (
        list(COMPILER_PROFILES.values()) if args.compiler == "both"
        else [COMPILER_PROFILES[args.compiler]]
    )

    nn_slug, slug = slug_from_post(args.post)
    examples_dir = CPP26_ROOT / "posts" / nn_slug / "examples"
    if not examples_dir.is_dir():
        sys.exit(f"error: not a directory: {examples_dir}")

    sources = sorted(p for p in examples_dir.glob("*.cpp"))
    if not sources:
        sys.exit(f"error: no .cpp files in {examples_dir}")

    yaml_data = {}
    if YAML_PATH.exists():
        with YAML_PATH.open() as f:
            yaml_data = yaml.safe_load(f) or {}
    yaml_data.setdefault(slug, {})

    changed = False
    for src in sources:
        variant = src.stem  # e.g. "teaser_peel"
        existing = yaml_data[slug].get(variant) or {}
        title = existing.get("title") or variant.replace("_", " ").capitalize()
        source_text = src.read_text()

        # Loop per compiler profile. clang and gcc each have their own YAML
        # keys (id/url/expected_output vs gcc_id/gcc_url/gcc_expected_output)
        # so the entry can carry both in parallel.
        for profile in profiles_to_run:
            id_key = profile["yaml_id_key"]
            url_key = profile["yaml_url_key"]
            output_key = profile["yaml_output_key"]
            label = f"{slug}.{variant} [{profile['id']}]"
            already_shortened = bool(existing.get(id_key)) and not args.force

            if args.dry_run:
                verb = "VERIFY" if already_shortened else "DRY"
                print(f"{verb:6} {label}  ({src.name}, {len(source_text)} chars)")
                continue

            # Apply per-profile source rewrites (e.g. <experimental/meta>
            # -> <meta> for GCC). Authoritative .cpp on disk is unchanged.
            profile_source = apply_rewrites(source_text, profile)

            stdout = ""
            if not args.no_run_verify:
                print(f"verify  {label}  ->", end=" ", flush=True)
                ok, stdout, err = compile_and_run(profile_source, profile)
                if not ok:
                    print("FAIL")
                    sys.exit(f"\nCE verification failed for {src.name} on {profile['id']}:\n{err}")
                print(f"OK (stdout: {len(stdout)} chars)")

            if already_shortened:
                old_out = existing.get(output_key)
                if old_out == stdout:
                    print(f"skip    {label}  (id={existing[id_key]}, output unchanged)")
                    continue
                existing[output_key] = stdout
                yaml_data[slug][variant] = existing
                kind = "added" if not old_out else "updated"
                print(f"OK      {label}  ({kind} {output_key} for id={existing[id_key]})")
                changed = True
                continue

            # Fresh shortener call.
            result = shorten(profile_source, title, profile)
            # Re-key the response to per-profile YAML keys, then merge into
            # the existing entry so clang and gcc fields coexist.
            entry = dict(existing)
            entry["title"] = title
            entry[id_key] = result["id"]
            entry[url_key] = result["url"]
            if stdout:
                entry[output_key] = stdout
            yaml_data[slug][variant] = entry
            existing = entry
            print(f"OK      {label}  -> {result['url']}")
            changed = True

    if changed and not args.dry_run:
        # Preserve the file header by re-reading and only rewriting from the
        # first non-comment line.
        header = []
        if YAML_PATH.exists():
            for line in YAML_PATH.read_text().splitlines(keepends=True):
                if line.startswith("#") or line.strip() == "":
                    header.append(line)
                else:
                    break
        body = yaml.safe_dump(yaml_data, sort_keys=False, allow_unicode=False, width=120)
        YAML_PATH.write_text("".join(header) + body)
        print(f"\nwrote {YAML_PATH.relative_to(REPO_ROOT)}")
    elif args.dry_run:
        print("\n(dry-run; YAML not written)")
    else:
        print("\nnothing to do (all variants already have ids)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
