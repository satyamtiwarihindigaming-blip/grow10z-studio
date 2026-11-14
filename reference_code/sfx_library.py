"""Free, code-only SFX synthesizers (numpy/scipy). Run `python reference_code/sfx_library.py` to render every sound into out/sfx_test/."""
import numpy as np
from scipy.signal import butter, lfilter
SR=44100; rng=np.random.default_rng(7)
def T(n): return np.arange(n)/SR
def noise(n): return rng.standard_normal(n)
def lp(x,fc): b,a=butter(2,fc/(SR/2)); return lfilter(b,a,x)
def hp(x,fc): b,a=butter(2,fc/(SR/2),"high"); return lfilter(b,a,x)
def bp(x,lo,hi): b,a=butter(2,[lo/(SR/2),hi/(SR/2)],"band"); return lfilter(b,a,x)
def thump(f0=90,f1=40,d=0.25,amp=1.0):
    n=int(d*SR); x=T(n); f=f1+(f0-f1)*np.exp(-x*30); return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-x*14)*amp
def heartbeat(bpm=72,dur=6.0,amp=0.8):
    out=np.zeros(int(dur*SR)); step=60/bpm; t=0.0
    while t<dur-0.4:
        for off,a in ((0,1.0),(0.18,0.6)):
            s=thump(60,35,0.18,amp*a); i=int((t+off)*SR); out[i:i+len(s)]+=s[:len(out)-i]
        t+=step
    return out
def breath(kind="in",amp=0.25):
    d=0.6 if kind=="in" else 0.8; n=int(d*SR); x=T(n); a=0.3 if kind=="in" else 0.15
    e=np.clip(x/(d*a),0,1)*np.clip((d-x)/(d*(1-a)),0,1); return bp(noise(n),500,5000)*e*amp
def gasp(amp=0.4):
    d=0.35; n=int(d*SR); x=T(n); e=np.clip(x/0.06,0,1)*np.exp(-x*7); return bp(noise(n),700,6500)*e*amp
def gulp(amp=0.5):
    n=int(0.2*SR); x=T(n); f=220-120*x/0.2; return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-x*22)*amp
def bus_rumble(dur=8.0,amp=0.5):
    n=int(dur*SR); x=T(n); f=47+2*np.sin(2*np.pi*0.4*x); ph=2*np.pi*np.cumsum(f)/SR
    s=(2*((ph/(2*np.pi))%1)-1)*(0.65+0.35*np.sin(2*np.pi*23*x)); s=lp(s,320)+0.35*lp(noise(n),180)
    return s*np.minimum(1,x/0.5)*np.minimum(1,(dur-x)/0.5)*amp
def wind(dur=8.0,amp=0.35):
    n=int(dur*SR); x=T(n); a=lp(noise(n),500); b=bp(noise(n),400,1500); m=0.5+0.5*np.sin(2*np.pi*0.18*x)
    return (a*(1-m)+b*m*0.6)*amp*np.minimum(1,x/1.0)*np.minimum(1,(dur-x)/1.0)
def crickets(dur=8.0,amp=0.12):
    out=np.zeros(int(dur*SR)); t=0.0
    while t<dur-0.3:
        for k in range(int(rng.integers(3,6))):
            n=int(0.025*SR); x=T(n); p=np.sin(2*np.pi*4800*x)*np.hanning(n); i=int((t+k*0.04)*SR); out[i:i+n]+=p[:len(out)-i]*amp
        t+=rng.uniform(0.35,0.8)
    return out
def door_hiss(amp=0.5):
    n=int(0.8*SR); x=T(n); th=np.pad(thump(120,60,0.3,0.6),(0,n-int(0.3*SR)))
    return (bp(noise(n),2000,8000)*np.exp(-x*5)*0.8+th)*amp
def clink(amp=0.5):
    n=int(0.5*SR); x=T(n); s=sum(np.sin(2*np.pi*f*x)*a for f,a in ((1800,1),(2750,.7),(4200,.4)))
    return s*np.exp(-x*16)*amp*0.4
def phone_buzz(dur=2.0,amp=0.4):
    n=int(dur*SR); x=T(n); gate=(np.sin(2*np.pi*3.3*x)>0).astype(float); s=np.sign(np.sin(2*np.pi*165*x))*0.5+np.sin(2*np.pi*165*x)
    return lp(s,1200)*gate*amp*np.minimum(1,(dur-x)/0.1)
def riser(dur=2.5,amp=0.5):
    n=int(dur*SR); x=T(n); f=200+2800*(x/dur)**2; tone=np.sin(2*np.pi*np.cumsum(f)/SR); nz=hp(noise(n),1500)
    return (0.5*tone+0.8*nz)*(x/dur)**2.2*amp
def impact(amp=0.9):
    n=int(1.2*SR); x=T(n); return (thump(75,28,1.2,1.0)+0.5*lp(noise(n),2200)*np.exp(-x*6))*amp
def whoosh(dur=0.7,amp=0.5):
    n=int(dur*SR); x=T(n); return bp(noise(n),300,3500)*np.sin(np.pi*np.clip(x/dur,0,1))**2*amp
def tick(amp=0.4):
    n=int(0.05*SR); x=T(n); return (np.sin(2*np.pi*2200*x)+0.4*noise(n))*np.exp(-x*80)*amp
def place(buf,snd,t,gain=1.0):
    i=int(t*SR)
    if 0<=i<len(buf): buf[i:i+len(snd)]+=snd[:len(buf)-i]*gain
    return buf
if __name__=="__main__":
    import os, soundfile as sf
    os.makedirs("out/sfx_test",exist_ok=True)
    for name,fn in [("heartbeat",heartbeat),("breath",breath),("gasp",gasp),("gulp",gulp),("bus_rumble",bus_rumble),("wind",wind),("crickets",crickets),("door_hiss",door_hiss),("clink",clink),("phone_buzz",phone_buzz),("riser",riser),("impact",impact),("whoosh",whoosh),("tick",tick)]:
        s=fn(); s=s/(np.max(np.abs(s))+1e-9)*0.9; sf.write(f"out/sfx_test/{name}.wav",s.astype(np.float32),SR); print(f"{name:12s} {len(s)/SR:5.2f}s peak {np.max(np.abs(s)):.2f}")
