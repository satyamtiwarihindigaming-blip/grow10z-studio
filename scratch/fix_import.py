with open("studio_ramayana/character_engine/cinematic_character_v2.py", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("import skia", "import numpy as np\nimport skia")

with open("studio_ramayana/character_engine/cinematic_character_v2.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Added numpy import successfully!")
