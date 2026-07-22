"""
generate_permanent_token.py
Converts a short-lived Graph API token into a permanent Page Access Token
and automatically saves it to .env
"""

import requests
import os
import sys
from dotenv import load_dotenv

ROOT = r"D:\play-ground\ai-automation-for-sd"
ENV_PATH = os.path.join(ROOT, ".env")

APP_ID     = "2211785452886589"
APP_SECRET = "c9be78eeb1edc4ab7131394f0be18828"
PAGE_ID    = "590121077506988"

def get_long_lived_user_token(short_token):
    print("[1/3] Exchanging short-lived token for long-lived user token...")
    url = "https://graph.facebook.com/oauth/access_token"
    params = {
        "grant_type":        "fb_exchange_token",
        "client_id":         APP_ID,
        "client_secret":     APP_SECRET,
        "fb_exchange_token": short_token
    }
    r = requests.get(url, params=params)
    data = r.json()
    if "access_token" not in data:
        print("FAILED:", data)
        sys.exit(1)
    print("    Got long-lived user token (60-day).")
    return data["access_token"]

def get_permanent_page_token(long_lived_user_token):
    print("[2/3] Fetching permanent Page Access Token...")
    url = f"https://graph.facebook.com/v20.0/me/accounts"
    params = {"access_token": long_lived_user_token}
    r = requests.get(url, params=params)
    data = r.json()
    if "data" not in data:
        print("FAILED:", data)
        sys.exit(1)
    for page in data["data"]:
        if page["id"] == PAGE_ID:
            print(f"    Found page: {page['name']}")
            return page["access_token"]
    print(f"FAILED: Page {PAGE_ID} not found in accounts.")
    sys.exit(1)

def save_to_env(page_token):
    print("[3/3] Saving permanent token to .env ...")
    with open(ENV_PATH, "w") as f:
        f.write(f"FACEBOOK_ACCESS_TOKEN={page_token}\n")
        f.write(f"FACEBOOK_PAGE_ID={PAGE_ID}\n")
    print(f"    Saved to {ENV_PATH}")

def main():
    load_dotenv(ENV_PATH)
    current_token = os.getenv("FACEBOOK_ACCESS_TOKEN", "").strip()
    if not current_token:
        print("ERROR: No token found in .env — please add a fresh short-lived token first.")
        sys.exit(1)

    long_lived  = get_long_lived_user_token(current_token)
    page_token  = get_permanent_page_token(long_lived)
    save_to_env(page_token)

    print("\n[DONE] Your Page Access Token is now permanent and saved to .env")
    print("  This token does NOT expire as long as your App and Page remain connected.")

if __name__ == "__main__":
    main()
