"""
facebook_poster.py
Posts a graphic + caption to the Facebook Page.
After a successful post, moves the image to output/archive/.

Usage (from agent/scheduler):
  python facebook_poster.py --caption "Your post caption here..."

Usage (manual, uses latest graphic in output/ folder):
  python facebook_poster.py --caption "Your caption"
"""

import os
import shutil
import argparse
import requests
from datetime import datetime
from dotenv import load_dotenv

ROOT        = os.path.dirname(os.path.abspath(__file__))
ARCHIVE_DIR = os.path.join(ROOT, "output", "archive")

load_dotenv(os.path.join(ROOT, ".env"))

ACCESS_TOKEN = os.getenv("FACEBOOK_ACCESS_TOKEN")
PAGE_ID      = os.getenv("FACEBOOK_PAGE_ID")

os.makedirs(ARCHIVE_DIR, exist_ok=True)


def post_to_facebook(message: str, image_path: str) -> bool:
    if not ACCESS_TOKEN or not PAGE_ID:
        print("[ERROR] Missing FACEBOOK_ACCESS_TOKEN or FACEBOOK_PAGE_ID in .env")
        return False

    if not image_path or not os.path.exists(image_path):
        print(f"[ERROR] Image not found: {image_path}")
        return False

    print(f"[POST] Posting to page: {PAGE_ID}")
    print(f"[POST] Image: {image_path}")
    print(f"[POST] Caption preview: {message[:80]}...")

    url  = f"https://graph.facebook.com/v20.0/{PAGE_ID}/photos"
    data = {"message": message, "access_token": ACCESS_TOKEN}

    with open(image_path, "rb") as img:
        response = requests.post(url, data=data, files={"source": img})

    result = response.json()

    if "id" in result:
        post_id = result["id"]
        print(f"[OK] Posted successfully! Post ID: {post_id}")

        # Move image to archive after successful post
        filename     = os.path.basename(image_path)
        archive_path = os.path.join(ARCHIVE_DIR, filename)
        shutil.move(image_path, archive_path)
        print(f"[OK] Image archived: {archive_path}")
        return True
    else:
        print(f"[FAILED] Facebook API error: {result}")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Post a graphic + caption to Facebook Page.")
    parser.add_argument(
        "--caption",
        required=True,
        help="The full Facebook post caption text to publish."
    )
    parser.add_argument(
        "--image",
        required=False,
        default=None,
        help="(Optional) Absolute path to the graphic image. If not provided, uses latest file in output/ folder."
    )
    args = parser.parse_args()

    # --- Resolve image path ---
    if args.image:
        image_path = args.image
        if not os.path.exists(image_path):
            print(f"[ERROR] Specified image not found: {image_path}")
            exit(1)
    else:
        # Auto-detect latest rendered graphic in output/
        output_dir = os.path.join(ROOT, "output")
        graphics = sorted([
            f for f in os.listdir(output_dir)
            if f.endswith("_graphic.jpg") and os.path.isfile(os.path.join(output_dir, f))
        ])
        if not graphics:
            print("[ERROR] No graphic found in output/ folder. Run render_graphic.py first.")
            exit(1)
        image_path = os.path.join(output_dir, graphics[-1])
        print(f"[INFO] Auto-selected latest graphic: {image_path}")

    # --- Post to Facebook ---
    success = post_to_facebook(args.caption, image_path)
    exit(0 if success else 1)
