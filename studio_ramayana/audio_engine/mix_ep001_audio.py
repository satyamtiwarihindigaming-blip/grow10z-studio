import os, json, subprocess
import numpy as np
import soundfile as sf
from scipy.signal import butter, lfilter, resample

SR = 44100

voice_raw, v_sr = sf.read("studio_ramayana/episodes/ep001/voice/full_voice.wav")
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

t_arr = np.arange(total_len) / SR

# 1. Divine Tanpura Drone (Sa - Pa - Sa' in D major: 146.8 Hz, 220.0 Hz, 293.6 Hz)
tanpura = (
    0.50 * np.sin(2 * np.pi * 146.83 * t_arr) +   # D3
    0.35 * np.sin(2 * np.pi * 220.00 * t_arr) +   # A3
    0.30 * np.sin(2 * np.pi * 293.66 * t_arr) +   # D4
    0.15 * np.sin(2 * np.pi * 73.41 * t_arr)      # Deep D2 Sub
)
# Gentle shimmer envelope
shimmer = 0.6 + 0.4 * np.sin(2 * np.pi * 0.25 * t_arr)
music_buf += (tanpura * shimmer * 0.05).astype(np.float32)

# 2. Shankh Sound (Conch Shell opening resonance at 0.2s)
# 420 Hz fundamental with golden harmonics, swelling up and sustaining
t_shankh = np.linspace(0, 3.5, int(3.5 * SR))
shankh = (
    np.sin(2 * np.pi * 420 * t_shankh) +
    0.6 * np.sin(2 * np.pi * 840 * t_shankh) +
    0.4 * np.sin(2 * np.pi * 1260 * t_shankh)
) * (1.0 - np.exp(-t_shankh * 3.0)) * np.exp(-t_shankh * 0.6)

idx_shankh = int(0.2 * SR)
end_shankh = min(total_len, idx_shankh + len(shankh))
sfx_buf[idx_shankh:end_shankh] += (shankh[:end_shankh - idx_shankh] * 0.45).astype(np.float32)

# 3. Temple Bell Chimes (Ghanta at 6.0s and 27.0s)
for bell_t in [6.5, 27.5]:
    t_bell = np.linspace(0, 3.0, int(3.0 * SR))
    bell = (
        np.sin(2 * np.pi * 1050 * t_bell) +
        0.7 * np.sin(2 * np.pi * 2100 * t_bell) +
        0.4 * np.sin(2 * np.pi * 3150 * t_bell)
    ) * np.exp(-t_bell * 2.2)
    b_idx = int(bell_t * SR)
    b_end = min(total_len, b_idx + len(bell))
    sfx_buf[b_idx:b_end] += (bell[:b_end - b_idx] * 0.35).astype(np.float32)

# 4. Devta Flower Shower Wind / Shimmer at 28.0s
t_shimmer = np.linspace(0, 4.0, int(4.0 * SR))
wind_chime = (
    np.sin(2 * np.pi * 2400 * t_shimmer) * np.sin(2 * np.pi * 4.0 * t_shimmer) +
    np.sin(2 * np.pi * 3200 * t_shimmer) * np.sin(2 * np.pi * 5.5 * t_shimmer)
) * np.exp(-t_shimmer * 0.8)
s_idx = int(28.0 * SR)
s_end = min(total_len, s_idx + len(wind_chime))
sfx_buf[s_idx:s_end] += (wind_chime[:s_end - s_idx] * 0.25).astype(np.float32)

# Strict Voice Priority Ducking
voice_env = np.abs(voice)
b_env, a_env = butter(1, 3.0 / (SR / 2))
voice_env_smooth = lfilter(b_env, a_env, voice_env)

ducking = np.clip(1.0 - voice_env_smooth * 2.5, 0.12, 1.0)
music_buf *= ducking
sfx_buf *= np.clip(1.0 - voice_env_smooth * 1.6, 0.25, 1.0)

# Voice 0.92 Peak - Pure Devotional Clarity
voice_norm = voice / (np.max(np.abs(voice)) + 1e-9) * 0.92
final_raw = voice_norm + sfx_buf + music_buf

sf.write("studio_ramayana/episodes/ep001/voice/mix_raw.wav", final_raw, SR)

cmd = [
    "ffmpeg", "-y", "-i", "studio_ramayana/episodes/ep001/voice/mix_raw.wav",
    "-af", "loudnorm=I=-14:TP=-1.5:LRA=10",
    "-ar", "44100",
    "studio_ramayana/episodes/ep001/voice/ep001_final_audio.wav"
]
subprocess.run(cmd, check=True)
print(f"Ramayana Ep 001 Divine Master Audio complete! ({total_dur:.2f}s)")
