"""Tests for scripts/social-analytics-report.py (stdlib unittest): python3 -m unittest discover -s scripts/tests

All data here is invented. The tests build a tiny repository in a temporary directory, so they do not
depend on the real posts, the real schedule or the real social cards.
"""

import contextlib
import importlib.util
import io
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("social_analytics", SCRIPTS / "social-analytics-report.py")
sa = importlib.util.module_from_spec(spec)
sys.modules["social_analytics"] = sa
spec.loader.exec_module(sa)

WINDOW = ("2026-09-01", "2026-09-30")
DOUBLES = {"2026-09-05": {"slug": "late-slot", "hour": 16, "why": "invented"}}
COLLISIONS = {"2026-09-01"}
DISTURBANCES = {"2026-09-01": "invented-collision"}


def post(slug, date, kind="short", tags="[news, cpp26]", body="Some text.\n", extra=""):
    return (
        f"---\ntitle: \"Title of {slug}\"\nslug: \"{slug}\"\npubDate: {date}\nkind: {kind}\n"
        f"tags: {tags}\nsummary: \"A summary: with a colon.\"\n{extra}---\n{body}"
    )


def git(root, *args, date=None):
    env = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@example.com",
               GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@example.com")
    if date:
        env.update(GIT_AUTHOR_DATE=date, GIT_COMMITTER_DATE=date)
    subprocess.run(["git", *args], cwd=root, check=True, env=env, capture_output=True)


def card(root, slug, h1, caption_body, date=None):
    folder = root / "social" / "linkedin" / slug
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "content.md").write_text(f"---\ntemplate: x\n---\n\n:::insight{{citation=\"c\"}}\n# {h1}\nSubtitle.\n:::\n")
    (folder / "caption.md").write_text(f"# {slug}\n\n## Body\n{caption_body}\n\n## Hashtags\n#cpp\n")
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", f"card {h1}", date=date)


def build_repo(root):
    posts = root / "src" / "content" / "posts"
    posts.mkdir(parents=True)
    git(root, "init", "-q")
    files = {
        "2026-07-01-before.mdx": post("before", "2026-07-01"),                       # outside the window
        "2026-09-01-first.mdx": post("first", "2026-09-01"),                          # collision day
        "2026-09-01-second.mdx": post("second", "2026-09-01", tags="[qt, moc]"),     # collision day
        "2026-09-03-demo.mdx": post("demo", "2026-09-03", kind="flagship", tags="[reflection]",
                                    body="import G from 'x';\n<GodboltEmbed id=\"abc\" />\n"),
        "2026-09-05-early-slot.mdx": post("early-slot", "2026-09-05", tags="[performance]",
                                          body="```cpp\nint x;\n```\n"),
        "2026-09-05-late-slot.mdx": post("late-slot", "2026-09-05", tags="[safety]",
                                         extra="series: s\nseries_order: 3\n"),
    }
    for name, text in files.items():
        (posts / name).write_text(text)
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "posts", date="2026-08-01T00:00:00Z")


def features(root, **kw):
    return sa.build_features(root, *WINDOW, doubles=DOUBLES, collisions=COLLISIONS,
                             disturbances=DISTURBANCES, **kw)


class HookNumber(unittest.TestCase):
    def test_a_quantity_claim_is_a_candidate(self):
        for text in ("C++26 ends a 40-year footgun", "Four CppCon keynotes", "A 1.7x gap between two designs",
                     "One bad port, reported four times", "Cuts 33 allocations to none"):
            with self.subTest(text=text):
                self.assertTrue(sa.hook_number(text))

    def test_versions_papers_years_and_dates_are_not_quantities(self):
        for text in ("Qt 6.12 LTS", "until 12 October", "GCC 16.2 adds P2795R5 in 2026",
                     "MSVC 14.52 release candidate", "C++26 contracts", "Clang 19.1.7 builds it",
                     "On 3 November the vote closes", "wro.cpp -- 2026-10-27"):
            with self.subTest(text=text):
                self.assertFalse(sa.hook_number(text))


class Frontmatter(unittest.TestCase):
    def test_reads_flat_keys_lists_and_quoted_values_with_colons(self):
        fm = sa.parse_frontmatter(post("demo", "2026-09-03", tags="[a, b-c, d]", extra="series_order: 3\n"))
        self.assertEqual(fm["slug"], "demo")
        self.assertEqual(fm["tags"], ["a", "b-c", "d"])
        self.assertEqual(fm["summary"], "A summary: with a colon.")
        self.assertEqual(fm["series_order"], "3")

    def test_kind_defaults_to_flagship(self):
        text = "---\nslug: x\npubDate: 2026-09-03\ntags: []\n---\nbody\n"
        self.assertEqual(sa.parse_frontmatter(text).get("kind", sa.DEFAULT_KIND), "flagship")


class TopicGroup(unittest.TestCase):
    def test_first_matching_group_wins(self):
        self.assertEqual(sa.topic_group(["reflection", "qt", "moc"]), "qt")
        self.assertEqual(sa.topic_group(["cpp26", "reflection"]), "reflection")

    def test_unknown_tags_fall_into_other(self):
        self.assertEqual(sa.topic_group(["cpp26", "news"]), "other")
        self.assertEqual(sa.topic_group([]), "other")


class Features(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        build_repo(self.root)
        self.rows = {r["slug"]: r for r in features(self.root)}

    def tearDown(self):
        self.tmp.cleanup()

    def test_only_posts_inside_the_window_are_listed(self):
        self.assertEqual(sorted(self.rows), ["demo", "early-slot", "first", "late-slot", "second"])

    def test_kind_news_series_and_content_type(self):
        self.assertEqual(self.rows["demo"]["kind"], "flagship")
        self.assertEqual(self.rows["first"]["news"], "1")
        self.assertEqual(self.rows["demo"]["news"], "0")
        self.assertEqual(self.rows["demo"]["content_type"], "demo")
        self.assertEqual(self.rows["early-slot"]["content_type"], "code")
        self.assertEqual(self.rows["first"]["content_type"], "commentary")
        self.assertEqual(self.rows["late-slot"]["series_order"], "3")
        self.assertEqual(self.rows["demo"]["series_order"], "")

    def test_a_planned_double_has_a_second_slot_at_its_planned_hour(self):
        self.assertEqual((self.rows["early-slot"]["slot"], self.rows["early-slot"]["planned_hour"]), ("1", "8"))
        self.assertEqual((self.rows["late-slot"]["slot"], self.rows["late-slot"]["planned_hour"]), ("2", "16"))
        self.assertEqual(self.rows["late-slot"]["day_posts"], "2")

    def test_a_collision_day_is_not_a_second_slot_and_is_disturbed(self):
        for slug in ("first", "second"):
            self.assertEqual(self.rows[slug]["slot"], "collision")
            self.assertEqual(self.rows[slug]["planned_hour"], "8")
            self.assertEqual(self.rows[slug]["disturbance"], "invented-collision")
        self.assertEqual(self.rows["demo"]["disturbance"], "")

    def test_gap_days_counts_from_the_previous_post_and_is_zero_on_a_double_day(self):
        self.assertEqual(self.rows["demo"]["gap_days"], "2")
        self.assertEqual(self.rows["late-slot"]["gap_days"], "0")

    def test_topic_group_uses_the_tags(self):
        self.assertEqual(self.rows["second"]["topic_group"], "qt")
        self.assertEqual(self.rows["demo"]["topic_group"], "reflection")

    def test_counts_for_the_report_header(self):
        counts = sa.summarise(list(self.rows.values()))
        self.assertEqual(counts, {"posts": 5, "flagship": 1, "short": 4, "double_days": 2, "disturbed": 2})


class CardAtSendTime(unittest.TestCase):
    def test_the_headline_is_the_version_that_was_current_when_the_post_went_out(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build_repo(root)
            # Three versions, with the one that was current on the post's day in the middle, so that
            # neither "first version" nor "latest version" can pass by accident.
            card(root, "demo", "Draft headline", "Draft caption.", date="2026-08-20T08:00:00Z")
            card(root, "demo", "Sent headline with 40 years", "First sentence. Second sentence.",
                 date="2026-09-03T08:00:00Z")
            card(root, "demo", "Later headline", "Edited caption.", date="2026-10-20T08:00:00Z")
            row = {r["slug"]: r for r in features(root)}["demo"]
            self.assertEqual(row["card_h1"], "Sent headline with 40 years")
            self.assertEqual(row["lead"], "First sentence.")
            self.assertEqual((row["h1_number_candidate"], row["lead_number_candidate"]), ("1", "0"))

    def test_a_post_without_a_card_has_empty_text_columns(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build_repo(root)
            row = {r["slug"]: r for r in features(root)}["first"]
            self.assertEqual((row["card_h1"], row["lead"], row["caption_words"]), ("", "", ""))


class PreRegistration(unittest.TestCase):
    """docs/analytics.md fixes the thresholds before any export is opened; the script must use the same ones."""

    BLOCK = re.compile(r"<!-- preregistration:start -->\n(.*?)\n<!-- preregistration:end -->", re.DOTALL)

    def registered(self):
        text = (SCRIPTS.parent / "docs" / "analytics.md").read_text()
        match = self.BLOCK.search(text)
        self.assertIsNotNone(match, "the registered-values block is missing from docs/analytics.md")
        pairs = (line.split(" = ", 1) for line in match.group(1).splitlines() if " = " in line)
        return {name: value for name, value in pairs}

    def test_every_registered_threshold_equals_the_constant_in_the_script(self):
        registered = self.registered()
        constants = {k: v for k, v in vars(sa).items() if k.isupper() and isinstance(v, (int, float, str))}
        thresholds = {k: v for k, v in registered.items() if not re.fullmatch(r"H\d", k)}
        self.assertTrue(thresholds)
        for name, text in thresholds.items():
            with self.subTest(name=name):
                self.assertIn(name, constants, f"{name} is registered but the script has no such constant")
                self.assertEqual(str(constants[name]), text)

    def test_the_primary_metrics_are_the_registered_ones(self):
        registered = self.registered()
        self.assertEqual({k: v for k, v in registered.items() if re.fullmatch(r"H\d", k)}, sa.PRIMARY_METRICS)

    def test_the_script_has_no_tunable_threshold_that_is_not_registered(self):
        registered = set(self.registered())
        tunables = {"MATURITY_DAYS", "MIN_GROUP", "EFFECT_RATIO", "OUTLIER_MULTIPLE", "TREND_DAYS", "FIRST_DAYS",
                    "SPLIT_DATE", "MIN_PER_HALF", "AGREEMENT_MIN", "COVERAGE_MIN", "PREFIX_CHARS", "SLACK_DAYS",
                    "FUZZY_MIN"}
        self.assertEqual(tunables - registered, set())
        self.assertTrue(all(hasattr(sa, name) for name in tunables))


class OutputGuard(unittest.TestCase):
    def run_features(self, root, out):
        sink = io.StringIO()
        with contextlib.redirect_stdout(sink), contextlib.redirect_stderr(sink):
            code = sa.main(["features", "--root", str(root), "--window", "2026-09-01:2026-09-30",
                            "--out", str(out)])
        return code, sink.getvalue()

    def test_refuses_to_write_into_a_directory_git_does_not_ignore(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build_repo(root)
            code, _ = self.run_features(root, root / ".notes" / "analytics" / "t")
            self.assertEqual(code, sa.EXIT_NOT_IGNORED)
            self.assertFalse((root / ".notes").exists())

    def test_the_guard_checks_the_checkout_that_holds_the_target_not_the_one_in_root(self):
        with tempfile.TemporaryDirectory() as tmp_a, tempfile.TemporaryDirectory() as tmp_b:
            root, other = Path(tmp_a), Path(tmp_b)
            build_repo(root)
            (root / ".gitignore").write_text(".notes/\n")   # root ignores it, the other checkout does not
            subprocess.run(["git", "init", "-q"], cwd=other, check=True)
            code, _ = self.run_features(root, other / ".notes" / "analytics" / "t")
            self.assertEqual(code, sa.EXIT_NOT_IGNORED)
            self.assertFalse((other / ".notes").exists())

    def test_a_directory_outside_every_repository_is_allowed(self):
        with tempfile.TemporaryDirectory() as tmp_a, tempfile.TemporaryDirectory() as tmp_b:
            root = Path(tmp_a)
            build_repo(root)
            code, text = self.run_features(root, Path(tmp_b) / "out")
            self.assertEqual(code, 0, text)

    def test_writes_features_and_a_label_template_when_the_directory_is_ignored(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build_repo(root)
            (root / ".gitignore").write_text(".notes/\n")
            out = root / ".notes" / "analytics" / "t"
            code, text = self.run_features(root, out)
            self.assertEqual(code, 0, text)
            self.assertTrue((out / "features.csv").exists())
            self.assertTrue((out / "labels.csv").exists())
            self.assertIn("posts=5", text)

    def test_existing_labels_are_never_overwritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build_repo(root)
            (root / ".gitignore").write_text(".notes/\n")
            out = root / ".notes" / "analytics" / "t"
            self.run_features(root, out)
            labels = out / "labels.csv"
            header, *rows = labels.read_text().splitlines()
            filled = [r.replace(",,,,", ",x,y,z,n") for r in rows]
            labels.write_text("\n".join([header, *filled]) + "\n")
            self.run_features(root, out)
            self.assertEqual(labels.read_text().splitlines()[1:], filled)


if __name__ == "__main__":
    unittest.main()
