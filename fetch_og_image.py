
"""
fetch_og_image.py
Tries to download the og:image from a news article URL.

Usage (by agent):
  python fetch_og_image.py --url "https://techcrunch.com/article/..."

Exit behavior:
  - Success : prints the saved image path to stdout  ->  agent uses this as --image
  - Failure : prints [OG_FAILED] to stdout           ->  agent falls back to AI image generation

All debug/status messages go to stderr so they do not interfere with the agent reading stdout.
"""

import argparse
import os
import re
import sys
import urllib.request
from datetime import datetime

ROOT       = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(ROOT, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}

# Reject images smaller than this — likely logos or placeholder icons
MIN_IMAGE_BYTES = 20_000


def fetch_html(url: str) -> str:
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as resp:
        charset = resp.headers.get_content_charset() or "utf-8"
        return resp.read().decode(charset, errors="replace")


def extract_og_image(html: str):
    patterns = [
        r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']',
        r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image["\']',
    ]
    for pattern in patterns:
        match = re.search(pattern, html, re.IGNORECASE)
        if match:
            url = match.group(1).strip()
            if url.startswith("http"):
                return url
    return None


def download_image(image_url: str) -> str:
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    ext = "jpg"
    clean_url = image_url.split("?")[0].lower()
    if clean_url.endswith(".png"):
        ext = "png"
    elif clean_url.endswith(".webp"):
        ext = "webp"

    save_path = os.path.join(OUTPUT_DIR, f"{timestamp}_og_image.{ext}")

    req = urllib.request.Request(image_url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=20) as resp:
        data = resp.read()

    if len(data) < MIN_IMAGE_BYTES:
        raise ValueError(
            f"Image too small ({len(data)} bytes) — likely a logo or placeholder."
        )

    with open(save_path, "wb") as f:
        f.write(data)

    return save_path


def main():
    parser = argparse.ArgumentParser(description="Fetch OG image from a news article URL.")
    parser.add_argument("--url", required=True, help="Full URL of the news article.")
    args = parser.parse_args()
    url = args.url.strip()

    try:
        print(f"[OG] Fetching article: {url}", file=sys.stderr)
        html = fetch_html(url)

        og_url = extract_og_image(html)
        if not og_url:
            print("[OG] No og:image meta tag found.", file=sys.stderr)
            print("[OG_FAILED]")
            return

        print(f"[OG] Found OG image: {og_url}", file=sys.stderr)
        saved_path = download_image(og_url)
        print(f"[OG] Downloaded: {saved_path}", file=sys.stderr)

        # ONLY the path goes to stdout — agent reads this line
        print(saved_path)

    except Exception as e:
        print(f"[OG] Failed: {e}", file=sys.stderr)
        print("[OG_FAILED]")


if __name__ == "__main__":
    main()

