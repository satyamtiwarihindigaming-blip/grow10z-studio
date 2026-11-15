import json
import urllib.request
import urllib.error

TOKEN = "DhMsR0Uslt8x2IUO_1F4nAUi2U5qelo7gDVexB3wZEJ"
GRAPHQL_URL = "https://api.buffer.com/graphql"

query = """
query GetPost($id: RecordID!) {
  post(id: $id) {
    id
    status
    state
    dueAt
    sentAt
    error {
      message
    }
  }
}
"""

payload = json.dumps({"query": query, "variables": {"id": "6af88692e86a5789a6b891c7"}}).encode("utf-8")
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
