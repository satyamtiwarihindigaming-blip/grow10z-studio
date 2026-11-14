import os, json, soundfile as sf, numpy as np
from kokoro_onnx import Kokoro

kokoro = Kokoro("models/kokoro-v1.0.onnx", "models/voices-v1.0.bin")

lines = [
    # Beat 1: Hook & Ayodhya Durbar (0-7s)
    {"speaker": "hm_omega", "speed": 1.05, "pause": 0.5, "text": "अयोध्या का भव्य राजदरबार... जहाँ चारों राजकुमारों के बाल्यकाल से महल गूँज रहा था।"},
    
    # Beat 2: Vishwamitra Entry (7-15s)
    {"speaker": "hm_omega", "speed": 1.05, "pause": 0.4, "text": "तभी दरबार में महाक्रोध और तपस्या के प्रतीक... महर्षि विश्वामित्र का अचानक आगमन हुआ!"},
    
    # Beat 3: Vishwamitra's Demand (15-22s)
    {"speaker": "hm_psi", "speed": 1.00, "pause": 0.5, "text": "राजन! वन में मारीच और सुबाहु ने यज्ञ विध्वंस कर दिया है... राक्षसों के संहार हेतु मुझे राम चाहिए!"},
    
    # Beat 4: Dasharatha's Grief (22-29s)
    {"speaker": "hm_psi", "speed": 0.95, "pause": 0.5, "text": "मुनिवर! मेरे राम अभी सुकुमार बालक हैं... मेरे प्राण ले लीजिए, पर मेरे राम को न मांगिए!"},
    
    # Beat 5: Shri Ram & Lakshman step forward (29-35s)
    {"speaker": "hm_omega", "speed": 1.05, "pause": 0.4, "text": "किंतु स्वयं मर्यादा पुरुषोत्तम श्रीराम और लक्ष्मण ने आगे बढ़कर महर्षि के चरण स्पर्श किए।"},
    
    # Beat 6: Heroic Departure & Cliffhanger (35-42s)
    {"speaker": "hm_omega", "speed": 1.05, "pause": 0.3, "text": "हाथों में कोदण्ड धनुष लिए दोनों वीर... धर्म और मानवता की रक्षा हेतु सरयू तट से निकल पड़े!"},
    {"speaker": "hm_omega", "speed": 1.10, "pause": 0.2, "text": "अगले भाग में देखिए: भयानक राक्षसी ताड़का का संहार... श्रीराम का पहला बाण!"}
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
out_dir = "studio_ramayana/episodes/ep002/voice"
os.makedirs(out_dir, exist_ok=True)
sf.write(f"{out_dir}/full_voice.wav", full_wav, SR)

with open(f"{out_dir}/voice_timeline.json", "w", encoding="utf-8") as f:
    json.dump(timeline, f, ensure_ascii=False, indent=2)

print(f"Ramayana Ep 002 Voice generated! Total duration: {current_time:.2f}s")
