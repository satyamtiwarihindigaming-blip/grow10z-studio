"""
GROW10Z — Automated Buffer & Instagram Publisher
Uses Buffer's official GraphQL API with the verified Access Token.
Target Channel: grow10z (Instagram) [ID: 6af8338e62b70b94b02aeee3]
"""

import os
import sys
import json
import urllib.request
import urllib.error

TOKEN = os.environ.get("BUFFER_ACCESS_TOKEN", "DhMsR0Uslt8x2IUO_1F4nAUi2U5qelo7gDVexB3wZEJ")
GRAPHQL_URL = "https://api.buffer.com/graphql"
GROW10Z_CHANNEL_ID = "6af8338e62b70b94b02aeee3"

def create_instagram_post(text, video_url=None, first_comment=None, share_now=False):
    """
    Creates a post/Reel on Instagram @grow10z via Buffer.
    """
    mode = "shareNow" if share_now else "addToQueue"
    
    mutation = """
    mutation CreatePost($input: CreatePostInput!) {
      createPost(input: $input) {
        ... on CreatePostSuccess {
          post {
            id
            status
            text
            dueAt
          }
        }
        ... on CreatePostError {
          message
        }
      }
    }
    """
    
    post_input = {
        "channelId": GROW10Z_CHANNEL_ID,
        "text": text,
        "schedulingType": "automatic",
        "mode": mode,
        "needsApproval": False,
        "metadata": {
            "instagram": {
                "shouldShareToFeed": True,
                "isAiGenerated": False
            }
        }
    }

    if first_comment:
        post_input["metadata"]["instagram"]["firstComment"] = first_comment

    if video_url:
        post_input["assets"] = [{
            "video": {
                "url": video_url
            }
        }]

    payload = json.dumps({"query": mutation, "variables": {"input": post_input}}).encode("utf-8")
    req = urllib.request.Request(
        GRAPHQL_URL,
        data=payload,
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json"
        }
    )

    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            print(f"Buffer API Response: {json.dumps(data, indent=2)}")
            return data
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.read().decode()}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    print("Buffer Publisher ready for @grow10z!")
