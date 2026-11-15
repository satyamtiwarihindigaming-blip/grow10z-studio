import json
import urllib.request
import time

TOKEN = "DhMsR0Uslt8x2IUO_1F4nAUi2U5qelo7gDVexB3wZEJ"
GRAPHQL_URL = "https://api.buffer.com/graphql"
POST_ID = "6af88e5376c23bf1c7295c1d"

query = f"""
query {{
  post(input: {{ id: "{POST_ID}" }}) {{
    id
    status
    sentAt
    externalLink
    error {{
      message
    }}
  }}
}}
"""

payload = json.dumps({"query": query}).encode("utf-8")
req = urllib.request.Request(
    GRAPHQL_URL,
    data=payload,
    headers={
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }
)

for i in range(15):
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            post = data.get("data", {}).get("post", {})
            status = post.get("status")
            ext_link = post.get("externalLink")
            err = post.get("error")
            print(f"[{i+1}/15] Status: {status} | Link: {ext_link} | Error: {err}")
            if status == "sent":
                print(f"🎉 Post is LIVE! Permalink: {ext_link}")
                break
            elif status == "error":
                print(f"❌ Error sending post: {err}")
                break
    except Exception as e:
        print(f"Request error: {e}")
    time.sleep(4)
