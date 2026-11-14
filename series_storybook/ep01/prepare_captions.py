import os, json, asyncio
from playwright.async_api import async_playwright

with open("series_storybook/ep01/voice/voice_timeline.json", "r", encoding="utf-8") as f:
    timeline = json.load(f)

caption_events = []
html_items = []

for item in timeline:
    idx = item["index"]
    text = item["text"]
    start = item["start"]
    end = item["end"]
    
    caption_events.append({
        "id": idx,
        "start": start,
        "end": end,
        "png": f"series_storybook/ep01/captions/sub_{idx}.png"
    })
    
    styled_text = text
    # Yellow / Crimson highlights on folklore keywords
    for word in ["तीन चेहरे", "झाँकना मना था", "अपना चेहरा", "औरत खड़ी थी", "पीछे मत देखना", "गलती कर दी", "मुस्कुरा रहा था", "तुम्हारा था"]:
        if word in styled_text:
            styled_text = styled_text.replace(word, f"<span class='hl'>{word}</span>")
            
    html_items.append((idx, styled_text, item["speaker"]))

with open("series_storybook/ep01/caption_events.json", "w", encoding="utf-8") as f:
    json.dump(caption_events, f, ensure_ascii=False, indent=2)

async def render_all():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1000, "height": 300})
        
        for idx, text_html, spk in html_items:
            border_color = "#e53935" if spk == "hf_alpha" else "#c5a059"
            content = f"""
            <!DOCTYPE html>
            <html>
            <head>
            <meta charset="utf-8">
            <style>
                body {{
                    margin: 0;
                    padding: 20px;
                    background: transparent;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                }}
                .box {{
                    background: rgba(12, 16, 26, 0.92);
                    border: 3px solid {border_color};
                    border-radius: 20px;
                    padding: 16px 36px;
                    text-align: center;
                    box-shadow: 0 10px 35px rgba(0,0,0,0.9);
                }}
                .text {{
                    font-family: 'FreeSans', 'Segoe UI', 'Nirmala UI', sans-serif;
                    font-size: 42px;
                    font-weight: 800;
                    color: #f7eedb;
                    line-height: 1.35;
                    text-shadow: 2px 2px 8px rgba(0,0,0,0.9);
                }}
                .hl {{
                    color: #ffd055;
                    text-shadow: 0 0 16px rgba(255, 208, 85, 0.85);
                }}
            </style>
            </head>
            <body>
                <div class="box">
                    <div class="text">{text_html}</div>
                </div>
            </body>
            </html>
            """
            await page.set_content(content)
            box = await page.query_selector(".box")
            await box.screenshot(path=f"series_storybook/ep01/captions/sub_{idx}.png", omit_background=True)
            
        await browser.close()

asyncio.run(render_all())
print("All Storybook Ep 01 subtitle sprites generated!")
