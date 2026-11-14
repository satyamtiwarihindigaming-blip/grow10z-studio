import os, json, asyncio
from playwright.async_api import async_playwright

chunks = [
    # Beat 1
    {"start": 0.0, "end": 3.2, "text": "अयोध्या का भव्य राजदरबार...", "hl": "भव्य राजदरबार"},
    {"start": 3.2, "end": 6.8, "text": "चारों राजकुमारों की बाल-लीला!", "hl": "चारों राजकुमार"},

    # Beat 2
    {"start": 7.0, "end": 10.4, "text": "तपस्या और महाक्रोध के प्रतीक...", "hl": "तपस्या"},
    {"start": 10.4, "end": 14.2, "text": "महर्षि विश्वामित्र का अचानक आगमन!", "hl": "विश्वामित्र का आगमन"},

    # Beat 3 (Vishwamitra)
    {"start": 14.4, "end": 18.2, "text": "मारीच-सुबाहु ने यज्ञ विध्वंस किया...", "hl": "यज्ञ विध्वंस"},
    {"start": 18.2, "end": 22.4, "text": "राक्षसों के संहार हेतु मुझे राम चाहिए!", "hl": "मुझे राम चाहिए"},

    # Beat 4 (Dasharatha's grief)
    {"start": 22.8, "end": 26.4, "text": "मुनिवर! मेरे राम अभी सुकुमार बालक हैं...", "hl": "सुकुमार बालक"},
    {"start": 26.4, "end": 30.2, "text": "मेरे प्राण ले लीजिए, पर राम को नहीं!", "hl": "मेरे प्राण ले लीजिए"},

    # Beat 5 (Shri Ram & Lakshman)
    {"start": 30.5, "end": 34.0, "text": "स्वयं मर्यादा पुरुषोत्तम श्रीराम...", "hl": "प्रभु श्रीराम"},
    {"start": 34.0, "end": 37.4, "text": "आगे बढ़कर महर्षि के चरण स्पर्श किए!", "hl": "चरण स्पर्श"},

    # Beat 6 (Heroic March)
    {"start": 37.7, "end": 41.2, "text": "हाथों में कोदण्ड धनुष लिए दोनों वीर...", "hl": "कोदण्ड धनुष"},
    {"start": 41.2, "end": 44.8, "text": "सरयू तट से धर्म-रक्षा हेतु प्रस्थान!", "hl": "धर्म-रक्षा हेतु प्रस्थान"},

    # Beat 7 (Cliffhanger)
    {"start": 45.0, "end": 50.8, "text": "अगला भाग: राक्षसी ताड़का का संहार!", "hl": "ताड़का का संहार"}
]

out_dir = "studio_ramayana/episodes/ep002/captions_v2"
os.makedirs(out_dir, exist_ok=True)
events = []

for i, ch in enumerate(chunks):
    events.append({
        "id": i,
        "start": ch["start"],
        "end": ch["end"],
        "png": f"{out_dir}/chunk_{i}.png"
    })

with open("studio_ramayana/episodes/ep002/caption_events_v2.json", "w", encoding="utf-8") as f:
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
                margin: 0; padding: 0;
                width: 1000px; height: 260px;
                display: flex; align-items: center; justify-content: center;
                background: transparent;
                font-family: 'Nirmala UI', 'Yatra One', 'Arial Unicode MS', sans-serif;
              }}
              .badge {{
                background: linear-gradient(135deg, rgba(35, 10, 15, 0.94), rgba(15, 5, 25, 0.96));
                border: 3.5px solid #FFD700;
                box-shadow: 0 0 25px rgba(255, 215, 0, 0.55), inset 0 0 15px rgba(255, 180, 0, 0.35);
                border-radius: 40px;
                padding: 16px 45px;
                max-width: 880px;
                text-align: center;
              }}
              .txt {{
                font-size: 44px;
                font-weight: 800;
                color: #FFFFFF;
                line-height: 1.35;
                text-shadow: 0 4px 12px rgba(0,0,0,0.95);
                letter-spacing: 0.5px;
              }}
              .hl {{
                color: #FFE066;
                text-shadow: 0 0 16px rgba(255, 215, 0, 0.9), 0 2px 6px #000000;
                font-weight: 900;
              }}
            </style>
            </head>
            <body>
              <div class="badge">
                <div class="txt">{styled}</div>
              </div>
            </body>
            </html>
            """
            await page.set_content(content)
            await page.screenshot(path=f"{out_dir}/chunk_{i}.png", omit_background=True)
            
        await browser.close()
        print(f"Generated {len(chunks)} kinetic caption pills for Ep 002!")

asyncio.run(render_kinetic())
