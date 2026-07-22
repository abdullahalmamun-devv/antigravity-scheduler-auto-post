"""
update_content.py
Updates the SubsDrop HTML template with today's content before rendering.

Usage:
  python update_content.py --headline "..." --summary "..." --credit "..." --image "C:\\path\\to\\photo.jpg"

Optional:
  --category "ARTIFICIAL INTELLIGENCE"   (default: TECHNOLOGY)
  --date "July 23, 2026"                (default: today's date auto-generated)
"""

import argparse
import re
import os
from datetime import datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(ROOT, "subsdrop_template.html")


def update_template(headline_html: str, summary: str, credit: str, image_path: str,
                    category: str = "TECHNOLOGY", date_str: str = None,
                    is_local_image: bool = False):
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # --- Auto-detect or toggle local-image-mode ---
    is_local = is_local_image or ("play-ground" in image_path.replace("\\", "/").lower() and "/images/" in image_path.replace("\\", "/").lower())
    if is_local:
        if 'class="local-image-mode"' not in content:
            content = re.sub(r'<body([^>]*)>', r'<body\1 class="local-image-mode">', content, count=1)
    else:
        content = content.replace(' class="local-image-mode"', '').replace('class="local-image-mode"', '')

    # --- Update CATEGORY ---
    content = re.sub(
        r'(<div class="category">)(.*?)(</div>)',
        lambda m: m.group(1) + category.upper() + m.group(3),
        content,
        count=1,
        flags=re.DOTALL
    )

    # --- Update DATE ---
    if date_str is None:
        date_str = datetime.now().strftime("%B %d, %Y")
    content = re.sub(
        r'(<div class="date">)(.*?)(</div>)',
        lambda m: m.group(1) + date_str + m.group(3),
        content,
        count=1,
        flags=re.DOTALL
    )

    # --- Update HEADLINE ---
    content = re.sub(
        r'(<div class="headline">)(.*?)(</div>)',
        lambda m: m.group(1) + headline_html + m.group(3),
        content,
        flags=re.DOTALL
    )

    # --- Update SUMMARY ---
    content = re.sub(
        r'(<div class="summary">)(.*?)(</div>)',
        lambda m: m.group(1) + summary + m.group(3),
        content,
        flags=re.DOTALL
    )

    # --- Update CREDIT (first .credit div only) ---
    parts = [p.strip() for p in credit.split("|")]
    credit_html = ' <span class="sep">|</span> '.join(parts)
    content = re.sub(
        r'(<div class="credit">)(.*?)(</div>)',
        lambda m: m.group(1) + credit_html + m.group(3),
        content,
        count=1,
        flags=re.DOTALL
    )

    # --- Update IMAGE SRC ---
    image_url = "file:///" + image_path.replace("\\", "/")
    content = re.sub(
        r'(<img[^>]+class="hero-image"[^>]*src=")[^"]*(")',
        lambda m: m.group(1) + image_url + m.group(2),
        content
    )
    content = re.sub(
        r'(<img[^>]+src=")[^"]*("[^>]+class="hero-image")',
        lambda m: m.group(1) + image_url + m.group(2),
        content
    )

    with open(TEMPLATE_PATH, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"[OK] Template updated.")
    print(f"     Category : {category}")
    print(f"     Date     : {date_str}")
    print(f"     Headline : {headline_html[:70]}...")
    print(f"     Summary  : {summary[:70]}...")
    print(f"     Credit   : {credit}")
    print(f"     Image    : {image_path} (Local Mode: {is_local})")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update SubsDrop HTML template content.")
    parser.add_argument("--headline", required=True, help="Headline HTML (may include <span class='highlight'>)")
    parser.add_argument("--summary",  required=True, help="Summary text, 2 short sentences")
    parser.add_argument("--credit",   required=True, help="Credit: Source | Date | Desk")
    parser.add_argument("--image",    required=True, help="Absolute path to hero photograph")
    parser.add_argument("--category", required=False, default="TECHNOLOGY",
                        help="Category label (e.g. ARTIFICIAL INTELLIGENCE, CYBERSECURITY). Default: TECHNOLOGY")
    parser.add_argument("--date",     required=False, default=None,
                        help="Date string (e.g. 'July 23, 2026'). Default: today's date auto-generated")
    parser.add_argument("--is-local-image", action="store_true", default=False,
                        help="Enlarge hero image layout when using Tier 2 local library images")
    args = parser.parse_args()

    update_template(args.headline, args.summary, args.credit, args.image,
                    args.category, args.date, args.is_local_image)
