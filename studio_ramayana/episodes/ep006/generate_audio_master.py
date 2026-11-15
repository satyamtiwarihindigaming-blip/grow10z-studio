import os
import sys
import json
import math
import subprocess
from pathlib import Path
import numpy as np
import soundfile as sf

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
EP_DIR = Path(__file__).resolve().parent

SR = 44100

# Accurate Shot & Voice Cue Timing (in seconds)
# Shot 1: 0.0 to 5.2s (Hook & Snap, voice 0.4s to 4.94s)
# Shot 2: 5.2 to 9.5s (Royal Court shockwave, voice 5.3s to 9.28s)
# Shot 3: 9.5 to 16.5s (Real India Map & Mahendra Parvat, voice 9.6s to 16.13s)
# Shot 4: 16.5 to 22.8s (Legend of 21 Battles & Parashu Axe, voice 16.6s to 22.53s)
# Shot 5: 22.8 to 27.0s (Tempest Entrance, voice 22.9s to 26.72s)
# Shot 6: 27.0 to 32.0s (Parashurama Roar, voice 27.2s to 31.66s)
# Shot 7: 32.0 to 40.5s (0 dB Silence & Laxman Smirk, voice 32.2s to 40.0s)
# Shot 8: 40.5 to 49.5s (Standoff & Cliffhanger, voice 40.8s to 48.82s)

TOTAL_DURATION = 49.5
TOTAL_SAMPLES = int(TOTAL_DURATION * SR)

def synth_sub_bass(start_t, dur=2.5, f_start=85.0, f_end=32.0, amp=0.8):
    samples = int(dur * SR)
    t = np.linspace(0, dur, samples, False)
    freq = np.linspace(f_start, f_end, samples)
    phase = 2 * np.pi * np.cumsum(freq) / SR
    env = np.exp(-t * 2.2)
    sig = amp * env * np.sin(phase)
    # Add slight 2nd harmonic saturation
    sig += 0.3 * amp * env * np.sin(2 * phase)
    return int(start_t * SR), sig.astype(np.float32)

def synth_metallic_snap(start_t, dur=1.2, amp=0.9):
    samples = int(dur * SR)
    t = np.linspace(0, dur, samples, False)
    # Multi-frequency metallic resonant crack
    env = np.exp(-t * 12.0)
    sig = (
        0.5 * np.sin(2 * np.pi * 1850 * t) +
        0.3 * np.sin(2 * np.pi * 3200 * t) +
        0.2 * np.sin(2 * np.pi * 5600 * t) +
        0.4 * (np.random.rand(samples) * 2 - 1)
    ) * env * amp
    return int(start_t * SR), sig.astype(np.float32)

def synth_earthquake_rumble(start_t, dur=4.0, amp=0.5):
    samples = int(dur * SR)
    t = np.linspace(0, dur, samples, False)
    # Low frequency rumble 35-55 Hz with random modulation
    noise = np.random.randn(samples)
    # Simple low pass via moving average
    kernel_size = 80
    kernel = np.ones(kernel_size) / kernel_size
    smoothed = np.convolve(noise, kernel, mode='same')
    env = np.sin(np.pi * (t / dur)) ** 0.8
    sig = (0.6 * np.sin(2 * np.pi * 42.0 * t) + 0.4 * smoothed) * env * amp
    return int(start_t * SR), sig.astype(np.float32)

def synth_singing_bowl(start_t, dur=6.0, freq=432.0, amp=0.45):
    samples = int(dur * SR)
    t = np.linspace(0, dur, samples, False)
    env = np.exp(-t * 0.6)
    sig = (
        0.6 * np.sin(2 * np.pi * freq * t) +
        0.25 * np.sin(2 * np.pi * freq * 2.76 * t) +
        0.15 * np.sin(2 * np.pi * freq * 5.4 * t)
    ) * env * amp
    return int(start_t * SR), sig.astype(np.float32)

def synth_radar_ping(start_t, dur=1.5, freq=1100.0, amp=0.5):
    samples = int(dur * SR)
    t = np.linspace(0, dur, samples, False)
    env = np.exp(-t * 4.5)
    sig = np.sin(2 * np.pi * freq * t) * env * amp
    return int(start_t * SR), sig.astype(np.float32)

def synth_shankh_blast(start_t, dur=4.5, amp=0.55):
    samples = int(dur * SR)
    t = np.linspace(0, dur, samples, False)
    env = np.sin(np.pi * (t / dur)) ** 1.6
    base_f = 275.0 + 12.0 * np.sin(2 * np.pi * 0.5 * t)
    sig = (
        0.45 * np.sin(2 * np.pi * base_f * t) +
        0.30 * np.sin(2 * np.pi * base_f * 2 * t) +
        0.15 * np.sin(2 * np.pi * base_f * 3 * t) +
        0.10 * np.sin(2 * np.pi * base_f * 4 * t)
    ) * env * amp
    return int(start_t * SR), sig.astype(np.float32)

def synth_sword_ring(start_t, dur=3.0, amp=0.4):
    samples = int(dur * SR)
    t = np.linspace(0, dur, samples, False)
    env = np.exp(-t * 1.5)
    sig = (
        0.6 * np.sin(2 * np.pi * 2400 * t) +
        0.3 * np.sin(2 * np.pi * 4820 * t) +
        0.1 * np.sin(2 * np.pi * 7200 * t)
    ) * env * amp
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

def mix_into(master, start_idx, buffer, volume=1.0):
    end_idx = min(len(master), start_idx + len(buffer))
    clip_len = end_idx - start_idx
    if clip_len > 0:
        master[start_idx:end_idx] += buffer[:clip_len] * volume

def build_audio_master():
    print(f"🎵 Synthesizing EP006 Audio Master ({TOTAL_DURATION}s @ {SR}Hz)...")
    master = np.zeros(TOTAL_SAMPLES, dtype=np.float32)
    sfx_layer = np.zeros(TOTAL_SAMPLES, dtype=np.float32)

    # 1. Tanpura / Mystic Drone throughout, with 0 dB vacuum at 32.0s - 34.5s
    t_full = np.linspace(0, TOTAL_DURATION, TOTAL_SAMPLES, False)
    d_root = 73.42 # D2 note
    drone = (
        0.35 * np.sin(2 * np.pi * d_root * t_full) +
        0.25 * np.sin(2 * np.pi * (d_root * 1.5) * t_full) +
        0.15 * np.sin(2 * np.pi * (d_root * 2.0) * t_full) +
        0.10 * np.sin(2 * np.pi * (d_root * 3.0) * t_full)
    )
    drone_mod = 0.85 + 0.15 * np.sin(2 * np.pi * 0.2 * t_full)
    drone = drone * drone_mod * 0.22

    # Apply 0 dB Silence Vacuum during Laxman's step (32.0s to 35.0s)
    silence_mask = (t_full >= 32.0) & (t_full <= 35.0)
    drone[silence_mask] = 0.0

    master += drone.astype(np.float32)

    # 2. SFX Cues Placement
    print("💥 Generating and placing cinematic SFX events...")
    # Shot 1 Snap & Sub-Bass
    idx, buf = synth_sub_bass(0.05, dur=3.0, amp=0.85)
    mix_into(sfx_layer, idx, buf)
    idx, buf = synth_metallic_snap(0.05, dur=1.2, amp=0.90)
    mix_into(sfx_layer, idx, buf)

    # Shot 2 Earthquake Rumble
    idx, buf = synth_earthquake_rumble(5.2, dur=4.2, amp=0.60)
    mix_into(sfx_layer, idx, buf)
    idx, buf = synth_sub_bass(5.3, dur=2.5, amp=0.55)
    mix_into(sfx_layer, idx, buf)

    # Shot 3 Singing Bowl & Radar Ping
    idx, buf = synth_singing_bowl(9.5, dur=6.5, freq=432.0, amp=0.45)
    mix_into(sfx_layer, idx, buf)
    idx, buf = synth_radar_ping(12.5, dur=2.0, freq=980.0, amp=0.40)
    mix_into(sfx_layer, idx, buf)

    # Shot 4 War Shankh Blast & Axe Clash
    idx, buf = synth_shankh_blast(16.5, dur=5.0, amp=0.55)
    mix_into(sfx_layer, idx, buf)
    idx, buf = synth_sub_bass(16.8, dur=2.2, amp=0.70)
    mix_into(sfx_layer, idx, buf)

    # Shot 5 Tempest / Heavy Stride
    idx, buf = synth_earthquake_rumble(22.8, dur=4.0, amp=0.50)
    mix_into(sfx_layer, idx, buf)

    # Shot 6 Roar of Divine Wrath Sub-Bass Swell
    idx, buf = synth_sub_bass(27.0, dur=4.5, f_start=95.0, f_end=40.0, amp=0.75)
    mix_into(sfx_layer, idx, buf)

    # Shot 7 Sword Sheath Ring after silence (at 35.2s)
    idx, buf = synth_sword_ring(35.2, dur=3.5, amp=0.45)
    mix_into(sfx_layer, idx, buf)

    # Shot 8 Climactic Riser, Sub-Bass Drop & Temple Gong Tail
    idx, buf = synth_sub_bass(40.5, dur=3.0, amp=0.85)
    mix_into(sfx_layer, idx, buf)
    idx, buf = synth_temple_gong(40.6, dur=8.5, amp=0.75)
    mix_into(sfx_layer, idx, buf)

    master += sfx_layer

    # 3. Voice Lines Placement
    voice_dir = EP_DIR / "audio_lines"
    voice_offsets = [
        ("line_00_fast.wav", 0.40),
        ("line_01_fast.wav", 5.30),
        ("line_02_fast.wav", 9.60),
        ("line_03_fast.wav", 16.60),
        ("line_04_fast.wav", 22.90),
        ("line_05_fast.wav", 27.20),
        ("line_06_fast.wav", 32.20),
        ("line_07_fast.wav", 40.80),
    ]

    print("🎙️ Mixing dialogue tracks with precise sync offsets...")
    dialogue_layer = np.zeros(TOTAL_SAMPLES, dtype=np.float32)
    timeline_records = []

    for fn, start_sec in voice_offsets:
        wav_path = voice_dir / fn
        if not wav_path.exists():
            raise FileNotFoundError(f"Missing voice track: {wav_path}")
        data, v_sr = sf.read(str(wav_path))
        if v_sr != SR:
            raise ValueError(f"Sample rate mismatch: {v_sr} != {SR}")
        dur = len(data) / SR
        end_sec = start_sec + dur
        idx = int(start_sec * SR)
        mix_into(dialogue_layer, idx, data, volume=1.0)
        timeline_records.append({
            "file": fn,
            "start": round(start_sec, 2),
            "end": round(end_sec, 2),
            "duration": round(dur, 2)
        })
        print(f"   ▶ {fn}: {start_sec:.2f}s -> {end_sec:.2f}s (dur={dur:.2f}s)")

    # Save timeline.json for accurate frame rendering sync
    timeline_path = EP_DIR / "timeline.json"
    with open(timeline_path, "w", encoding="utf-8") as f:
        json.dump(timeline_records, f, indent=2)
    print(f"✅ Saved timeline to {timeline_path}")

    # Combine Dialogue + Master SFX/Music
    # Normalize dialogue slightly to sit nicely in the mix
    master = master * 0.70 + dialogue_layer * 0.95

    # Peak Limiter / Soft Clipping
    max_peak = np.max(np.abs(master))
    if max_peak > 0.95:
        print(f"⚠️ Peak level {max_peak:.2f} exceeds 0.95, applying soft mastering limiter...")
        master = np.tanh(master / max_peak * 0.95)

    out_wav = EP_DIR / "audio_master.wav"
    sf.write(str(out_wav), master, SR, subtype='PCM_16')
    print(f"🎉 MASTER AUDIO EXPORTED: {out_wav} (Duration: {len(master)/SR:.2f}s)")

if __name__ == "__main__":
    build_audio_master()
