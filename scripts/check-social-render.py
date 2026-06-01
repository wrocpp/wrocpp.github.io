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

# wrocpp.css is 300 lines after inject.sh; if assets/scudoai.css doesn't match,
# inject didn't run or assets are missing.
EXPECTED_CSS_LINES_MIN = 280
EXPECTED_CSS_LINES_MAX = 320

# Logo SVG embedded by brand-gen is ~6KB; less means missing or wrong.
MIN_LOGO_SVG_BYTES = 5_000


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

    # Sample title-area pixel: should contain dark ink (not just paper background)
    # The mixed colour for rendered text is around #B0A0A0 (dark text + paper);
    # pure paper background gives #FCFAF5 or similar light value.
    if img.exists():
        try:
            color = subprocess.run(
                [
                    "magick", str(img),
                    "-crop", "1600x200+400+800",
                    "+repage", "-resize", "1x1!",
                    "-format", "%[hex:u]", "info:",
                ],
                capture_output=True, text=True, check=True, timeout=10,
            ).stdout.strip()
            # Treat darker mixed colors as evidence of rendered text.
            if color and len(color) >= 6:
                r = int(color[0:2], 16)
                g = int(color[2:4], 16)
                b = int(color[4:6], 16)
                avg = (r + g + b) // 3
                if avg > 220:
                    issues.append(
                        f"{yellow('WARN')}  {label}: title area sample is light (#{color[:6]}, avg {avg}); "
                        f"text may not be rendering"
                    )
        except (FileNotFoundError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
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
        print("Fix: rm -rf the broken card dir, then brand-gen init + inject.sh + brand-gen image.")
        sys.exit(1)

    print()
    print(green(f"OK: {len(targets)} card(s) passed all checks."))
    sys.exit(0)


if __name__ == "__main__":
    main()
