import subprocess
from PIL import Image

timestamps = [2.0, 10.0, 25.0, 40.0, 58.0, 75.0]
frames = []

for i, t in enumerate(timestamps):
    out_jpg = f"studio_ramayana/episodes/ep005/clean_f{i+1}.jpg"
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

# Build 3x2 Contact Sheet
W, H = 540, 960
sheet = Image.new("RGB", (W * 3, H * 2), (10, 10, 10))

for idx, f_path in enumerate(frames):
    img = Image.open(f_path).resize((W, H), Image.Resampling.LANCZOS)
    col = idx % 3
    row = idx // 3
    sheet.paste(img, (col * W, row * H))

sheet_path = "studio_ramayana/episodes/ep005/ep005_clean_contact_sheet.jpg"
sheet.save(sheet_path, quality=92)
sheet.save("C:/Users/LENOVO/.gemini/antigravity/brain/f2ebddc4-8c1b-498e-b760-53e53a5b9bcf/ep005_clean_contact_sheet.jpg", quality=92)
print("✅ Clean contact sheet built successfully!")
