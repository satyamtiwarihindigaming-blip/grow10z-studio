import json

with open("studio_ramayana/episodes/ep005/timeline.json", "r", encoding="utf-8") as f:
    tl = json.load(f)

for item in tl:
    item["wav_path"] = f"studio_ramayana/episodes/ep005/audio_lines/line_{item['idx']:02d}.wav"

with open("studio_ramayana/episodes/ep005/timeline.json", "w", encoding="utf-8") as f:
    json.dump(tl, f, ensure_ascii=False, indent=2)

print("Updated timeline paths to local ep005/audio_lines successfully!")
