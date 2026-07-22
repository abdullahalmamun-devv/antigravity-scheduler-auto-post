# BANNED.md — Hard Rules. Never Break These.

## Read this before producing any output. No exceptions. No special cases.

---

## POST CAPTION — BANNED

| Banned | Reason |
|--------|--------|
| Any emoji | Professional publication. Zero emojis. |
| Exclamation marks `!` | No hype. Calm authority only. |
| "Game-changing" | Cliché. Permanently banned. |
| "Revolutionary" | Overused. Permanently banned. |
| "In a world where..." | Generic AI opener. Never use. |
| "It's worth noting" | Filler. Cut it. |
| "Let's dive in" / "Dive deep" | Casual. Unprofessional. |
| "Groundbreaking" | Cliché. Banned. |
| "Exciting" / "Amazing" | Too casual. Banned. |
| Bullet points in caption | Flowing paragraphs only. |
| Numbered lists in caption | Same as above. |
| More than 5 hashtags | Looks spammy. Hard limit: 5. |
| `#tech` `#news` `#viral` `#trending` | Too generic. Use specific hashtags. |
| Copying original article headline | Always rewrite. Always. |
| Posting a story older than 48 hours | Verify dates before writing. |
| Making up facts | Only use what was found in research. |

---

## PHOTOGRAPH — BANNED

| Banned | Reason |
|--------|--------|
| Text baked into the photograph | All text lives in HTML only. |
| Logos baked into the photograph | Same rule. |
| SubsDrop branding inside the photo | Brand lives in HTML, never in the image. |
| Glowing circuit boards | Overused AI visual cliché. |
| Humanoid robot imagery | Overused AI visual cliché. |
| Neon / cyberpunk aesthetics | Not our brand. |
| Hacker in a dark hoodie | Banned cybersecurity cliché. |
| AI-generated likeness of a real named person | Legal and ethical risk. |
| Abstract or fantasy imagery | Editorial photography only. |
| Generic fallbacks for company news | If the story is about a specific company (e.g. Google), do NOT use generic images (like standard server racks). You MUST use their specific recognizable visual cue (see IMAGE_GEN.md Q5). |
| Multiple competing subjects in one photo | One subject, one emotion, one focal point. |

### PHOTOGRAPH — ALLOWED (Do Not Confuse With Banned Items Above)

The following ARE allowed and encouraged when the story is about a recognizable company:

| Allowed | Why |
|---------|-----|
| Recognizable company buildings (e.g. Apple Park, Googleplex) | These are physical environments, not logos. Reuters photographers use them. |
| Real products on a clean surface (e.g. GPU, VR headset, phone) | Products are editorial subjects, not branding. |
| Company campus exteriors or interiors | Gives story-specific visual context. |
| Manufacturing facilities, clean rooms, labs | Industry-specific environments that tell the story. |

**The rule is simple:** Photograph what a Reuters photographer would photograph at the scene — buildings, hardware, environments. Never photograph a logo, text, or watermark.

---

## DESIGN — BANNED

| Banned | Reason |
|--------|--------|
| Modifying the HTML template's CSS or layout | Design is permanently locked. |
| Changing the font family | Inter is locked. Never swap it. |
| Changing the background color | `#f4f3f0` is locked. |
| Changing the accent/highlight color | `#b91d22` is locked. |
| Removing the SubsDrop brand name | Brand is mandatory. Always top-right. |
| Centering the brand name | It lives on the right side. Always. |
| More than 2 highlighted phrases in headline | Default is 1. Max is 2. |
| Highlighting the entire headline | Only 2-3 key words get highlighted. |
| Adding badges, ribbons, or corner tags | Not in the component system. Banned. |
| Adding bullet/icon feature strips | Not in the component system. Banned. |
| Adding social media follow bars | Not in the component system. Banned. |
| Posting without rendering the final graphic | Photo is mandatory every single time. |
| Running render before running update_content | Always update content first. |

---

## CONSISTENCY — BANNED

| Banned | Reason |
|--------|--------|
| Skipping the daily log save | Logs track every post. Required. |
| Posting without a confirmed Post ID from API | Always verify success response. |
| Reposting a story already published | Check `agent/logs/` before selecting a story. |
| Changing schedule or posting time | Only the user changes the schedule. |
| Stopping halfway through the 7-step cycle | Complete all steps every time. |

---

## If Uncertain
Default to: **restraint over addition, quality over speed, less over more.**
Do not add anything not described in your instruction files.
