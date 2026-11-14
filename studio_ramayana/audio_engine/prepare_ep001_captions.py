import os, json, asyncio
from playwright.async_api import async_playwright

with open("studio_ramayana/episodes/ep001/voice/voice_timeline.json", "r", encoding="utf-8") as f:
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
        "png": f"studio_ramayana/episodes/ep001/captions/sub_{idx}.png"
    })
    
    styled_text = text
    # Golden divine highlights on Ramayana sacred keywords
    for word in ["चैत्र मास", "अयोध्या", "सूर्योदय", "महाराज दशरथ", "स्वयं नारायण", "नील कमल", "मंद मुस्कान", "फूलों की वर्षा", "दिव्य दुंदुभी", "प्रभु श्रीराम", "विश्वामित्र"]:
        if word in styled_text:
            styled_text = styled_text.replace(word, f"<span class='hl'>{word}</span>")
            
    html_items.append((idx, styled_text, item["speaker"]))

with open("studio_ramayana/episodes/ep001/caption_events.json", "w", encoding="utf-8") as f:
    json.dump(caption_events, f, ensure_ascii=False, indent=2)

async def render_all():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1000, "height": 300})
        
        for idx, text_html, spk in html_items:
            border_color = "#ffb300" if spk == "hm_psi" else "#ffd700"
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
                    background: rgba(14, 18, 32, 0.94);
                    border: 3px solid {border_color};
                    border-radius: 22px;
                    padding: 18px 40px;
                    text-align: center;
                    box-shadow: 0 10px 40px rgba(255, 180, 0, 0.35);
                }}
                .text {{
                    font-family: 'FreeSans', 'Segoe UI', 'Nirmala UI', sans-serif;
                    font-size: 42px;
                    font-weight: 800;
                    color: #ffffff;
                    line-height: 1.35;
                    text-shadow: 2px 2px 8px rgba(0,0,0,0.95);
                }}
                .hl {{
                    color: #ffe066;
                    text-shadow: 0 0 18px rgba(255, 224, 102, 0.95);
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
            await box.screenshot(path=f"studio_ramayana/episodes/ep001/captions/sub_{idx}.png", omit_background=True)
            
        await browser.close()

asyncio.run(render_all())
print("All Ramayana Ep 001 subtitle sprites generated!")
