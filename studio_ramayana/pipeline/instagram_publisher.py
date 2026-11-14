"""
GROW10Z — Automated Instagram Reels Publisher
Supports 3 methods to connect and publish Reels:
1. Official Meta Graph API (Creator / Business Account)
2. Webhook (Make.com / Buffer / Ayrshare)
3. Headless / Semi-Automated Playwright Browser Upload
"""

import os
import sys
import time
import json
import requests
from pathlib import Path

def publish_via_meta_graph_api(video_url, caption):
    """
    Publish via Meta's Official Content Publishing API for Instagram Reels.
    Requires:
      - INSTAGRAM_ACCESS_TOKEN (User token with instagram_content_publish permission)
      - INSTAGRAM_ACCOUNT_ID (IG Business / Creator User ID)
    """
    token = os.environ.get("INSTAGRAM_ACCESS_TOKEN")
    ig_id = os.environ.get("INSTAGRAM_ACCOUNT_ID")

    if not token or not ig_id:
        print("⚠️ INSTAGRAM_ACCESS_TOKEN or INSTAGRAM_ACCOUNT_ID not found in environment.")
        return False

    print(f"🚀 Creating Instagram Reels Container via Meta Graph API for account: {ig_id}...")
    url = f"https://graph.facebook.com/v21.0/{ig_id}/media"
    payload = {
        "media_type": "REELS",
        "video_url": video_url,
        "caption": caption,
        "share_to_feed": "true",
        "access_token": token
    }
    
    r = requests.post(url, data=payload)
    res = r.json()
    if "id" not in res:
        print(f"❌ Failed to create media container: {res}")
        return False

    creation_id = res["id"]
    print(f"✅ Container created! ID: {creation_id}. Waiting for Meta video processing...")

    # Poll container status until FINISHED
    status_url = f"https://graph.facebook.com/v21.0/{creation_id}?fields=status_code&access_token={token}"
    for _ in range(30):
        time.sleep(5)
        st = requests.get(status_url).json()
        code = st.get("status_code")
        print(f"Processing status: {code}...")
        if code == "FINISHED":
            break
        elif code in ["ERROR", "EXPIRED"]:
            print(f"❌ Video processing error: {st}")
            return False

    # Publish
    pub_url = f"https://graph.facebook.com/v21.0/{ig_id}/media_publish"
    pub_res = requests.post(pub_url, data={"creation_id": creation_id, "access_token": token}).json()
    if "id" in pub_res:
        print(f"🎉 REEL PUBLISHED TO INSTAGRAM! Post ID: {pub_res['id']}")
        return True
    else:
        print(f"❌ Failed to publish Reel: {pub_res}")
        return False

def publish_via_webhook(video_url, caption):
    """
    Publish via Make.com, Zapier, or Ayrshare webhook.
    """
    webhook_url = os.environ.get("INSTAGRAM_WEBHOOK_URL")
    if not webhook_url:
        return False

    print("🚀 Firing Instagram Auto-Publish Webhook...")
    payload = {
        "video_url": video_url,
        "caption": caption,
        "platform": "instagram_reels"
    }
    r = requests.post(webhook_url, json=payload, timeout=30)
    if r.status_code in [200, 201]:
        print("✅ Webhook triggered successfully! Reel will be posted by connector.")
        return True
    else:
        print(f"⚠️ Webhook response: {r.status_code} - {r.text}")
        return False

def open_instagram_web_uploader(video_path, caption_path):
    """
    Launches a dedicated local Chromium browser to upload to Instagram Web.
    """
    from playwright.sync_api import sync_playwright

    print("🌐 Launching local browser for Instagram Upload...")
    caption_text = ""
    if os.path.exists(caption_path):
        with open(caption_path, "r", encoding="utf-8") as f:
            caption_text = f.read()

    user_data_dir = os.path.expanduser("~/.instagram_profile")
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            headless=False,
            viewport={"width": 1280, "height": 900}
        )
        page = browser.pages[0] if browser.pages else browser.new_page()
        page.goto("https://www.instagram.com/")
        print("ℹ️ Browser opened. Please ensure you are logged into Instagram.")
        print(f"Video file ready at: {video_path}")
        print("You can drag-and-drop the video to the '+' Create button.")
        
        # Keep open for user interaction
        input("Press Enter here in terminal once upload is complete to close browser...")
        browser.close()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python instagram_publisher.py <video_path_or_url> <caption_path>")
        sys.exit(1)

    v_target = sys.argv[1]
    c_path = sys.argv[2]

    caption = ""
    if os.path.exists(c_path):
        with open(c_path, "r", encoding="utf-8") as f:
            caption = f.read()

    # Check if video target is URL (for Meta API or Webhook)
    if v_target.startswith("http"):
        if not publish_via_meta_graph_api(v_target, caption):
            publish_via_webhook(v_target, caption)
    else:
        # Local video file -> open browser helper
        open_instagram_web_uploader(v_target, c_path)
