import os, json, soundfile as sf, numpy as np
from kokoro_onnx import Kokoro

kokoro = Kokoro("models/kokoro-v1.0.onnx", "models/voices-v1.0.bin")

# Kokoro voice lines matching the blueprint
# NARRATOR: hm_omega (deep, intimate, restrained storyteller)
# GHOST WOMAN: hf_alpha (soft, eerie whisper)

lines = [
    # Scene 1: Impossible Hook (0-3s)
    {"speaker": "hm_omega", "speed": 1.05, "pause": 0.4, "text": "उस कुएँ में... तीन चेहरे दिखते थे!"},
    
    # Scene 2: Ancient warning (3-9s)
    {"speaker": "hm_omega", "speed": 1.05, "pause": 0.5, "text": "कहते हैं, उस गाँव के कुएँ में रात को झाँकना मना था।"},
    
    # Scene 3: First discovery (9-15s)
    {"speaker": "hm_omega", "speed": 1.05, "pause": 0.5, "text": "एक रात राघव ने कुएँ में अपना चेहरा देखा..."},
    
    # Scene 4: Second discovery (15-22s)
    {"speaker": "hm_omega", "speed": 1.10, "pause": 0.5, "text": "लेकिन पानी में... उसके पीछे एक औरत खड़ी थी!"},
    
    # Scene 5: The ghost warning (22-29s)
    {"speaker": "hf_alpha", "speed": 0.90, "pause": 0.6, "text": "पीछे मत देखना..."},
    {"speaker": "hm_omega", "speed": 1.05, "pause": 0.4, "text": "लेकिन राघव ने गलती कर दी।"},
    
    # Scene 6: The twist (29-36s)
    {"speaker": "hm_omega", "speed": 1.05, "pause": 0.8, "text": "क्योंकि अब पानी में... उसका चेहरा मुस्कुरा रहा था।"},
    
    # Scene 7: The loop (36-40s)
    {"speaker": "hm_omega", "speed": 0.95, "pause": 0.2, "text": "और तीसरा चेहरा... तुम्हारा था।"}
]

combined_audio = []
timeline = []
current_time = 0.0
SR = 24000

for i, item in enumerate(lines):
    samples, sr = kokoro.create(item["text"], voice=item["speaker"], speed=item["speed"], lang="hi")
    dur = len(samples) / sr
    
    # Special whisper DSP processing for ghost woman (index 4)
    if item["speaker"] == "hf_alpha":
        # Apply high-pass / whisper presence
        from scipy.signal import butter, lfilter
        b, a = butter(2, 600 / (sr / 2), 'high')
        samples = lfilter(b, a, samples) * 0.75
        
    timeline.append({
        "index": i,
        "text": item["text"],
        "start": current_time,
        "end": current_time + dur,
        "speaker": item["speaker"]
    })
    combined_audio.append(samples)
    current_time += dur
    
    pause_samples = int(sr * item["pause"])
    combined_audio.append(np.zeros(pause_samples, dtype=np.float32))
    current_time += item["pause"]

full_wav = np.concatenate(combined_audio)
sf.write("series_storybook/ep01/voice/full_voice.wav", full_wav, SR)

with open("series_storybook/ep01/voice/voice_timeline.json", "w", encoding="utf-8") as f:
    json.dump(timeline, f, ensure_ascii=False, indent=2)

print(f"Storybook Ep 01 Voice complete! Total duration: {current_time:.2f}s")
