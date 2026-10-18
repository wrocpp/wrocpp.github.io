"""Tests for scripts/news-radar/coverage.py (stdlib unittest, hermetic: posts live in a temp dir)."""

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent


def load():
    spec = importlib.util.spec_from_file_location("news_radar_coverage", SCRIPTS / "news-radar" / "coverage.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["news_radar_coverage"] = mod
    spec.loader.exec_module(mod)
    return mod


coverage = load()

LIVE = '---\ntitle: "Live"\nslug: "live-post"\npubDate: 2026-10-01\ndraft: false\n---\nBody mentions P2287R6 and Búzios and std::hive.\n'
DRAFT = '---\ntitle: "Draft"\nslug: "draft-post"\npubDate: 2026-10-02\ndraft: true\n---\nBody mentions P3533R2.\n'
NODRAFTKEY = '---\ntitle: "No key"\nslug: "no-key-post"\npubDate: 2026-10-03\n---\nBody.\n'


class CoverageTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        d = Path(self.tmp.name)
        (d / "2026-10-01-live-post.mdx").write_text(LIVE, encoding="utf-8")
        (d / "2026-10-02-draft-post.mdx").write_text(DRAFT, encoding="utf-8")
        (d / "2026-10-03-no-key-post.mdx").write_text(NODRAFTKEY, encoding="utf-8")
        self.posts = coverage.load_posts(d)

    def tearDown(self):
        self.tmp.cleanup()

    def test_draft_posts_do_not_count_as_published(self):
        self.assertEqual(sorted(p.slug for p in self.posts if p.published), ["live-post", "no-key-post"])

    def test_expect_slug_passes_for_a_published_post(self):
        self.assertEqual(coverage.missing_slugs(self.posts, ["live-post"]), [])

    def test_expect_slug_fails_for_a_draft_and_for_an_unknown_slug(self):
        self.assertEqual(coverage.missing_slugs(self.posts, ["draft-post", "nope"]), ["draft-post", "nope"])

    def test_pattern_is_extended_regex_not_basic(self):
        # "\|" in an ERE is a literal pipe; alternation is a bare "|".
        self.assertEqual([p.slug for p in coverage.matching(self.posts, r"P2287|P9999")], ["live-post"])
        self.assertEqual(coverage.matching(self.posts, r"P2287\|P9999"), [])

    def test_matching_ignores_drafts_and_handles_non_ascii(self):
        self.assertEqual(coverage.matching(self.posts, "P3533"), [])
        self.assertEqual([p.slug for p in coverage.matching(self.posts, "Búzios")], ["live-post"])

    def test_topic_table_maps_each_topic_to_its_matching_posts(self):
        table = dict(coverage.topic_table(self.posts, {"hive": r"std::hive"}))
        self.assertEqual([p.slug for p in table["hive"]], ["live-post"])


if __name__ == "__main__":
    unittest.main()
