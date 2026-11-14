import os, json, subprocess
import numpy as np
import soundfile as sf
from scipy.signal import butter, lfilter, resample

import sys
sys.path.append("reference_code")
from sfx_library import (
    SR, thump, heartbeat, breath, gasp, bus_rumble,
    wind, phone_buzz, riser, impact, whoosh, place
)

voice_raw, v_sr = sf.read("out/ep03/voice/full_voice.wav")
if voice_raw.ndim > 1:
    voice_raw = voice_raw[:, 0]

if v_sr != SR:
    num_samples = int(len(voice_raw) * SR / v_sr)
    voice = resample(voice_raw, num_samples)
else:
    voice = voice_raw

total_dur = len(voice) / SR
total_len = len(voice)

sfx_buf = np.zeros(total_len, dtype=np.float32)
music_buf = np.zeros(total_len, dtype=np.float32)

# Subtle rain bed (-22 dB below voice, not masking speech)
rng = np.random.default_rng(42)
rain_noise = rng.standard_normal(total_len)
b_rain, a_rain = butter(2, [300 / (SR / 2), 4000 / (SR / 2)], "band")
rain_bed = lfilter(b_rain, a_rain, rain_noise) * 0.04
sfx_buf += rain_bed.astype(np.float32)

# Fast bus engine speeding up to 100-120 km/h
b_rumble = bus_rumble(dur=total_dur, amp=0.14)
place(sfx_buf, b_rumble, 0.0, gain=0.28)

# Whoosh sound when curtain opens (around 24s)
wh = whoosh(dur=0.7, amp=0.35)
place(sfx_buf, wh, 23.8, gain=0.45)

# Heartbeat acceleration (during panic)
hb = heartbeat(bpm=120, dur=12.0, amp=0.25)
place(sfx_buf, hb, 14.0, gain=0.40)

# Sudden Shock Impact when empty seat is revealed (around 38s)
imp = impact(amp=0.60)
place(sfx_buf, imp, 38.2, gain=0.65)

# Final cliffhanger deep impact at 53.5s
imp_final = impact(amp=0.70)
place(sfx_buf, imp_final, 53.5, gain=0.75)

# Sub-bass horror drone (36Hz D1)
t_arr = np.arange(total_len) / SR
drone = (0.6 * np.sin(2 * np.pi * 36.7 * t_arr) + 0.4 * np.sin(2 * np.pi * 55.0 * t_arr))
music_buf = (drone * 0.04).astype(np.float32)

# AGGRESSIVE VOICE DUCKING (Voice remains supreme)
voice_env = np.abs(voice)
b_env, a_env = butter(1, 3.0 / (SR / 2))
voice_env_smooth = lfilter(b_env, a_env, voice_env)

ducking = np.clip(1.0 - voice_env_smooth * 2.5, 0.10, 1.0)
music_buf *= ducking
sfx_buf *= np.clip(1.0 - voice_env_smooth * 1.8, 0.18, 1.0)

voice_norm = voice / (np.max(np.abs(voice)) + 1e-9) * 0.92
final_raw = voice_norm + sfx_buf + music_buf

sf.write("out/ep03/voice/mix_raw.wav", final_raw, SR)

cmd = [
    "ffmpeg", "-y", "-i", "out/ep03/voice/mix_raw.wav",
    "-af", "loudnorm=I=-14:TP=-1.5:LRA=10",
    "-ar", "44100",
    "out/ep03/voice/ep03_final_audio.wav"
]
subprocess.run(cmd, check=True)
print(f"Ep 03 Audio mix finished: out/ep03/voice/ep03_final_audio.wav ({total_dur:.2f}s)")
