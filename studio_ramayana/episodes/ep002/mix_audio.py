import numpy as np
import soundfile as sf
from scipy.signal import butter, sosfilt

SR = 44100

def butter_bandpass_filter(data, lowcut, highcut, fs, order=4):
    sos = butter(order, [lowcut, highcut], btype='band', fs=fs, output='sos')
    return sosfilt(sos, data)

# 1. Load Voice
voice_data, v_sr = sf.read("studio_ramayana/episodes/ep002/voice/full_voice.wav")
if len(voice_data.shape) > 1:
    voice_data = voice_data[:, 0]

# Resample voice to 44100
t_orig = np.linspace(0, len(voice_data) / v_sr, len(voice_data))
total_duration = len(voice_data) / v_sr + 1.2
t_target = np.linspace(0, total_duration, int(total_duration * SR))

voice_44k = np.interp(t_target[:int(len(voice_data) * (SR / v_sr))], t_orig, voice_data)
# Pad to full duration
padded_voice = np.zeros(len(t_target))
padded_voice[:len(voice_44k)] = voice_44k

# 2. Synthesize Vedic Shankhnaad (Conch Shell)
def synth_shankh(duration=3.5):
    t = np.linspace(0, duration, int(duration * SR), False)
    f0 = 220.0
    f_env = f0 * (1.0 + 0.18 * np.sin(np.pi * t / duration) + 0.05 * np.sin(2 * np.pi * 5.0 * t))
    phase = 2 * np.pi * np.cumsum(f_env) / SR
    shankh = (
        0.55 * np.sin(phase) +
        0.30 * np.sin(2 * phase) +
        0.18 * np.sin(3 * phase) +
        0.10 * np.sin(4 * phase) +
        0.05 * np.sin(5 * phase)
    )
    env = np.sin(np.pi * (t / duration) ** 0.6) ** 1.8
    return shankh * env * 0.45

# 3. Synthesize Tanpura Drone in D-Major
d2 = 73.42
drone = (
    0.35 * np.sin(2 * np.pi * d2 * t_target) +
    0.28 * np.sin(2 * np.pi * (d2 * 1.5) * t_target) +
    0.20 * np.sin(2 * np.pi * (d2 * 2.0) * t_target) +
    0.14 * np.sin(2 * np.pi * (d2 * 3.0) * t_target) +
    0.08 * np.sin(2 * np.pi * (d2 * 4.0) * t_target)
)
mod = 0.85 + 0.15 * np.sin(2 * np.pi * 0.22 * t_target)
drone = drone * mod * 0.22

# 4. Synthesize Temple Bells
bell_track = np.zeros_like(t_target)
bell_times = [0.8, 7.2, 14.5, 22.8, 30.6, 38.0]
for bt in bell_times:
    idx = int(bt * SR)
    dur_b = min(int(3.0 * SR), len(t_target) - idx)
    tb = np.linspace(0, 3.0, dur_b, False)
    bell = (
        0.5 * np.sin(2 * np.pi * 880 * tb) * np.exp(-1.4 * tb) +
        0.3 * np.sin(2 * np.pi * 1760 * tb) * np.exp(-2.2 * tb) +
        0.2 * np.sin(2 * np.pi * 2640 * tb) * np.exp(-3.5 * tb)
    )
    bell_track[idx:idx+dur_b] += bell * 0.25

# Shankh at start and at heroic departure (t=37s)
s1 = synth_shankh(3.2)
bell_track[:len(s1)] += s1
idx_s2 = int(37.5 * SR)
s2 = synth_shankh(3.5)
bell_track[idx_s2:idx_s2+len(s2)] += s2

# Master Mix: Voice priority (ducking drone during voice)
voice_env = np.abs(padded_voice)
sos_lpf = butter(2, 5.0, btype='low', fs=SR, output='sos')
smooth_env = sosfilt(sos_lpf, voice_env)
duck = 1.0 - np.clip(smooth_env * 2.2, 0.0, 0.55)

master_bg = (drone * duck) + bell_track
master = padded_voice * 0.95 + master_bg * 0.75

# Peak normalize to -1.0 dB
peak = np.max(np.abs(master))
if peak > 0:
    master = master / peak * 0.89

out_wav = "studio_ramayana/episodes/ep002/voice/ep002_final_audio.wav"
sf.write(out_wav, master.astype(np.float32), SR)
print(f"Master audio mixed successfully: {out_wav} (Duration: {total_duration:.2f}s)")
