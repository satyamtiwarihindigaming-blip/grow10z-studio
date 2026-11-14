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

def create_instagram_post(text, video_url=None, share_now=True):
    """
    Creates a Reel on Instagram @grow10z via Buffer GraphQL API.
    """
    mode = "shareNow" if share_now else "addToQueue"
    
    mutation = """
    mutation CreatePost($input: CreatePostInput!) {
      createPost(input: $input) {
        ... on PostActionSuccess {
          post {
            id
            status
            text
            dueAt
          }
        }
        ... on InvalidInputError {
          message
        }
        ... on UnexpectedError {
          message
        }
        ... on LimitReachedError {
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
                "type": "reel",
                "shouldShareToFeed": True,
                "isAiGenerated": False
            }
        }
    }

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
    if len(sys.argv) > 2:
        caption_text = sys.argv[1]
        v_url = sys.argv[2]
        create_instagram_post(caption_text, video_url=v_url, share_now=True)
    else:
        print("Buffer Publisher ready for @grow10z!")
