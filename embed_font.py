"""
embed_font.py
One-time setup script: embeds Inter font as base64 into subsdrop_template.html
so that render_graphic.py works offline (no Google Fonts dependency).

Run once:
  python embed_font.py
"""

import base64
import re
import os
import urllib.request

ROOT          = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(ROOT, "subsdrop_template.html")
FONT_CACHE    = os.path.join(ROOT, "inter_latin.woff2")

FONT_URL = "https://fonts.gstatic.com/s/inter/v20/UcC73FwrK3iLTeHuS_nVMrMxCp50SjIa1ZL7.woff2"
HEADERS  = {"User-Agent": "Mozilla/5.0 Chrome/120"}


def download_font() -> bytes:
    """Download Inter latin subset woff2 if not already cached."""
    if os.path.exists(FONT_CACHE):
        print(f"[FONT] Using cached font: {FONT_CACHE}")
        with open(FONT_CACHE, "rb") as f:
            return f.read()

    print(f"[FONT] Downloading Inter from Google Fonts...")
    req = urllib.request.Request(FONT_URL, headers=HEADERS)
    with urllib.request.urlopen(req) as resp:
        data = resp.read()
    with open(FONT_CACHE, "wb") as f:
        f.write(data)
    print(f"[FONT] Saved to {FONT_CACHE} ({len(data)} bytes)")
    return data


def build_font_style(b64: str) -> str:
    """Build the embedded @font-face CSS block."""
    return (
        '<style id="inter-embedded-font">\n'
        '/* Inter font — embedded base64 woff2 (latin) — offline-safe */\n'
        "@font-face {\n"
        "  font-family: 'Inter';\n"
        "  font-style: normal;\n"
        "  font-weight: 400 900;\n"
        "  font-display: block;\n"
        f"  src: url(data:font/woff2;base64,{b64}) format('woff2');\n"
        "  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, "
        "U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, "
        "U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;\n"
        "}\n"
        "</style>"
    )


def patch_template(font_style: str):
    """Replace Google Fonts <link> tags with the embedded font block."""
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        html = f.read()

    # Check if already embedded
    if 'id="inter-embedded-font"' in html:
        print("[OK] Font already embedded in template. Nothing to do.")
        return

    # Remove Google Fonts preconnect + stylesheet link tags
    html = re.sub(
        r'\s*<link[^>]+fonts\.googleapis\.com[^>]*>\r?\n?',
        '',
        html
    )
    html = re.sub(
        r'\s*<link[^>]+fonts\.gstatic\.com[^>]*>\r?\n?',
        '',
        html
    )

    # Insert embedded font style block just before </head>
    html = html.replace("</head>", f"\n    {font_style}\n</head>", 1)

    with open(TEMPLATE_PATH, "w", encoding="utf-8") as f:
        f.write(html)

    print("[OK] Font successfully embedded into subsdrop_template.html")
    print("[OK] Google Fonts external links removed.")
    print("[OK] Template is now fully offline-capable.")


if __name__ == "__main__":
    font_bytes = download_font()
    b64_str    = base64.b64encode(font_bytes).decode("utf-8")
    style_tag  = build_font_style(b64_str)
    patch_template(style_tag)
