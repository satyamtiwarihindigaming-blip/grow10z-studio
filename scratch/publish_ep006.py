import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from studio_ramayana.pipeline.buffer_publisher import create_instagram_post

caption = """एक भयानक आवाज़... और भगवान शिव का पिनाक दो टुकड़ों में फट गया! 🏹💥

धमाका इतना भीषण था कि तीनों लोकों की नींव हिल गई। और 3,000 किलोमीटर दूर... महेंद्र पर्वत पर ध्यान में बैठे स्वयं भगवान परशुराम की आँखें खुल गईं! 

जिन्होंने 21 बार इस समूची धरती को क्षत्रिय-विहीन कर दिया था, वो तूफान की तरह मिथिला के राज-दरबार में दाखिल हुए! उनकी दहाड़ से सारा राज-महल कांप उठा:
"किसकी गर्दन पर मौत सवार है, जिसने मेरे महादेव का धनुष छुआ?!"

पूरी सभा में सन्नाटा था... तभी लक्ष्मण आगे बढ़े। चेहरे पर एक बेखौफ मुस्कान! 🔥

आगे क्या होगा? लक्ष्मण और परशुराम का महा-संवाद अगले भाग में!

👉 इस दिव्य गाथा से जुड़ने के लिए अभी फॉलो करें: @grow10z 🚩
🔔 रोज़ाना नए रोमांचक प्रसंग के लिए शेयर और सेव करें!

#ramayana #parashurama #shriram #mithila #pinaka #shivdhanush #lakshman #hinduism #sanatandharma #mythology #indiananimation #grow10z #viralreels #reelsindia #trendingreels #vedic #cliffhanger"""

video_url = "https://github.com/satyamtiwarihindigaming-blip/grow10z-studio/releases/download/v0.0.6/ep006_final.mp4"

print("Publishing Episode 006 to Instagram Reels @grow10z via Buffer GraphQL API...")
res = create_instagram_post(caption, video_url=video_url, share_now=True)
print("Buffer Response:", res)
