# GROW10Z Ramayana Studio Architecture

```
                  +----------------------------------------------+
                  |         STORY DATABASE (10 Episodes)         |
                  | Valmiki Ramayana & Ramcharitmanas Tradition  |
                  +----------------------------------------------+
                                         |
                                         v
                  +----------------------------------------------+
                  |                 AUDIO ENGINE                 |
                  |  Kokoro-ONNX Hindi Multi-voice (Ram/Sita/..) |
                  |  + Demucs DSP Noise Cleaning & Balancing     |
                  |  + Whisper.cpp (Large-v3) Micro-Timestamps   |
                  +----------------------------------------------+
                                         |
                                         v
       +---------------------------------+---------------------------------+
       |                                                                   |
       v                                                                   v
+-----------------------------+                             +-----------------------------+
|    3D BOOK ENGINE           |                             |    3D ENVIRONMENT ENGINE    |
| - Ancient Manuscript Rig    |                             | - Ayodhya Golden Palace     |
| - Sanskrit Borders & Gold   |                             | - Sarayu River & Forest     |
| - 3D Dolly into Page        |                             | - Procedural Vedic Arches   |
+-----------------------------+                             +-----------------------------+
       \                                                                   /
        \                                                                 /
         v                                                               v
       +-------------------------------------------------------------------+
       |                 3D MYTHOLOGICAL CHARACTER ENGINE                  |
       |  - Detailed Human Anatomy + Vedic Costumes & Pitambari           |
       |  - Golden Mukut, Kundal, Dhanush-Baan, Kavach                    |
       |  - Facial Expression Blendshapes + Natural Breathing & Gestures  |
       +-------------------------------------------------------------------+
                                         |
                                         v
                  +----------------------------------------------+
                  |               HYPERFRAMES RENDER             |
                  |  Three.js WebGL 60fps + Skia Post-Composite  |
                  |  1080x1920 Vertical (Reels / Shorts Format)  |
                  +----------------------------------------------+
                                         |
                                         v
                  +----------------------------------------------+
                  |         OUTPUT & STUDIO DASHBOARD            |
                  |  out/epNN/epNN_final.mp4 + Live Local Web UI |
                  +----------------------------------------------+
```
