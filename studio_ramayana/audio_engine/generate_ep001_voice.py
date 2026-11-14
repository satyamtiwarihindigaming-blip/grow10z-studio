import os, json, soundfile as sf, numpy as np
from kokoro_onnx import Kokoro

kokoro = Kokoro("models/kokoro-v1.0.onnx", "models/voices-v1.0.bin")

lines = [
    # Scene 1: Divine Hook (0-6s)
    {"speaker": "hm_omega", "speed": 1.05, "pause": 0.5, "text": "चैत्र मास की नवमी तिथि... अयोध्या में एक ऐसा सूर्योदय हुआ, जो युगों तक अमर हो गया!"},
    
    # Scene 2: Dasharatha's Palace joy (6-13s)
    {"speaker": "hm_omega", "speed": 1.05, "pause": 0.4, "text": "महाराज दशरथ के महल में गूँज उठी वो किलकारी, जिसका इंतज़ार तीनों लोकों को था।"},
    
    # Scene 3: Maharaja Dasharatha Dialogue (13-19s)
    {"speaker": "hm_psi", "speed": 1.00, "pause": 0.5, "text": "कौशल्या! देखो... हमारे घर स्वयं नारायण पधारे हैं!"},
    
    # Scene 4: Divine Description of Baal Ram (19-27s)
    {"speaker": "hm_omega", "speed": 1.05, "pause": 0.5, "text": "नील कमल सी कांति, विशाल नयन और मुख पर वो मंद मुस्कान..."},
    
    # Scene 5: Celebration & Devtas showering flowers (27-34s)
    {"speaker": "hm_omega", "speed": 1.05, "pause": 0.5, "text": "अयोध्या की गलियों में फूलों की वर्षा होने लगी, और देवताओं ने आकाश से दिव्य दुंदुभी बजाई!"},
    
    # Scene 6: Resolution & Next Ep Teaser (34-40s)
    {"speaker": "hm_omega", "speed": 1.05, "pause": 0.3, "text": "मर्यादा पुरुषोत्तम प्रभु श्रीराम का यह दिव्य बाल रूप... अधर्म के अंत की पहली शुरुआत थी!"},
    {"speaker": "hm_omega", "speed": 1.10, "pause": 0.2, "text": "अगले भाग में देखिए: महर्षि विश्वामित्र का अयोध्या आगमन!"}
]

combined_audio = []
timeline = []
current_time = 0.0
SR = 24000

for i, item in enumerate(lines):
    samples, sr = kokoro.create(item["text"], voice=item["speaker"], speed=item["speed"], lang="hi")
    dur = len(samples) / sr
    
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
os.makedirs("studio_ramayana/episodes/ep001/voice", exist_ok=True)
sf.write("studio_ramayana/episodes/ep001/voice/full_voice.wav", full_wav, SR)

with open("studio_ramayana/episodes/ep001/voice/voice_timeline.json", "w", encoding="utf-8") as f:
    json.dump(timeline, f, ensure_ascii=False, indent=2)

print(f"Ramayana Ep 001 Voice generated! Total duration: {current_time:.2f}s")
