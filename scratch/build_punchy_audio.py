import json
import os
import numpy as np
import soundfile as sf

def build_punchy_cinema_audio(timeline_path, out_wav):
    with open(timeline_path, "r", encoding="utf-8") as f:
        timeline = json.load(f)
        
    sr = 44100
    total_dur = timeline[-1]["end"] + 2.4 # 83.56s
    total_samples = int(total_dur * sr)
    t = np.linspace(0, total_dur, total_samples, False)
    
    # 1. Place Voice Audio
    voice = np.zeros(total_samples, dtype=np.float32)
    voice_mask = np.zeros(total_samples, dtype=bool)
    
    for item in timeline:
        s_idx = int(item["start"] * sr)
        wav_file = item["wav_path"]
        data, _ = sf.read(wav_file)
        e_idx = min(total_samples, s_idx + len(data))
        voice[s_idx:e_idx] = data[:e_idx - s_idx]
        voice_mask[s_idx:e_idx] = True

    # 2. Warm Cinematic Prologue (0.0s to 2.2s) - Punchy & fast hook
    prologue_sub = 0.32 * np.sin(2 * np.pi * 42.0 * t) * np.clip(t / 0.8, 0, 1) * np.exp(-0.4 * t)
    
    # Sacred 432Hz Singing Bowl chime
    bowl_t = np.clip(t - 0.2, 0, total_dur)
    bowl = (
        0.28 * np.sin(2 * np.pi * 432.0 * bowl_t) +
        0.14 * np.sin(2 * np.pi * 864.0 * bowl_t)
    ) * np.exp(-0.75 * bowl_t) * (t >= 0.2)
    
    # Soft air/wind sweep
    wind_env = np.sin(np.pi * np.clip(t / 2.2, 0, 1)) ** 2 * (t <= 2.2)
    air = 0.08 * np.sin(2 * np.pi * 180 * t) * wind_env

    # 3. Sacred Tanpura Drone (Throughout video, ducked during speech)
    d2 = 73.42
    drone = (
        0.28 * np.sin(2 * np.pi * d2 * t) +
        0.22 * np.sin(2 * np.pi * (d2 * 1.5) * t) +
        0.15 * np.sin(2 * np.pi * (d2 * 2.0) * t) +
        0.10 * np.sin(2 * np.pi * (d2 * 3.0) * t)
    )
    mod = 0.85 + 0.15 * np.sin(2 * np.pi * 0.25 * t)
    drone = drone * mod * 0.18
    
    # Duck drone during voice speech
    duck_gain = np.where(voice_mask, 0.35, 1.0).astype(np.float32)
    drone *= duck_gain

    # 4. Silence Vacuum during Shri Ram's divine stride (Line 07)
    ram_stride_start = timeline[7]["start"]
    ram_stride_end = timeline[8]["start"]
    vac_mask = (t >= ram_stride_start) & (t <= ram_stride_end)
    drone[vac_mask] *= 0.05 # complete suspense silence!
    
    # Subtle heartbeat thumps during silence vacuum
    heartbeats = np.zeros(total_samples, dtype=np.float32)
    for beat_t in np.arange(ram_stride_start + 0.3, ram_stride_end - 0.3, 0.75): # ~80 bpm suspense
        idx = int(beat_t * sr)
        dur_b = min(int(0.35 * sr), total_samples - idx)
        tb = np.linspace(0, 0.35, dur_b, False)
        hb = 0.45 * np.sin(2 * np.pi * 50 * tb) * np.exp(-9.0 * tb)
        heartbeats[idx:idx+dur_b] += hb

    # 5. Climax Titanic Bow Snap (at Line 10 end: 81.16s)
    climax_t = timeline[10]["end"]
    climax_sfx = np.zeros(total_samples, dtype=np.float32)
    if climax_t < total_dur:
        c_idx = int(climax_t * sr)
        dur_c = min(int(2.4 * sr), total_samples - c_idx)
        tc = np.linspace(0, 2.4, dur_c, False)
        # Deep 38Hz seismic thump + explosive snap
        thump = 0.80 * np.sin(2 * np.pi * 38 * tc) * np.exp(-2.2 * tc)
        crack_noise = (np.random.rand(dur_c).astype(np.float32) * 2 - 1) * np.exp(-20.0 * tc)
        climax_sfx[c_idx:c_idx+dur_c] = thump + crack_noise * 0.70

    # Master mix
    master = voice * 0.96 + prologue_sub * 0.35 + bowl * 0.40 + air * 0.30 + drone * 0.55 + heartbeats * 0.60 + climax_sfx * 0.90
    peak = np.max(np.abs(master))
    if peak > 0:
        master = master / peak * 0.90

    sf.write(out_wav, master.astype(np.float32), sr)
    print(f"Punchy Master Audio generated: {out_wav} (Duration: {total_dur:.2f}s, Peak: {peak:.3f})")

if __name__ == "__main__":
    build_punchy_cinema_audio("scratch/ep005_punchy_timeline.json", "studio_ramayana/episodes/ep005/audio_master.wav")
