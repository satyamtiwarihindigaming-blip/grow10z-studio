# Ultimate Cinematic Studio — Memory & Rendering Architecture

## 1. Fast Mode Architecture (Default for 8GB RAM)
- **Target Resolution**: 1080 x 1920 (9:16 Vertical Video) or 720p preview.
- **Framerate**: 30.0 FPS.
- **Rendering Throughput**: **40 to 45 FPS** on AMD Ryzen 5 2500U.
- **Peak Memory Usage**: **< 350 MB RAM**.

## 2. Core Rendering Principles
1. **Snapshot Caching**:
   - Complex vector gradients and static scene layers are rasterized into `skia.Image` snapshots once during scene initialization.
   - During the per-frame render loop, only blits (`drawImage`) and lightweight transformations (translation, breathing float, particle offsets) are performed.
   - Avoid re-instantiating complex radial shaders or vector paths per-frame.

2. **Zero-Copy Byte Streaming**:
   - Frames are read directly from `skia.Surface` via `readPixels()` into a reusable bytearray buffer.
   - The buffer is piped directly into FFmpeg's `stdin` via subprocess pipe.
   - No intermediate PNG/JPEG image files are written to disk, saving SSD wear and eliminating disk I/O bottlenecks.

3. **Encoder Strategy on AMD APUs**:
   - **Multi-threaded CPU (`libx264 -preset ultrafast`)**: Performs at **40-45 FPS** by utilizing all 8 threads of the Ryzen 5 2500U with zero PCIe/driver sync latency.
   - **AMD AMF (`h264_amf`)**: Fully supported by the installed FFmpeg and driver version `26.20.12036.1`. Available for hardware-accelerated exports when CPU offloading is needed.

4. **Audio Subsystem**:
   - 44.1 kHz 16-bit PCM arrays.
   - Synchronous multi-track mixing: Voiceover, Tanpura Drone, Foley Reactions, Sub-bass Drops, and 0 dB Silence Vacuums.
   - Soft-limiting via `tanh` prevents clipping and audio distortion.
