# RESEARCH.md — How to Find Today's Top Tech/AI News

## Your Goal
Find ONE single, important, real tech or AI news story published within the last 24 hours.
This story becomes today's entire post. Choose the most impactful story available.

---

## Step-by-Step Research Process

### Step 1 — Run Multiple Searches
Use your web search tool with at least 2-3 of these queries:
- `"top AI news today [current date]"`
- `"biggest tech news today"`
- `"AI industry breaking news [current date]"`
- `"OpenAI Google Meta Microsoft Apple tech news today"`
- `"AI startup funding news today"`

### Step 2 — Story Selection Criteria

| Factor | Requirement |
|--------|------------|
| Recency | Published in the last 24-48 hours only |
| Impact | Affects many people, companies, or the industry broadly |
| Category | AI first, then Big Tech, Cybersecurity, Startups, Policy |
| Source | Reuters, Bloomberg, TechCrunch, Wired, The Verge, WSJ, FT |
| Novelty | Not a repeat of a recently posted story (check `agent/logs/`) |

### Step 3 — Validate Before Proceeding
- [ ] Published within the last 48 hours?
- [ ] Genuinely important, not a minor update?
- [ ] From a credible source?
- [ ] Not already posted recently?

### Step 4 — Extract These 6 Details
Once selected, note down:
1. **Rewritten Headline** — Your original 6-12 word journalistic headline
2. **Source Name** — e.g. Reuters, TechCrunch
3. **Date** — Format: `Month DD, YYYY`
4. **Key Facts** — 3-5 bullet points (for your own reference only, not for the post)
5. **2-Line Summary** — Two clean sentences (used in the graphic)
6. **Article URL** — The full direct URL of the article (e.g. `https://techcrunch.com/2026/07/23/...`). You will pass this to `fetch_og_image.py` in the image step. This is mandatory.

---

## Category Priority (High → Low)
1. Artificial Intelligence (new models, company moves, policy)
2. Big Tech (Google, Apple, Microsoft, Meta, Amazon, OpenAI, Anthropic)
3. Cybersecurity
4. Startups & Funding
5. Semiconductors & Hardware
6. Regulation & Government Policy

---

## What to Avoid
- Opinion pieces or editorials
- Unverified rumours or leaks
- Stories older than 48 hours
- Routine earnings beats (unless truly surprising)
- Product reviews or buying guides
