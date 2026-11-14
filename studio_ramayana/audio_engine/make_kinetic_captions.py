import os, json, asyncio
from playwright.async_api import async_playwright

# Break long sentences into natural 3-6 word punchy cinematic chunks
chunks = [
    # Line 0
    {"start": 0.0, "end": 2.8, "text": "चैत्र मास की नवमी तिथि...", "hl": "चैत्र मास"},
    {"start": 2.8, "end": 6.4, "text": "अयोध्या में एक ऐसा सूर्योदय हुआ!", "hl": "सूर्योदय हुआ"},
    
    # Line 1
    {"start": 6.9, "end": 9.8, "text": "महाराज दशरथ के महल में...", "hl": "महाराज दशरथ"},
    {"start": 9.8, "end": 13.2, "text": "गूँज उठी वो दिव्य किलकारी!", "hl": "दिव्य किलकारी"},
    
    # Line 2 (Maharaja Dasharatha)
    {"start": 13.6, "end": 15.2, "text": "कौशल्या! देखो...", "hl": "कौशल्या"},
    {"start": 15.2, "end": 17.5, "text": "हमारे घर स्वयं नारायण पधारे हैं!", "hl": "स्वयं नारायण"},
    
    # Line 3
    {"start": 18.0, "end": 20.0, "text": "नील कमल सी कांति...", "hl": "नील कमल"},
    {"start": 20.0, "end": 22.4, "text": "विशाल नयन और वो मंद मुस्कान!", "hl": "मंद मुस्कान"},
    
    # Line 4
    {"start": 22.8, "end": 25.8, "text": "अयोध्या में फूलों की वर्षा होने लगी...", "hl": "फूलों की वर्षा"},
    {"start": 25.8, "end": 29.5, "text": "देवताओं ने आकाश से दुंदुभी बजाई!", "hl": "दुंदुभी बजाई"},
    
    # Line 5
    {"start": 30.0, "end": 33.2, "text": "मर्यादा पुरुषोत्तम प्रभु श्रीराम...", "hl": "प्रभु श्रीराम"},
    {"start": 33.2, "end": 37.0, "text": "अधर्म के अंत की पहली शुरुआत थी!", "hl": "अधर्म के अंत"},
    
    # Line 6
    {"start": 37.3, "end": 41.6, "text": "अगला भाग: विश्वामित्र का आगमन!", "hl": "विश्वामित्र का आगमन"}
]

os.makedirs("studio_ramayana/episodes/ep001/captions_v2", exist_ok=True)
events = []

for i, ch in enumerate(chunks):
    events.append({
        "id": i,
        "start": ch["start"],
        "end": ch["end"],
        "png": f"studio_ramayana/episodes/ep001/captions_v2/chunk_{i}.png"
    })

with open("studio_ramayana/episodes/ep001/caption_events_v2.json", "w", encoding="utf-8") as f:
    json.dump(events, f, ensure_ascii=False, indent=2)

async def render_kinetic():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1000, "height": 260})
        
        for i, ch in enumerate(chunks):
            styled = ch["text"]
            hl = ch["hl"]
            if hl in styled:
                styled = styled.replace(hl, f"<span class='hl'>{hl}</span>")
                
            content = f"""
            <!DOCTYPE html>
            <html>
            <head>
            <meta charset="utf-8">
            <style>
                body {{
                    margin: 0;
                    padding: 15px;
                    background: transparent;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                }}
                .pill {{
                    display: inline-block;
                    background: linear-gradient(135deg, rgba(20, 16, 28, 0.96), rgba(35, 24, 45, 0.94));
                    border: 3.5px solid #ffcc00;
                    border-radius: 40px;
                    padding: 16px 45px;
                    text-align: center;
                    box-shadow: 0 12px 35px rgba(0,0,0,0.85), 0 0 25px rgba(255, 204, 0, 0.4);
                }}
                .text {{
                    font-family: 'FreeSans', 'Segoe UI', 'Nirmala UI', sans-serif;
                    font-size: 46px;
                    font-weight: 900;
                    color: #ffffff;
                    letter-spacing: 0.5px;
                    line-height: 1.25;
                    text-shadow: 3px 3px 6px rgba(0,0,0,0.9);
                }}
                .hl {{
                    color: #ffe600;
                    text-shadow: 0 0 20px #ffbb00, 0 0 35px #ff8800;
                }}
            </style>
            </head>
            <body>
                <div class="pill">
                    <div class="text">{styled}</div>
                </div>
            </body>
            </html>
            """
            await page.set_content(content)
            pill = await page.query_selector(".pill")
            await pill.screenshot(path=f"studio_ramayana/episodes/ep001/captions_v2/chunk_{i}.png", omit_background=True)
            
        await browser.close()

asyncio.run(render_kinetic())
print("Micro-chunk kinetic subtitle sprites generated!")
