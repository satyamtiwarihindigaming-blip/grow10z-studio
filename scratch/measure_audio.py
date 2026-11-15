import asyncio
import json
import os
import subprocess
import numpy as np
import soundfile as sf
import edge_tts

async def measure_lines():
    with open("studio_ramayana/episodes/episodes_database.json", "r", encoding="utf-8") as f:
        db = json.load(f)
    ep5 = [ep for ep in db if ep["id"] == "EP005"][0]
    lines = ep5["script_lines"]
    
    os.makedirs("scratch/ep005_audio_test", exist_ok=True)
    sr = 44100
    timeline = []
    
    current_time = 3.8 # start after 3.8s manuscript intro
    
    for i, line in enumerate(lines):
        fn_mp3 = f"scratch/ep005_audio_test/line_{i:02d}.mp3"
        fn_wav = f"scratch/ep005_audio_test/line_{i:02d}.wav"
        
        # Janak has a deeper voice / different pitch or rate
        voice = "hi-IN-MadhurNeural"
        rate = "-2%" if line["speaker"] == "janak" else "+0%"
        pitch = "-4Hz" if line["speaker"] == "janak" else "-1Hz"
        
        comm = edge_tts.Communicate(line["text"], voice=voice, rate=rate, pitch=pitch)
        await comm.save(fn_mp3)
        
        subprocess.run(["ffmpeg", "-y", "-i", fn_mp3, "-ar", str(sr), "-ac", "1", fn_wav],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        
        data, _ = sf.read(fn_wav)
        dur = len(data) / sr
        
        t_start = current_time
        t_end = t_start + dur
        pause = 0.55 if i in [1, 3, 5, 7, 9] else 0.40 # dramatic pause between scene shifts
        current_time = t_end + pause
        
        words = line["text"].split()
        
        timeline.append({
            "idx": i,
            "speaker": line["speaker"],
            "text": line["text"],
            "words": words,
            "dur": dur,
            "start": t_start,
            "end": t_end,
            "next_start": current_time,
            "wav_path": fn_wav
        })
        print(f"Line {i:02d} ({line['speaker']}): {dur:.2f}s | Start: {t_start:.2f}s -> End: {t_end:.2f}s")
        
    print(f"\nTotal speech finished at: {t_end:.2f}s")
    total_video_dur = t_end + 3.2 # cliffhanger hold
    print(f"Total video duration will be: {total_video_dur:.2f}s")
    
    with open("scratch/ep005_timeline.json", "w", encoding="utf-8") as f:
        json.dump(timeline, f, ensure_ascii=False, indent=2)

asyncio.run(measure_lines())
