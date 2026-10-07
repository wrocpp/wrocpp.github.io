"""Tests for scripts/check-rewrite-invariants.py (stdlib unittest)."""

import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "check-rewrite-invariants.py"
FIXTURES = Path(__file__).resolve().parent / "fixtures"
spec = importlib.util.spec_from_file_location("check_rewrite_invariants", SCRIPT)
inv = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = inv
spec.loader.exec_module(inv)


def cli(new_fixture):
    return subprocess.run([sys.executable, str(SCRIPT), "-", "--base-file", str(FIXTURES / "invariants_base.mdx"),
                           "--file", str(FIXTURES / new_fixture)], capture_output=True, text=True)


def read(name):
    return (FIXTURES / name).read_text(encoding="utf-8")


class Invariants(unittest.TestCase):
    def test_wording_only_change_passes(self):
        r = cli("invariants_wording.mdx")
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("invariants: hold", r.stdout)

    def test_changed_number_fails(self):
        r = cli("invariants_number.mdx")
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("number", r.stdout)

    def test_changed_code_block_fails(self):
        new = read("invariants_base.mdx").replace("char a; long b;", "long b; char a;")
        self.assertTrue(any("fenced code" in p for p in inv.check(read("invariants_base.mdx"), new)))

    def test_changed_component_prop_fails(self):
        new = read("invariants_base.mdx").replace('id="abc123"', 'id="zzz999"')
        self.assertTrue(any("component" in p for p in inv.check(read("invariants_base.mdx"), new)))

    def test_changed_url_fails(self):
        new = read("invariants_base.mdx").replace("wg21.link/p2996", "wg21.link/p1306")
        self.assertTrue(any(p.startswith("url") for p in inv.check(read("invariants_base.mdx"), new)))

    def test_renamed_heading_fails_but_added_heading_passes(self):
        base = read("invariants_base.mdx")
        self.assertTrue(any("heading" in p for p in inv.check(base, base.replace("What it measures", "What is measured"))))
        self.assertEqual(inv.check(base, base.replace("The related post", "## Related\n\nThe related post")), [])

    def test_frontmatter_change_fails_except_summary_and_updated_date(self):
        base = read("invariants_base.mdx")
        self.assertTrue(any("frontmatter title" in p for p in inv.check(base, base.replace('"Invariant fixture"', '"Other"'))))
        self.assertEqual(inv.check(base, read("invariants_wording.mdx")), [])


if __name__ == "__main__":
    unittest.main()
