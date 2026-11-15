import subprocess
from PIL import Image

timestamps = [2.0, 12.0, 30.0, 48.0, 70.0, 88.0]
frames = []

for i, t in enumerate(timestamps):
    out_jpg = f"studio_ramayana/episodes/ep005/verify_f{i+1}.jpg"
    cmd = [
        "ffmpeg", "-y",
        "-ss", str(t),
        "-i", "studio_ramayana/episodes/ep005/ep005_final.mp4",
        "-vframes", "1",
        "-q:v", "2",
        out_jpg
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    frames.append(out_jpg)
    print(f"Extracted Frame {i+1} at {t}s: {out_jpg}")

# Build 3x2 Contact Sheet
W, H = 540, 960 # half-size thumbnails
sheet = Image.new("RGB", (W * 3, H * 2), (10, 10, 10))

for idx, f_path in enumerate(frames):
    img = Image.open(f_path).resize((W, H), Image.Resampling.LANCZOS)
    col = idx % 3
    row = idx // 3
    sheet.paste(img, (col * W, row * H))

sheet_path = "studio_ramayana/episodes/ep005/ep005_fixed_contact_sheet.jpg"
sheet.save(sheet_path, quality=92)
print(f"✅ Contact sheet saved: {sheet_path}")

# Also copy to artifact directory
sheet.save("C:/Users/LENOVO/.gemini/antigravity/brain/f2ebddc4-8c1b-498e-b760-53e53a5b9bcf/ep005_fixed_contact_sheet.jpg", quality=92)
