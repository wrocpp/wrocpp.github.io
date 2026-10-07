#!/usr/bin/env python3
"""Readability metrics for wro.cpp posts (rules and numbers: docs/STYLE.md, "Readability").

Measures the prose of a post after stripping frontmatter, imports, fenced code, JSX
components (<GodboltEmbed .../>, <PostLink ...> keeps its link text), HTML, comments and
link/image URLs. Inline code spans count as one word each for sentence statistics.
Fog is a trend line only: it is weak on C++ vocabulary and is never a gate.

Usage:
  scripts/readability-report.py --slug S            # one post
  scripts/readability-report.py --file F.mdx        # one file
  scripts/readability-report.py --all               # table, one row per post
  scripts/readability-report.py --group             # group medians
  scripts/readability-report.py --write-baseline    # scripts/readability-baseline.json

The analysis lives in analyze(); prose-lint.py and check-rewrite-invariants.py import it.
"""

import argparse
import json
import math
import re
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASELINE_PATH = Path(__file__).resolve().parent / "readability-baseline.json"
SPAN = "\x00"

# Thresholds (docs/STYLE.md, Readability). GOV.UK / Microsoft sentence limits are evidence
# based; the span, paragraph, run and section numbers are house choices.
SENT_WARN, SENT_ERROR = 25, 35
SENT_MEAN_MAX = 20
SENT_MEAN_MIN_SENTENCES = 3
SPANS_SENT_WARN, SPANS_SENT_ERROR = 2, 4
SPANS_PER100_WARN = 8
PARA_WORDS_WARN, PARA_SENT_ERROR = 120, 7
RUN_WARN = 4
SECTION_WORDS_WARN = 300
IN_SHORT_MIN_WORDS = 500
GROUP_DATE_SPLIT = "2026-06-01"

TOKEN_RE = re.compile(SPAN + r"|[A-Za-z0-9_]+(?:['\u2019-][A-Za-z0-9_]+)*")
FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")
LIST_RE = re.compile(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$")
HEADING_RE = re.compile(r"^#{1,6}\s+(.*?)\s*#*\s*$")
EMBED_RE = re.compile(r"^\s*<[A-Z][A-Za-z0-9]*\b[^>]*/>\s*$")
ABBREV_RE = re.compile(r"\b(e\.g|i\.e|vs|etc|cf|approx|incl|resp)\.", re.IGNORECASE)
SPAN_RE = re.compile(r"(`+)(?!`)(.+?)(?<!`)\1(?!`)")


# --- block structure ----------------------------------------------------------

def split_frontmatter(text):
    lines = text.split("\n")
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                return lines[1:i], lines[i + 1:], i + 2
    return [], lines, 1


def frontmatter_fields(fm_lines):
    """Top-level `key: value` fields; continuation lines join the previous field."""
    fields, key = {}, None
    for line in fm_lines:
        m = re.match(r"^([A-Za-z_][\w-]*):\s?(.*)$", line)
        if m:
            key = m.group(1)
            fields[key] = m.group(2).strip()
        elif key is not None:
            fields[key] += "\n" + line
    return fields


class _Parser:
    """Line walker that groups the body into heading/para/list/table/code/embed blocks."""

    def __init__(self, lines, first_lineno):
        self.lines, self.first = lines, first_lineno
        self.blocks, self.cur = [], None
        self.in_fence, self.in_comment, self.blank_after_list = "", False, False

    def flush(self):
        if self.cur:
            self.blocks.append(self.cur)
        self.cur, self.blank_after_list = None, False

    def start(self, kind, no, text=""):
        self.flush()
        self.cur = {"kind": kind, "line": no, "items": [text] if text else []}

    def push_single(self, kind, no, text=""):
        self.flush()
        self.blocks.append({"kind": kind, "line": no, "items": [text]})

    def skip_noise(self, line):
        """Fences, comments, imports. Returns True when the line was consumed."""
        if self.in_fence:
            m = FENCE_RE.match(line)
            if m and m.group(1)[0] == self.in_fence:
                self.in_fence = ""
            return True
        if self.in_comment:
            self.in_comment = "-->" not in line
            return True
        s = line.strip()
        if s.startswith("<!--"):
            self.in_comment = "-->" not in s
            return True
        return bool(re.match(r"^\s*import\b.*\bfrom\b", line))

    def block_line(self, line, no):
        """Headings, fences, tables, embeds, rules. Returns True when consumed."""
        s = line.strip()
        fm = FENCE_RE.match(line)
        if fm:
            self.push_single("code", no)
            self.in_fence = fm.group(1)[0]
            return True
        return self.structural_line(line, s, no)

    def structural_line(self, line, s, no):
        if HEADING_RE.match(s):
            self.push_single("heading", no, HEADING_RE.match(s).group(1))
        elif s.startswith("|"):
            if not self.cur or self.cur["kind"] != "table":
                self.start("table", no)
        elif EMBED_RE.match(line) or re.match(r"^\s*<[A-Z]\w*\s*$", line):
            self.push_single("embed", no)
        elif re.match(r"^(-{3,}|\*{3,}|_{3,})$", s):
            self.flush()
        else:
            return False
        return True

    def text_line(self, line, no):
        m = LIST_RE.match(line)
        if m and self.cur and self.cur["kind"] == "list":
            self.cur["items"].append(m.group(3))
        elif m:
            self.start("list", no, m.group(3))
        elif self.cur and self.cur["kind"] == "list":
            self.list_continuation(line, no)
        elif self.cur and self.cur["kind"] == "para":
            self.cur["items"][0] += " " + line.strip().lstrip("> ")
        else:
            self.start("para", no, line.strip().lstrip("> "))
        self.blank_after_list = False

    def list_continuation(self, line, no):
        if self.blank_after_list and not line[:1].isspace():
            self.start("para", no, line.strip())
        else:
            self.cur["items"][-1] += " " + line.strip()

    def run(self):
        for offset, line in enumerate(self.lines):
            no = self.first + offset
            if self.skip_noise(line):
                continue
            if not line.strip():
                if self.cur and self.cur["kind"] == "list":
                    self.blank_after_list = True
                else:
                    self.flush()
            elif not self.block_line(line, no):
                self.text_line(line, no)
        self.flush()
        return self.blocks


def parse_blocks(text):
    fm, body, first = split_frontmatter(text)
    return frontmatter_fields(fm), _Parser(body, first).run()


# --- sentences ----------------------------------------------------------------

def clean_inline(raw):
    """Markdown/HTML inline text -> plain text with each code span replaced by SPAN."""
    t = SPAN_RE.sub(f" {SPAN} ", raw)
    t = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", t)
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)
    t = re.sub(r"</?[A-Za-z][^>]*>", " ", t)
    t = re.sub(r"https?://\S+", " ", t)
    t = re.sub(r"\*+|~~", "", t)
    return t


def split_sentences(plain):
    t = ABBREV_RE.sub(lambda m: m.group(0).replace(".", "\x01"), plain)
    parts = re.split(r"(?<=[.!?])[\"'\u201d\u2019)]*\s+(?=[^a-z])", t)
    return [p.replace("\x01", ".").strip() for p in parts if p.strip()]


def tokens_of(sentence):
    return TOKEN_RE.findall(sentence)


def syllables(word):
    w = re.sub(r"[^a-z]", "", word.lower())
    n = len(re.findall(r"[aeiouy]+", w))
    if n > 1 and w.endswith("e") and not w.endswith(("le", "ee", "ye")):
        n -= 1
    elif n > 1 and re.search(r"[^td]ed$|[^sxzcg]es$", w):
        n -= 1
    return max(n, 1)


def is_complex(tok):
    if tok == SPAN or tok[0].isupper() or "-" in tok or "_" in tok:
        return False
    return tok.isalpha() and syllables(tok) >= 3


def fog(sentences_tokens):
    words = sum(len(t) for t in sentences_tokens)
    if not words or not sentences_tokens:
        return 0.0
    complex_n = sum(1 for toks in sentences_tokens for t in toks if is_complex(t))
    return 0.4 * (words / len(sentences_tokens) + 100 * complex_n / words)


# --- metrics ------------------------------------------------------------------

def _units(blocks):
    """Prose units (paragraphs and list items) tagged with their section index."""
    sec, units = 0, []
    for b in blocks:
        if b["kind"] == "heading":
            sec += 1
        elif b["kind"] in ("para", "list"):
            for item in b["items"]:
                units.append({"sec": sec, "line": b["line"], "kind": b["kind"], "raw": item})
    return units


def _plain(sentence):
    flat = re.sub(r"\s+", " ", sentence.replace(SPAN, "`..`"))
    return re.sub(r"\s+([,.;:])", r"\1", flat).strip()


def _sentence_rows(units):
    rows = []
    for u in units:
        for s in split_sentences(clean_inline(u["raw"])):
            toks = tokens_of(s)
            if toks:
                rows.append({"sec": u["sec"], "line": u["line"], "text": _plain(s),
                             "toks": toks, "n": len(toks), "spans": toks.count(SPAN)})
    return rows


def _percentile90(values):
    if not values:
        return 0
    return sorted(values)[math.ceil(0.9 * len(values)) - 1]


def _prose_runs(blocks):
    runs, cur = [], 0
    for b in blocks:
        if b["kind"] == "para":
            cur += 1
        else:
            runs.append(cur)
            cur = 0
    runs.append(cur)
    return runs


def _section_stats(rows, units):
    secs = {}
    for r in rows:
        s = secs.setdefault(r["sec"], {"lens": [], "words": 0})
        s["lens"].append(r["n"])
        s["words"] += r["n"] - r["spans"]
    return secs


def _paragraph_rows(blocks):
    out = []
    for b in blocks:
        if b["kind"] == "para":
            sents = [tokens_of(s) for s in split_sentences(clean_inline(b["items"][0]))]
            sents = [t for t in sents if t]
            out.append({"line": b["line"], "words": sum(len(t) for t in sents), "sents": len(sents)})
    return out


def _headings(blocks):
    return [b["items"][0] for b in blocks if b["kind"] == "heading"]


def _in_short(blocks):
    paras_before = 0
    for b in blocks:
        if b["kind"] == "heading":
            return bool(re.match(r"in short\b", b["items"][0], re.IGNORECASE)) and paras_before <= 1
        if b["kind"] == "para":
            paras_before += 1
    return False


def _pct(part, whole):
    return round(100 * part / whole, 1) if whole else 0.0


def _core_metrics(rows):
    lens = [r["n"] for r in rows]
    spans = sum(r["spans"] for r in rows)
    words = sum(r["n"] for r in rows) - spans
    nocode = [[t for t in r["toks"] if t != SPAN] for r in rows]
    return {
        "words": words, "sentences": len(rows),
        "mean_sent": round(statistics.fmean(lens or [0]), 2),
        "p90_sent": _percentile90(lens),
        "over25_share": _pct(sum(1 for n in lens if n > SENT_WARN), len(lens)),
        "fog": round(fog([r["toks"] for r in rows]), 2),
        "fog_nocode": round(fog([t for t in nocode if t]), 2),
        "spans": spans,
        "spans_per100": round(100 * spans / (words or 1), 2),
        "sent3_share": _pct(sum(1 for r in rows if r["spans"] >= 3), len(rows)),
    }


def _count(items, pred):
    return sum(1 for i in items if pred(i))


def _violation_counts(rows, paras, secs, runs, words, in_short):
    sec_mean20 = _count(secs.values(), lambda s: len(s["lens"]) >= SENT_MEAN_MIN_SENTENCES
                        and statistics.fmean(s["lens"]) > SENT_MEAN_MAX)
    return {
        "n_over25": _count(rows, lambda r: r["n"] > SENT_WARN),
        "n_over35": _count(rows, lambda r: r["n"] > SENT_ERROR),
        "n_sec_mean20": sec_mean20,
        "n_sent_spans_gt2": _count(rows, lambda r: r["spans"] > SPANS_SENT_WARN),
        "n_sent_spans_gt4": _count(rows, lambda r: r["spans"] > SPANS_SENT_ERROR),
        "n_para_over120": _count(paras, lambda p: p["words"] > PARA_WORDS_WARN),
        "n_para_over7": _count(paras, lambda p: p["sents"] > PARA_SENT_ERROR),
        "n_runs_over4": _count(runs, lambda r: r > RUN_WARN),
        "n_sec_over300": _count(secs.values(), lambda s: s["words"] > SECTION_WORDS_WARN),
        "no_in_short": int(words > IN_SHORT_MIN_WORDS and not in_short),
    }


def analyze(text):
    """Return (metrics, detail). metrics is JSON-able and is what the baseline stores;
    detail carries line-numbered findings for prose-lint."""
    fields, blocks = parse_blocks(text)
    units = _units(blocks)
    rows = _sentence_rows(units)
    paras = _paragraph_rows(blocks)
    secs = _section_stats(rows, units)
    runs = _prose_runs(blocks)
    core = _core_metrics(rows)
    in_short = _in_short(blocks)
    heads = _headings(blocks)
    metrics = dict(core)
    metrics.update({
        "paragraphs": len(paras),
        "para_mean_words": round(statistics.fmean([p["words"] for p in paras]), 1) if paras else 0.0,
        "para_max_words": max([p["words"] for p in paras], default=0),
        "para_max_sent": max([p["sents"] for p in paras], default=0),
        "headings": len(heads),
        "max_section_words": max([s["words"] for s in secs.values()], default=0),
        "max_prose_run": max(runs),
        "list_items": sum(len(b["items"]) for b in blocks if b["kind"] == "list"),
        "tables": sum(1 for b in blocks if b["kind"] == "table"),
        "in_short": int(in_short),
        "dense_excess": round(max(0.0, core["spans_per100"] - SPANS_PER100_WARN), 2),
    })
    metrics.update(_violation_counts(rows, paras, secs, runs, core["words"], in_short))
    detail = {"rows": rows, "paras": paras, "secs": secs, "fields": fields, "headings": heads}
    return metrics, detail


def post_slug(path, fields):
    slug = fields.get("slug", "").strip("\"'")
    return slug or re.sub(r"^\d{4}-\d{2}-\d{2}-", "", Path(path).stem)


def all_posts(root=ROOT):
    return sorted((root / "src" / "content" / "posts").glob("*.mdx"))


def analyze_path(path):
    text = Path(path).read_text(encoding="utf-8")
    metrics, detail = analyze(text)
    fields = detail["fields"]
    metrics_row = {"slug": post_slug(path, fields), "kind": fields.get("kind", ""),
                   "series": fields.get("series", ""), "pubDate": fields.get("pubDate", "")}
    return metrics_row, metrics


def load_baseline(path=BASELINE_PATH):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


# --- CLI ----------------------------------------------------------------------

BASELINE_KEYS = ["words", "mean_sent", "fog", "spans_per100", "sent3_share", "over25_share",
                 "max_prose_run", "headings", "dense_excess", "n_over25", "n_over35", "n_sec_mean20",
                 "n_sent_spans_gt2", "n_sent_spans_gt4", "n_para_over120", "n_para_over7",
                 "n_runs_over4", "n_sec_over300", "no_in_short"]


def print_one(meta, m):
    print(f"{meta['slug']}  ({meta['kind'] or '?'}, {meta['series'] or 'no series'}, {meta['pubDate']})")
    rows = [
        ("prose words", m["words"]), ("sentences", m["sentences"]),
        ("sentence mean / p90", f"{m['mean_sent']} / {m['p90_sent']}"),
        ("sentences over 25 words", f"{m['over25_share']}%"),
        ("Fog (spans as CODE) / without code", f"{m['fog']} / {m['fog_nocode']}"),
        ("paragraphs: mean words / max words / max sentences",
         f"{m['para_mean_words']} / {m['para_max_words']} / {m['para_max_sent']}"),
        ("code spans per 100 words", m["spans_per100"]),
        ("sentences with 3+ spans", f"{m['sent3_share']}%"),
        ("headings / max section words", f"{m['headings']} / {m['max_section_words']}"),
        ("longest prose run (paragraphs)", m["max_prose_run"]),
        ("list items / tables", f"{m['list_items']} / {m['tables']}"),
        ("'In short' first section", "yes" if m["in_short"] else "no"),
    ]
    for label, value in rows:
        print(f"  {label:52} {value}")
    base = load_baseline().get(meta["slug"])
    if base:
        print(f"  baseline: spans/100 {base['spans_per100']}, over-25 sentences {base['n_over25']}, "
              f"longest run {base['max_prose_run']}")


TABLE_COLS = [("slug", 46, "<"), ("words", 6, ">"), ("fog", 5, ">"), ("fogNC", 5, ">"),
              ("mean", 5, ">"), (">25%", 5, ">"), ("sp/100", 6, ">"), ("3sp%", 5, ">"),
              ("head", 4, ">"), ("run", 3, ">"), ("short", 5, ">")]


def print_table(rows):
    print(" ".join(f"{n:{a}{w}}" for n, w, a in TABLE_COLS))
    for meta, m in rows:
        vals = [meta["slug"][:46], m["words"], m["fog"], m["fog_nocode"], m["mean_sent"],
                m["over25_share"], m["spans_per100"], m["sent3_share"], m["headings"],
                m["max_prose_run"], "yes" if m["in_short"] else "-"]
        print(" ".join(f"{v:{a}{w}}" for v, (_, w, a) in zip(vals, TABLE_COLS)))


GROUPS = [
    ("cpp26-reflection series", lambda p: p["series"] == "cpp26-reflection"),
    ("kind: short", lambda p: p["kind"] == "short"),
    ("ub-checks-per-statement series", lambda p: p["series"] == "ub-checks-per-statement"),
    ("other flagships", lambda p: p["kind"] == "flagship"
     and p["series"] not in ("cpp26-reflection", "ub-checks-per-statement")),
    (f"published before {GROUP_DATE_SPLIT}", lambda p: p["pubDate"] < GROUP_DATE_SPLIT),
    (f"published from {GROUP_DATE_SPLIT}", lambda p: p["pubDate"] >= GROUP_DATE_SPLIT),
    ("all posts", lambda p: True),
]
GROUP_COLS = [("n", None), ("Fog", "fog"), ("Fog no code", "fog_nocode"), ("mean sent", "mean_sent"),
              ("% >25", "over25_share"), ("spans/100", "spans_per100"), ("% 3+ spans", "sent3_share"),
              ("headings", "headings"), ("max run", "max_prose_run"), ("list items", "list_items")]


def group_table(rows):
    lines = ["| group | " + " | ".join(c for c, _ in GROUP_COLS) + " |",
             "|---|" + "---|" * len(GROUP_COLS)]
    for name, pred in GROUPS:
        sel = [m for meta, m in rows if pred(meta)]
        cells = [str(len(sel))]
        for _, key in GROUP_COLS[1:]:
            cells.append(f"{statistics.median([m[key] for m in sel]):.1f}" if sel else "-")
        lines.append(f"| {name} | " + " | ".join(cells) + " |")
    return "\n".join(lines)


def write_baseline(rows, path=BASELINE_PATH):
    data = {meta["slug"]: {k: m[k] for k in BASELINE_KEYS} for meta, m in rows}
    body = ",\n".join(f"{json.dumps(slug)}: {json.dumps(v, separators=(',', ':'))}"
                      for slug, v in sorted(data.items()))
    Path(path).write_text("{\n" + body + "\n}\n", encoding="utf-8")
    return len(data)


def resolve_slug(slug):
    hits = sorted((ROOT / "src" / "content" / "posts").glob(f"*-{slug}.mdx"))
    return hits[0] if hits else None


def run_single(args):
    path = args.file or resolve_slug(args.slug)
    if path is None or not Path(path).exists():
        print("ERROR: post not found")
        return 2
    print_one(*analyze_path(path))
    return 0


def run_corpus(args):
    rows = [analyze_path(p) for p in all_posts()]
    if args.all:
        print_table(rows)
    if args.group:
        print(group_table(rows))
    if args.write_baseline:
        print(f"wrote {write_baseline(rows)} entries to {BASELINE_PATH.relative_to(ROOT)}")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--slug")
    ap.add_argument("--file", type=Path)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--group", action="store_true")
    ap.add_argument("--write-baseline", action="store_true")
    args = ap.parse_args()
    if args.slug or args.file:
        return run_single(args)
    if args.all or args.group or args.write_baseline:
        return run_corpus(args)
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
