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

# Load voice audio
voice_raw, v_sr = sf.read("out/ep02/voice/full_voice.wav")
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

# 1. Rain & Storm Ambience (Subtle background bed: -20dB under voice)
rng = np.random.default_rng(42)
rain_noise = rng.standard_normal(total_len)
# Bandpass 300 - 4500 Hz (soft rain so it doesn't mask speech consonants 2k-5k)
b_rain, a_rain = butter(2, [300 / (SR / 2), 4500 / (SR / 2)], "band")
rain_bed = lfilter(b_rain, a_rain, rain_noise) * 0.05
sfx_buf += rain_bed.astype(np.float32)

# Gentle Wind gusts
t = 0.0
while t < total_dur:
    w = wind(min(8.0, total_dur - t), amp=0.08)
    place(sfx_buf, w, t, gain=0.35)
    t += 7.5

# 2. Bus diesel engine rumble (Subtle low-end, notched below voice fundamentals)
bus_dur = min(36.0, total_dur)
b_rumble = bus_rumble(dur=bus_dur, amp=0.15)
place(sfx_buf, b_rumble, 0.0, gain=0.3)

# 3. Thunder claps & Sub-bass booms (low rumble, placed at pauses)
th1 = thump(55, 24, 2.0, amp=0.35)
place(sfx_buf, th1, 1.5, gain=0.45)

th2 = thump(70, 22, 2.5, amp=0.55)
place(sfx_buf, th2, 23.0, gain=0.6)

# 4. Phone buzz vibration (at 14.2s and 16.0s)
pb1 = phone_buzz(dur=1.2, amp=0.35)
place(sfx_buf, pb1, 14.2, gain=0.5)
pb2 = phone_buzz(dur=1.2, amp=0.35)
place(sfx_buf, pb2, 16.0, gain=0.5)

# 5. Heartbeat escalation (muffled, low frequency 60Hz so it doesn't fight narration)
hb1 = heartbeat(bpm=82, dur=8.0, amp=0.20)
place(sfx_buf, hb1, 20.0, gain=0.45)

hb2 = heartbeat(bpm=118, dur=6.0, amp=0.30)
place(sfx_buf, hb2, 30.0, gain=0.55)

# 6. Riser swell (gentle tension rise)
rs = riser(dur=3.2, amp=0.25)
place(sfx_buf, rs, 29.5, gain=0.45)

# 7. Cliffhanger impact boom at 42.5s (hit when narrator pauses)
imp = impact(amp=0.65)
place(sfx_buf, imp, 42.5, gain=0.75)

# 8. Dark Drone Music (sub-bass only, -18dB relative to voice)
t_arr = np.arange(total_len) / SR
drone = (
    0.65 * np.sin(2 * np.pi * 36.7 * t_arr) +  # D1 (deep 36Hz)
    0.35 * np.sin(2 * np.pi * 55.0 * t_arr)    # A1 (55Hz)
)
lfo = 0.5 + 0.5 * np.sin(2 * np.pi * 0.1 * t_arr)

# Silence drop at suspense beat
mute_mask = np.ones(total_len, dtype=np.float32)
i_mute_start = int(33.0 * SR)
i_mute_end = int(35.5 * SR)
mute_mask[i_mute_start:i_mute_end] = 0.0

music_buf = (drone * lfo * 0.05 * mute_mask).astype(np.float32)

# --- AGGRESSIVE VOICE DUCKING ---
# Whenever voice is present, suppress all BGM and SFX down to 10% (-20 dB)
voice_env = np.abs(voice)
b_env, a_env = butter(1, 3.0 / (SR / 2))
voice_env_smooth = lfilter(b_env, a_env, voice_env)

# Ducking curve: cuts BGM/SFX deeply whenever dialogue happens
ducking = np.clip(1.0 - voice_env_smooth * 2.5, 0.10, 1.0)
music_buf *= ducking
sfx_buf *= np.clip(1.0 - voice_env_smooth * 1.8, 0.18, 1.0)

# Voice is Master King (0.92 peak, crystal clear in front)
voice_norm = voice / (np.max(np.abs(voice)) + 1e-9) * 0.90
final_raw = voice_norm + sfx_buf + music_buf

sf.write("out/ep02/voice/mix_raw.wav", final_raw, SR)

# Loudnorm normalization to -14 LUFS with voice focus
cmd = [
    "ffmpeg", "-y", "-i", "out/ep02/voice/mix_raw.wav",
    "-af", "loudnorm=I=-14:TP=-1.5:LRA=10",
    "-ar", "44100",
    "out/ep02/voice/ep02_final_audio.wav"
]
subprocess.run(cmd, check=True)
print("Finished remastered audio mixing: out/ep02/voice/ep02_final_audio.wav")
