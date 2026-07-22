# Antigravity Scheduler Auto Post

An automated tool designed to generate high-quality graphics from an HTML template and automatically post them to a Facebook Page. Specifically tailored for tech and AI news, it uses Python, Playwright for rendering, and the Facebook Graph API for posting.

## Features

- **Automated Graphic Generation:** Converts a dynamic HTML template (`subsdrop_template.html`) into a 1080x1080 JPG graphic using Playwright (`render_graphic.py`).
- **Dynamic Content Updates:** `update_content.py` easily injects today's headline, summary, category, date, image, and credits into the template.
- **Facebook Integration:** `facebook_poster.py` securely posts the generated graphic along with a caption directly to your Facebook Page.
- **Token Management:** Includes `generate_permanent_token.py` to seamlessly convert short-lived Graph API tokens into permanent Page Access Tokens.
- **Offline Font Support:** `embed_font.py` embeds Google Fonts directly into the HTML to ensure offline rendering without external dependencies.
- **Archive Management:** Automatically moves successfully posted images to an `output/archive/` folder to keep your workspace clean.

## Prerequisites

- Python 3.8+
- Node.js (for Playwright dependencies, if applicable)
- A Facebook App and Page with Graph API access.

### Python Packages Required:
- `requests`
- `python-dotenv`
- `playwright`

Install Playwright browsers after installing the package:
```bash
playwright install chromium
```

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/abdullahalmamun-devv/antigravity-scheduler-auto-post.git
   cd antigravity-scheduler-auto-post
   ```

2. **Environment Variables (`.env`):**
   Create a `.env` file in the root directory (do not commit this file) with your Facebook credentials:
   ```env
   FACEBOOK_ACCESS_TOKEN=your_page_access_token_here
   FACEBOOK_PAGE_ID=your_facebook_page_id_here
   ```

3. **Generate Permanent Token (Optional):**
   If you only have a short-lived user token, use the included script to get a permanent token:
   ```bash
   python generate_permanent_token.py
   ```

4. **Embed Fonts (One-time Setup):**
   Ensure the HTML template has the required fonts embedded for offline rendering:
   ```bash
   python embed_font.py
   ```

## Usage

### 1. Update the Template Content
Update the HTML template with the news for the day:
```bash
python update_content.py --headline "Your Headline" --summary "A short summary." --credit "Source | Date | Desk" --image "C:\\path\\to\\photo.jpg"
```
*(Optional flags: `--category` and `--date`)*

### 2. Render the Graphic
Generate the 1080x1080 JPG from the updated HTML:
```bash
python render_graphic.py
```
This will save a timestamped image in the `output/` directory.

### 3. Post to Facebook
Post the generated image to Facebook:
```bash
python facebook_poster.py --caption "Here is the full caption for the post!"
```
The script will automatically pick the most recent graphic from the `output/` folder, post it, and then archive the image.

## Scripts Overview

- `facebook_poster.py`: Handles the actual posting to the Facebook Page via Graph API.
- `generate_permanent_token.py`: Exchanges short-lived tokens for long-lived/permanent page tokens.
- `render_graphic.py`: Uses Playwright to render `subsdrop_template.html` to a JPG.
- `update_content.py`: Modifies the HTML template with new content.
- `embed_font.py`: Downloads and base64-encodes the Inter font into the HTML for offline use.
- `post_now.py` / `post_today.py`: Driver scripts containing example content for quick posting.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
