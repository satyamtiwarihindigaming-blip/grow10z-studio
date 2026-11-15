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
EP_DIR = BASE_DIR / "studio_ramayana" / "episodes" / "ep007"
AUDIO_LINES_DIR = EP_DIR / "audio_lines"
AUDIO_LINES_DIR.mkdir(parents=True, exist_ok=True)

SR = 44100
TOTAL_DURATION = 55.0
TOTAL_SAMPLES = int(TOTAL_DURATION * SR)

sys.path.insert(0, str(BASE_DIR))
from reference_code.sfx_library import gasp, breath, gulp, thump, place

def synth_sub_bass(start_t, dur=2.5, f_start=85.0, f_end=32.0, amp=0.8):
    samples = int(dur * SR)
    t = np.linspace(0, dur, samples, False)
    freq = np.linspace(f_start, f_end, samples)
    phase = 2 * np.pi * np.cumsum(freq) / SR
    env = np.exp(-t * 2.2)
    sig = amp * env * np.sin(phase) + 0.3 * amp * env * np.sin(2 * phase)
    return int(start_t * SR), sig.astype(np.float32)

def synth_temple_gong(start_t, dur=8.0, amp=0.7):
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

def build_audio_master():
    print(f"🎵 Assembling Master Audio with Zero Overlaps ({TOTAL_DURATION}s @ {SR}Hz)...")
    
    voice_offsets = [
        ("line_00.wav", 0.50),
        ("line_01.wav", 5.70),
        ("line_02.wav", 12.80),
        ("line_03.wav", 19.80),
        ("line_04.wav", 26.80),
        ("line_05.wav", 33.10),
        ("line_06.wav", 38.00),
        ("line_07.wav", 44.50)
    ]
    
    master = np.zeros(TOTAL_SAMPLES, dtype=np.float32)
    sfx_layer = np.zeros(TOTAL_SAMPLES, dtype=np.float32)

    # 1. Background Mystic Tanpura Drone (D2 Root)
    t_full = np.linspace(0, TOTAL_DURATION, TOTAL_SAMPLES, False)
    d_root = 73.42
    drone = (
        0.35 * np.sin(2 * np.pi * d_root * t_full) +
        0.25 * np.sin(2 * np.pi * (d_root * 1.5) * t_full) +
        0.15 * np.sin(2 * np.pi * (d_root * 2.0) * t_full) +
        0.10 * np.sin(2 * np.pi * (d_root * 3.0) * t_full)
    )
    drone = drone * (0.85 + 0.15 * np.sin(2 * np.pi * 0.2 * t_full)) * 0.20

    # 0 dB Silence Vacuum during Shri Ram's peaceful step (37.2s to 40.5s)
    silence_mask = (t_full >= 37.2) & (t_full <= 40.5)
    drone[silence_mask] = 0.0
    master += drone.astype(np.float32)

    dialogue_layer = np.zeros(TOTAL_SAMPLES, dtype=np.float32)
    timeline_records = []

    for fn, start_sec in voice_offsets:
        wav_path = AUDIO_LINES_DIR / fn
        data, _ = sf.read(str(wav_path))
        dur = len(data) / SR
        end_sec = start_sec + dur
        idx = int(start_sec * SR)
        end_idx = min(TOTAL_SAMPLES, idx + len(data))
        dialogue_layer[idx:end_idx] += data[:end_idx - idx]
        timeline_records.append({
            "file": fn,
            "start": round(start_sec, 2),
            "end": round(end_sec, 2),
            "duration": round(dur, 2)
        })
        print(f"   ▶ {fn}: {start_sec:.2f}s -> {end_sec:.2f}s (dur={dur:.2f}s)")

    with open(EP_DIR / "timeline.json", "w", encoding="utf-8") as f:
        json.dump(timeline_records, f, indent=2)

    # 2. Layer Natural Human Reactions & Foley
    print("🎭 Layering organic human reactions (Gasps, Inhales, Gulps, Thumps)...")
    # Reaction 1: Suspense Inhale at 0.1s
    place(sfx_layer, breath("in", amp=0.35), 0.1)
    
    # Reaction 2: Sub-bass swell & ground rumble at 5.2s before Parashurama speaks
    idx, buf = synth_sub_bass(5.2, dur=3.0, f_start=90.0, f_end=35.0, amp=0.75)
    sfx_layer[idx:idx+len(buf)] += buf
    
    # Reaction 3: Confident sharp inhale at 12.3s before Laxman smiles
    place(sfx_layer, breath("in", amp=0.30), 12.3)
    
    # Reaction 4: Metallic bow clink at 19.3s
    place(sfx_layer, thump(f0=120, f1=60, d=0.25, amp=0.4), 19.3)
    
    # Reaction 5: Collective crowd shock gasp at 26.3s!
    place(sfx_layer, gasp(amp=0.55), 26.3)
    place(sfx_layer, gulp(amp=0.45), 26.5)
    
    # Reaction 6: Thunder roar at 32.6s
    idx, buf = synth_sub_bass(32.6, dur=3.2, f_start=95.0, f_end=40.0, amp=0.80)
    sfx_layer[idx:idx+len(buf)] += buf
    
    # Reaction 7: Divine Temple Chime at 39.5s (432Hz pure peace)
    idx, buf = synth_divine_chime(39.5, dur=3.8, freq=432.0, amp=0.45)
    sfx_layer[idx:idx+len(buf)] += buf
    
    # Reaction 8: Climactic Sub-Bass Drop & Temple Gong Tail at 44.0s
    idx, buf = synth_sub_bass(44.0, dur=3.2, amp=0.85)
    sfx_layer[idx:idx+len(buf)] += buf
    idx, buf = synth_temple_gong(44.2, dur=8.5, amp=0.75)
    sfx_layer[idx:idx+len(buf)] += buf

    master += sfx_layer
    master = master * 0.70 + dialogue_layer * 0.95

    # Soft Limiter
    max_peak = np.max(np.abs(master))
    if max_peak > 0.95:
        master = np.tanh(master / max_peak * 0.95)

    out_master = EP_DIR / "audio_master.wav"
    sf.write(str(out_master), master, SR, subtype='PCM_16')
    print(f"🎉 EP007 AUDIO MASTER READY: {out_master} (Duration: {len(master)/SR:.2f}s)")

if __name__ == "__main__":
    build_audio_master()
