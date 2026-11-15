import asyncio
import os
import subprocess
from pathlib import Path
import soundfile as sf
import edge_tts

lines = [
    {"id": "line_00", "text": "एक भयानक आवाज़... और पिनाक दो टुकड़ों में फट गया!"},
    {"id": "line_01", "text": "धमाका इतना भीषण था कि तीनों लोकों की नींव हिल गई!"},
    {"id": "line_02", "text": "3,000 किलोमीटर दूर... महेंद्र पर्वत पर ध्यान में बैठे एक महा-ऋषि की आँखें खुल गईं!"},
    {"id": "line_03", "text": "स्वयं भगवान परशुराम! जिन्होंने 21 बार इस धरती को क्षत्रिय-विहीन किया था!"},
    {"id": "line_04", "text": "वो तूफान की तरह मिथिला के राज-दरबार में दाखिल हुए!"},
    {"id": "line_05", "text": "किसकी गर्दन पर मौत सवार है, जिसने मेरे महादेव का धनुष छुआ?!"},
    {"id": "line_06", "text": "पूरी सभा खामोश थी। लेकिन तभी... लक्ष्मण आगे बढ़े। चेहरे पर बेखौफ मुस्कान!"},
    {"id": "line_07", "text": "दो महा-शक्तियों का महा-टकराव! अगले भाग में: परशुराम-लक्ष्मण संवाद! फॉलो करें @grow10z"}
]

out_dir = Path("studio_ramayana/episodes/ep006/audio_lines")
out_dir.mkdir(parents=True, exist_ok=True)

async def test_fast_tts():
    total_dur = 0
    for item in lines:
        mp3_path = out_dir / f"{item['id']}_fast.mp3"
        wav_path = out_dir / f"{item['id']}_fast.wav"
        comm = edge_tts.Communicate(item["text"], voice="hi-IN-MadhurNeural", rate="+24%", pitch="-1Hz")
        await comm.save(str(mp3_path))
        subprocess.run(["ffmpeg", "-y", "-i", str(mp3_path), "-ar", "44100", "-ac", "1", str(wav_path)],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        data, sr = sf.read(str(wav_path))
        dur = len(data) / sr
        total_dur += dur
        print(f"[{item['id']}] dur={dur:.2f}s: {item['text']}")
    print(f"TOTAL DIALOGUE DURATION: {total_dur:.2f}s")

if __name__ == "__main__":
    asyncio.run(test_fast_tts())
