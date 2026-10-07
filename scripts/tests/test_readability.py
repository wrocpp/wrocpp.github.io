"""Tests for the readability tooling (stdlib unittest): python3 -m unittest discover -s scripts/tests"""

import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent
REPO = SCRIPTS.parent
FIXTURES = Path(__file__).resolve().parent / "fixtures"


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / filename)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


report = load("readability_report", "readability-report.py")
lint = load("prose_lint", "prose-lint.py")


def run_lint(fixture):
    return subprocess.run([sys.executable, str(SCRIPTS / "prose-lint.py"), "--file", str(FIXTURES / fixture)],
                          capture_output=True, text=True, cwd=REPO)


class ReportMetrics(unittest.TestCase):
    def metrics(self, text):
        return report.analyze(text)[0]

    def test_spans_counted_as_one_word_each_and_excluded_from_prose_words(self):
        m = self.metrics("Use `a` and `b` here.\n")
        self.assertEqual((m["spans"], m["words"], m["sentences"]), (2, 3, 1))

    def test_fenced_code_and_embeds_are_not_prose(self):
        m = self.metrics('Text one.\n\n```cpp\nint x = 1;\n```\n\n<GodboltEmbed id="x" />\n\nText two.\n')
        self.assertEqual((m["words"], m["max_prose_run"]), (4, 1))

    def test_link_keeps_text_and_drops_url(self):
        m = self.metrics("See [the draft paper](https://example.com/p1.pdf) today.\n")
        self.assertEqual(m["words"], 5)

    def test_run_resets_on_heading_list_and_table(self):
        text = "A.\n\nB.\n\nC.\n\n- item\n\nD.\n\n## H\n\nE.\n"
        self.assertEqual(self.metrics(text)["max_prose_run"], 3)

    def test_in_short_requires_first_section(self):
        self.assertEqual(self.metrics("## In short\n\n- a\n\n## Next\n\nText.\n")["in_short"], 1)
        self.assertEqual(self.metrics("Lead one.\n\nLead two.\n\n## In short\n\n- a\n")["in_short"], 0)

    def test_fog_ignores_capitalised_and_hyphenated_words(self):
        plain = self.metrics("The extraordinary compilation proceeds.\n")["fog"]
        capped = self.metrics("The Extraordinary Compilation proceeds.\n")["fog"]
        hyph = self.metrics("The extra-ordinary compile-time proceeds.\n")["fog"]
        self.assertGreater(plain, capped)
        self.assertGreater(plain, hyph)


class LintFixtures(unittest.TestCase):
    def test_dense_fixture_fails_with_code_density_and_sentence_length(self):
        r = run_lint("dense.mdx")
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("code-density", r.stdout)
        self.assertIn("sentence-length", r.stdout)

    def test_clean_fixture_passes_without_readability_findings(self):
        r = run_lint("clean.mdx")
        self.assertEqual(r.returncode, 0, r.stdout)
        for tell in ("code-density", "sentence-length", "paragraph", "prose-run", "section-length"):
            self.assertNotIn(tell, r.stdout)

    def test_five_prose_paragraphs_in_a_row_warn(self):
        text = "---\nslug: x-run\n---\n\n" + "\n\n".join("Short one." for _ in range(5)) + "\n"
        tells = [m.split(":")[0] for _, m in lint.readability_issues(text, baseline={})]
        self.assertIn("prose-run", tells)

    def test_baseline_only_flags_worse_posts(self):
        dense = (FIXTURES / "dense.mdx").read_text()
        metrics, _ = report.analyze(dense)
        same = {"dense-fixture": metrics}
        self.assertEqual(lint.readability_issues(dense, baseline=same), [])
        better = {"dense-fixture": dict(metrics, n_over35=metrics["n_over35"] + 1,
                                        n_sent_spans_gt4=metrics["n_sent_spans_gt4"] + 1,
                                        n_over25=metrics["n_over25"] + 1,
                                        n_sent_spans_gt2=metrics["n_sent_spans_gt2"] + 1,
                                        dense_excess=metrics["dense_excess"] + 1)}
        self.assertEqual(lint.readability_issues(dense, baseline=better), [])
        worse = {"dense-fixture": dict(metrics, n_over35=0, n_sent_spans_gt4=0)}
        levels = {lv for lv, _ in lint.readability_issues(dense, baseline=worse)}
        self.assertEqual(levels, {"ERROR"})

    def test_checked_in_baseline_keeps_the_corpus_green(self):
        baseline = report.load_baseline()
        for path in report.all_posts():
            issues = lint.readability_issues(path.read_text(encoding="utf-8"), baseline=baseline)
            self.assertEqual(issues, [], path.name)


if __name__ == "__main__":
    unittest.main()
