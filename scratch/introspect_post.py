import json
import urllib.request

TOKEN = "DhMsR0Uslt8x2IUO_1F4nAUi2U5qelo7gDVexB3wZEJ"
GRAPHQL_URL = "https://api.buffer.com/graphql"

# Introspect Post fields
query = """
query {
  __type(name: "Post") {
    fields {
      name
      type {
        name
        kind
      }
    }
  }
}
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

try:
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())
        fields = [f["name"] for f in data["data"]["__type"]["fields"]]
        print("Fields on Post:", fields)
except Exception as e:
    print(f"Error: {e}")
