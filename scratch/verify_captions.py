import json
import os

with open("studio_ramayana/episodes/ep005/caption_events.json", "r", encoding="utf-8") as f:
    events = json.load(f)

missing = 0
for ev in events:
    if not os.path.exists(ev["img_path"]):
        missing += 1

print(f"Total events: {len(events)}, Missing image files: {missing}")
