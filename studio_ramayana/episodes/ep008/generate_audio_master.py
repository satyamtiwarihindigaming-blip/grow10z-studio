import os
import sys
import json
import math
import subprocess
from pathlib import Path
import numpy as np
import soundfile as sf
import asyncio
import edge_tts

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
EP_DIR = BASE_DIR / "studio_ramayana" / "episodes" / "ep008"
AUDIO_LINES_DIR = EP_DIR / "audio_lines"
AUDIO_LINES_DIR.mkdir(parents=True, exist_ok=True)

SR = 44100

sys.path.insert(0, str(BASE_DIR))
from reference_code.sfx_library import gasp, breath, gulp, thump, place

def safe_add(target, buf, idx):
    if idx < 0 or idx >= len(target):
        return
    fit_len = min(len(buf), len(target) - idx)
    target[idx:idx + fit_len] += buf[:fit_len]

def synth_sub_bass(start_t, dur=2.5, f_start=85.0, f_end=32.0, amp=0.8):
    samples = int(dur * SR)
    t = np.linspace(0, dur, samples, False)
    freq = np.linspace(f_start, f_end, samples)
    phase = 2 * np.pi * np.cumsum(freq) / SR
    env = np.exp(-t * 2.2)
    sig = amp * env * np.sin(phase) + 0.3 * amp * env * np.sin(2 * phase)
    return int(start_t * SR), sig.astype(np.float32)

def synth_temple_gong(start_t, dur=7.0, amp=0.7):
    samples = int(dur * SR)
    t = np.linspace(0, dur, samples, False)
    env = np.exp(-t * 0.45)
    sig = (
        0.50 * np.sin(2 * np.pi * 110.0 * t) +
        0.30 * np.sin(2 * np.pi * 164.8 * t) +
        0.15 * np.sin(2 * np.pi * 220.0 * t) +
        0.05 * np.sin(2 * np.pi * 440.0 * t)
    ) * env * amp
    return int(start_t * SR), sig.astype(np.float32)

def synth_divine_chime(start_t, dur=4.0, freq=432.0, amp=0.45):
    samples = int(dur * SR)
    t = np.linspace(0, dur, samples, False)
    env = np.exp(-t * 1.2)
    sig = (
        0.6 * np.sin(2 * np.pi * freq * t) +
        0.3 * np.sin(2 * np.pi * freq * 2 * t) +
        0.1 * np.sin(2 * np.pi * freq * 3 * t)
    ) * env * amp
    return int(start_t * SR), sig.astype(np.float32)

def synth_celestial_hum(start_t, dur=5.0, amp=0.5):
    samples = int(dur * SR)
    t = np.linspace(0, dur, samples, False)
    env = np.sin(np.pi * (t / dur)) ** 1.5
    f0 = 216.0
    sig = (
        0.45 * np.sin(2 * np.pi * f0 * t) +
        0.35 * np.sin(2 * np.pi * (f0 * 1.5) * t) +
        0.20 * np.sin(2 * np.pi * (f0 * 2.0) * t)
    ) * env * amp
    return int(start_t * SR), sig.astype(np.float32)

LINES_DATA = [
    {
        "id": "line_00",
        "text": "परशुराम का परशु उठा... और मिथिला की सभा में सन्नाटा छा गया!",
        "rate": "+6%",
        "pitch": "-2Hz"
    },
    {
        "id": "line_01",
        "text": "जैसे ही लक्ष्मण पर वार होने को हुआ... मर्यादा पुरुषोत्तम श्रीराम बीच में आ गए!",
        "rate": "+4%",
        "pitch": "+0Hz"
    },
    {
        "id": "line_02",
        "text": "श्रीराम ने हाथ जोड़कर कहा: 'हे मुनिवर! बालक अबोध है, सारा दोष मेरा है। जो दंड देना है, मुझे दीजिए।'",
        "rate": "+2%",
        "pitch": "+1Hz"
    },
    {
        "id": "line_03",
        "text": "परशुराम ने ललकारते हुए दिव्य वैष्णव धनुष आगे किया: 'यदि तुम वीर हो, तो इस शारंग पर प्रत्यंचा चढ़ाओ!'",
        "rate": "+4%",
        "pitch": "-2Hz"
    },
    {
        "id": "line_04",
        "text": "श्रीराम ने मुस्कुराते हुए महा-धनुष थामा... और पलक झपकते ही बाण चढ़ा दिया!",
        "rate": "+4%",
        "pitch": "+1Hz"
    },
    {
        "id": "line_05",
        "text": "धनुष खिंचते ही परशुराम का सारा तेज विलीन हो गया! वो हाथ जोड़कर नतमस्तक हो गए!",
        "rate": "+3%",
        "pitch": "-1Hz"
    },
    {
        "id": "line_06",
        "text": "अगले भाग में देखिए: भव्य श्रीराम-सीता विवाह! फॉलो करें @grow10z",
        "rate": "+6%",
        "pitch": "+0Hz"
    }
]

def build_audio_master():
    durations = {}
    for item in LINES_DATA:
        wav_path = AUDIO_LINES_DIR / f"{item['id']}.wav"
        data, _ = sf.read(str(wav_path))
        durations[item["id"]] = len(data) / SR
        print(f"   {item['id']} len = {durations[item['id']]:.2f}s")

    voice_offsets = []
    current_time = 0.50
    for i, item in enumerate(LINES_DATA):
        lid = item["id"]
        voice_offsets.append((f"{lid}.wav", current_time))
        pause = 1.30 if lid == "line_03" else 0.85
        current_time += durations[lid] + pause

    # Ensure full tail for final reverberation
    total_duration = math.ceil(current_time + 4.5)
    total_samples = int(total_duration * SR)
    print(f"🎵 Master Audio Duration calculated: {total_duration:.2f}s ({total_samples} samples)")

    master = np.zeros(total_samples, dtype=np.float32)
    sfx_layer = np.zeros(total_samples, dtype=np.float32)
    dialogue_layer = np.zeros(total_samples, dtype=np.float32)

    # 1. Background Mystic Tanpura Drone (D2 Root)
    t_full = np.linspace(0, total_duration, total_samples, False)
    d_root = 73.42
    drone = (
        0.35 * np.sin(2 * np.pi * d_root * t_full) +
        0.25 * np.sin(2 * np.pi * (d_root * 1.5) * t_full) +
        0.15 * np.sin(2 * np.pi * (d_root * 2.0) * t_full) +
        0.10 * np.sin(2 * np.pi * (d_root * 3.0) * t_full)
    )
    drone = drone * (0.85 + 0.15 * np.sin(2 * np.pi * 0.2 * t_full)) * 0.20

    # 0 dB Silence Vacuum when Shri Ram grasps the Vaishnava bow
    line_04_start = [vo[1] for vo in voice_offsets if vo[0] == "line_04.wav"][0]
    silence_start = line_04_start - 0.9
    silence_end = line_04_start + 0.3
    silence_mask = (t_full >= silence_start) & (t_full <= silence_end)
    drone[silence_mask] = 0.0
    master += drone.astype(np.float32)

    timeline_records = []
    for fn, start_sec in voice_offsets:
        wav_path = AUDIO_LINES_DIR / fn
        data, _ = sf.read(str(wav_path))
        dur = len(data) / SR
        end_sec = start_sec + dur
        idx = int(start_sec * SR)
        safe_add(dialogue_layer, data, idx)
        timeline_records.append({
            "file": fn,
            "start": round(start_sec, 2),
            "end": round(end_sec, 2),
            "duration": round(dur, 2)
        })
        print(f"   ▶ {fn}: {start_sec:.2f}s -> {end_sec:.2f}s (dur={dur:.2f}s)")

    with open(EP_DIR / "timeline.json", "w", encoding="utf-8") as f:
        json.dump(timeline_records, f, indent=2)

    # 2. Human Reactions & Foley
    print("🎭 Layering organic human reactions...")
    # Reaction 1: Suspense Inhale at 0.1s
    place(sfx_layer, breath("in", amp=0.35), 0.1)
    
    # Reaction 2: Crowd terror gasp & sub bass at line_00 end / line_01 start
    l0_end = voice_offsets[0][1] + durations["line_00"]
    place(sfx_layer, gasp(amp=0.55), l0_end + 0.1)
    place(sfx_layer, gulp(amp=0.45), l0_end + 0.3)
    idx, buf = synth_sub_bass(l0_end + 0.2, dur=2.8, f_start=95.0, f_end=35.0, amp=0.75)
    safe_add(sfx_layer, buf, idx)

    # Reaction 3: Serene breath & divine chime before Shri Ram speaks (line_02)
    l1_end = voice_offsets[1][1] + durations["line_01"]
    place(sfx_layer, breath("in", amp=0.30), l1_end + 0.2)
    idx, buf = synth_divine_chime(l1_end + 0.3, dur=4.0, freq=432.0, amp=0.40)
    safe_add(sfx_layer, buf, idx)

    # Reaction 4: Metallic bow hum when Vaishnava bow appears (line_03)
    l3_start = voice_offsets[3][1]
    place(sfx_layer, thump(f0=140, f1=70, d=0.35, amp=0.5), l3_start - 0.4)
    idx, buf = synth_celestial_hum(l3_start - 0.3, dur=5.0, amp=0.45)
    safe_add(sfx_layer, buf, idx)

    # Reaction 5: Deep heartbeat thump before Ram touches the bow
    place(sfx_layer, thump(f0=80, f1=38, d=0.5, amp=0.7), silence_start + 0.2)

    # Reaction 6: Blinding Cosmic Aura release when arrow is strung (line_04 climax)
    l4_mid = voice_offsets[4][1] + durations["line_04"] * 0.65
    idx, buf = synth_sub_bass(l4_mid, dur=3.5, f_start=110.0, f_end=32.0, amp=0.88)
    safe_add(sfx_layer, buf, idx)
    idx, buf = synth_divine_chime(l4_mid + 0.1, dur=5.5, freq=528.0, amp=0.55)
    safe_add(sfx_layer, buf, idx)

    # Reaction 7: Grand Temple Gong Tail at end
    l6_end = voice_offsets[6][1] + durations["line_06"]
    idx, buf = synth_temple_gong(l6_end - 0.5, dur=6.5, amp=0.80)
    safe_add(sfx_layer, buf, idx)

    master += sfx_layer
    master = master * 0.70 + dialogue_layer * 0.95

    # Soft Limiter
    max_peak = np.max(np.abs(master))
    if max_peak > 0.95:
        master = np.tanh(master / max_peak * 0.95)

    out_master = EP_DIR / "audio_master.wav"
    sf.write(str(out_master), master, SR, subtype='PCM_16')
    print(f"🎉 EP008 AUDIO MASTER READY: {out_master} (Duration: {len(master)/SR:.2f}s)")
    return total_duration

if __name__ == "__main__":
    dur = build_audio_master()
    print(f"Final Audio Master Duration: {dur:.2f}s")
