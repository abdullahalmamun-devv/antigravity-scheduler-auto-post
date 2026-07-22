# IMAGE_GEN.md — How to Generate Today's Hero Photograph

## Your Goal
Generate ONE clean, realistic, editorial-quality photograph that visually represents
today's news story. The photo must contain ZERO text, ZERO logos, and ZERO graphics.
It is a pure photograph only — all text and branding is handled by the HTML template.

---

## The Golden Rule
The photo must look like it came from Reuters, AP, or Bloomberg.
It should feel like a real photographer captured a real moment — not AI-generated.

---

## How to Decide What to Photograph — The 4-Question Framework

Before writing any prompt, answer these 4 questions about the news story:

### Question 1 — What is the core ACTION or EVENT?
(e.g. a company launched something, a court ruled, a deal was signed, a model was released)

### Question 2 — Who or What is the SUBJECT?
(e.g. a person category like "engineer", a device like "a server", a place like "a courtroom")

### Question 3 — What EMOTION or ATMOSPHERE does this story carry?
(e.g. tension → darker tones, optimism → clean bright light, seriousness → formal environment)

### Question 4 — What single image would a Reuters photographer take at this moment?
(Think: what would appear on the front page of a newspaper illustrating this story?)

Your answers to these 4 questions define your image subject. Use that — not a preset table.

---

## Prompt Construction Rules

Build the prompt in this structure:

```
A high-end editorial photograph of [ANSWER TO Q2 — the subject].
[ANSWER TO Q1+Q3 — scene description that reflects the event and atmosphere].
[Camera/lighting details: natural light, shallow depth of field, realistic].
Shot as if by a Reuters or AP photojournalist.
Grayscale. Clean composition. One clear focal point.
STRICTLY NO TEXT. NO LOGOS. NO WATERMARKS. NO GRAPHICS. NO OVERLAID ELEMENTS.
Pure raw editorial photograph only.
```

---

## 4-Question Examples in Practice

### Example A — AI Model Launch Story
- Q1: A major AI lab released a new language model
- Q2: A researcher working at a computer in a lab environment
- Q3: Calm, focused, technical — clean bright office
- Q4: Close-up of hands on a keyboard, clean desk, shallow DOF

**Generated Prompt:**
```
A high-end editorial photograph of a researcher's hands typing carefully on a
modern laptop in a clean, well-lit research office. Calm, focused atmosphere.
Natural window light from the side. Shallow depth of field, neutral surfaces.
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
