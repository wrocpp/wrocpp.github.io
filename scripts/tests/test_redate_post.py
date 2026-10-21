"""Tests for scripts/redate_post.py (stdlib unittest): python3 -m unittest discover -s scripts/tests"""

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("redate_post", SCRIPTS / "redate_post.py")
redate = importlib.util.module_from_spec(spec)
sys.modules["redate_post"] = redate
spec.loader.exec_module(redate)

OLD, NEW = "2026-10-22", "2026-10-23"
CAPTION = "# t\n\n## Suggested post time\nThursday 2026-10-22, 10:00 CET\nReason: x.\n"


def build(root, card_date=OLD, caption=CAPTION):
    (root / "src/content/posts").mkdir(parents=True)
    (root / "public/og").mkdir(parents=True)
    (root / f"src/content/posts/{OLD}-demo.mdx").write_text(f"---\ntitle: t\npubDate: {OLD}\n---\nbody\n")
    for platform in redate.PLATFORMS:
        card = root / "social" / platform / "demo"
        card.mkdir(parents=True)
        (card / "config.yaml").write_text(f'project:\n  date: "{card_date}"\n')
        (card / "content.md").write_text(f'::::insight{{citation="wro.cpp -- {card_date}"}}\n')
        (card / "index.html").write_text(f"<div>wro.cpp -- {card_date}</div>\n")
        (card / "caption.md").write_text(caption)
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    subprocess.run(["git", "add", "-A"], cwd=root, check=True)


class RedatePost(unittest.TestCase):
    def run_it(self, root, *extra):
        return redate.main(["--slug", "demo", "--to", NEW, "--root", str(root), "--no-render", *extra])

    def test_moves_the_file_and_every_date(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build(root)
            self.assertEqual(self.run_it(root), 0)
            self.assertFalse((root / f"src/content/posts/{OLD}-demo.mdx").exists())
            self.assertIn(f"pubDate: {NEW}", (root / f"src/content/posts/{NEW}-demo.mdx").read_text())
            for platform in redate.PLATFORMS:
                card = root / "social" / platform / "demo"
                for name in ("config.yaml", "content.md", "index.html"):
                    text = (card / name).read_text()
                    self.assertIn(NEW, text)
                    self.assertNotIn(OLD, text)
                self.assertIn("Friday 2026-10-23, 10:00 CET", (card / "caption.md").read_text())

    def test_dry_run_changes_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build(root)
            self.assertEqual(self.run_it(root, "--dry-run"), 0)
            self.assertTrue((root / f"src/content/posts/{OLD}-demo.mdx").exists())
            self.assertIn(OLD, (root / "social/linkedin/demo/config.yaml").read_text())

    def test_a_card_with_another_date_is_left_alone(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build(root, card_date="2026-09-05")
            self.run_it(root)
            self.assertIn("2026-09-05", (root / "social/linkedin/demo/index.html").read_text())
            self.assertNotIn(NEW, (root / "social/linkedin/demo/index.html").read_text())

    def test_a_caption_naming_another_day_is_left_alone(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            other = CAPTION.replace(OLD, "2026-09-05")
            build(root, caption=other)
            self.run_it(root)
            self.assertEqual((root / "social/linkedin/demo/caption.md").read_text(), other)

    def test_refuses_a_pubdate_that_disagrees_with_the_file_name(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build(root)
            path = root / f"src/content/posts/{OLD}-demo.mdx"
            path.write_text(path.read_text().replace(f"pubDate: {OLD}", "pubDate: 2026-10-21"))
            with self.assertRaises(SystemExit):
                self.run_it(root)

    def test_weekday_in_the_caption_follows_the_new_day(self):
        self.assertEqual(redate.weekday("2026-10-25"), "Sunday")
        self.assertEqual(redate.retime_caption(CAPTION, OLD, "2026-10-25").split("\n")[3], "Sunday 2026-10-25, 10:00 CET")


if __name__ == "__main__":
    unittest.main()
