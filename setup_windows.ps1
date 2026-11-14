# Windows PowerShell: .\setup_windows.ps1   (Antigravity agent ye script chala sakta hai; fail ho to error dikhao aur fix karo)
winget install -e --id Python.Python.3.12
winget install -e --id Gyan.FFmpeg
winget install -e --id Git.Git
python -m venv .venv
.\.venv\Scripts\python -m pip install --upgrade pip
.\.venv\Scripts\pip install -r requirements.txt
.\.venv\Scripts\pip install --no-deps tinysoundfont
New-Item -ItemType Directory -Force models | Out-Null
Invoke-WebRequest -Uri https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx -OutFile models\kokoro-v1.0.onnx
Invoke-WebRequest -Uri https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin -OutFile models\voices-v1.0.bin
Invoke-WebRequest -Uri https://github.com/mrbumpy409/GeneralUser-GS/raw/main/GeneralUser-GS.sf2 -OutFile models\GeneralUser-GS.sf2
.\.venv\Scripts\python check_env.py
