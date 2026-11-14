import os, json, soundfile as sf, numpy as np
from kokoro_onnx import Kokoro

kokoro = Kokoro("models/kokoro-v1.0.onnx", "models/voices-v1.0.bin")

lines = [
    # Beat 1: Hook
    {"speaker": "hm_omega", "speed": 1.05, "pause": 0.4, "text": "रात के दो बज चुके थे।"},
    {"speaker": "hm_omega", "speed": 1.15, "pause": 0.5, "text": "बस की रफ़्तार अब अस्सी से बढ़कर सौ पार कर चुकी थी!"},
    {"speaker": "hm_omega", "speed": 1.05, "pause": 0.6, "text": "बाहर मूसलाधार बारिश और गहरा कोहरा था।"},
    
    # Beat 2: Panic & Action
    {"speaker": "hm_omega", "speed": 1.15, "pause": 0.4, "text": "राघव का दिल सीने में हथौड़े की तरह धड़क रहा था।"},
    {"speaker": "hm_omega", "speed": 1.10, "pause": 0.5, "text": "उसने टिफ़िन फ़र्श पर फेंका, और लड़खड़ाते हुए आगे केबिन की तरफ़ भागा।"},
    
    # Beat 3: Raghav dialogue
    {"speaker": "hm_omega", "speed": 1.25, "pause": 0.5, "text": "भैया! बस रोको! कोई है आगे?!"},
    {"speaker": "hm_omega", "speed": 1.10, "pause": 0.6, "text": "राघव ने ड्राइवर के केबिन का भारी पर्दा एक झटके में खींचा!"},
    
    # Beat 4: Reveal
    {"speaker": "hm_omega", "speed": 1.10, "pause": 0.5, "text": "लेकिन अंदर का नज़ारा देखकर उसके पैरों तले ज़मीन खिसक गई!"},
    {"speaker": "hm_omega", "speed": 1.15, "pause": 0.6, "text": "स्टीयरिंग व्हील अपने आप तेज़ी से घूम रहा था..."},
    {"speaker": "hm_omega", "speed": 1.00, "pause": 0.8, "text": "ड्राइवर की सीट बिल्कुल खाली थी!"},
    
    # Beat 5: Cliffhanger
    {"speaker": "hm_omega", "speed": 1.15, "pause": 0.5, "text": "और स्पीडोमीटर की सुई एक सौ बीस पर कांप रही थी!"},
    {"speaker": "hm_omega", "speed": 1.05, "pause": 0.5, "text": "तभी रियर-व्यू मिरर में राघव को पीछे की सीट पर..."},
    {"speaker": "hm_omega", "speed": 1.00, "pause": 0.7, "text": "सफ़ेद शॉल ओढ़े वह बूढ़ी औरत सीधी उसकी आँखों में घूरते दिखी!"},
    {"speaker": "hm_omega", "speed": 1.10, "pause": 0.4, "text": "क्या राघव इस भूतिया बस से ज़िंदा बच पाएगा?"},
    {"speaker": "hm_omega", "speed": 1.15, "pause": 0.2, "text": "जानने के लिए सब्सक्राइब करें!"}
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
sf.write("out/ep03/voice/full_voice.wav", full_wav, SR)

with open("out/ep03/voice/voice_timeline.json", "w", encoding="utf-8") as f:
    json.dump(timeline, f, ensure_ascii=False, indent=2)

print(f"Ep 03 Voice generated! Total duration: {current_time:.2f}s")
