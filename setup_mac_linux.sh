#!/bin/sh
# Mac/Linux: sh setup_mac_linux.sh   (pehle: brew install python@3.12 ffmpeg  ya  sudo apt install python3.12-venv ffmpeg libraqm0)
set -e
python3 -m venv .venv && . .venv/bin/activate
pip install --upgrade pip && pip install -r requirements.txt && pip install --no-deps tinysoundfont
mkdir -p models
curl -L -o models/kokoro-v1.0.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
curl -L -o models/voices-v1.0.bin https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
curl -L -o models/GeneralUser-GS.sf2 https://github.com/mrbumpy409/GeneralUser-GS/raw/main/GeneralUser-GS.sf2
python check_env.py
