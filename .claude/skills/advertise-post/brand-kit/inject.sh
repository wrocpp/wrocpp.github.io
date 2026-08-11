#!/usr/bin/env bash
# inject.sh -- swap brand-gen's vendored scudoai assets for wro.cpp ones.
#
# Usage:  inject.sh <project-dir>
#
# Run AFTER `brand-gen build` (so index.html exists) and BEFORE
# `brand-gen image` (so the screenshot picks up our changes).
#
# Three operations, all idempotent on re-run:
#   1. assets/scudoai.css <- wrocpp.css (standalone wro.cpp stylesheet,
#      independent from scudoai-social.css; styles .card / .card-insight /
#      .card-quote / .card-stat / .card-announcement from scratch in the
#      Editorial Magnet aesthetic).
#   2. The inlined <symbol id="scudo-logo"> block in index.html <-
#      our magnet logo. brand-gen reads BRAND_KIT_ROOT/assets/logo-symbol.svg
#      directly (generator/lib/logo.js:14), bypassing the vendored copy --
#      so we have to patch the rendered HTML.
#   3. An "AI-generated" disclosure badge (bottom-right; styled by .ai-badge
#      in wrocpp.css), so the AI disclosure rides with the card image on
#      social. See the /ai policy page.

set -euo pipefail

PROJECT_DIR="${1:-}"
[[ -n "$PROJECT_DIR" ]] || { echo "usage: $0 <project-dir>" >&2; exit 1; }
[[ -d "$PROJECT_DIR" ]] || { echo "not a directory: $PROJECT_DIR" >&2; exit 1; }

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WROCPP_CSS="$SKILL_DIR/wrocpp.css"
WROCPP_LOGO="$SKILL_DIR/logo-symbol.svg"

# 1. Replace assets/scudoai.css with the standalone wrocpp.css.
#    Keeping the file NAMED scudoai.css means we don't have to patch
#    the <link rel="stylesheet" href="assets/scudoai.css"> in index.html.
SCUDOAI_CSS="$PROJECT_DIR/assets/scudoai.css"
if [[ -f "$SCUDOAI_CSS" ]]; then
  cp "$WROCPP_CSS" "$SCUDOAI_CSS"
  echo "ok   replaced assets/scudoai.css with wrocpp.css ($(wc -l < "$SCUDOAI_CSS") lines)"
fi

# Drop layout.css too -- we don't need brand-gen's per-template layout
# tweaks since wrocpp.css already sizes the card to 1200x1200.
LAYOUT_CSS="$PROJECT_DIR/assets/layout.css"
if [[ -f "$LAYOUT_CSS" ]]; then
  : > "$LAYOUT_CSS"   # truncate; harmless empty file keeps the <link> happy
  echo "ok   blanked assets/layout.css"
fi

# 2. Swap the inlined logo SVG in index.html.
INDEX_HTML="$PROJECT_DIR/index.html"
if [[ -f "$INDEX_HTML" ]]; then
  python3 - "$INDEX_HTML" "$WROCPP_LOGO" <<'PY'
import re, sys
index_html, logo_svg = sys.argv[1], sys.argv[2]
html = open(index_html).read()
new_logo = open(logo_svg).read().strip()
# Match the FIRST <svg ... position:absolute;width:0;height:0 ... </svg> block.
pattern = re.compile(
    r'<svg[^>]*position:absolute;\s*width:0;\s*height:0[^>]*>.*?</svg>',
    re.DOTALL,
)
new_html, n = pattern.subn(new_logo, html, count=1)
if n == 0:
    sys.exit("error: did not find inlined logo svg in index.html")
open(index_html, 'w').write(new_html)
print(f"ok   swapped inlined logo svg ({n} replacement)")
PY

  # 3. Stamp the AI-disclosure badge into the card (bottom-right; styled by
  #    .ai-badge in wrocpp.css). Idempotent: skip if already present.
  #
  #    The label follows `ai_disclosure` in the card's config.yaml, mirroring
  #    the post's own frontmatter field (see content.config.ts):
  #      ai-generated (default) -> "AI-generated"
  #      ai-assisted            -> "AI-assisted"
  #      human                  -> NO badge at all
  #    A human-authored guest post must not carry an AI badge: labelling a
  #    contributor's own writing as machine-generated is exactly the kind of
  #    misattribution the /ai page exists to prevent.
  python3 - "$INDEX_HTML" "$PROJECT_DIR/config.yaml" <<'PY'
import re, sys
index_html, config_yaml = sys.argv[1], sys.argv[2]

disclosure = "ai-generated"
try:
    for line in open(config_yaml):
        m = re.match(r'\s*ai_disclosure:\s*["\']?([a-z-]+)', line)
        if m:
            disclosure = m.group(1)
            break
except OSError:
    pass

if disclosure == "human":
    print("ok   ai_disclosure: human -> no badge stamped")
    raise SystemExit(0)

label = "AI-assisted" if disclosure == "ai-assisted" else "AI-generated"
html = open(index_html).read()
if 'class="ai-badge"' in html:
    print(f"ok   ai-badge already present (skipped)")
elif '</section>' in html:
    html = html.replace('</section>', f'<div class="ai-badge">{label}</div></section>', 1)
    open(index_html, 'w').write(html)
    print(f"ok   stamped ai-badge ({label})")
else:
    sys.exit("error: no </section> anchor to attach ai-badge")
PY
fi
