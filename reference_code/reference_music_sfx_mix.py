import numpy as np, soundfile as sf, json
from scipy.signal import resample_poly, lfilter, butter
SR=44100; rng=np.random.default_rng(7)
dur=json.load(open("dur.json"))
# ---------- timeline ----------
GAP=0.5; t=1.0; starts=[]; ends=[]
for d in dur:
    starts.append(t); ends.append(t+d); t+=d+GAP
END=ends[-1]+2.2
json.dump({"starts":starts,"ends":ends,"end":END},open("timeline.json","w"))
N=int(END*SR); 
def T(n): return np.arange(n)/SR
def env_ad(n,a=0.01,dec=8.0):
    x=T(n); e=np.minimum(1,x/a)*np.exp(-x*dec); return e
def lp(x,fc,order=2): b,a=butter(order,fc/(SR/2)); return lfilter(b,a,x)
def hp(x,fc,order=2): b,a=butter(order,fc/(SR/2),'high'); return lfilter(b,a,x)
def bp(x,lo,hi): b,a=butter(2,[lo/(SR/2),hi/(SR/2)],'band'); return lfilter(b,a,x)
def noise(n): return rng.standard_normal(n)
# ---------- sfx ----------
def whoosh(d=0.7):
    n=int(d*SR); x=T(n); e=np.sin(np.pi*np.clip(x/d,0,1))**2
    return bp(noise(n),300,3500)*e*1.2
def horn(d=0.28):
    n=int(d*SR); x=T(n); s=0
    for f in (392,494): s=s+np.sign(np.sin(2*np.pi*f*x))*0.5+np.sin(2*np.pi*f*x)
    return lp(s,2500)*np.minimum(1,x/0.01)*np.minimum(1,(d-x)/0.03)*0.35
def thump(f0=90,f1=40,d=0.25,amp=1.0):
    n=int(d*SR); x=T(n); f=f1+(f0-f1)*np.exp(-x*30); ph=2*np.pi*np.cumsum(f)/SR
    return np.sin(ph)*np.exp(-x*14)*amp
def tick(f=2200,d=0.06,amp=0.5):
    n=int(d*SR); x=T(n); return (np.sin(2*np.pi*f*x)+0.5*noise(n))*np.exp(-x*70)*amp
def sputter(d):
    out=np.zeros(int(d*SR)); t=0.0
    while t<d-0.2:
        p=thump(80,38,0.22,0.9)+0.4*lp(noise(int(0.22*SR)),400)*np.exp(-T(int(0.22*SR))*20)
        i=int(t*SR); out[i:i+len(p)]+=p[:len(out)-i]
        if rng.random()<0.6:
            k=tick(rng.choice([1800,2400,3100]),0.05,0.4); j=i+int(0.11*SR); out[j:j+len(k)]+=k[:max(0,len(out)-j)]
        t+=rng.choice([0.16,0.19,0.23,0.31,0.45])
    return out
def squeal(d=0.7):
    n=int(d*SR); x=T(n); f=3000-1400*x/d; ph=2*np.pi*np.cumsum(f)/SR
    s=np.sin(ph)+0.4*np.sin(2*ph)+0.3*noise(n); return bp(s,1500,5000)*np.sin(np.pi*np.clip(x/d,0,1))**0.6*0.5
def ding(f=1320,d=1.3,amp=0.6):
    n=int(d*SR); x=T(n); s=np.sin(2*np.pi*f*x)+0.4*np.sin(2*np.pi*2*f*x)+0.2*np.sin(2*np.pi*3.01*f*x)
    return s*np.minimum(1,x/0.003)*np.exp(-x*3.2)*amp
def clank(amp=0.7):
    n=int(0.45*SR); x=T(n); s=sum(np.sin(2*np.pi*f*x)*a for f,a in ((620,1),(1130,.7),(1870,.5),(2750,.35)))
    return (s+0.6*noise(n)*np.exp(-x*80))*np.exp(-x*13)*amp*0.5
def pop(d=0.12,amp=0.5):
    n=int(d*SR); x=T(n); f=380+900*x/d; return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-x*22)*amp
def purr(d,amp=0.5):
    n=int(d*SR); x=T(n); f=48+3*np.sin(2*np.pi*0.7*x); ph=2*np.pi*np.cumsum(f)/SR
    s=(2*((ph/(2*np.pi))%1)-1)*(0.6+0.4*np.sin(2*np.pi*24*x)); s=lp(s,380)+0.15*lp(noise(n),300)
    return s*np.minimum(1,x/0.3)*np.minimum(1,(d-x)/0.4)*amp
def sparkle(d=1.5):
    out=np.zeros(int(d*SR))
    for k in range(9):
        p=ding(float(rng.choice([2093,2637,3136,3520])),0.5,0.25); i=int((k*d/10+rng.random()*0.05)*SR); out[i:i+len(p)]+=p[:len(out)-i]
    return out
def tada():
    out=np.zeros(int(2.2*SR))
    for k,f in enumerate((523,659,784,1046)):
        p=ding(f,1.6,0.5); i=int(k*0.11*SR); out[i:i+len(p)]+=p[:len(out)-i]
    return out
# ---------- music ----------
def pluck(f,d=0.6,amp=0.5):
    L=int(SR/f); cur=rng.uniform(-1,1,L); out=[]; n=int(d*SR); 
    while sum(len(o) for o in out)<n: out.append(cur); cur=0.996*0.5*(cur+np.roll(cur,1))
    y=np.concatenate(out)[:n]; return lp(y,3500)*amp*np.minimum(1,(n-np.arange(n))/(0.05*SR))
BPM=104; step=60/BPM/4
mus=np.zeros(N)
def put(buf,s,t):
    i=int(t*SR); 
    if i<0 or i>=len(buf): return
    buf[i:i+len(s)]+=s[:len(buf)-i]
D=[146.83,155.56,185.0,196.0,220.0,233.08,261.63,293.66]  # D phrygian dominant
motif=[(0,3),(2,4),(4,2),(6,1),(8,0),(10,1),(12,2),(14,1),(16,0),(18,2),(20,3),(22,4),(24,5),(26,4),(28,3),(30,2)]
nb=int(END/(step*16))+1
kick=thump(100,45,0.3,0.9); tak=(bp(noise(int(0.12*SR)),1800,5000)+0.7*np.sin(2*np.pi*330*T(int(0.12*SR))))*np.exp(-T(int(0.12*SR))*35)*0.5
dha=(thump(160,90,0.2,0.6)+0.4*bp(noise(int(0.2*SR)),600,2500)*np.exp(-T(int(0.2*SR))*25))
shk=hp(noise(int(0.05*SR)),6000)*np.exp(-T(int(0.05*SR))*60)*0.15
for b in range(nb):
    t0=b*step*16
    for s_ in (0,8,10): put(mus,kick,t0+s_*step)
    for s_ in (4,12): put(mus,tak,t0+s_*step)
    for s_ in (14,15): put(mus,dha,t0+s_*step)
    for s_ in range(0,16,2): put(mus,shk,t0+s_*step)
    if b%2==0:
        for st,idx in motif:
            if st<16*2: 
                put(mus,pluck(D[idx]*(2 if idx<3 else 1),0.55,0.55),t0+st*step*1.0)  # two bars
# drone
x=T(N); drone=(np.sin(2*np.pi*73.42*x)+0.5*np.sin(2*np.pi*110.0*x)+0.25*np.sin(2*np.pi*146.8*x))*(0.7+0.3*np.sin(2*np.pi*0.25*x))*0.12
mus=mus*0.55+drone
# ---------- voice ----------
voice=np.zeros(N)
for i,(s,d) in enumerate(zip(starts,dur)):
    w,sr=sf.read(f"L{i+1}.wav"); w=resample_poly(w,147,80); w=w/np.max(np.abs(w))*0.95
    put(voice,w,s)
venv=lp(np.abs(voice),8,1); venv=np.clip(venv/ (venv.max()+1e-9)*3,0,1)
mus=mus*(1-0.65*venv)*0.45
# ---------- sfx placement ----------
sfx=np.zeros(N)
s1,s2,s3,s4,s5,s6=starts
put(sfx,whoosh(0.7),0.1); put(sfx,horn(0.2),0.55); put(sfx,horn(0.2),0.82)
put(sfx,sputter(ends[1]-s2+0.3)*0.45,s2)
put(sfx,squeal(0.7),ends[1]-0.9)
put(sfx,whoosh(0.8),s3-0.35); put(sfx,squeal(0.6)*0.8,s3+0.9); put(sfx,ding(1568,1.4,0.5),s3+2.0); put(sfx,thump(70,40,0.3,0.7),s3+1.6)
fo=[0.04,1.26,1.75,2.36,2.97]
for f in fo: put(sfx,pop(),s4+f-0.05); put(sfx,clank(),s4+f+0.02)
put(sfx,purr(dur[4]+1.2,0.55),s5-0.5); put(sfx,sparkle(1.6),s5+0.6); put(sfx,ding(1760,1.2,0.5),s5+0.6)
put(sfx,whoosh(0.6),s6-0.3); put(sfx,tada(),ends[5]+0.1); put(sfx,sparkle(1.6),ends[5]+0.2)
mix=voice*1.0+mus*1.0+sfx*0.55
mix=mix/np.max(np.abs(mix))*0.92
st=np.stack([mix,mix],1).astype(np.float32); sf.write("mix.wav",st,SR)
np.save("venv.npy",venv)
# speech segments per line for word timing
seg={}
for i in range(6):
    w,sr=sf.read(f"L{i+1}.wav"); e=np.abs(w); hop=int(sr*0.01); r=np.array([e[j:j+hop].mean() for j in range(0,len(e)-hop,hop)])
    on=r>0.02*r.max(); S=[];st_=None
    for j,v in enumerate(on):
        if v and st_ is None: st_=j
        if not v and st_ is not None:
            if j-st_>=4: S.append((st_*0.01,j*0.01)); 
            st_=None
    if st_ is not None: S.append((st_*0.01,len(on)*0.01))
    # merge gaps <0.09
    M=[]
    for a,b in S:
        if M and a-M[-1][1]<0.09: M[-1]=(M[-1][0],b)
        else: M.append((a,b))
    seg[i+1]=M
json.dump(seg,open("segs.json","w")); print({k:[(round(a,2),round(b,2)) for a,b in v] for k,v in seg.items()}); print("END",END)
