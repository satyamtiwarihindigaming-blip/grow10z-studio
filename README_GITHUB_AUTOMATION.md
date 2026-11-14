# GROW10Z — 24/7 Cloud Automated Ramayana Studio 🚩

इस सेटअप के साथ आपका Ramayana Animation Studio **24/7 Cloud (GitHub Actions)** पर चलता रहेगा — चाहे आपका **PC On रहे या Off रहे**, हर दिन का नया एपिसोड अपने आप बनेगा, रेंडर होगा और डाउनलोड/पोस्टिंग के लिए तैयार रहेगा!

---

## 🚀 यह कैसे काम करता है (How 24/7 Automation Works)

1. **Daily Cron Schedule (GitHub Cloud)**:
   - हर दिन सुबह 11:00 AM IST (05:30 UTC) पर GitHub Cloud Servers (Ubuntu Runner) अपने आप चालू होते हैं।
2. **Autonomous Producer (`studio_ramayana/pipeline/auto_daily_producer.py`)**:
   - `episodes_database.json` से अगला एपिसोड (EP002, EP003, ...) उठाता है।
   - देवनागरी काइनेटिक कैप्शन और हाई-डिटेल कैरेक्टर रिग्स (श्रीराम, विश्वामित्र, ताड़का, दशरथ) को ड्रा करता है।
   - शंख, तानपुरा और डिवाइन ऑडियो के साथ 60fps 1080x1920 MP4 वीडियो रेंडर करता है।
3. **Automatic Delivery**:
   - वीडियो को **GitHub Releases** में डायरेक्ट MP4 डाउनलोड लिंक के साथ पब्लिश कर देता है (आप अपने मोबाइल से सीधे डाउनलोड कर सकते हैं)।
   - अगर आपने Telegram Bot Token डाला है, तो सीधे आपके **Telegram Channel/Bot** पर वीडियो + कैप्शन भेज देता है।
   - प्रोग्रेस को गिट में अपने आप कमिट कर देता है ताकि अगले दिन उसके आगे का एपिसोड बने।

---

## 🔗 GitHub से जोड़ने के 2 आसान स्टेप्स (Only 1-Time Setup)

### Step 1: GitHub पर एक नया Empty Repo बनाएँ
1. [github.com/new](https://github.com/new) पर जाएँ।
2. Repository Name डालें: `grow10z-studio` (Private या Public कोई भी चुन सकते हैं)।
3. "Add README" या ".gitignore" को **Unchecked** रखें (खाली रहने दें)।
4. **Create repository** पर क्लिक करें।

### Step 2: Local Repo को Push करें
अपने Terminal में सिर्फ यह 2 कमांड्स चलाएं (या हमें अपना Repo Link बता दें):
```bash
git remote add origin https://github.com/<YOUR_GITHUB_USERNAME>/grow10z-studio.git
git branch -M main
git push -u origin main
```

---

## 📱 Mobile पर Direct Video पाने के लिए (Optional Telegram Push)
GitHub Repo Settings > **Secrets and variables** > **Actions** में जाकर 2 secrets जोड़ें:
- `TELEGRAM_BOT_TOKEN`: (BotFather से मिला हुआ टोकन)
- `TELEGRAM_CHAT_ID`: (आपका Telegram Chat / Channel ID)

---

## ⚡ Manual 1-Click Trigger (जब भी तुरंत बनाना हो)
1. अपने GitHub Repo के **Actions** टैब में जाएँ।
2. **"GROW10Z Daily Ramayana 24/7 Automation"** पर क्लिक करें।
3. **Run workflow** बटन दबाएं (Episode ID खाली छोड़ेंगे तो अगला एपिसोड बनेगा, या "EP002" लिख सकते हैं)।
4. 3-4 मिनट में पूरा 60fps वीडियो बनकर Releases में आ जाएगा!
