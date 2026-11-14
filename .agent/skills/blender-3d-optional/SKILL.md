---
name: blender-3d-optional
description: Optional 3D hero shots with headless Blender (free) composited into the 2D pipeline. Use only when the human asks for 3D or a shot cannot be done in 2.5D.
---
# Blender 3D (optional)

- Install Blender from blender.org (free). Headless render: `blender -b scene.blend -P render_shot.py -- --frames 1 90` → PNG sequence with alpha, then composite in the 2D pipeline.
- Default stays **2.5D parallax** (fast, consistent). Use 3D only for hero shots (bus interior sweep, tiffin close-up).
- Toon look to match style: Principled BSDF → Shader-to-RGB → colour ramp (3 stops), rim light via Fresnel, 1 key + 1 rim light, EEVEE for speed. Keep palette identical to `character-style-2d`.
- Time budget: without a GPU, keep ≤ 90 frames per shot at 1080×1920, 32 samples; estimate on 3 test frames first and report the estimate before committing.
- Never claim a 3D shot renders until the PNG sequence exists and was viewed.
