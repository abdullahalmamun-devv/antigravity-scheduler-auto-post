# IMAGE_GEN.md — How to Generate Today's Hero Photograph

## 3-TIER IMAGE STRATEGY — Follow This Exact Order Every Time

You have THREE image sources in strict priority order. Never skip a tier.
Stop at the first tier that succeeds.

```
Tier 1: OG Image      → fetch_og_image.py     (real editorial photo from the article)
   ↓ [OG_FAILED]
Tier 2: Local Library  → search_local_image.py (curated photo library, 164 images)
   ↓ [LIB_FAILED]
Tier 3: AI Generation  → generate_image tool   (last resort only)
```

---

### Tier 1 — Try OG Image First

Run this command with the news article URL you found in RESEARCH step:

```bash
python D:\play-ground\ai-automation-for-sd\fetch_og_image.py --url "FULL_NEWS_ARTICLE_URL"
```

**Read the output carefully:**

| Output | Meaning | What to do |
|--------|---------|------------|
| A file path (e.g. `D:\...\output\2026-07-23_og_image.jpg`) | OG image downloaded successfully | ✅ Use this path as `--image` in update_content.py. Skip Tier 2 and Tier 3 entirely. |
| `[OG_FAILED]` | Site blocked access or no OG image found | Proceed to Tier 2 immediately. |

**Why this is the best source:**
- The OG image is the exact editorial photo the journalists chose for this story
- It is already perfectly consistent with the news content
- The HTML template applies `grayscale(100%)` CSS — so any color photo becomes B&W automatically
- No manual processing needed

---

### Tier 2 — Search Local Image Library (Only if Tier 1 returned [OG_FAILED])

Before generating any AI image, search the curated local library of 164 professional photos.
This library contains tech CEOs, company buildings, AI products, and world leaders — all
curated to match the types of stories SubsDrop covers.

**Step 1 — Extract keywords from the story.**
From the story headline and summary, extract:
- Company names (e.g. `openai nvidia meta microsoft apple google deepseek`)
- Person names (e.g. `sam altman jensen huang mark zuckerberg elon musk`)
- Technology topics (e.g. `gpu chips ai model llm semiconductor cloud`)
- Country or government names if relevant (e.g. `trump usa china xi jinping eu`)

Example — Story: "NVIDIA Announces Blackwell B300 AI Chip for Data Centers"
Keywords to pass: `nvidia jensen huang blackwell gpu chips ai semiconductor data center`

**Step 2 — Run the library search:**
```bash
python D:\play-ground\ai-automation-for-sd\search_local_image.py --keywords "YOUR EXTRACTED KEYWORDS HERE"
```

**Read the output carefully:**

| Output | Meaning | What to do |
|--------|---------|------------|
| A file path (e.g. `D:\play-ground\images\02\Jensen_Huang_CEO_NVIDIA_Speaking_Leather_Jacket.png`) | Matching image found in library | ✅ Use this path as `--image` in update_content.py. Skip Tier 3 entirely. |
| `[LIB_FAILED]` | No sufficiently close match found in library | Proceed to Tier 3 (AI generation). |

**Why this is better than AI generation:**
- These are real, high-quality curated photos — not AI-generated
- They directly feature the actual people and companies in the news
- The grayscale CSS filter means color branding in the photo is neutralized automatically
- A real photo of Sam Altman is infinitely more relevant than an AI-generated "researcher in a lab"

**The local library covers:**
- Tech CEOs: Sam Altman (OpenAI), Jensen Huang (NVIDIA), Mark Zuckerberg (Meta), Elon Musk,
  Dario Amodei (Anthropic), Bill Gates, Jeff Bezos, Steve Jobs
- Companies: Google, Microsoft, Meta, Apple, NVIDIA, Amazon, Samsung, DeepSeek, Anthropic,
  Mistral, Perplexity, Cohere, AWS, Alibaba Cloud, Grok/xAI
- World Leaders: Trump, Xi Jinping, Putin, Modi, Macron, Merz, Erdogan, Netanyahu,
  Zelenskyy, Starmer, Yunus, MBS, and more

---

## Tier 3 — AI Image Generation (Last Resort — Only if BOTH Tier 1 and Tier 2 Failed)

Only reach this step if:
- Tier 1 returned `[OG_FAILED]` AND
- Tier 2 returned `[LIB_FAILED]`

Generate ONE clean, realistic, editorial-quality photograph that visually represents
today's news story. The photo must contain ZERO text, ZERO logos, and ZERO graphics.
It is a pure photograph only — all text and branding is handled by the HTML template.

---

## The Golden Rule
The photo must look like it came from Reuters, AP, or Bloomberg.
It should feel like a real photographer captured a real moment — not AI-generated.

---

## How to Decide What to Photograph — The 5-Question Framework

Before writing any prompt, answer these 5 questions about the news story:

### Question 1 — What is the core ACTION or EVENT?
(e.g. a company launched something, a court ruled, a deal was signed, a model was released)

### Question 2 — Who or What is the SUBJECT?
(e.g. a person category like "engineer", a device like "a server", a place like "a courtroom")

### Question 3 — What EMOTION or ATMOSPHERE does this story carry?
(e.g. tension → darker tones, optimism → clean bright light, seriousness → formal environment)

### Question 4 — What single image would a Reuters photographer take at this moment?
(Think: what would appear on the front page of a newspaper illustrating this story?)

### Question 5 — Is a major recognizable company or person central to this story?

**[MANDATORY RULE]:** If a well-known tech company is at the center of the story (e.g., Google, OpenAI, Apple), you **MUST** include their **recognizable physical environment, product, or iconic setting** in the image. 
You are **BANNED** from using generic fallback images (like "server racks", "laptops", or "meeting rooms") when a specific company is the main subject.

Think like a Reuters photographer: they don't photograph logos, but they also don't photograph generic server rooms if the story is about Google. They photograph the **building, the campus, the hardware, the specific product** that people visually associate with that exact company.

**Recognizable Visual Cues (use when relevant):**

| Company | What to show instead of logo |
|---------|------------------------------|
| Apple | Apple Park (circular spaceship building), minimalist product on clean surface |
| Google | Googleplex campus with colorful modern architecture, Android robot statue garden |
| NVIDIA | Close-up of a high-end GPU/graphics card, green-tinted server infrastructure |
| Microsoft | Redmond campus exterior, Surface device on executive desk |
| Meta | VR headset (Quest) resting on a clean desk, virtual reality lab |
| OpenAI | Ultra-clean minimalist research lab, white modern office interior |
| Anthropic | Quiet, thoughtful research workspace, warm-lit modern office |
| Amazon/AWS | Massive warehouse interior, rows of server racks at scale |
| Tesla | Electric vehicle on manufacturing floor, Gigafactory interior |
| Samsung | Semiconductor fabrication clean room, folding phone on display |
| Any Government | Formal government building exterior, courtroom interior, legislative chamber |

**If the company is NOT in the table above**, apply the same principle:
photograph their **most iconic physical object, place, or product** — never their logo or name.

**If no specific company is central**, skip Q5 and use Q1-Q4 only.

Your answers to these 5 questions define your image subject.

---

## Prompt Construction Rules

Build the prompt in this structure:

```
A high-end editorial photograph of [ANSWER TO Q2 — the subject].
[ANSWER TO Q5 — if applicable, include recognizable visual environment/product].
[ANSWER TO Q1+Q3 — scene description that reflects the event and atmosphere].
[Camera/lighting details: natural light, shallow depth of field, realistic].
Shot as if by a Reuters or AP photojournalist.
Grayscale. Clean composition. One clear focal point.
STRICTLY NO TEXT. NO LOGOS. NO WATERMARKS. NO GRAPHICS. NO OVERLAID ELEMENTS.
Pure raw editorial photograph only.
```

---

## 5-Question Examples in Practice

### Example A — OpenAI Model Launch Story
- Q1: A major AI lab released a new language model
- Q2: A researcher working at a computer in a lab environment
- Q3: Calm, focused, technical — clean bright office
- Q4: Close-up of hands on a keyboard, clean desk, shallow DOF
- Q5: OpenAI → ultra-clean minimalist research lab, white modern office interior

**Generated Prompt:**
```
A high-end editorial photograph of a researcher's hands typing carefully on a
modern laptop in an ultra-clean, minimalist white research office.
Calm, focused atmosphere. Natural window light from the side.
Shallow depth of field, neutral surfaces.
Shot as if by a Reuters or AP photojournalist.
Grayscale. Clean composition. One clear focal point.
STRICTLY NO TEXT. NO LOGOS. NO WATERMARKS. NO GRAPHICS.
Pure raw editorial photograph only.
```

---

### Example B — Patent Lawsuit / Legal Story
- Q1: A tech company was sued over intellectual property
- Q2: A formal legal setting — documents, a gavel, a desk
- Q3: Serious, weighty, institutional
- Q4: A judge's gavel resting beside legal papers on a formal desk

**Generated Prompt:**
```
A high-end editorial photograph of a wooden judge's gavel resting beside a stack
of formal legal documents on a polished wooden desk in a quiet institutional setting.
Serious, composed atmosphere. Soft directional light. Shallow depth of field.
Shot as if by a Reuters or AP photojournalist.
Grayscale. Clean composition. One clear focal point.
STRICTLY NO TEXT. NO LOGOS. NO WATERMARKS. NO GRAPHICS.
Pure raw editorial photograph only.
```

---

### Example C — Data Center / Infrastructure Story
- Q1: A cloud company is expanding its server infrastructure
- Q2: Server racks inside a data center
- Q3: Industrial, large-scale, precise
- Q4: A corridor of server racks, clean and ordered

**Generated Prompt:**
```
A high-end editorial photograph of a long corridor of modern server racks inside
a large, clean enterprise data center. Ordered rows of equipment, cool ambient light
from indicator panels, wide angle perspective showing scale.
Shot as if by a Reuters or AP photojournalist.
Grayscale. Clean composition. One clear focal point.
STRICTLY NO TEXT. NO LOGOS. NO WATERMARKS. NO GRAPHICS.
Pure raw editorial photograph only.
```

---

### Example D — Regulation / Government Policy Story
- Q1: A government body announced new AI regulation
- Q2: An official-looking building or formal meeting room
- Q3: Authoritative, institutional, deliberate
- Q4: Exterior of a government building, or suited figures in a meeting room (no faces)

**Generated Prompt:**
```
A high-end editorial photograph of the exterior of a formal government building
with clean stone architecture and steps. Overcast natural light, empty foreground,
strong geometry. Serious and institutional atmosphere.
Shot as if by a Reuters or AP photojournalist.
Grayscale. Clean composition. One clear focal point.
STRICTLY NO TEXT. NO LOGOS. NO WATERMARKS. NO GRAPHICS.
Pure raw editorial photograph only.
```

---

### Example E — Startup Funding Story
- Q1: A startup raised a large funding round
- Q2: A modern startup office, or two people in a clean meeting setting (no faces)
- Q3: Energetic but focused, professional
- Q4: A clean modern desk with open laptops, empty chairs, whiteboard in background

**Generated Prompt:**
```
A high-end editorial photograph of a modern startup workspace — clean desks,
open laptops, a whiteboard with diagrams in the background. Bright, open atmosphere.
Natural daylight. No people visible, environment only.
Shot as if by a Reuters or AP photojournalist.
Grayscale. Clean composition. One clear focal point.
STRICTLY NO TEXT. NO LOGOS. NO WATERMARKS. NO GRAPHICS.
Pure raw editorial photograph only.
```

---

### Example F — NVIDIA Chip Announcement (Q5 in Action)
- Q1: NVIDIA announced a next-generation AI chip
- Q2: A high-end GPU / graphics card
- Q3: Powerful, cutting-edge, industrial precision
- Q4: Close-up of the actual hardware, clean industrial setting
- Q5: NVIDIA → close-up of a high-end GPU, green-tinted server infrastructure

**Generated Prompt:**
```
A high-end editorial photograph of a modern high-end GPU graphics card
resting on a clean anti-static surface inside a server infrastructure room
with subtle green ambient lighting from indicator panels.
Powerful, precise, industrial atmosphere. Macro lens detail on the chip.
Shot as if by a Reuters or AP photojournalist.
Grayscale. Clean composition. One clear focal point.
STRICTLY NO TEXT. NO LOGOS. NO WATERMARKS. NO GRAPHICS.
Pure raw editorial photograph only.
```

---

## Permanent Visual Rules — Never Break These

| Never Include | Why |
|---------------|-----|
| Any text in the photo | Text lives in HTML only |
| Any logo or watermark | Branding lives in HTML only |
| Glowing or neon elements | Not editorial |
| Humanoid robots or sci-fi figures | Cliché, not our aesthetic |
| Blue matrix code or holograms | Overused, banned |
| Abstract shapes or illustrations | Photography only |
| Multiple competing subjects | One subject, one focal point |
| Busy or cluttered backgrounds | Clean composition always |

---

## Quality Checklist Before Moving to DESIGN Step
- [ ] Does the photo directly relate to the story without being cliché?
- [ ] Is there exactly one clear focal point?
- [ ] Is the background clean and uncluttered?
- [ ] Is there zero text, zero logo, zero watermark in the image?
- [ ] Does it look like it could have been taken by a real photojournalist?

If any answer is No — regenerate before proceeding.

---

## After Generating the Image
Note the full absolute path of the saved image.
Pass it to `update_content.py` as the `--image` argument in the DESIGN step.
