import os
import sys
from pathlib import Path

# Repo root is 4 levels up from this file
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(BASE_DIR))

from studio_ramayana.character_engine.playwright_typography import (
    generate_cliffhanger_badge,
    generate_manuscript_image
)

ep_dir = BASE_DIR / "studio_ramayana" / "episodes" / "ep008"
ep_dir.mkdir(parents=True, exist_ok=True)

badge_path = ep_dir / "cliffhanger_badge.png"
generate_cliffhanger_badge(
    str(badge_path),
    title="अगले भाग में: भव्य श्रीराम-सीता विवाह महोत्सव! 🌸",
    subtitle="मिथिला में बरसे फूल और गूँजे वैदिक मंत्र — फॉलो करें @grow10z"
)
print(f"✅ Generated cliffhanger badge: {badge_path}")

manuscript_path = ep_dir / "manuscript_page.png"
generate_manuscript_image(
    "श्रीराम-परशुराम मिलन",
    "॥ वैष्णव धनुष की प्रत्यंचा ॥",
    manuscript_path
)
print(f"✅ Generated manuscript page: {manuscript_path}")
