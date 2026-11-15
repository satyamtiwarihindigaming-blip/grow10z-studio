import numpy as np
import soundfile as sf

sr = 44100
dur = 10.0
t = np.linspace(0, dur, int(sr * dur), False)

# 1. Warm cinematic sub-bass rumble (42Hz) with smooth fade-in
sub_env = np.clip(t / 2.0, 0, 1) * np.clip((10.0 - t) / 2.0, 0, 1)
sub_rumble = 0.35 * np.sin(2 * np.pi * 42.0 * t) * sub_env

# 2. Sacred Tibetan / Temple Bowl (432Hz pure tone with natural harmonics)
bowl_t = np.clip(t - 0.4, 0, dur)
bowl_env = np.exp(-0.6 * bowl_t) * (t >= 0.4)
bowl = (
    0.28 * np.sin(2 * np.pi * 432.0 * bowl_t) +
    0.14 * np.sin(2 * np.pi * 864.0 * bowl_t) +
    0.06 * np.sin(2 * np.pi * 1296.0 * bowl_t)
) * bowl_env

# 3. Soft atmospheric air/wind swell
noise = (np.random.rand(len(t)).astype(np.float32) * 2 - 1)
# simple 3-point moving average for smoothing
smooth_noise = np.convolve(noise, np.ones(80)/80, mode='same')
wind_env = np.sin(np.pi * (t / 4.0)) ** 2 * (t <= 4.0)
air = smooth_noise * wind_env * 0.15

mix = sub_rumble + bowl + air
peak = np.max(np.abs(mix))
if peak > 0:
    mix = mix / peak * 0.85

sf.write("scratch/test_cinema_opening.wav", mix.astype(np.float32), sr)
print("Saved test cinema opening successfully!")
