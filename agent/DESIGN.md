# DESIGN.md — How to Render the Final Graphic

## Your Goal
Inject today's content into the fixed HTML template and render a perfect
1080x1080px (1:1) JPEG. The design system is permanently locked — never redesign it.
You only update the content values (headline, summary, credit, image).

---

## Fixed File Locations

| File | Path |
|------|------|
| HTML Template | `D:\play-ground\ai-automation-for-sd\subsdrop_template.html` |
| Content Injector | `D:\play-ground\ai-automation-for-sd\update_content.py` |
| Renderer | `D:\play-ground\ai-automation-for-sd\render_graphic.py` |
| Output Folder | `D:\play-ground\ai-automation-for-sd\output\` |
| Archive Folder | `D:\play-ground\ai-automation-for-sd\output\archive\` |

---

## Step-by-Step Rendering Process

### Step 1 — Prepare Your 4 Values

| Value | Format | Example |
|-------|--------|---------|
| `--headline` | HTML string, may include one `<span class='highlight'>` | `"THE AI <span class='highlight'>EFFICIENCY RACE</span> ESCALATES"` |
| `--summary` | Plain text, 1-2 short sentences, max 35 words | `"Google releases Gemini 3.6 Flash for enterprise. OpenAI agentic tools cross 10 million users."` |
| `--credit` | `Source \| Date \| Desk` | `"Reuters \| Jul 22 \| Tech Desk"` |
| `--image` | Absolute Windows path to the generated photo | `"C:\Users\USER\.gemini\...\photo.jpg"` |
| `--category` | Topic label for top-left corner (optional, default: TECHNOLOGY) | `"ARTIFICIAL INTELLIGENCE"` or `"CYBERSECURITY"` |
| `--date` | Date string (optional, auto-generated if omitted) | `"July 23, 2026"` |

### Step 2 — Run the Content Injector

```bash
python D:\play-ground\ai-automation-for-sd\update_content.py ^
  --headline "THE AI <span class='highlight'>EFFICIENCY RACE</span> ESCALATES" ^
  --summary "Google releases Gemini 3.6 Flash for enterprise. OpenAI agentic tools cross 10 million users." ^
  --credit "Reuters | Jul 22 | Tech Desk" ^
  --image "C:\Users\USER\.gemini\antigravity\brain\[id]\photo.jpg" ^
  --category "ARTIFICIAL INTELLIGENCE"
```

Note: `--date` is auto-generated from today's date. Only pass it if you need to override.

### Step 3 — Render the Screenshot

After updating the HTML, run the render script:

```bash
python D:\play-ground\ai-automation-for-sd\render_graphic.py
```

This saves the graphic as a **timestamped file** inside the output folder:
```
D:\play-ground\ai-automation-for-sd\output\YYYY-MM-DD_HHMMSS_graphic.jpg
```

The script prints the exact saved path. **Note this path exactly** — you will pass it as `--image` to `facebook_poster.py`.

After `facebook_poster.py` posts successfully, it automatically moves the image to:
```
D:\play-ground\ai-automation-for-sd\output\archive\YYYY-MM-DD_HHMMSS_graphic.jpg
```
This keeps the output folder clean between runs.

---

## Headline Highlight Rules

- Maximum ONE highlighted phrase per headline (default).
- Two highlights only if the story has two equally critical facts — keep them on separate lines.
- Highlight uses `<span class="highlight">PHRASE</span>` in the HTML argument.
- Choose 2-3 words maximum for the highlighted phrase.
- The highlighted phrase must be the most newsworthy part of the headline.

```html
<!-- Good: -->
THE AI <span class="highlight">EFFICIENCY RACE</span> ESCALATES

<!-- Also good: -->
ANTHROPIC HIT WITH <span class="highlight">PATENT LAWSUIT</span>

<!-- Bad — entire headline highlighted: -->
<span class="highlight">THE AI EFFICIENCY RACE ESCALATES</span>
```

---

## Locked Design Values (Never Change These)

| Property | Value |
|----------|-------|
| Canvas | 1080 × 1080 px |
| Background | `#f4f3f0` (warm off-white) |
| Font | Inter |
| Headline size | 66px, weight 900 |
| Brand name | SubsDrop — always top-right, weight 900 |
| Category | Uppercase — always top-left, weight 800. Dynamic per story topic. |
| Date | Below category, auto-generated, weight 600 |
| Accent / Highlight | `#b91d22` (Deep Red) |
| Image filter | `grayscale(100%)` — applied by CSS, do not pre-process the photo |
| Image frame | Rounded corners `border-radius: 14px`, fills remaining space below text |
| Masthead divider | 2px solid `#111111` |

### Category Options
Choose the most appropriate category for the story:

| Category | When to Use |
|----------|------------|
| `TECHNOLOGY` | General tech news (default) |
| `ARTIFICIAL INTELLIGENCE` | AI models, AI companies, AI research |
| `CYBERSECURITY` | Hacks, data breaches, security tools |
| `STARTUPS` | Startup funding, acquisitions |
| `POLICY` | Government regulation, antitrust |
| `SEMICONDUCTORS` | Chips, hardware, manufacturing |

---

## Pre-Post Checklist
Before running `facebook_poster.py`, confirm:
- [ ] SubsDrop visible — top-right, bold
- [ ] Category label visible — top-left, uppercase
- [ ] Headline is large, bold, dominant
- [ ] Red highlight block is on the correct phrase
- [ ] Image fills the bottom portion
- [ ] No duplicate text, no extra elements

## How to Post
After confirming the graphic looks correct, run:
```bash
python D:\play-ground\ai-automation-for-sd\facebook_poster.py --caption "Full caption from POST_FORMAT step" --image "D:\play-ground\ai-automation-for-sd\output\YYYY-MM-DD_HHMMSS_graphic.jpg"
```
- `--caption` — the full text you wrote in the POST_FORMAT step
- `--image` — the exact path printed by render_graphic.py
- Script will confirm success with a Post ID, then auto-archive the image.
