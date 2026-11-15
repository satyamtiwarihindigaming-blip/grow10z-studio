import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from studio_ramayana.character_engine.playwright_typography import generate_cliffhanger_badge

out_path = BASE_DIR / "studio_ramayana" / "episodes" / "ep006" / "cliffhanger_badge.png"
generate_cliffhanger_badge(
    str(out_path),
    title="अगले भाग में: परशुराम-लक्ष्मण संवाद! ⚡",
    subtitle="देखिए सबसे बड़ा महा-टकराव — फॉलो करें @grow10z"
)
print(f"Generated cliffhanger badge: {out_path}")
