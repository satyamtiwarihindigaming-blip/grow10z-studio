"""Hindi script ko Kokoro voices me bolwao aur pitch (F0) compare karo. python reference_code/tts_compare_voices.py"""
import numpy as np, soundfile as sf, os
from kokoro_onnx import Kokoro
k=Kokoro("models/kokoro-v1.0.onnx","models/voices-v1.0.bin"); TXT=open("project/episodes/ep01/script_hi.txt",encoding="utf-8").read().replace("\n"," ")
def f0(x,sr):
    x=x[:sr*10]; fr=int(0.04*sr); hop=int(0.02*sr); v=[]
    for i in range(0,len(x)-fr,hop):
        s=x[i:i+fr]
        if np.sqrt(np.mean(s**2))<0.02: continue
        s=s-s.mean(); ac=np.correlate(s,s,"full")[fr-1:]; lo,hi=int(sr/300),int(sr/70)
        if ac[0]<=0: continue
        j=int(np.argmax(ac[lo:hi]))
        if ac[lo+j]/ac[0]>0.3: v.append(sr/(lo+j))
    return float(np.median(v)) if v else 0
os.makedirs("out/voices",exist_ok=True)
for vc in ("hm_omega","hm_psi","hf_alpha","hf_beta"):
    s,sr=k.create(TXT,voice=vc,speed=0.92,lang="hi"); sf.write(f"out/voices/{vc}.wav",s,sr); print(vc,"F0 %.0f Hz"%f0(s,sr),"dur %.1fs"%(len(s)/sr))
