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

    def test_the_summary_is_read_for_the_labellers(self):
        self.assertEqual(self.rows["demo"]["summary"], "A summary: with a colon.")

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


LI_HEADER = ("Post title,Post link,Post type,Campaign name,Posted by,Created date,Campaign start date,"
             "Campaign end date,Audience,Impressions,Views,Offsite Views,Clicks,Click through rate (CTR),Likes,"
             "Comments,Reposts,Follows,Engagement rate,Content Type")


def li_row(text, link, created, impressions="100", clicks="2", likes="5", comments="0", reposts="0",
           kind="Organic", campaign=""):
    return (f'"{text}",{link},{kind},{campaign},Someone,{created},,,All followers,{impressions},,,{clicks},0.02,'
            f'{likes},{comments},{reposts},0,0.05,')


def write_linkedin(path, rows, header=LI_HEADER):
    path.write_text("\n".join([header, *rows]) + "\n", encoding="utf-8")


def feat(slug, day, lead):
    return {"slug": slug, "date": day, "lead": lead}


class NormaliseText(unittest.TestCase):
    def test_case_accents_punctuation_and_spacing_do_not_matter(self):
        self.assertEqual(sa.normalise_text("  Bu\u0301zios,  GCC-17: \u201cstage 3\u201d!"), "buziosgcc17stage3")


class ReadLinkedIn(unittest.TestCase):
    def test_reads_numbers_and_converts_the_date(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "posts.csv"
            write_linkedin(path, [li_row("Hello world", "https://l/1", "10/27/2026", impressions="184", comments="3")])
            row = sa.read_linkedin_posts(path)[0]
            self.assertEqual((row["created"], row["impressions"], row["comments"]), ("2026-10-27", 184, 3))

    def test_a_missing_required_column_is_named(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "posts.csv"
            write_linkedin(path, [], header=LI_HEADER.replace("Impressions,", "Impr,"))
            with self.assertRaises(sa.ExportError) as ctx:
                sa.read_linkedin_posts(path)
            self.assertIn("Impressions", str(ctx.exception))

    def test_a_sponsored_row_is_refused_because_the_review_is_organic_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "posts.csv"
            write_linkedin(path, [li_row("Ad", "https://l/2", "10/27/2026", kind="Sponsored", campaign="X")])
            with self.assertRaises(sa.ExportError):
                sa.read_linkedin_posts(path)


class JoinPosts(unittest.TestCase):
    FEATS = [
        feat("contracts", "2026-10-27", "Pavel wrote that contracts are glorified assertions, and listed what would help."),
        feat("ballot", "2026-10-27", "The 12-week ISO ballot on C++26 concluded on 22 October."),
        feat("old", "2026-10-01", "An unrelated post from another month about enums and flags in C++."),
    ]

    def li(self, text, link, created, impressions=100):
        return {"text": text, "link": link, "created": created, "impressions": impressions}

    def test_a_row_whose_text_starts_with_the_caption_lead_matches_by_prefix(self):
        out = sa.join_posts([self.li("Pavel wrote that contracts are glorified assertions, and listed what would help. More.",
                                     "l1", "2026-10-27")], self.FEATS, {})
        self.assertEqual((out.rows[0]["slug"], out.rows[0]["method"]), ("contracts", "prefix"))

    def test_the_same_text_on_a_far_away_date_does_not_match(self):
        out = sa.join_posts([self.li("An unrelated post from another month about enums and flags in C++. Tail.",
                                     "l1", "2026-10-27")], self.FEATS, {})
        self.assertEqual(out.rows[0]["slug"], "")
        self.assertEqual(len(out.unresolved), 1)

    def test_punctuation_changes_still_match_by_prefix_and_a_word_inserted_matches_fuzzily(self):
        edited = "Pavel wrote that contracts are glorified assertions and listed what would help"
        out = sa.join_posts([self.li(edited.replace("glorified", "glorified-"), "l1", "2026-10-27")], self.FEATS, {})
        self.assertEqual((out.rows[0]["slug"], out.rows[0]["method"]), ("contracts", "prefix"))
        edited = "Pavel wrote that contracts are only glorified assertions, and listed what would help. Tail."
        out = sa.join_posts([self.li(edited, "l2", "2026-10-27")], self.FEATS, {})
        self.assertEqual((out.rows[0]["slug"], out.rows[0]["method"]), ("contracts", "fuzzy"))

    def test_an_override_classifies_a_row_that_is_not_a_blog_post(self):
        out = sa.join_posts([self.li("Leonardo, the write-up is up: https://lnkd.in/x", "l9", "2026-10-27")],
                            self.FEATS, {"l9": "non-blog:reply to a commenter"})
        self.assertEqual(out.rows[0]["method"], "non-blog")
        self.assertEqual(out.unresolved, [])

    def test_two_rows_for_one_post_are_flagged_as_multi_send(self):
        text = "The 12-week ISO ballot on C++26 concluded on 22 October. Text."
        out = sa.join_posts([self.li(text, "l1", "2026-10-27"), self.li(text, "l2", "2026-10-27")], self.FEATS, {})
        self.assertEqual([r["multi_send"] for r in out.rows], ["1", "1"])

    def test_coverage_is_the_matched_share_of_impressions_and_excludes_classified_non_blog_rows(self):
        rows = [self.li("Pavel wrote that contracts are glorified assertions, and listed what would help.", "l1", "2026-10-27", 900),
                self.li("Something nobody can place at all", "l2", "2026-10-26", 100),
                self.li("Leonardo, the write-up is up", "l3", "2026-10-21", 5000)]
        out = sa.join_posts(rows, self.FEATS, {"l3": "non-blog:reply"})
        self.assertAlmostEqual(out.coverage, 0.9)
        self.assertEqual([r["link"] for r in out.unresolved], ["l2"])

    def test_a_short_first_sentence_matches_through_the_longer_caption_start(self):
        feats = [{"slug": "short", "date": "2026-10-20", "lead": "Why can you write this?",
                  "caption_head": 'Why can you write this? match<"x">(s) A string template parameter makes the pattern part of the type.'}]
        text = "Why can you write this?\n\n  match<\"x\">(s)\n\nA string template parameter makes the pattern part of the type."
        out = sa.join_posts([self.li(text, "l1", "2026-10-20")], feats, {})
        self.assertEqual((out.rows[0]["slug"], out.rows[0]["method"]), ("short", "prefix"))

    def test_a_short_lead_without_a_caption_start_is_too_generic_to_match(self):
        feats = [{"slug": "short", "date": "2026-10-20", "lead": "Why can you write this?"}]
        out = sa.join_posts([self.li("Why can you write this? A string template.", "l1", "2026-10-20")], feats, {})
        self.assertEqual(out.rows[0]["slug"], "")

    def test_a_post_sent_on_another_day_than_its_pubdate_is_flagged_as_redated(self):
        lead = "Pavel wrote that contracts are glorified assertions, and listed what would help."
        same = sa.join_posts([self.li(lead, "l1", "2026-10-27")], self.FEATS, {})
        moved = sa.join_posts([self.li(lead, "l1", "2026-10-29")], self.FEATS, {})
        self.assertEqual((same.rows[0]["redated"], moved.rows[0]["redated"]), ("0", "1"))

    def test_blog_posts_with_no_linkedin_row_are_listed_and_not_counted_as_zero(self):
        out = sa.join_posts([self.li("Pavel wrote that contracts are glorified assertions, and listed what would help.",
                                     "l1", "2026-10-27")], self.FEATS, {})
        self.assertEqual(sorted(out.unadvertised), ["ballot", "old"])


class JoinCommand(unittest.TestCase):
    def prepare(self, root):
        build_repo(root)
        (root / ".gitignore").write_text(".notes/\n")
        out = root / ".notes" / "analytics" / "t"
        out.mkdir(parents=True)
        with contextlib.redirect_stdout(io.StringIO()):
            sa.main(["features", "--root", str(root), "--window", "2026-09-01:2026-09-30", "--out", str(out)])
        return out

    def run_join(self, root, out, *extra):
        sink = io.StringIO()
        with contextlib.redirect_stdout(sink), contextlib.redirect_stderr(sink):
            code = sa.main(["join", "--dir", str(out), *extra])
        return code, sink.getvalue()

    def test_exit_2_and_a_loud_list_when_a_row_cannot_be_placed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            out = self.prepare(root)
            write_linkedin(out / "linkedin-posts.csv", [li_row("Nothing matches this text at all", "https://l/9", "09/03/2026")])
            code, text = self.run_join(root, out)
            self.assertEqual(code, sa.EXIT_UNRESOLVED)
            self.assertIn("https://l/9", text)

    def test_allow_unmatched_still_writes_the_files_and_stamps_the_report_incomplete(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            out = self.prepare(root)
            write_linkedin(out / "linkedin-posts.csv", [li_row("Nothing matches this text at all", "https://l/9", "09/03/2026")])
            code, text = self.run_join(root, out, "--allow-unmatched")
            self.assertEqual(code, 0, text)
            self.assertIn("INCOMPLETE", text)
            self.assertTrue((out / "joined.csv").exists())

    def test_refuses_to_write_next_to_data_in_a_directory_git_does_not_ignore(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build_repo(root)
            out = root / "analytics"
            out.mkdir()
            write_linkedin(out / "linkedin-posts.csv", [])
            code, _ = self.run_join(root, out)
            self.assertEqual(code, sa.EXIT_NOT_IGNORED)


def rec(day, value, impressions=1000, comments=0, reposts=0, **extra):
    """An invented comparable post for the statistics tests."""
    return {"sent": day, "imp_index": value, "impressions": impressions, "comments": comments, "reposts": reposts,
            "site_per_1000": value, **extra}


def run_of(day_numbers, value, start="2026-08-01"):
    base = sa.date.fromisoformat(start)
    return [rec((base + sa.timedelta(days=n)).isoformat(), value) for n in day_numbers]


class Statistics(unittest.TestCase):
    def test_median_and_quartiles(self):
        self.assertEqual(sa.median([3, 1, 2]), 2)
        self.assertEqual(sa.median([4, 1, 3, 2]), 2.5)
        self.assertEqual(sa.quartiles([1, 2, 3, 4, 5, 6, 7, 8]), (2.5, 6.5))

    def test_pooled_rate_is_comments_plus_reposts_per_thousand_impressions(self):
        rows = [rec("2026-08-01", 1, impressions=1000, comments=2, reposts=1),
                rec("2026-08-02", 1, impressions=3000, comments=0, reposts=0)]
        self.assertAlmostEqual(sa.comment_repost_rate(rows), 0.75)

    def test_imp_index_divides_by_the_median_of_the_neighbours_within_the_trend_window(self):
        pool = [rec("2026-09-10", None, impressions=100), rec("2026-09-11", None, impressions=300),
                rec("2026-09-12", None, impressions=600), rec("2026-09-30", None, impressions=9999)]
        self.assertAlmostEqual(sa.imp_index(pool[1], pool), 300 / sa.median([100, 600]))

    def test_a_post_with_no_neighbour_has_no_index(self):
        lone = rec("2026-09-10", None, impressions=100)
        self.assertIsNone(sa.imp_index(lone, [lone, rec("2026-12-31", None)]))


class Verdict(unittest.TestCase):
    """The registered rule: group sizes, effect ratio, drop the best post, both halves, and the placebo."""

    def judge(self, a, b):
        return sa.judge(a, b, sa.median_of("imp_index"), a + b)

    def spread(self, n, value, start="2026-08-01", step=2):
        return run_of([i * step for i in range(n)], value, start)

    def test_a_group_below_the_minimum_gives_too_little_data_whatever_the_ratio(self):
        out = self.judge(self.spread(sa.MIN_GROUP - 1, 3.0), self.spread(40, 1.0))
        self.assertEqual(out["verdict"], "too little data")

    def test_a_clear_and_stable_effect_is_supported(self):
        a = run_of(range(0, 60, 3), 1.6)           # both sides of 2026-09-13
        b = run_of(range(1, 60, 3), 1.0) + run_of(range(2, 60, 3), 1.0)
        out = self.judge(a, b)
        self.assertEqual(out["verdict"], "supported", out)
        self.assertAlmostEqual(out["ratio"], 1.6)

    def test_an_effect_below_the_registered_ratio_is_not_supported(self):
        a = run_of(range(0, 60, 3), 1.3)
        b = run_of(range(1, 60, 3), 1.0) + run_of(range(2, 60, 3), 1.0)
        self.assertEqual(self.judge(a, b)["verdict"], "too little data")

    def test_an_effect_that_flips_in_one_half_is_not_supported(self):
        early = run_of(range(0, 40, 3), 2.5)        # before 2026-09-13
        late = run_of(range(43, 75, 3), 0.7)        # after it
        b = run_of(range(1, 75, 3), 1.0) + run_of(range(2, 75, 3), 1.0)
        out = self.judge(early + late, b)
        self.assertNotEqual(out["verdict"], "supported", out)

    def test_the_best_post_of_a_is_dropped_by_the_registered_robustness_check(self):
        rows = [rec("2026-08-01", 1.0), rec("2026-08-02", 9.0), rec("2026-08-03", 2.0)]
        kept = sa.without_best(rows, sa.median_of("imp_index"))
        self.assertEqual(sorted(r["imp_index"] for r in kept), [1.0, 2.0])
        out = self.judge(run_of(range(0, 60, 3), 1.6), run_of(range(1, 60, 3), 1.0) + run_of(range(2, 60, 3), 1.0))
        self.assertAlmostEqual(out["ratio_without_best"], 1.6)

    def test_a_ratio_that_only_equals_the_placebo_ratio_is_not_supported(self):
        # The value depends only on the parity of the calendar day: 1.7 on even days, 1.0 on odd days. A sits on
        # even days only and B mostly on odd days, so A/B = 1.7, but the even/odd placebo ratio is also 1.7.
        base = sa.date.fromisoformat("2026-08-01")
        days = [base + sa.timedelta(days=n) for n in range(0, 89)]
        even = [d for d in days if d.toordinal() % 2 == 0]
        odd = [d for d in days if d.toordinal() % 2 == 1]
        value = lambda d: 1.7 if d.toordinal() % 2 == 0 else 1.0
        a = [rec(d.isoformat(), value(d)) for d in even[::2][:20]]
        b = [rec(d.isoformat(), value(d)) for d in odd[:30] + even[1::2][:10]]
        out = self.judge(a, b)
        self.assertAlmostEqual(out["ratio"], 1.7)
        self.assertAlmostEqual(out["noise_floor"], 1.7)
        self.assertNotEqual(out["verdict"], "supported", out)

    def test_a_group_that_is_not_better_in_the_whole_window_and_either_half_is_contradicted(self):
        a = run_of(range(0, 60, 3), 0.8)
        b = run_of(range(1, 60, 3), 1.0) + run_of(range(2, 60, 3), 1.0)
        self.assertEqual(self.judge(a, b)["verdict"], "contradicted")

    def test_not_better_overall_but_better_in_one_half_is_not_called_contradicted(self):
        early = run_of(range(0, 36, 6), 1.4)         # 6 posts before 2026-09-13: A ahead
        late = run_of(range(43, 80, 3), 0.4)         # after it: A far behind, so the whole window is below 1
        b = run_of(range(1, 80, 3), 1.0) + run_of(range(2, 80, 3), 1.0)
        out = self.judge(early + late, b)
        self.assertLessEqual(out["ratio"], 1.0, out)
        self.assertGreater(out["ratio_early"], 1.0, out)
        self.assertEqual(out["verdict"], "too little data")

    def test_a_group_with_too_few_posts_on_one_side_of_the_split_is_undecided_even_if_both_sides_look_good(self):
        early = run_of(range(0, 36, 4), 1.8)         # 9 posts before 2026-09-13
        late = run_of([45, 55, 65], 1.8)             # only 3 after it, fewer than MIN_PER_HALF
        b = run_of(range(1, 80, 3), 1.0) + run_of(range(2, 80, 3), 1.0)
        out = self.judge(early + late, b)
        self.assertGreater(out["ratio_early"], 1.0)
        self.assertGreater(out["ratio_late"], 1.0)
        self.assertEqual((out["halves_ok"], out["verdict"]), (False, "too little data"), out)

    def test_a_pooled_rate_that_rests_on_one_post_is_not_supported(self):
        # B: 1 comment per 1,000 impressions. A: one post with 20 comments carries the early half; the late half
        # is only just above B. Overall 2.6x, but without that one post A is below B.
        def post(day, comments):
            return rec(day, 1.0, impressions=1000, comments=comments)
        a = ([post(d, c) for d, c in zip(("2026-08-02", "2026-08-05", "2026-08-08", "2026-08-11", "2026-08-14"), (20, 0, 0, 0, 0))]
             + [post(d, c) for d, c in zip(("2026-09-20", "2026-09-23", "2026-09-26", "2026-09-29", "2026-10-02"), (6, 0, 0, 0, 0))])
        b = [post(d, 1) for d in [x["sent"] for x in run_of(range(1, 80, 2), 1.0)]]
        out = sa.judge(a, b, sa.comment_repost_rate, a + b)
        self.assertGreaterEqual(out["ratio"], sa.EFFECT_RATIO)
        self.assertGreater(out["ratio_early"], 1.0)
        self.assertGreater(out["ratio_late"], 1.0)
        self.assertLessEqual(out["ratio_without_best"], 1.0)
        self.assertNotEqual(out["verdict"], "supported", out)

    def test_the_noise_floor_is_symmetric_whichever_parity_is_higher(self):
        base = sa.date.fromisoformat("2026-08-01")
        pool = [rec((base + sa.timedelta(days=n)).isoformat(), 1.7 if (base + sa.timedelta(days=n)).toordinal() % 2 else 1.0)
                for n in range(0, 60)]
        self.assertAlmostEqual(sa.noise_floor(sa.median_of("imp_index"), pool), 1.7)

    def test_too_few_posts_on_one_side_of_the_split_leaves_it_undecided(self):
        a = run_of(range(0, 30, 2), 1.8)            # every A post is before 2026-09-13
        b = run_of(range(1, 60, 3), 1.0) + run_of(range(2, 60, 3), 1.0)
        self.assertEqual(self.judge(a, b)["verdict"], "too little data")


class Groups(unittest.TestCase):
    def post(self, **kw):
        base = {"news": "0", "content_type": "commentary", "hook_number": "no", "hook_reframe": "no",
                "person_role": "none"}
        return {**base, **kw}

    def test_each_hypothesis_puts_a_post_in_a_or_b_by_its_registered_definition(self):
        h1, h2, h3, h4 = (sa.HYPOTHESES[k]["in_a"] for k in ("H1", "H2", "H3", "H4"))
        self.assertTrue(h1(self.post(hook_number="yes")) and h1(self.post(hook_reframe="yes")))
        self.assertFalse(h1(self.post()))
        self.assertTrue(h2(self.post(news="1")) and not h2(self.post()))
        self.assertTrue(h3(self.post(person_role="answer")) and h3(self.post(person_role="credit")))
        self.assertFalse(h3(self.post()))
        self.assertTrue(h4(self.post(content_type="demo")))
        self.assertFalse(h4(self.post(content_type="code")) or h4(self.post(content_type="commentary")))


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
