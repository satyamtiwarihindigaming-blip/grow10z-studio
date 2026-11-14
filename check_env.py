# Har cheez ka asli pass/fail. Chalao: python check_env.py
import sys, os, shutil, importlib
res=[]
def ok(name,cond,note=""): res.append((name,bool(cond),note)); print(("PASS " if cond else "FAIL ")+name+(" - "+str(note) if note else ""))
ok("python>=3.10",sys.version_info>=(3,10),sys.version.split()[0])
for m in ("numpy","scipy","PIL","skia","pymunk","pedalboard","soundfile","kokoro_onnx","tinysoundfont","imageio_ffmpeg"):
    try: importlib.import_module(m); ok("import "+m,True)
    except Exception as e: ok("import "+m,False,repr(e)[:80])
try:
    from PIL import features; ok("Pillow raqm (Hindi shaping)",features.check("raqm"),"" if features.check("raqm") else "FAIL: Playwright fallback use karo (skill: caption-system)")
except Exception as e: ok("raqm",False,repr(e)[:60])
ok("ffmpeg on PATH",shutil.which("ffmpeg"),shutil.which("ffmpeg") or "install karo ya imageio_ffmpeg.get_ffmpeg_exe()")
for f in ("models/kokoro-v1.0.onnx","models/voices-v1.0.bin","models/GeneralUser-GS.sf2","fonts/FreeSansBold.ttf"):
    ok("file "+f,os.path.exists(f) and os.path.getsize(f)>100000,f"{os.path.getsize(f)//1024} KB" if os.path.exists(f) else "missing")
try:
    from PIL import Image, ImageDraw, ImageFont; import numpy as np
    im=Image.new("L",(600,200),0); ImageDraw.Draw(im).text((300,100),"आख़िरी बस",font=ImageFont.truetype("fonts/FreeSansBold.ttf",90),fill=255,anchor="mm")
    os.makedirs("out",exist_ok=True); im.save("out/devanagari_test.png"); ok("Devanagari render test",np.array(im).sum()>50000,"out/devanagari_test.png dekho: matras sahi hone chahiye")
except Exception as e: ok("Devanagari render test",False,repr(e)[:80])
bad=[n for n,c,_ in res if not c]; print("\nSUMMARY:", "ALL PASS" if not bad else "FAILED -> "+", ".join(bad))
