import asyncio
import edge_tts

async def main():
    communicate = edge_tts.Communicate("क्या आपने कभी सोचा है", voice="hi-IN-MadhurNeural")
    types = set()
    async for chunk in communicate.stream():
        types.add(chunk["type"])
        if chunk["type"] != "audio":
            print(chunk)
    print("All types received:", types)

asyncio.run(main())
