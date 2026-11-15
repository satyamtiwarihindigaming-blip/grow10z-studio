import json
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE_DIR = Path(".").resolve()
FONTS_DIR = BASE_DIR / "fonts"

font_yatra = (FONTS_DIR / "YatraOne-Regular.ttf").as_uri()
font_noto = (FONTS_DIR / "NotoSansDevanagari-Bold.ttf").as_uri()
font_rozha = (FONTS_DIR / "RozhaOne-Regular.ttf").as_uri()

COMMON_CSS = f"""
@font-face {{
  font-family: 'Yatra One';
  src: url('{font_yatra}') format('truetype');
}}
@font-face {{
  font-family: 'Rozha One';
  src: url('{font_rozha}') format('truetype');
}}
@font-face {{
  font-family: 'Noto Sans Devanagari';
  src: url('{font_noto}') format('truetype');
  font-weight: bold;
}}
"""

def generate_word_by_word_captions_from_timeline(timeline, captions_dir):
    captions_dir = Path(captions_dir)
    captions_dir.mkdir(parents=True, exist_ok=True)
    word_events = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 980, "height": 160})

        for item in timeline:
            line_idx = item["idx"]
            words = item["words"]
            line_dur = item["dur"]
            line_start = item["start"]
            
            char_counts = [max(1, len(w)) for w in words]
            total_chars = sum(char_counts)
            w_durs = [(c / total_chars) * line_dur for c in char_counts]

            current_w_start = line_start

            for w_idx in range(len(words)):
                w_dur = w_durs[w_idx]
                w_start = current_w_start
                w_end = w_start + w_dur
                if w_idx == len(words) - 1:
                    w_end = max(w_end, item.get("next_start", w_end))
                current_w_start = w_end

                word_spans = []
                for j, w in enumerate(words):
                    if j == w_idx:
                        word_spans.append(f"<span class='word active'>{w}</span>")
                    else:
                        word_spans.append(f"<span class='word idle'>{w}</span>")

                html_content = " ".join(word_spans)
                html = f"""
                <!DOCTYPE html>
                <html>
                <head>
                <meta charset="utf-8">
                <style>
                  {COMMON_CSS}
                  body {{
                    margin: 0; padding: 0; background: transparent; overflow: hidden;
                  }}
                  .badge {{
                    width: 980px;
                    height: 160px;
                    background: linear-gradient(135deg, rgba(20, 8, 14, 0.95), rgba(10, 4, 12, 0.96), rgba(30, 10, 18, 0.95));
                    border: 4px solid #f5c641;
                    border-radius: 32px;
                    box-shadow: 0 12px 35px rgba(0,0,0,0.9), inset 0 0 18px rgba(245,198,65,0.35);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    position: relative;
                    box-sizing: border-box;
                    padding: 14px 32px;
                  }}
                  .inner-border {{
                    position: absolute;
                    top: 6px; left: 6px; right: 6px; bottom: 6px;
                    border: 1.5px solid rgba(255, 235, 140, 0.55);
                    border-radius: 26px;
                    pointer-events: none;
                  }}
                  .caption-text {{
                    font-family: 'Noto Sans Devanagari', 'Yatra One', sans-serif;
                    font-weight: bold;
                    text-align: center;
                    line-height: 1.35;
                  }}
                  .word {{
                    display: inline-block;
                    margin: 0 6px;
                  }}
                  .idle {{
                    color: rgba(255, 255, 255, 0.85);
                    font-size: 42px;
                    text-shadow: 0 2px 4px rgba(0,0,0,0.8);
                  }}
                  .active {{
                    color: #ffe066;
                    font-size: 50px;
                    font-weight: 900;
                    text-shadow: 0 0 20px #ffcc00, 0 0 35px #ff9900, 0 4px 8px rgba(0,0,0,0.9);
                    transform: translateY(-2px) scale(1.08);
                  }}
                </style>
                </head>
                <body>
                  <div class="badge">
                    <div class="inner-border"></div>
                    <div class="caption-text">{html_content}</div>
                  </div>
                </body>
                </html>
                """
                page.set_content(html)
                out_file = captions_dir / f"line_{line_idx:02d}_word_{w_idx:02d}.png"
                page.screenshot(path=str(out_file), omit_background=True)

                word_events.append({
                    "line_idx": line_idx,
                    "word_idx": w_idx,
                    "word": words[w_idx],
                    "start": w_start,
                    "end": w_end,
                    "img_path": str(out_file)
                })

        browser.close()
    return word_events

if __name__ == "__main__":
    with open("scratch/ep005_timeline.json", "r", encoding="utf-8") as f:
        tl = json.load(f)
    events = generate_word_by_word_captions_from_timeline(tl, "studio_ramayana/episodes/ep005/captions_v2")
    with open("studio_ramayana/episodes/ep005/caption_events.json", "w", encoding="utf-8") as f:
        json.dump(events, f, ensure_ascii=False, indent=2)
    print(f"Generated {len(events)} word-by-word caption frames perfectly synced!")
