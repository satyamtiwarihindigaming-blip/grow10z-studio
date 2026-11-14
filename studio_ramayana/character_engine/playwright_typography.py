"""
GROW10Z — Flawless HarfBuzz Devanagari Typography Engine
Uses Playwright + Chromium to guarantee 100% shaped, beautiful Hindi & Sanskrit typography.
ZERO TOFU BOXES (□□□). Perfect conjuncts, matras, golden text gradients, and drop shadows.
"""

import os
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE_DIR = Path(__file__).resolve().parent.parent.parent
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

def generate_manuscript_image(title, shloka="॥ ॐ श्री गणेशाय नमः ॥", out_path=None):
    """Render ancient Sanskrit manuscript page with 100% Devanagari shaping"""
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
      {COMMON_CSS}
      body {{
        margin: 0; padding: 0; width: 1080px; height: 1920px;
        background: #0c0812;
        display: flex; align-items: center; justify-content: center;
        overflow: hidden;
      }}
      .sheet {{
        width: 940px;
        height: 1560px;
        background: linear-gradient(135deg, #f6e6b9 0%, #e4ca91 55%, #d2b278 100%);
        border-radius: 28px;
        box-shadow: 0 25px 60px rgba(0,0,0,0.85), inset 0 0 80px rgba(110,65,25,0.45);
        position: relative;
        box-sizing: border-box;
        padding: 60px;
        border: 1px solid #c2994d;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: space-between;
      }}
      .burn-vignette {{
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        border-radius: 28px;
        box-shadow: inset 0 0 100px rgba(80,35,10,0.6);
        pointer-events: none;
      }}
      .outer-border {{
        position: absolute;
        top: 25px; left: 25px; right: 25px; bottom: 25px;
        border: 5px solid #b88628;
        border-radius: 20px;
        pointer-events: none;
      }}
      .inner-border {{
        position: absolute;
        top: 38px; left: 38px; right: 38px; bottom: 38px;
        border: 2px solid #8c5d15;
        border-radius: 14px;
        pointer-events: none;
      }}
      .corner-lotus {{
        position: absolute;
        width: 28px; height: 28px;
        background: #d4a025;
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
      }}
      .corner-lotus::after {{
        content: '';
        width: 14px; height: 14px;
        background: #992211;
        border-radius: 50%;
      }}
      .tl {{ top: 25px; left: 25px; transform: translate(-50%, -50%); }}
      .tr {{ top: 25px; right: 25px; transform: translate(50%, -50%); }}
      .bl {{ bottom: 25px; left: 25px; transform: translate(-50%, 50%); }}
      .br {{ bottom: 25px; right: 25px; transform: translate(50%, 50%); }}

      .shloka {{
        font-family: 'Rozha One', 'Yatra One', serif;
        font-size: 52px;
        color: #8c1e18;
        text-shadow: 0 2px 4px rgba(255,255,255,0.4);
        margin-top: 50px;
        letter-spacing: 2px;
      }}
      .divider {{
        width: 80%;
        height: 3px;
        background: linear-gradient(90deg, transparent, #b88628, transparent);
        margin-top: 15px;
        position: relative;
      }}
      .divider::after {{
        content: '❖';
        position: absolute;
        top: -14px;
        left: 50%;
        transform: translateX(-50%);
        color: #b88628;
        font-size: 20px;
      }}
      .title-box {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        margin: auto 0;
        padding: 0 40px;
      }}
      .title-text {{
        font-family: 'Yatra One', 'Noto Sans Devanagari', sans-serif;
        font-size: 64px;
        color: #2b120c;
        line-height: 1.4;
        text-shadow: 0 2px 5px rgba(255,235,160,0.6);
      }}
      .footer {{
        font-family: 'Yatra One', 'Rozha One', serif;
        font-size: 40px;
        color: #7a3a12;
        margin-bottom: 40px;
        letter-spacing: 1.5px;
      }}
    </style>
    </head>
    <body>
      <div class="sheet">
        <div class="burn-vignette"></div>
        <div class="outer-border">
          <div class="corner-lotus tl"></div>
          <div class="corner-lotus tr"></div>
          <div class="corner-lotus bl"></div>
          <div class="corner-lotus br"></div>
        </div>
        <div class="inner-border"></div>

        <div style="display:flex; flex-direction:column; align-items:center; width:100%;">
          <div class="shloka">{shloka}</div>
          <div class="divider"></div>
        </div>

        <div class="title-box">
          <div class="title-text">{title}</div>
        </div>

        <div class="footer">॥ मर्यादा पुरुषोत्तम श्रीराम गाथा ॥</div>
      </div>
    </body>
    </html>
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1080, "height": 1920})
        page.set_content(html)
        page.screenshot(path=str(out_path))
        browser.close()


def generate_captions_batch(lines, captions_dir):
    """
    Render all kinetic caption badges in a single high-speed Chromium session.
    Guarantees 100% shaped Devanagari with zero missing glyph boxes.
    """
    captions_dir = Path(captions_dir)
    captions_dir.mkdir(parents=True, exist_ok=True)
    generated_paths = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 960, "height": 160})

        for i, item in enumerate(lines):
            text = item["text"]
            # Highlight first punchy word or name
            words = text.split(" ")
            if len(words) > 3:
                styled_text = f"<span class='active-word'>{words[0]}</span> " + " ".join(words[1:])
            else:
                styled_text = text

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
                width: 960px;
                height: 160px;
                background: linear-gradient(135deg, rgba(38,12,18,0.96), rgba(18,8,24,0.96), rgba(45,15,20,0.96));
                border: 4.5px solid #f5c641;
                border-radius: 35px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.85), inset 0 0 15px rgba(245,198,65,0.3);
                display: flex;
                align-items: center;
                justify-content: center;
                position: relative;
                box-sizing: border-box;
              }}
              .inner-border {{
                position: absolute;
                top: 6px; left: 6px; right: 6px; bottom: 6px;
                border: 1.5px solid rgba(255, 235, 140, 0.6);
                border-radius: 28px;
                pointer-events: none;
              }}
              .corner-dot {{
                position: absolute;
                width: 9px; height: 9px;
                background: #ffd750;
                border-radius: 50%;
                box-shadow: 0 0 6px #ffe580;
              }}
              .tl {{ top: 12px; left: 12px; }}
              .tr {{ top: 12px; right: 12px; }}
              .bl {{ bottom: 12px; left: 12px; }}
              .br {{ bottom: 12px; right: 12px; }}
              
              .caption-text {{
                font-family: 'Yatra One', 'Noto Sans Devanagari', sans-serif;
                font-size: 46px;
                color: #fff8e1;
                text-shadow: 0 3px 6px rgba(0,0,0,0.95), 0 0 12px rgba(245,198,65,0.4);
                text-align: center;
                padding: 0 40px;
                line-height: 1.3;
              }}
              .active-word {{
                color: #ffe066;
                text-shadow: 0 0 15px #ffcc00, 0 0 25px #ff9900;
              }}
            </style>
            </head>
            <body>
              <div class="badge">
                <div class="inner-border"></div>
                <div class="corner-dot tl"></div>
                <div class="corner-dot tr"></div>
                <div class="corner-dot bl"></div>
                <div class="corner-dot br"></div>
                <div class="caption-text">
                  {styled_text}
                </div>
              </div>
            </body>
            </html>
            """
            page.set_content(html)
            out_file = captions_dir / f"chunk_{i:02d}.png"
            page.screenshot(path=str(out_file), omit_background=True)
            generated_paths.append(str(out_file))

        browser.close()
    return generated_paths


def generate_cliffhanger_badge(out_path, title="क्या आप जानते हैं आगे क्या हुआ? 🚩", subtitle="देखिए अगले भाग में! फॉलो करें @grow10z"):
    """Render high-impact cliffhanger suspense card with zero tofu boxes"""
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
      .card {{
        width: 920px;
        height: 280px;
        background: linear-gradient(135deg, rgba(28,10,16,0.95), rgba(14,6,18,0.95), rgba(35,12,18,0.95));
        border: 4.5px solid #f5c641;
        border-radius: 28px;
        box-shadow: 0 15px 40px rgba(0,0,0,0.9), inset 0 0 20px rgba(245,198,65,0.35);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        box-sizing: border-box;
      }}
      .c1 {{
        font-family: 'Yatra One', 'Noto Sans Devanagari', sans-serif;
        font-size: 52px;
        color: #ffe066;
        text-shadow: 0 0 18px #ffcc00, 0 3px 6px rgba(0,0,0,0.9);
        margin-bottom: 12px;
      }}
      .c2 {{
        font-family: 'Noto Sans Devanagari', sans-serif;
        font-weight: bold;
        font-size: 38px;
        color: #ffffff;
        text-shadow: 0 3px 6px rgba(0,0,0,0.9);
      }}
    </style>
    </head>
    <body>
      <div class="card">
        <div class="c1">{title}</div>
        <div class="c2">{subtitle}</div>
      </div>
    </body>
    </html>
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 920, "height": 280})
        page.set_content(html)
        page.screenshot(path=str(out_path), omit_background=True)
        browser.close()


def generate_word_by_word_captions(lines, active_start, active_end, captions_dir):
    """
    Renders word-by-word active highlighted captions.
    Each spoken word lights up in glowing solar gold while surrounding words remain clean white.
    Returns a list of timed word events.
    """
    captions_dir = Path(captions_dir)
    captions_dir.mkdir(parents=True, exist_ok=True)
    
    total_time = max(0.1, active_end - active_start)
    total_words = sum(len(line["text"].split(" ")) for line in lines)
    dur_per_word = total_time / max(1, total_words)

    word_events = []
    current_time = active_start

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 980, "height": 160})

        for line_idx, line in enumerate(lines):
            words = line["text"].split(" ")
            # Render a card for each active word index in this line
            for w_idx in range(len(words)):
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

                t_start = current_time
                t_end = current_time + dur_per_word
                current_time = t_end

                word_events.append({
                    "line_idx": line_idx,
                    "word_idx": w_idx,
                    "word": words[w_idx],
                    "start": t_start,
                    "end": t_end,
                    "img_path": str(out_file)
                })

        browser.close()
    return word_events
