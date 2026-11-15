import asyncio
import json
import os
import subprocess
import soundfile as sf
import edge_tts

async def measure_rates():
    with open("studio_ramayana/episodes/episodes_database.json", "r", encoding="utf-8") as f:
        db = json.load(f)
    ep5 = [ep for ep in db if ep["id"] == "EP005"][0]
    lines = ep5["script_lines"]
    
    for rate_str in ["+0%", "+6%", "+10%"]:
        sr = 44100
        current_time = 3.6
        for i, line in enumerate(lines):
            fn_mp3 = f"scratch/test_r_{i}.mp3"
            voice = "hi-IN-MadhurNeural"
            rate = rate_str
            pitch = "-3Hz" if line["speaker"] == "janak" else "-1Hz"
            comm = edge_tts.Communicate(line["text"], voice=voice, rate=rate, pitch=pitch)
            await comm.save(fn_mp3)
            fn_wav = fn_mp3.replace(".mp3", ".wav")
            subprocess.run(["ffmpeg", "-y", "-i", fn_mp3, "-ar", str(sr), "-ac", "1", fn_wav],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            data, _ = sf.read(fn_wav)
            dur = len(data) / sr
            current_time += dur + (0.45 if i in [1, 3, 5, 7, 9] else 0.35)
            if os.path.exists(fn_mp3): os.remove(fn_mp3)
            if os.path.exists(fn_wav): os.remove(fn_wav)
        print(f"Rate {rate_str} -> Total speech end: {current_time:.2f}s | Video total: {current_time + 3.0:.2f}s")

asyncio.run(measure_rates())
