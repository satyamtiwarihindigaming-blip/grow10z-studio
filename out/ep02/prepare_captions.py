import os, json
from playwright.sync_api import sync_playwright

timeline = json.load(open("out/ep02/voice/voice_timeline.json", encoding="utf-8"))

caption_events = []

for line in timeline["lines"]:
    words = line["words"]
    chunk_size = 4
    for i in range(0, len(words), chunk_size):
        chunk_words = words[i:i+chunk_size]
        for active_idx, target_w in enumerate(chunk_words):
            event = {
                "chunk_id": f"{line['id']}_{i//chunk_size}_{active_idx}",
                "start": target_w["start"],
                "end": target_w["end"],
                "chunk_words": [w["word"] for w in chunk_words],
                "active_index": active_idx
            }
            caption_events.append(event)

with open("out/ep02/captions/caption_events.json", "w", encoding="utf-8") as f:
    json.dump(caption_events, f, ensure_ascii=False, indent=2)

print(f"Total caption events: {len(caption_events)}")

html_template = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {
    margin: 0;
    padding: 0;
    background: transparent;
    display: flex;
    justify-content: center;
    align-items: center;
    width: 1080px;
    height: 220px;
  }
  .caption-box {
    background: rgba(10, 14, 28, 0.85);
    padding: 16px 36px;
    border-radius: 24px;
    border: 2px solid rgba(255, 214, 64, 0.4);
    display: inline-flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 14px;
    max-width: 960px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.7);
  }
  .word {
    font-family: 'Segoe UI', 'Noto Sans Devanagari', 'Nirmala UI', sans-serif;
    font-size: 58px;
    font-weight: 800;
    color: #F8F9FA;
    text-shadow: 0 2px 8px rgba(0,0,0,0.9);
  }
  .active {
    color: #FFD640;
    transform: scale(1.08);
    text-shadow: 0 0 16px rgba(255, 214, 64, 0.8), 0 2px 8px rgba(0,0,0,0.9);
  }
</style>
</head>
<body>
  <div class="caption-box" id="box">
    %WORDS%
  </div>
</body>
</html>
"""

p = sync_playwright().start()
browser = p.chromium.launch()
page = browser.new_page(viewport={"width": 1080, "height": 220})

for ev in caption_events:
    words_html = []
    for idx, w in enumerate(ev["chunk_words"]):
        cls = "word active" if idx == ev["active_index"] else "word"
        words_html.append(f'<span class="{cls}">{w}</span>')
    content = html_template.replace("%WORDS%", "".join(words_html))
    page.set_content(content)
    out_png = f"out/ep02/captions/{ev['chunk_id']}.png"
    box = page.locator("#box")
    page.screenshot(path=out_png, omit_background=True)

browser.close()
p.stop()
print("Episode 2 caption sprites rendered successfully!")
