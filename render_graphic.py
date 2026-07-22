"""
render_graphic.py
Renders the SubsDrop HTML template to a timestamped 1080x1080 JPG.
Output goes to: output/YYYY-MM-DD_HHMMSS_graphic.jpg
"""

from playwright.sync_api import sync_playwright
import os
from datetime import datetime

ROOT       = os.path.dirname(os.path.abspath(__file__))
HTML_PATH  = "file:///" + os.path.join(ROOT, "subsdrop_template.html").replace("\\", "/")
OUTPUT_DIR = os.path.join(ROOT, "output")

os.makedirs(OUTPUT_DIR, exist_ok=True)


def render_image():
    timestamp   = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    output_file = os.path.join(OUTPUT_DIR, f"{timestamp}_graphic.jpg")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1080, "height": 1080})
        print(f"Loading: {HTML_PATH}")
        page.goto(HTML_PATH)
        page.wait_for_timeout(2500)
        page.screenshot(path=output_file, type="jpeg", quality=97)
        browser.close()

    print(f"[OK] Graphic saved: {output_file}")
    return output_file   # Returns the full path so caller can use it


if __name__ == "__main__":
    path = render_image()
    print(f"Path: {path}")
