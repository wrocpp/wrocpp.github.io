#!/usr/bin/env python3
"""Detect broken social card renders before they ship.

Catches the "giant magnet logo, no CSS" failure mode where Chrome rendered
the index.html without any stylesheet (empty assets/ directory). Also catches
missing image, wrong dimensions, and other structural failures.

Usage:
  scripts/check-social-render.py --slug <slug> [--platform linkedin|facebook|both]
  scripts/check-social-render.py --all                  # check every rendered card

Exit code: 0 = all OK, 1 = at least one ERROR.
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# Bounds tuned to actual file sizes observed in production:
# - Correct cards: 200-420 KB (text + small logo watermark; HTML-styled
#   titles with spans tend to fall in the 300-420 range)
# - Broken "giant logo" cards: 440-460 KB (magnet PNG fills the whole card)
# We pick 430 KB as the hard ceiling: legitimate cards have always come in
# under that, and the broken renders we have seen have always exceeded it.
MIN_PNG_BYTES = 150_000
MAX_PNG_BYTES = 430_000

# wrocpp.css is ~325 lines after inject.sh; if assets/scudoai.css doesn't match,
# inject didn't run or assets are missing. (The default scudoai.css is ~870
# lines and an erroneous append is ~1189, so this band stays well clear of both.)
EXPECTED_CSS_LINES_MIN = 280
EXPECTED_CSS_LINES_MAX = 345

# Logo SVG embedded by brand-gen is ~6KB; less means missing or wrong.
MIN_LOGO_SVG_BYTES = 5_000

# Branding markers that inject.sh patches into the RENDERED index.html.
#
# These have to be checked separately from assets/, because the two live on
# different lifecycles: `brand-gen build` regenerates index.html from scratch
# and drops inject.sh's patches, while assets/ survives untouched from an
# earlier run. So a re-render that skips inject.sh (wrong path, or a swallowed
# error) leaves correct assets next to an index.html with the stock logo and no
# AI badge -- and every asset-based check below still passes. That happened on
# 2026-08-10 and shipped a card with no AI disclosure on it.
#
# MAGNET_VIEWBOX is the viewBox of our magnet logo symbol (brand-kit/
# logo-symbol.svg); the stock brand-gen logo uses the same id but not this box.
MAGNET_VIEWBOX = 'viewBox="0 0 320 320"'
AI_BADGE_MARKER = 'class="ai-badge"'


def red(s: str) -> str:
    return f"\033[31m{s}\033[0m"


def green(s: str) -> str:
    return f"\033[32m{s}\033[0m"


def yellow(s: str) -> str:
    return f"\033[33m{s}\033[0m"


def check_one(platform: str, slug: str) -> list[str]:
    """Return list of issue strings. Empty list = card is healthy."""
    issues = []
    base = REPO / "social" / platform / slug
    label = f"{platform}/{slug}"

    if not base.exists():
        return [f"{red('ERROR')} {label}: directory does not exist"]

    img = base / "image.png"
    if not img.exists():
        issues.append(f"{red('ERROR')} {label}: image.png missing")
        return issues

    # File size sanity (catches the "giant logo no CSS" failure)
    size = img.stat().st_size
    if size > MAX_PNG_BYTES:
        issues.append(
            f"{red('ERROR')} {label}: image.png is {size} bytes (>{MAX_PNG_BYTES}); "
            f"likely the 'no CSS, giant logo' failure -- check assets/ has scudoai.css"
        )
    elif size < MIN_PNG_BYTES:
        issues.append(
            f"{yellow('WARN')}  {label}: image.png is {size} bytes (<{MIN_PNG_BYTES}); "
            f"may be missing content"
        )

    # Dimensions
    try:
        dims = subprocess.run(
            ["identify", "-format", "%wx%h", str(img)],
            capture_output=True, text=True, check=True, timeout=10,
        ).stdout.strip()
        if dims != "2400x2400":
            issues.append(f"{red('ERROR')} {label}: image.png dimensions {dims}, expected 2400x2400")
    except (FileNotFoundError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        issues.append(f"{yellow('WARN')}  {label}: could not run identify ({e})")

    # Assets integrity
    css = base / "assets" / "scudoai.css"
    logo = base / "assets" / "logo-symbol.svg"

    if not css.exists():
        issues.append(
            f"{red('ERROR')} {label}: assets/scudoai.css missing -- this is the root cause "
            f"of the 'giant logo no CSS' bug. Re-run brand-gen init + inject.sh."
        )
    else:
        try:
            lines = sum(1 for _ in css.open())
            if not EXPECTED_CSS_LINES_MIN <= lines <= EXPECTED_CSS_LINES_MAX:
                issues.append(
                    f"{red('ERROR')} {label}: assets/scudoai.css has {lines} lines "
                    f"(expected {EXPECTED_CSS_LINES_MIN}-{EXPECTED_CSS_LINES_MAX}); "
                    f"inject.sh did not replace scudoai.css with wrocpp.css. Re-run inject.sh."
                )
        except OSError as e:
            issues.append(f"{yellow('WARN')}  {label}: could not read scudoai.css ({e})")

    if not logo.exists():
        issues.append(f"{red('ERROR')} {label}: assets/logo-symbol.svg missing")
    elif logo.stat().st_size < MIN_LOGO_SVG_BYTES:
        issues.append(f"{yellow('WARN')}  {label}: assets/logo-symbol.svg only {logo.stat().st_size} bytes")

    # Rendered-HTML branding: magnet logo + AI-disclosure badge (see the
    # MAGNET_VIEWBOX comment above for why assets/ passing is not enough).
    index_html = base / "index.html"
    if not index_html.exists():
        issues.append(f"{red('ERROR')} {label}: index.html missing -- run brand-gen build")
    else:
        try:
            html = index_html.read_text(encoding="utf-8", errors="replace")
        except OSError as e:
            html = ""
            issues.append(f"{yellow('WARN')}  {label}: could not read index.html ({e})")
        if html:
            if MAGNET_VIEWBOX not in html:
                issues.append(
                    f"{red('ERROR')} {label}: index.html has no wro.cpp magnet logo "
                    f"({MAGNET_VIEWBOX} not found); inject.sh did not run after "
                    f"brand-gen build. Re-run inject.sh, then brand-gen image."
                )
            # The badge requirement follows the card's ai_disclosure, mirroring
            # the post frontmatter. A human-authored guest post must NOT carry
            # an AI badge, so for those the check inverts.
            disclosure = "ai-generated"
            cfg = base / "config.yaml"
            if cfg.exists():
                try:
                    for line in cfg.open():
                        m = re.match(r'\s*ai_disclosure:\s*["\']?([a-z-]+)', line)
                        if m:
                            disclosure = m.group(1)
                            break
                except OSError:
                    pass

            if disclosure == "human":
                if AI_BADGE_MARKER in html:
                    issues.append(
                        f"{red('ERROR')} {label}: ai_disclosure is 'human' but the card "
                        f"carries an AI badge. That mislabels a person's writing as "
                        f"machine-generated. Re-run inject.sh, then brand-gen image."
                    )
            elif AI_BADGE_MARKER not in html:
                issues.append(
                    f"{red('ERROR')} {label}: index.html has no AI-disclosure badge "
                    f"({AI_BADGE_MARKER} not found). Cards for AI-drafted posts must "
                    f"carry it per the /ai policy. Re-run inject.sh, then brand-gen image."
                )

    # Confirm the card actually rendered text, by measuring ink coverage.
    #
    # This used to crop a fixed 1600x200 band, average it down to one pixel, and
    # warn when that average came out light. It did not work. A short title line
    # leaves most of the band as blank paper, so the average goes light even
    # though the text rendered perfectly. Measured over all 296 cards in the repo
    # on 2026-08-21 it produced 15 false positives and zero true ones, and it was
    # not even ordering cards correctly: contracts-dispute was flagged at 12.5%
    # ink while cpp26-contracts passed at 9.9%.
    #
    # Counting dark pixels survives short lines, long lines and layout changes: a
    # rendered card has genuinely dark glyph pixels wherever the text sits, and a
    # card that rendered no text has essentially none. Observed range across every
    # current card is 3.0% (splicing, whose title is deliberately just "[:r:].")
    # to 19.2%, so the floor below leaves a wide margin while still catching the
    # failure this is here to catch.
    MIN_INK_PERCENT = 1.0
    if img.exists():
        try:
            raw = subprocess.run(
                [
                    "magick", str(img),
                    "-crop", "2000x1100+200+300", "+repage",
                    "-colorspace", "gray", "-threshold", "50%",
                    "-format", "%[fx:100*(1-mean)]", "info:",
                ],
                capture_output=True, text=True, check=True, timeout=10,
            ).stdout.strip()
            if raw:
                ink = float(raw)
                if ink < MIN_INK_PERCENT:
                    issues.append(
                        f"{red('ERROR')} {label}: title/body region is only {ink:.2f}% ink "
                        f"(floor {MIN_INK_PERCENT}%); the card looks like it rendered no text"
                    )
        except (FileNotFoundError, subprocess.CalledProcessError,
                subprocess.TimeoutExpired, ValueError):
            pass

    return issues


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--slug", help="Check a single slug")
    parser.add_argument("--platform", choices=["linkedin", "facebook", "both"],
                        default="both", help="Which platform to check")
    parser.add_argument("--all", action="store_true",
                        help="Check every rendered card under social/{linkedin,facebook}/")
    args = parser.parse_args()

    targets: list[tuple[str, str]] = []
    if args.all:
        for plat in ("linkedin", "facebook"):
            d = REPO / "social" / plat
            if d.exists():
                for child in sorted(d.iterdir()):
                    if child.is_dir() and (child / "image.png").exists():
                        targets.append((plat, child.name))
    elif args.slug:
        plats = ["linkedin", "facebook"] if args.platform == "both" else [args.platform]
        for plat in plats:
            targets.append((plat, args.slug))
    else:
        parser.print_help()
        sys.exit(2)

    if not targets:
        print("No social cards found to check.")
        sys.exit(0)

    all_issues: list[str] = []
    for plat, slug in targets:
        issues = check_one(plat, slug)
        if not issues:
            print(f"{green('OK')}    {plat}/{slug}")
        else:
            for i in issues:
                print(i)
                if "ERROR" in i:
                    all_issues.append(i)

    if all_issues:
        print()
        print(f"{red('FAIL')}: {len(all_issues)} error(s) found. Do not publish.")
        print("Fix, cheapest first -- read the errors above before reaching for the big hammer:")
        print("  missing magnet/badge, or wrong scudoai.css line count:")
        print("    .claude/skills/advertise-post/brand-kit/inject.sh <card-dir> && brand-gen image")
        print("  missing assets/ entirely (brand-gen init was never run for this card):")
        print("    back up caption.md/content.md/config.yaml, remove the card dir,")
        print("    brand-gen init, restore them, then build + inject.sh + image.")
        sys.exit(1)

    print()
    print(green(f"OK: {len(targets)} card(s) passed all checks."))
    sys.exit(0)


if __name__ == "__main__":
    main()
