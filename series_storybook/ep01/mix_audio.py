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

voice_raw, v_sr = sf.read("series_storybook/ep01/voice/full_voice.wav")
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

# 1. 0.0s - 3.0s: Water drop + sudden reverse whisper + low cinematic impact
# Water drip resonance (sine sweep 1200 -> 300 Hz)
t_drip = np.linspace(0, 0.4, int(0.4 * SR))
drip = np.sin(2 * np.pi * (1200 - 900 * (t_drip / 0.4)**0.5) * t_drip) * np.exp(-t_drip * 15)
place(sfx_buf, drip.astype(np.float32), 0.1, gain=0.6)

# Opening Impact (0.0s)
imp_open = impact(amp=0.65)
place(sfx_buf, imp_open, 0.0, gain=0.75)

# 2. 3.0s - 9.0s: Ancient page opening / paper rustle + night insects & eerie wind
t = 3.0
while t < total_dur:
    w = wind(min(6.0, total_dur - t), amp=0.06)
    place(sfx_buf, w, t, gain=0.30)
    t += 5.5

# High frequency night crickets/insects bed (4.5 kHz bandpass)
rng = np.random.default_rng(77)
cricket_noise = rng.standard_normal(total_len)
b_crick, a_crick = butter(2, [4000 / (SR / 2), 6500 / (SR / 2)], "band")
crickets = lfilter(b_crick, a_crick, cricket_noise) * 0.018
sfx_buf += crickets.astype(np.float32)

# 3. 15.0s - 22.0s: Ghost woman breathing + sudden anklet chime
# Anklet chime at 16.5s (metallic cluster 2.8k, 3.2k, 4.1k Hz)
t_anklet = np.linspace(0, 0.8, int(0.8 * SR))
anklet = (
    np.sin(2 * np.pi * 2800 * t_anklet) +
    0.7 * np.sin(2 * np.pi * 3240 * t_anklet) +
    0.5 * np.sin(2 * np.pi * 4150 * t_anklet)
) * np.exp(-t_anklet * 8)
place(sfx_buf, anklet.astype(np.float32), 16.2, gain=0.35)

# Ghost breath at 18.0s
gb = breath(kind='in', amp=0.35)
place(sfx_buf, gb, 18.0, gain=0.45)

# 4. 22.0s - 29.0s: Rising tension riser + muffled heartbeat
hb = heartbeat(bpm=95, dur=8.0, amp=0.25)
place(sfx_buf, hb, 21.0, gain=0.45)

rs = riser(dur=3.5, amp=0.25)
place(sfx_buf, rs, 23.0, gain=0.40)

# 5. 29.0s - 36.0s: Twist impact & sudden silence before "तुम्हारा था"
imp_twist = impact(amp=0.75)
place(sfx_buf, imp_twist, 25.5, gain=0.85)

# 6. 36.0s - end: Page turn sound + match opening water drop
place(sfx_buf, drip.astype(np.float32), min(total_dur - 0.5, 26.5), gain=0.6)

# Dark Folk Horror Drone (Tanpura/D-minor sub bass 36.7 Hz + 55 Hz)
t_arr = np.arange(total_len) / SR
drone = (
    0.65 * np.sin(2 * np.pi * 36.7 * t_arr) +
    0.35 * np.sin(2 * np.pi * 55.0 * t_arr)
)
lfo = 0.5 + 0.5 * np.sin(2 * np.pi * 0.15 * t_arr)
music_buf = (drone * lfo * 0.045).astype(np.float32)

# --- STRICT VOICE DUCKING ---
voice_env = np.abs(voice)
b_env, a_env = butter(1, 3.0 / (SR / 2))
voice_env_smooth = lfilter(b_env, a_env, voice_env)

ducking = np.clip(1.0 - voice_env_smooth * 2.8, 0.12, 1.0)
music_buf *= ducking
sfx_buf *= np.clip(1.0 - voice_env_smooth * 1.8, 0.20, 1.0)

# Voice 0.92 Peak - crisp & authoritative storytelling
voice_norm = voice / (np.max(np.abs(voice)) + 1e-9) * 0.92
final_raw = voice_norm + sfx_buf + music_buf

sf.write("series_storybook/ep01/voice/mix_raw.wav", final_raw, SR)

# Master to EBU R128 (-14 LUFS)
cmd = [
    "ffmpeg", "-y", "-i", "series_storybook/ep01/voice/mix_raw.wav",
    "-af", "loudnorm=I=-14:TP=-1.5:LRA=10",
    "-ar", "44100",
    "series_storybook/ep01/voice/ep01_final_audio.wav"
]
subprocess.run(cmd, check=True)
print(f"Storybook Ep 01 Master Audio complete! ({total_dur:.2f}s)")
