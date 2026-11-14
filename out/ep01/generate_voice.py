import os, json
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro
from pedalboard import Pedalboard, Compressor, HighpassFilter, LowpassFilter, Gain, Limiter, Reverb

kokoro = Kokoro("models/kokoro-v1.0.onnx", "models/voices-v1.0.bin")
SR = 24000

def fx_narration(x):
    board = Pedalboard([
        HighpassFilter(70),
        Compressor(threshold_db=-20, ratio=2.5),
        Reverb(room_size=0.25, wet_level=0.12, dry_level=0.9),
        Gain(2.0),
        Limiter(-1.0)
    ])
    return board(np.asarray(x, dtype=np.float32).reshape(1, -1), SR)[0]

def fx_tension(x):
    board = Pedalboard([
        HighpassFilter(80),
        Compressor(threshold_db=-22, ratio=3.0),
        Reverb(room_size=0.5, wet_level=0.22, dry_level=0.85),
        Gain(2.2),
        Limiter(-1.0)
    ])
    return board(np.asarray(x, dtype=np.float32).reshape(1, -1), SR)[0]

lines = [
    {"id": "L1", "text": "रात के ग्यारह बजे… रोहन की आख़िरी बस छूटने ही वाली थी। बस में सिर्फ़ एक ही सवारी थी, एक बूढ़ी अम्मा।", "fx": "narration", "pause_after": 0.35},
    {"id": "L2", "text": "अम्मा ने उसकी तरफ़ देखा और बोलीं, रोहन… आ गया बेटा? रोहन चौंक गया। उसने तो अपना नाम किसी को बताया ही नहीं था।", "fx": "tension", "pause_after": 0.45},
    {"id": "L3", "text": "अम्मा ने एक टिफ़िन उसके हाथ में थमाया और धीरे से कहा, घर पहुँचने से पहले इसे मत खोलना।", "fx": "tension", "pause_after": 0.50},
    {"id": "L4_a", "text": "फिर बस रुकी। अम्मा उतर गईं। रोहन ने खिड़की से बाहर देखा… और उसका दिल बैठ गया।", "fx": "narration", "pause_after": 0.85},
    {"id": "L4_b", "text": "वहाँ कोई गाँव था ही नहीं।", "fx": "tension", "pause_after": 0.70},
    {"id": "L5", "text": "आगे क्या होगा? कल बताता हूँ। कमेंट में अपना अंदाज़ा लिखो।", "fx": "narration", "pause_after": 0.80}
]

timeline = []
full_audio = []
current_time = 0.0

for item in lines:
    txt = item["text"]
    raw_s, sr = kokoro.create(txt, voice="hm_omega", speed=0.92, lang="hi")
    
    if item["fx"] == "tension":
        proc_s = fx_tension(raw_s)
    else:
        proc_s = fx_narration(raw_s)
    
    dur = len(proc_s) / SR
    start_t = current_time
    end_t = start_t + dur
    
    # Word level distribution
    words = txt.replace("…", " ").replace("।", " ").replace("?", " ").replace(",", " ").split()
    total_chars = sum(len(w) for w in words)
    w_t = start_t
    w_list = []
    for w in words:
        w_dur = dur * (len(w) / max(1, total_chars))
        w_list.append({
            "word": w,
            "start": round(w_t, 3),
            "end": round(w_t + w_dur, 3)
        })
        w_t += w_dur
        
    timeline.append({
        "id": item["id"],
        "text": txt,
        "start": round(start_t, 3),
        "end": round(end_t, 3),
        "words": w_list
    })
    
    full_audio.append(proc_s)
    current_time += dur
    
    # Pause
    pause_samples = int(item["pause_after"] * SR)
    full_audio.append(np.zeros(pause_samples, dtype=np.float32))
    current_time += item["pause_after"]

full_audio_arr = np.concatenate(full_audio)
out_wav = "out/ep01/voice/full_voice.wav"
sf.write(out_wav, full_audio_arr, SR)

timeline_data = {
    "sample_rate": SR,
    "total_duration": round(current_time, 3),
    "lines": timeline
}

with open("out/ep01/voice/voice_timeline.json", "w", encoding="utf-8") as f:
    json.dump(timeline_data, f, ensure_ascii=False, indent=2)

print(f"Generated {out_wav}: duration {current_time:.2f}s, {len(timeline)} segments")
