import json
import urllib.request

TOKEN = "DhMsR0Uslt8x2IUO_1F4nAUi2U5qelo7gDVexB3wZEJ"
GRAPHQL_URL = "https://api.buffer.com/graphql"

query = """
query GetChannelPosts($channelId: String!) {
  channel(id: $channelId) {
    id
    name
    service
    posts {
      total
      edges {
        node {
          id
          status
          text
          sentAt
        }
      }
    }
  }
}
"""

payload = json.dumps({"query": query, "variables": {"channelId": "6af8338e62b70b94b02aeee3"}}).encode("utf-8")
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
        print(json.dumps(data, indent=2))
except Exception as e:
    print(f"Error: {e}")
