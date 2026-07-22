"""
search_local_image.py
Searches the local curated image library for the best candidates for a news story.
This is Tier 2 of the image pipeline — runs only if fetch_og_image.py returned [OG_FAILED].

Usage (by agent):
  python search_local_image.py --keywords "openai sam altman gpt model release"

Exit behavior:
  - Matches found : prints a [LIB_MATCH] block with up to 5 candidate paths + filenames.
                    The AGENT reads this block and picks the most tonally appropriate image.
  - No match      : prints [LIB_FAILED] — agent falls back to AI generation.

IMPORTANT: All debug/status messages go to stderr.
           Only the [LIB_MATCH] block or [LIB_FAILED] goes to stdout.

Filename Mood Guide (for the agent to use when selecting among candidates):
  _Speaking_          -> announcement, keynote, product launch, press conference
  _Serious_           -> controversy, legal issues, criticism, market downturn, security breach
  _Smiling_ / _Happy_ -> positive news, record earnings, funding round, award, milestone
  _Portrait_          -> neutral, general profile story, no strong tone required
  _Standing_          -> general coverage, official announcement
  _Building_ / _Sign_ -> company-level news when no good person photo matches
  _Logo_              -> brand/product news, lower preference than person/building photos
"""

import argparse
import json
import os
import re
import sys

INDEX_PATH = r"D:\play-ground\images\IMAGE_INDEX.json"
MIN_SCORE = 1      # At least 1 keyword token must match
MAX_RESULTS = 5    # Return up to 5 candidates for agent to choose from


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
        phrase_tokens = set(keyword_phrase.lower().split())
        if phrase_tokens and phrase_tokens.issubset(query_tokens):
            # Longer phrases are more specific -> higher reward
            phrase_weight = len(phrase_tokens) ** 1.5
            score += phrase_weight
    return score


def main():
    parser = argparse.ArgumentParser(
        description="Search local image library for best story candidates."
    )
    parser.add_argument(
        "--keywords",
        required=True,
        help=(
            "Space-separated keywords from the news story. "
            "Include company names, person names, technology topics, country names. "
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

    # Filter to only files that actually exist on disk
    valid = []
    for s, tier, img in scored:
        if os.path.isfile(img["path"]):
            valid.append((s, tier, img))
        else:
            print(f"[LIB] Skipping missing file: {img['filename']}", file=sys.stderr)

    if not valid:
        print("[LIB] All matched images are missing from disk.", file=sys.stderr)
        print("[LIB_FAILED]")
        return

    # Take top N results
    top = valid[:MAX_RESULTS]

    print(f"[LIB] Returning {len(top)} candidates for agent selection:", file=sys.stderr)
    for i, (s, tier, img) in enumerate(top):
        print(f"  [{i+1}] score={s:.1f} tier={tier} -> {img['filename']}", file=sys.stderr)

    # -----------------------------------------------------------------------
    # Output the [LIB_MATCH] block to stdout.
    # The AGENT reads each line and picks the most tonally appropriate image
    # based on the filename mood clues (_Serious_, _Smiling_, _Speaking_, etc.)
    # Each line format: PATH | FILENAME | score=X | tier=Y | category=Z
    # -----------------------------------------------------------------------
    print("[LIB_MATCH]")
    for s, tier, img in top:
        print(
            f"{img['path']} | {img['filename']} | "
            f"score={s:.1f} | tier={tier} | category={img.get('category', 'unknown')}"
        )
    print("[/LIB_MATCH]")


if __name__ == "__main__":
    main()
