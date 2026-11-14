"""
GROW10Z — Automated Cloud Uploader & Notifier
Sends newly generated episode MP4 and ready-to-copy metadata to Telegram / Webhook.
"""

import os
import sys
import requests

def send_telegram(video_path, txt_path):
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    if not bot_token or not chat_id:
        print("ℹ️ TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not configured. Skipping instant Telegram push.")
        print("💡 Tip: Add these secrets in your GitHub Repo Settings > Secrets & Variables > Actions to get auto-delivery on phone!")
        return

    caption = "🎬 New GROW10Z Ramayana Episode Ready to Post!\n\n"
    if os.path.exists(txt_path):
        with open(txt_path, "r", encoding="utf-8") as f:
            caption += f.read()[:950]  # Telegram caption max length

    print(f"📡 Sending video to Telegram chat {chat_id}...")
    url = f"https://api.telegram.org/bot{bot_token}/sendVideo"
    with open(video_path, "rb") as video_file:
        files = {"video": video_file}
        data = {"chat_id": chat_id, "caption": caption}
        resp = requests.post(url, files=files, data=data, timeout=120)
        if resp.status_code == 200:
            print("✅ Successfully delivered to Telegram!")
        else:
            print(f"⚠️ Telegram delivery error: {resp.status_code} - {resp.text}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python cloud_uploader.py <video_path> <txt_path>")
        sys.exit(0)

    v_path = sys.argv[1]
    t_path = sys.argv[2]
    if os.path.exists(v_path):
        send_telegram(v_path, t_path)
    else:
        print(f"Video file not found at: {v_path}")
