import os, json, subprocess
import numpy as np
import soundfile as sf
from scipy.signal import butter, lfilter
from pedalboard import Pedalboard, Reverb, Compressor, HighpassFilter, Gain, Limiter

# Load SFX synthesizer functions from reference_code
import sys
sys.path.append("reference_code")
from sfx_library import (
    SR, thump, heartbeat, breath, gasp, gulp, bus_rumble,
    wind, crickets, door_hiss, clink, phone_buzz, riser, impact, whoosh, tick, place
)

# Load voice audio
voice_raw, v_sr = sf.read("out/ep01/voice/full_voice.wav")
if voice_raw.ndim > 1:
    voice_raw = voice_raw[:, 0]

# Resample voice to 44100 if needed
if v_sr != SR:
    from scipy.signal import resample
    num_samples = int(len(voice_raw) * SR / v_sr)
    voice = resample(voice_raw, num_samples)
else:
    voice = voice_raw

total_dur = len(voice) / SR
total_len = len(voice)

# Allocate mix buffers
sfx_buf = np.zeros(total_len, dtype=np.float32)
music_buf = np.zeros(total_len, dtype=np.float32)

# 1. Ambience bed
t = 0.0
while t < total_dur:
    w = wind(min(8.0, total_dur - t), amp=0.18)
    place(sfx_buf, w, t, gain=0.6)
    c = crickets(min(8.0, total_dur - t), amp=0.08)
    place(sfx_buf, c, t, gain=0.5)
    t += 7.5

# 2. Bus rumble (during transit: 0 to 27s)
bus_dur = min(27.0, total_dur)
b_rumble = bus_rumble(dur=bus_dur, amp=0.35)
place(sfx_buf, b_rumble, 0.0, gain=0.55)

# 3. Amma says his name (around 12-14s)
# Reaction gasp at 13.5s
g = gasp(amp=0.3)
place(sfx_buf, g, 13.4, gain=0.8)

# Heartbeat starts at 13.8s (bpm=72, 8s)
hb1 = heartbeat(bpm=72, dur=8.0, amp=0.3)
place(sfx_buf, hb1, 13.8, gain=0.7)

# 4. Tiffin clink at 20.0s
clk = clink(amp=0.4)
place(sfx_buf, clk, 20.0, gain=0.9)

# 5. Bus stop & Door hiss at 27.2s
dh = door_hiss(amp=0.45)
place(sfx_buf, dh, 27.2, gain=0.85)

# 6. Riser leading into the reveal (31.5s to 34.0s)
rs = riser(dur=2.8, amp=0.4)
place(sfx_buf, rs, 31.5, gain=0.8)

# Fast panicked heartbeat at 34.8s (bpm=110, 4s)
hb2 = heartbeat(bpm=110, dur=4.0, amp=0.5)
place(sfx_buf, hb2, 34.8, gain=0.9)

# 7. Cliffhanger impact at 37.2s
imp = impact(amp=0.8)
place(sfx_buf, imp, 37.2, gain=1.0)

# Music synthesis (Low ominous drone + suspense pads)
t_arr = np.arange(total_len) / SR
# D minor low root (D1 = 36.7 Hz, A1 = 55.0 Hz, F2 = 87.3 Hz)
drone = (
    0.6 * np.sin(2 * np.pi * 36.7 * t_arr) +
    0.3 * np.sin(2 * np.pi * 55.0 * t_arr) +
    0.2 * np.sin(2 * np.pi * 87.3 * t_arr)
)
# Swelling suspense LFO modulation
lfo = 0.5 + 0.5 * np.sin(2 * np.pi * 0.12 * t_arr)
# Cut music completely at 34.0s for reveal silence, return at 37.2s
mute_mask = np.ones(total_len, dtype=np.float32)
i_mute_start = int(34.0 * SR)
i_mute_end = int(37.2 * SR)
mute_mask[i_mute_start:i_mute_end] = 0.0

music_buf = (drone * lfo * 0.12 * mute_mask).astype(np.float32)

# Ducking music & sfx under voice
voice_env = np.abs(voice)
# Smoothing filter
b_env, a_env = butter(1, 2.0 / (SR / 2))
voice_env_smooth = lfilter(b_env, a_env, voice_env)
ducking = np.clip(1.0 - voice_env_smooth * 1.5, 0.25, 1.0)

music_buf *= ducking
sfx_buf *= np.clip(1.0 - voice_env_smooth * 0.6, 0.4, 1.0)

# Combine: Voice (-3dB peak) + SFX + Music
voice_norm = voice / (np.max(np.abs(voice)) + 1e-9) * 0.75
final_raw = voice_norm + sfx_buf + music_buf

# Write intermediate mix
sf.write("out/ep01/voice/mix_raw.wav", final_raw, SR)

# Run ffmpeg loudnorm to normalize to -14 LUFS, true peak -1.5 dBFS
cmd = [
    "ffmpeg", "-y", "-i", "out/ep01/voice/mix_raw.wav",
    "-af", "loudnorm=I=-14:TP=-1.5:LRA=11",
    "-ar", "44100",
    "out/ep01/voice/ep01_final_audio.wav"
]
subprocess.run(cmd, check=True)
print("Finished audio mixing and loudnorm normalization: out/ep01/voice/ep01_final_audio.wav")
