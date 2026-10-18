"""Tests for the input checks in scripts/news-radar/probe.py (stdlib unittest, no network)."""

import importlib.util
import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent


def load():
    spec = importlib.util.spec_from_file_location("news_radar_probe", SCRIPTS / "news-radar" / "probe.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["news_radar_probe"] = mod
    spec.loader.exec_module(mod)
    return mod


probe = load()


class ProbeValidationTests(unittest.TestCase):
    def test_accepts_a_normal_request(self):
        probe.validate("gsnapshot", ["boost:191"], ["__cpp_lib_hive"], "int main(){}")

    def test_rejects_a_compiler_id_that_could_change_the_url(self):
        for bad in ("g161 --options=x", "../x", "g161/../../api", "a b", ""):
            with self.assertRaises(SystemExit, msg=bad):
                probe.validate(bad, [], [], "int main(){}")

    def test_rejects_a_malformed_library(self):
        with self.assertRaises(SystemExit):
            probe.validate("g161", ["boost"], [], "int main(){}")

    def test_rejects_a_macro_name_that_is_not_a_feature_test_macro(self):
        with self.assertRaises(SystemExit):
            probe.validate("g161", [], ["__FILE__"], "")

    def test_rejects_code_over_the_size_cap(self):
        with self.assertRaises(SystemExit):
            probe.validate("g161", [], [], "x" * (probe.MAX_CODE_BYTES + 1))

    def test_there_is_no_file_reading_option(self):
        parser_help = (SCRIPTS / "news-radar" / "probe.py").read_text(encoding="utf-8")
        self.assertNotIn("--source", parser_help)
        self.assertNotIn("open(args", parser_help)


if __name__ == "__main__":
    unittest.main()
