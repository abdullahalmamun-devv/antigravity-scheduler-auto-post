"""
search_local_image.py
Searches the local curated image library for the best match for a news story.
This is Tier 2 of the image pipeline — runs only if fetch_og_image.py returned [OG_FAILED].

Usage (by agent):
  python search_local_image.py --keywords "openai sam altman gpt model release"
  python search_local_image.py --keywords "nvidia jensen huang blackwell chip"
  python search_local_image.py --keywords "trump usa tariff policy executive order"

Exit behavior:
  - Match found : prints the absolute image path to stdout -> agent uses as --image
  - No match    : prints [LIB_FAILED] to stdout          -> agent falls back to AI generation

All debug/status messages go to stderr so they do not interfere with the agent reading stdout.

Scoring logic:
  - Multi-word keyword phrases receive higher weight (more tokens = more specific = higher score)
  - Among equal scores, lower preference_tier wins (tier 1 = person photo, tier 4 = logo/icon)
  - Minimum score threshold: at least 1 keyword token must match
"""

import argparse
import json
import os
import re
import sys

INDEX_PATH = r"D:\play-ground\images\IMAGE_INDEX.json"
MIN_SCORE = 1  # At least 1 keyword token must match to be considered


def load_index() -> list:
    """Load the IMAGE_INDEX.json and return the images list."""
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("images", [])


def tokenize(text: str) -> set:
    """Lowercase and split into word tokens, removing common stop words."""
    stop_words = {
        "the", "a", "an", "is", "are", "was", "were", "be", "been",
        "has", "have", "had", "do", "does", "did", "will", "would",
        "could", "should", "may", "might", "shall", "can", "to", "of",
        "in", "on", "at", "for", "by", "with", "from", "and", "or",
        "but", "not", "its", "it", "this", "that", "new", "report",
        "says", "said", "after", "about", "over", "more", "than", "up"
    }
    tokens = set(re.findall(r'\b[a-z][a-z0-9]*\b', text.lower()))
    return tokens - stop_words


def score_image(image: dict, query_tokens: set) -> float:
    """
    Score an image based on keyword overlap with query tokens.
    Multi-word keyword phrases score higher than single words.
    Returns a float score: 0.0 means no match.
    """
    score = 0.0
    for keyword_phrase in image.get("keywords", []):
        # Tokenize the keyword phrase
        phrase_tokens = set(keyword_phrase.lower().split())
        # Check if ALL tokens of the phrase appear in the query
        if phrase_tokens and phrase_tokens.issubset(query_tokens):
            # Weight: longer phrases are more specific -> higher reward
            phrase_weight = len(phrase_tokens) ** 1.5
            score += phrase_weight
    return score


def main():
    parser = argparse.ArgumentParser(
        description="Search local image library for best story match."
    )
    parser.add_argument(
        "--keywords",
        required=True,
        help=(
            "Space-separated keywords extracted from the news story. "
            "Include: company names, person names, technology topics, "
            "country names if relevant. "
            "Example: 'openai sam altman gpt model release chatgpt'"
        )
    )
    args = parser.parse_args()

    query = args.keywords.strip()
    if not query:
        print("[LIB] ERROR: --keywords cannot be empty.", file=sys.stderr)
        print("[LIB_FAILED]")
        return

    query_tokens = tokenize(query)
    print(f"[LIB] Query tokens ({len(query_tokens)}): {sorted(query_tokens)}", file=sys.stderr)

    # Load index
    try:
        images = load_index()
    except FileNotFoundError:
        print(f"[LIB] ERROR: Image index not found at: {INDEX_PATH}", file=sys.stderr)
        print("[LIB_FAILED]")
        return
    except json.JSONDecodeError as e:
        print(f"[LIB] ERROR: Failed to parse image index: {e}", file=sys.stderr)
        print("[LIB_FAILED]")
        return

    print(f"[LIB] Loaded {len(images)} images from index.", file=sys.stderr)

    # Score all images
    scored = []
    for img in images:
        s = score_image(img, query_tokens)
        if s >= MIN_SCORE:
            tier = img.get("preference_tier", 4)
            scored.append((s, tier, img))

    if not scored:
        print("[LIB] No matching image found for this story.", file=sys.stderr)
        print("[LIB_FAILED]")
        return

    # Sort: highest score first, then lowest tier (best visual quality) first
    scored.sort(key=lambda x: (-x[0], x[1]))

    # Log top 3 matches for transparency
    print(f"[LIB] Top matches ({min(3, len(scored))}):", file=sys.stderr)
    for i, (s, tier, img) in enumerate(scored[:3]):
        print(f"  [{i+1}] score={s:.1f} tier={tier} -> {img['filename']}", file=sys.stderr)

    # Pick the best match
    best_score, best_tier, best_img = scored[0]
    best_path = best_img["path"]

    # Verify the file actually exists
    if not os.path.isfile(best_path):
        print(f"[LIB] Match found but file missing on disk: {best_path}", file=sys.stderr)
        # Try next best match
        for s, tier, img in scored[1:]:
            candidate = img["path"]
            if os.path.isfile(candidate):
                print(f"[LIB] Using fallback match: {img['filename']}", file=sys.stderr)
                print(candidate)
                return
        print("[LIB] No accessible image found.", file=sys.stderr)
        print("[LIB_FAILED]")
        return

    print(
        f"[LIB] Selected: {best_img['filename']} "
        f"(score={best_score:.1f}, tier={best_tier}, category={best_img.get('category', 'unknown')})",
        file=sys.stderr
    )

    # Output ONLY the path to stdout — this is what the agent reads
    print(best_path)


if __name__ == "__main__":
    main()
