#!/usr/bin/env python3
"""Compile (and optionally run) a snippet on Compiler Explorer, or check feature macros.

Read-only against Compiler Explorer's public API; writes nothing. The radar uses it to
answer "does this feature run today, and on which compiler".

It reads no files on purpose. The radar session reads untrusted web pages, so a probe that
could upload any path to a third party would be an exfiltration channel. The code to compile
arrives as an argument, is size-capped, and goes only to godbolt.org.

Usage:
    probe.py --compiler g161 --options=-std=c++26 --code 'int main(){}' --run
    probe.py --compiler gsnapshot --options=-std=c++29 --macro __cpp_lib_hive --macro __cpp_constexpr_virtual_inheritance
    probe.py --compiler g161 --code "$(cat demo.cpp)" --lib boost:191 --run     # shell reads the file, not probe.py
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time

API = "https://godbolt.org/api/compiler/{}/compile"
TIMEOUT_S = 120  # Compiler Explorer queues; its own execution limit is shorter
ATTEMPTS = 3     # the public API drops requests now and then
BACKOFF_S = 5
MAX_CODE_BYTES = 20_000  # a demo is a few hundred bytes; this bounds what can leave the machine
COMPILER_ID = re.compile(r"[A-Za-z0-9_.-]{1,40}")
LIB_SPEC = re.compile(r"[a-z0-9_]{1,30}:[A-Za-z0-9_.-]{1,30}")
MACRO_NAME = re.compile(r"__cpp_[a-z0-9_]{1,60}|__cplusplus|_LIBCPP_VERSION|__GLIBCXX__")
MACRO_HEADERS = "#include <version>\n#include <cstdio>\n"
ANSI = re.compile(r"\x1b\[[0-9;]*[mK]")


def validate(compiler: str, libs: list[str], macros: list[str], source: str) -> None:
    """Reject anything that could change where the request goes or how much leaves."""
    if not COMPILER_ID.fullmatch(compiler):
        raise SystemExit(f"probe: bad compiler id {compiler!r}")
    for lib in libs:
        if not LIB_SPEC.fullmatch(lib):
            raise SystemExit(f"probe: bad library spec {lib!r}; expected id:versionId")
    for macro in macros:
        if not MACRO_NAME.fullmatch(macro):
            raise SystemExit(f"probe: {macro!r} is not a feature-test macro name")
    if len(source.encode("utf-8")) > MAX_CODE_BYTES:
        raise SystemExit(f"probe: code is over {MAX_CODE_BYTES} bytes")


def macro_source(macros: list[str]) -> str:
    body = "".join(
        f'#ifdef {m}\n  std::printf("{m} = %ld\\n", (long){m});\n#else\n  std::puts("{m}: undefined");\n#endif\n'
        for m in macros
    )
    return f"{MACRO_HEADERS}int main() {{\n{body}}}\n"


def request(compiler: str, source: str, options: str, run: bool, libs: list[str]) -> dict:
    body = {
        "source": source,
        "options": {
            "userArguments": options,
            "executeParameters": {},
            "compilerOptions": {"executorRequest": run},
            "libraries": [{"id": l.split(":")[0], "version": l.split(":")[1]} for l in libs],
            "filters": {"execute": run},
        },
        "lang": "c++",
    }
    command = ["curl", "-s", "-m", str(TIMEOUT_S), "-X", "POST", "-H", "Content-Type: application/json",
               "-H", "Accept: application/json", API.format(compiler), "-d", json.dumps(body)]
    last = "no attempt made"
    for attempt in range(ATTEMPTS):
        if attempt:
            time.sleep(BACKOFF_S)
        proc = subprocess.run(command, capture_output=True, text=True)
        try:
            return json.loads(proc.stdout)
        except json.JSONDecodeError:
            last = f"curl exit {proc.returncode}, body {proc.stdout[:120]!r}"
    raise SystemExit(f"probe: Compiler Explorer gave no JSON after {ATTEMPTS} attempts ({last})")


def render(result: dict) -> str:
    stdout = "\n".join(x["text"] for x in result.get("stdout", []))
    errs = result.get("buildResult", {}).get("stderr") or result.get("stderr") or []
    stderr = ANSI.sub("", "\n".join(x["text"] for x in errs))[:600]
    head = f"build={result.get('code')}"
    return "\n".join(part for part in (head, stdout, stderr) if part)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--compiler", required=True, help="Compiler Explorer compiler id, e.g. g161, gsnapshot, clang_trunk")
    ap.add_argument("--options", default="-std=c++26")
    ap.add_argument("--code", help="C++ source text to compile (not a path; probe.py reads no files)")
    ap.add_argument("--macro", action="append", default=[], help="feature-test macro to report (repeatable)")
    ap.add_argument("--lib", action="append", default=[], help="library as id:versionId, e.g. boost:191")
    ap.add_argument("--run", action="store_true", help="execute the program")
    args = ap.parse_args()
    if bool(args.code) == bool(args.macro):
        ap.error("give exactly one of --code or --macro")
    source = args.code if args.code else macro_source(args.macro)
    validate(args.compiler, args.lib, args.macro, source)
    run = args.run or bool(args.macro)
    print(render(request(args.compiler, source, args.options, run, args.lib)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
