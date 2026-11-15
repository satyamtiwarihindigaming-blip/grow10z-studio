import os
import subprocess
from pathlib import Path
import skia

EP_DIR = Path("studio_ramayana/episodes/ep006")
video_file = EP_DIR / "ep006_final.mp4"
shots_dir = EP_DIR / "final_frames"
shots_dir.mkdir(parents=True, exist_ok=True)

timestamps = [2.5, 7.0, 13.0, 19.5, 25.0, 29.5, 36.0, 45.0]
frame_paths = []

for i, ts in enumerate(timestamps):
    out_f = shots_dir / f"shot_{i+1:02d}.jpg"
    subprocess.run([
        "ffmpeg", "-y",
        "-ss", str(ts),
        "-i", str(video_file),
        "-vframes", "1",
        "-q:v", "2",
        str(out_f)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    frame_paths.append(out_f)
    print(f"Extracted shot {i+1} at {ts}s: {out_f}")

# Build 1920x1080 contact sheet (4 cols x 2 rows)
cs_w, cs_h = 1920, 1080
surf = skia.Surface(cs_w, cs_h)
cv = surf.getCanvas()
cv.clear(skia.ColorSetARGB(255, 12, 8, 16))

thumb_w, thumb_h = 440, 480
pad_x, pad_y = 32, 40

for idx, fpath in enumerate(frame_paths):
    img = skia.Image.MakeFromEncoded(skia.Data.MakeFromFileName(str(fpath)))
    col = idx % 4
    row = idx // 4
    x = pad_x + col * (thumb_w + 24)
    y = pad_y + row * (thumb_h + 30)
    dest = skia.Rect(x, y, x + thumb_w, y + thumb_h)
    cv.drawImageRect(img, dest)
    cv.drawRect(dest, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=2.5, Color=skia.ColorSetARGB(255, 235, 185, 55), AntiAlias=True))

contact_sheet_path = EP_DIR / "ep006_final_contact_sheet.jpg"
final_img = surf.makeImageSnapshot()
final_img.save(str(contact_sheet_path), skia.kJPEG)
print(f"✅ Contact sheet created at {contact_sheet_path}")
