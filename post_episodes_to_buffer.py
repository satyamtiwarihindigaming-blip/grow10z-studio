import urllib.request
import urllib.error
import json

TOKEN = "DhMsR0Uslt8x2IUO_1F4nAUi2U5qelo7gDVexB3wZEJ"
GRAPHQL_URL = "https://api.buffer.com/graphql"
GROW10Z_CHANNEL_ID = "6af8338e62b70b94b02aeee3"

ep002_video = "https://github.com/satyamtiwarihindigaming-blip/grow10z-studio/releases/download/v0.0.2/RAMAYANA_EP002_Vishwamitra_Aagaman.mp4"

caption = """"मुनिवर! मेरे प्राण ले लीजिए, पर मेरे राम को न मांगिए..." जब अयोध्या में हुआ विश्वामित्र का आगमन! 🚩 #GROW10Z #रामायण

अयोध्या का भव्य राजदरबार... जहाँ चारों राजकुमारों के बाल्यकाल से महल गूँज रहा था।
तभी दरबार में महाक्रोध और तपस्या के प्रतीक महर्षि विश्वामित्र का अचानक आगमन हुआ! 
यज्ञ की रक्षा और राक्षसों के संहार हेतु जब महर्षि ने श्रीराम को माँगा, तो महाराज दशरथ का हृदय काँप उठा।
किंतु स्वयं मर्यादा पुरुषोत्तम श्रीराम और लक्ष्मण ने आगे बढ़कर धर्म की रक्षा हेतु कोदण्ड धनुष उठाया!
धर्म और अधर्म के पहले महा-युद्ध का दिव्य प्रस्थान।

👇 प्रभु श्रीराम और महर्षि विश्वामित्र के इस प्रसंग पर "जय श्री राम" लिखें! 🚩 (अगला भाग: राक्षसी ताड़का का संहार!)

#श्रीराम #रामायण #विश्वामित्र #Ayodhya #Ramayan #ShriRam #SanatanDharma #IndianMythology #GROW10Z #DivineAnimation"""

def post_ep002():
    mutation = """
    mutation CreatePost($input: CreatePostInput!) {
      createPost(input: $input) {
        ... on PostActionSuccess {
          post {
            id
            status
            text
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
        "text": caption,
        "schedulingType": "automatic",
        "mode": "addToQueue",
        "needsApproval": False,
        "assets": [
            {
                "video": {
                    "url": ep002_video
                }
            }
        ],
        "metadata": {
            "instagram": {
                "type": "reel",
                "shouldShareToFeed": True,
                "isAiGenerated": False
            }
        }
    }

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
            print(json.dumps(data, indent=2))
            return data
    except urllib.error.HTTPError as e:
        print("HTTP Error:", e.code, e.read().decode())
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    post_ep002()
