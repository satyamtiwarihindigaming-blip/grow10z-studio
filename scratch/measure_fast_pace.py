import asyncio
import json
import os
import subprocess
import soundfile as sf
import edge_tts

async def measure_fast_pace():
    with open("studio_ramayana/episodes/episodes_database.json", "r", encoding="utf-8") as f:
        db = json.load(f)
    ep5 = [ep for ep in db if ep["id"] == "EP005"][0]
    lines = ep5["script_lines"]
    
    os.makedirs("scratch/ep005_punchy_audio", exist_ok=True)
    sr = 44100
    timeline = []
    
    # 2.2s quick manuscript intro (punchy, fast hook, no dragging)
    current_time = 2.2 
    
    for i, line in enumerate(lines):
        fn_mp3 = f"scratch/ep005_punchy_audio/line_{i:02d}.mp3"
        fn_wav = f"scratch/ep005_punchy_audio/line_{i:02d}.wav"
        
        # Natural punchy viral speed (+12% speed for energy & suspense)
        voice = "hi-IN-MadhurNeural"
        rate = "+10%" if line["speaker"] == "janak" else "+14%"
        pitch = "-2Hz" if line["speaker"] == "janak" else "+0Hz"
        
        comm = edge_tts.Communicate(line["text"], voice=voice, rate=rate, pitch=pitch)
        await comm.save(fn_mp3)
        
        subprocess.run(["ffmpeg", "-y", "-i", fn_mp3, "-ar", str(sr), "-ac", "1", fn_wav],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        
        data, _ = sf.read(fn_wav)
        dur = len(data) / sr
        
        t_start = current_time
        t_end = t_start + dur
        # Tight, natural dialogue pauses (0.20s to 0.25s max)
        pause = 0.30 if i in [3, 5, 7, 9] else 0.20
        current_time = t_end + pause
        
        timeline.append({
            "idx": i,
            "speaker": line["speaker"],
            "text": line["text"],
            "dur": dur,
            "start": t_start,
            "end": t_end,
            "next_start": current_time,
            "wav_path": fn_wav
        })
        print(f"Line {i:02d}: {dur:.2f}s | {t_start:.2f}s -> {t_end:.2f}s")
        
    total_speech_end = t_end
    total_video_dur = total_speech_end + 2.4 # fast cliffhanger hold
    print(f"\nTotal speech end: {total_speech_end:.2f}s | Total video: {total_video_dur:.2f}s")
    
    with open("scratch/ep005_punchy_timeline.json", "w", encoding="utf-8") as f:
        json.dump(timeline, f, ensure_ascii=False, indent=2)

asyncio.run(measure_fast_pace())
