import os, json, asyncio
from playwright.async_api import async_playwright

with open("out/ep03/voice/voice_timeline.json", "r", encoding="utf-8") as f:
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
        "png": f"out/ep03/captions/sub_{idx}.png"
    })
    
    # Yellow suspense highlight on hook words
    styled_text = text
    for word in ["रात", "दो बज", "सौ पार", "मूसलाधार बारिश", "दिल", "हथौड़े", "फ़र्श पर फेंका", "बस रोको", "भारी पर्दा", "ज़मीन खिसक गई", "घूम रहा था", "बिल्कुल खाली", "एक सौ बीस", "सफ़ेद शॉल", "घूरते दिखी", "ज़िंदा", "सब्सक्राइब"]:
        if word in styled_text:
            styled_text = styled_text.replace(word, f"<span class='hl'>{word}</span>")
            
    html_items.append((idx, styled_text))

with open("out/ep03/caption_events.json", "w", encoding="utf-8") as f:
    json.dump(caption_events, f, ensure_ascii=False, indent=2)

async def render_all():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1000, "height": 300})
        
        for idx, text_html in html_items:
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
                    background: rgba(8, 12, 22, 0.88);
                    border: 3px solid #ffcc00;
                    border-radius: 20px;
                    padding: 16px 36px;
                    text-align: center;
                    box-shadow: 0 8px 32px rgba(0,0,0,0.85);
                }}
                .text {{
                    font-family: 'FreeSans', 'Segoe UI', 'Nirmala UI', sans-serif;
                    font-size: 44px;
                    font-weight: 800;
                    color: #ffffff;
                    line-height: 1.35;
                    text-shadow: 2px 2px 8px rgba(0,0,0,0.9);
                }}
                .hl {{
                    color: #ffea00;
                    text-shadow: 0 0 16px rgba(255, 234, 0, 0.8);
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
            await box.screenshot(path=f"out/ep03/captions/sub_{idx}.png", omit_background=True)
            
        await browser.close()

asyncio.run(render_all())
print("All Ep 03 subtitle sprites generated via Playwright Chromium!")
