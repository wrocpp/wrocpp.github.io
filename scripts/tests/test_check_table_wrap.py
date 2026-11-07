"""Tests for scripts/check-table-wrap.py (stdlib unittest): python3 -m unittest discover -s scripts/tests"""

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("check_table_wrap", SCRIPTS / "check-table-wrap.py")
gate = importlib.util.module_from_spec(spec)
sys.modules["check_table_wrap"] = gate
spec.loader.exec_module(gate)

TABLE = "<table><tr><td>x</td></tr></table>"


def page(body):
    return f"<html><body><article class=\"prose\">{body}</article></body></html>"


class UncontainedTables(unittest.TestCase):
    def test_a_bare_table_under_prose_is_reported(self):
        self.assertEqual(len(gate.uncontained_tables(page(TABLE))), 1)

    def test_a_table_inside_table_wrap_passes(self):
        self.assertEqual(gate.uncontained_tables(page(f'<div class="table-wrap">{TABLE}</div>')), [])

    def test_table_scroll_and_table_fit_also_pass(self):
        for name in ("table-scroll", "table-fit table-fit-3col"):
            with self.subTest(name=name):
                self.assertEqual(gate.uncontained_tables(page(f'<div class="{name}">{TABLE}</div>')), [])

    def test_the_container_must_be_the_direct_parent(self):
        nested = f'<div class="table-wrap"><div>{TABLE}</div></div>'
        self.assertEqual(len(gate.uncontained_tables(page(nested))), 1)

    def test_a_class_that_only_contains_the_name_does_not_count(self):
        self.assertEqual(len(gate.uncontained_tables(page(f'<div class="table-wrapper">{TABLE}</div>'))), 1)

    def test_each_offender_in_a_page_is_reported(self):
        wrapped = f'<div class="table-wrap">{TABLE}</div>'
        self.assertEqual(len(gate.uncontained_tables(page(TABLE + wrapped + TABLE))), 2)

    def test_void_elements_do_not_hide_the_parent(self):
        body = f'<div class="table-wrap"><img src="a.png"><br>{TABLE}</div>'
        self.assertEqual(gate.uncontained_tables(page(body)), [])


class CommandLine(unittest.TestCase):
    def run_gate(self, files):
        with tempfile.TemporaryDirectory() as tmp:
            for name, html in files.items():
                path = Path(tmp) / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(html)
            return subprocess.run(
                [sys.executable, str(SCRIPTS / "check-table-wrap.py"), tmp], capture_output=True, text=True
            )

    def test_exit_1_and_the_page_name_when_a_table_is_bare(self):
        result = self.run_gate({"posts/a/index.html": page(TABLE)})
        self.assertEqual(result.returncode, 1)
        self.assertIn("posts/a/index.html", result.stdout)

    def test_exit_0_when_every_table_is_contained(self):
        result = self.run_gate({"posts/a/index.html": page(f'<div class="table-wrap">{TABLE}</div>')})
        self.assertEqual(result.returncode, 0)

    def test_exit_2_for_a_missing_directory(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / "check-table-wrap.py"), "/nonexistent-dir-for-test"],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main()
