import json, math, random, subprocess, sys, os
import numpy as np, soundfile as sf
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageFilter

W,H,FPS=1080,1920,30; SCH=940; S=3
TD="/home/claude/tts/"
TL=json.load(open(TD+"timeline.json")); ST=TL["starts"]; EN=TL["ends"]; END=TL["end"]
SEG={int(k):v for k,v in json.load(open(TD+"segs.json")).items()}
NF=int(END*FPS)
FD="/usr/share/fonts/truetype/freefont/FreeSansBold.ttf"; FL="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
@lru_cache(None)
def fd(sz): return ImageFont.truetype(FD,int(sz))
@lru_cache(None)
def fl(sz): return ImageFont.truetype(FL,int(sz))
def cl(x): return max(0.0,min(1.0,x))
def lerp(a,b,x): return a+(b-a)*x
def eo3(x): x=cl(x); return 1-(1-x)**3
def eob(x):
    x=cl(x); c1=1.70158; c3=c1+1; return 1+c3*(x-1)**3+c1*(x-1)**2

SKIN=(201,139,92,255); SKIN_D=(168,108,68,255); SAFA=(244,140,32,255); SAFA_D=(200,96,14,255); SAFA_L=(255,190,80,255)
GOLD=(255,205,60,255); NAVY=(31,58,95,255); NAVY_D=(20,38,66,255); RED=(226,0,21,255); BLACK=(26,20,22,255); WHITE=(250,250,250,255)

class D:
    def __init__(s,w,h):
        s.w,s.h=w,h; s.im=Image.new("RGBA",(w*S,h*S),(0,0,0,0)); s.d=ImageDraw.Draw(s.im)
    def _p(s,p): return [(x*S,y*S) for x,y in p]
    def poly(s,p,fill): s.d.polygon(s._p(p),fill=fill)
    def ell(s,b,fill,outline=None,width=0): s.d.ellipse([v*S for v in b],fill=fill,outline=outline,width=int(width*S))
    def rr(s,b,r,fill,outline=None,width=0): s.d.rounded_rectangle([v*S for v in b],radius=r*S,fill=fill,outline=outline,width=int(width*S))
    def line(s,p,fill,w): s.d.line(s._p(p),fill=fill,width=int(w*S),joint="curve")
    def arc(s,b,a0,a1,fill,w): s.d.arc([v*S for v in b],a0,a1,fill=fill,width=int(w*S))
    def clear(s,b): s.d.rectangle([v*S for v in b],fill=(0,0,0,0))
    def blend(s,fn):
        lay=Image.new("RGBA",s.im.size,(0,0,0,0)); fn(ImageDraw.Draw(lay)); s.im=Image.alpha_composite(s.im,lay); s.d=ImageDraw.Draw(s.im)
    def text(s,xy,t,font,fill): s.d.text((xy[0]*S,xy[1]*S),t,font=font,fill=fill,anchor="mm")
    def out(s): return s.im.resize((s.w,s.h),Image.LANCZOS)

def smooth(pts,it=3):
    for _ in range(it):
        n=[pts[0]]
        for a,b in zip(pts[:-1],pts[1:]):
            n+=[(0.75*a[0]+0.25*b[0],0.75*a[1]+0.25*b[1]),(0.25*a[0]+0.75*b[0],0.25*a[1]+0.75*b[1])]
        n.append(pts[-1]); pts=n
    return pts
def taper(d,pts,r0,r1,fill):
    p=smooth(pts); n=len(p)
    for i,(x,y) in enumerate(p):
        r=r0+(r1-r0)*i/(n-1); d.ell((x-r,y-r,x+r,y+r),fill)

def blit(cv,sp,x,y,alpha=1.0):
    x=int(round(x)); y=int(round(y)); w,h=sp.size; CW,CH=cv.size
    x0=max(0,x); y0=max(0,y); x1=min(CW,x+w); y1=min(CH,y+h)
    if x1<=x0 or y1<=y0 or alpha<=0: return
    c=sp.crop((x0-x,y0-y,x1-x,y1-y))
    if alpha<1: c=c.copy(); c.putalpha(c.getchannel("A").point(lambda v:int(v*alpha)))
    cv.alpha_composite(c,(x0,y0))
def scaled(sp,s): return sp.resize((max(1,int(sp.width*s)),max(1,int(sp.height*s))),Image.BICUBIC)

# ================= CHARACTER =================
def make_head():
    d=D(420,520)
    d.poly([(300,90),(380,130),(412,340),(372,356),(356,190),(300,150)],SAFA_D)
    d.poly([(312,102),(372,138),(396,326),(378,332),(354,192)],SAFA)
    d.ell((62,300,112,385),SKIN_D); d.ell((308,300,358,385),SKIN_D)
    d.ell((66,372,86,392),GOLD); d.ell((334,372,354,392),GOLD)
    d.ell((82,185,338,495),SKIN); d.rr((100,330,320,490),70,SKIN)
    d.blend(lambda dd:(dd.ellipse([v*S for v in (92,360,170,415)],fill=(225,100,80,70)),dd.ellipse([v*S for v in (250,360,328,415)],fill=(225,100,80,70)),dd.ellipse([v*S for v in (95,205,325,270)],fill=(120,70,40,45))))
    d.ell((188,335,234,392),SKIN_D); d.ell((196,372,206,384),(120,70,45,255)); d.ell((216,372,226,384),(120,70,45,255))
    # safa
    d.ell((40,30,380,245),SAFA)
    lay=Image.new("RGBA",d.im.size,(0,0,0,0)); ld=ImageDraw.Draw(lay)
    for k,c in enumerate((SAFA_D,SAFA_L,SAFA_D,SAFA_L,SAFA_D)):
        y=60+k*38; ld.line([(30*S,(y+60)*S),(210*S,(y-30)*S),(390*S,(y+50)*S)],fill=c,width=9*S)
    mask=Image.new("L",d.im.size,0); ImageDraw.Draw(mask).ellipse([40*S,30*S,380*S,245*S],fill=255)
    lay.putalpha(ImageChops.multiply(lay.getchannel("A"),mask)); d.im=Image.alpha_composite(d.im,lay); d.d=ImageDraw.Draw(d.im)
    d.poly([(70,215),(210,190),(350,215),(352,240),(210,218),(68,240)],GOLD)
    for x in (110,160,260,310):
        y=218-15*(1-((x-210)/140)**2); d.ell((x-5,y-5,x+5,y+5),RED)
    d.ell((190,180,230,222),GOLD); d.ell((199,189,221,213),RED)
    return d.out()
def make_mous():
    d=D(420,520)
    taper(d,[(210,404),(160,422),(108,416),(76,386),(84,352)],24,9,BLACK)
    taper(d,[(210,404),(260,422),(312,416),(344,386),(336,352)],24,9,BLACK)
    d.ell((165,392,255,432),BLACK); d.ell((80,346,90,358),(130,125,125,255)); d.ell((330,346,340,358),(130,125,125,255))
    return d.out()
def make_eyes(state):
    d=D(260,80); DK=(50,30,25,255)
    for cx in (65,195):
        if state in ("open","wide"):
            a,b=(34,26) if state=="open" else (38,33); r=13 if state=="open" else 10
            d.ell((cx-a,40-b,cx+a,40+b),(250,250,250,255),outline=DK,width=3)
            d.ell((cx-r,40-r+2,cx+r,40+r+2),(60,35,20,255)); d.ell((cx-4,40-r+3,cx+4,40-r+11),WHITE)
            d.arc((cx-a-2,40-b-6,cx+a+2,40+b-4),200,340,DK,5)
        elif state=="blink": d.arc((cx-30,22,cx+30,58),20,160,DK,6)
        else: d.arc((cx-30,26,cx+30,64),200,340,DK,7)
    return d.out()
def make_brow():
    d=D(140,60); taper(d,[(14,38),(46,24),(90,20),(126,30)],8,13,BLACK); return d.out()
def make_mouth(k):
    d=D(110,70); DK=(85,25,30,255)
    if k==0: d.arc((25,0,85,38),20,160,DK,6)
    elif k==1: d.ell((38,6,72,26),DK)
    elif k==2: d.ell((32,4,78,38),DK); d.ell((42,24,68,38),(210,90,100,255))
    else: d.ell((26,2,84,54),DK); d.rr((38,4,72,14),4,WHITE); d.ell((38,34,72,54),(210,90,100,255))
    return d.out()
def make_body():
    d=D(780,420)
    d.rr((335,0,445,130),30,SKIN_D); d.rr((70,90,710,560),130,NAVY)
    d.poly([(320,90),(460,90),(390,200)],(240,240,240,255))
    d.poly([(296,85),(345,85),(390,205),(328,150)],NAVY_D); d.poly([(484,85),(435,85),(390,205),(452,150)],NAVY_D)
    d.line([(390,205),(390,430)],NAVY_D,6)
    d.rr((170,250,340,320),10,(245,245,245,255)); d.text((255,285),"GURUJI",fl(34*S),RED)
    d.rr((450,240,600,340),12,NAVY_D); d.rr((470,205,484,260),4,(230,230,230,255)); d.rr((500,215,514,262),4,RED)
    d.rr((70,375,710,398),0,RED)
    return d.out()
def make_arm(kind):
    d=D(940,940); cx=cy=470; SP=(176,186,198,255)
    taper(d,[(cx,cy),(cx,cy+60),(cx,cy+130),(cx,cy+185)],60,48,NAVY)
    d.rr((cx-50,cy+168,cx+50,cy+198),10,NAVY_D)
    taper(d,[(cx,cy+195),(cx,cy+240),(cx,cy+270)],36,32,SKIN)
    if kind=="spanner":
        d.rr((cx-16,cy+250,cx+16,cy+415),14,SP); d.ell((cx-44,cy+385,cx+44,cy+458),SP); d.ell((cx-17,cy+420,cx+17,cy+470),(0,0,0,0))
        d.rr((cx-6,cy+260,cx+2,cy+400),3,(225,232,240,255))
        d.ell((cx-38,cy+265,cx+38,cy+335),SKIN)
        for dy in (285,303,321): d.line([(cx-30,cy+dy),(cx+30,cy+dy)],SKIN_D,3)
    elif kind=="open":
        d.ell((cx-40,cy+262,cx+40,cy+335),SKIN)
        for dx in (-27,-9,9,27): taper(d,[(cx+dx,cy+325),(cx+dx,cy+355),(cx+dx,cy+376)],9,8,SKIN)
        taper(d,[(cx+34,cy+290),(cx+60,cy+315),(cx+72,cy+340)],10,8,SKIN)
    else:
        d.ell((cx-36,cy+264,cx+36,cy+338),SKIN)
        for dy in (285,303,321): d.line([(cx-30,cy+dy),(cx+10,cy+dy)],SKIN_D,3)
        taper(d,[(cx-10,cy+290),(cx-10,cy+340),(cx-10,cy+384)],15,12,SKIN)
    return d.out()
HEAD=make_head(); MOUS=make_mous(); BODY=make_body()
EYES={k:make_eyes(k) for k in ("open","wide","blink","happy")}
BROW_L=make_brow(); BROW_R=BROW_L.transpose(Image.FLIP_LEFT_RIGHT)
MOUTH=[make_mouth(k) for k in range(4)]
ARMS={k:make_arm(k) for k in ("spanner","open","thumb")}
print("character sprites ok",flush=True)
# ================= CAR =================
CW_,CH_=900,420; CARC=(238,242,247,255); WC=[(210,300),(690,300)]
def make_car_body():
    d=D(CW_,CH_)
    d.rr((60,200,840,305),45,CARC); d.rr((60,268,840,305),20,(196,204,214,255))
    d.poly([(240,205),(330,115),(580,115),(670,205)],CARC)
    d.poly([(262,200),(338,132),(440,132),(440,200)],(150,205,235,255)); d.poly([(456,132),(572,132),(646,200),(456,200)],(150,205,235,255))
    d.poly([(290,198),(340,150),(362,150),(318,198)],(205,235,250,255))
    d.line([(448,205),(448,292)],(186,194,204,255),3); d.line([(610,208),(610,292)],(186,194,204,255),3)
    d.rr((470,226,512,236),5,(170,178,188,255)); d.ell((655,198,692,222),CARC,outline=(190,198,208,255),width=2)
    d.rr((50,278,850,312),14,(62,66,76,255))
    d.rr((676,200,832,220),4,(36,36,44,255))
    d.ell((812,222,846,256),(255,238,160,255)); d.ell((820,230,838,248),(255,255,230,255)); d.rr((56,214,74,248),6,(230,30,40,255))
    for cx,cy in WC: d.ell((cx-68,cy-68,cx+68,cy+68),(26,26,32,255))
    d.clear((0,312,CW_,CH_))
    return d.out()
def make_car_hood():
    d=D(CW_,CH_); d.poly([(668,194),(838,210),(838,234),(668,228)],CARC); d.line([(672,206),(832,220)],(205,212,222,255),3); return d.out()
def make_wheel():
    d=D(120,120); d.ell((4,4,116,116),(26,26,32,255)); d.ell((24,24,96,96),(192,200,210,255)); d.ell((30,30,90,90),(138,146,158,255))
    for k in range(5):
        a=math.radians(k*72); d.line([(60,60),(60+29*math.cos(a),60+29*math.sin(a))],(88,94,104,255),6)
    d.ell((51,51,69,69),(50,54,62,255))
    for k in range(6):
        a=math.radians(k*60+10); d.line([(60+50*math.cos(a),60+50*math.sin(a)),(60+55*math.cos(a),60+55*math.sin(a))],(120,124,132,255),5)
    return d.out()
CAR_BODY=make_car_body(); CAR_HOOD=make_car_hood(); WHEEL=make_wheel(); CAR_ALPHA=CAR_BODY.getchannel("A")
def draw_car(sc,cx,gy,wheel_deg,hood_deg,tilt,shine):
    lay=Image.new("RGBA",(CW_,CH_),(0,0,0,0)); lay.alpha_composite(CAR_BODY)
    if shine is not None:
        band=Image.new("L",(CW_,CH_),0); bd=ImageDraw.Draw(band); x=lerp(-200,1000,shine)
        bd.polygon([(x,100),(x+70,100),(x-60,330),(x-130,330)],fill=150)
        m=ImageChops.multiply(band,CAR_ALPHA); w=Image.new("RGBA",(CW_,CH_),(255,255,255,0)); w.putalpha(m); lay.alpha_composite(w)
    hd=CAR_HOOD.rotate(hood_deg,resample=Image.BICUBIC,center=(668,212)) if abs(hood_deg)>0.2 else CAR_HOOD
    lay.alpha_composite(hd)
    wr=WHEEL.rotate(wheel_deg,resample=Image.BICUBIC)
    for wx,wy in WC: lay.alpha_composite(wr,(wx-60,wy-60))
    if abs(tilt)>0.05: lay=lay.rotate(tilt,resample=Image.BICUBIC,center=(450,330))
    blit(sc,lay,cx-450,gy-356)

# ================= WORKSHOP =================
def make_building():
    d=D(940,650); SAND=(232,200,150,255)
    d.rr((20,150,920,650),8,SAND); d.rr((0,128,940,176),6,(188,118,70,255))
    for x in range(10,930,60): d.rr((x,112,x+36,132),4,(188,118,70,255))
    d.rr((20,240,120,650),6,(214,176,126,255)); d.rr((820,240,920,650),6,(214,176,126,255))
    for x in (45,845): d.rr((x,300,x+50,400),25,(120,70,60,255)); d.rr((x+8,312,x+42,396),17,(255,200,110,255))
    d.rr((140,270,800,650),10,(34,28,36,255)); d.rr((150,340,790,650),6,(78,58,62,255))
    d.rr((140,270,800,338),8,(120,112,108,255))
    for y in range(280,338,13): d.line([(142,y),(798,y)],(90,84,82,255),3)
    d.rr((170,560,262,650),6,RED); d.rr((178,545,254,562),4,(150,0,14,255))
    for i,x in enumerate((690,716,742,768)): d.rr((x,590,x+18,650),4,[(240,170,30,255),(30,120,200,255),(240,170,30,255),(60,170,90,255)][i])
    d.line([(660,586),(790,586)],(150,150,160,255),4)
    d.rr((60,20,880,190),16,RED,outline=WHITE,width=7); d.rr((74,34,866,176),10,None,outline=(255,150,150,255),width=2)
    d.text((470,84),"GURUJI MOTORS",fl(80*S),WHITE); d.text((470,150),"BOSCH AUTHORISED CAR SERVICE",fl(33*S),WHITE)
    d.text((470,218),"नीमकाथाना  •  सीकर  •  राजस्थान",fd(36*S),(110,30,40,255))
    return d.out()
def make_signglow():
    d=D(940,650); d.rr((60,20,880,190),16,(255,255,255,255)); im=d.out(); im.putalpha(im.getchannel("A").point(lambda v:int(v*0.55))); return im
BLD=make_building(); SIGNGLOW=make_signglow()

# ================= SCENERY =================
def build_sky():
    ys=np.linspace(0,1,SCH); arr=np.zeros((SCH,3))
    stops=[(0,(38,20,78)),(0.38,(150,42,92)),(0.72,(250,110,46)),(0.92,(255,188,92)),(1,(255,200,110))]
    for (p0,c0),(p1,c1) in zip(stops[:-1],stops[1:]):
        m=(ys>=p0)&(ys<=p1); x=((ys[m]-p0)/(p1-p0))[:,None]; arr[m]=np.array(c0)*(1-x)+np.array(c1)*x
    arr=np.repeat(arr[:,None,:],W,axis=1)
    im=Image.fromarray(arr.astype(np.uint8)).convert("RGBA"); d=ImageDraw.Draw(im); rg=random.Random(3)
    for _ in range(40):
        x=rg.randrange(W); y=rg.randrange(0,300); r=rg.choice((1,1,2)); d.ellipse((x-r,y-r,x+r,y+r),fill=(255,255,255,255))
    glow=Image.new("RGBA",(W,SCH),(0,0,0,0)); ImageDraw.Draw(glow).ellipse((450,310,1110,970),fill=(255,170,60,70)); glow=glow.filter(ImageFilter.GaussianBlur(60))
    im=Image.alpha_composite(im,glow); ImageDraw.Draw(im).ellipse((630,490,930,790),fill=(255,226,140,255)); return im
def build_dunes():
    P=1440; d=D(P,300)
    def curve(base,amps):
        pts=[(0,300)]
        for x in range(0,P+1,12): pts.append((x,base+sum(a*math.sin(2*math.pi*k*x/P+ph) for k,a,ph in amps)))
        pts.append((P,300)); return pts
    d.poly(curve(120,[(2,35,0.5),(5,14,1.7),(7,6,0.2)]),(176,78,70,255)); d.poly(curve(170,[(3,30,1.9),(6,12,0.4)]),(128,52,58,255)); return d.out()
def build_haveli():
    P=1440; d=D(P,400); HV=(66,26,56,255); rg=random.Random(5)
    for x,w,h in [(30,250,230),(330,190,280),(560,300,200),(900,210,270),(1150,240,240)]:
        top=400-h; d.rr((x,top,x+w,400),6,HV); d.rr((x-8,top-12,x+w+8,top+6),4,(84,34,66,255)); cx=x+w//2
        d.rr((cx-34,top-60,cx-26,top-12),2,HV); d.rr((cx+26,top-60,cx+34,top-12),2,HV); d.rr((cx-40,top-70,cx+40,top-58),3,HV)
        d.ell((cx-38,top-110,cx+38,top-52),HV); d.rr((cx-3,top-128,cx+3,top-100),2,HV)
        cols=max(2,w//70); rows=max(2,(h-120)//80)
        for r_ in range(rows):
            for c_ in range(cols):
                wx=x+(w/cols)*(c_+0.5); wy=top+40+r_*80
                d.rr((wx-14,wy,wx+14,wy+46),14,(255,176,70,255) if rg.random()<0.45 else (40,14,36,255))
        d.rr((cx-22,310,cx+22,400),22,(255,150,60,255))
    return d.out()
SKY=build_sky(); DUNE=build_dunes(); HAV=build_haveli()
def build_panel():
    ys=np.linspace(0,1,H-SCH)[:,None]; xs=np.linspace(-1,1,W)[None,:]
    a=np.zeros((H-SCH,W,3)); top=np.array([58,16,34]); bot=np.array([14,8,16])
    for c in range(3): a[:,:,c]=(top[c]*(1-ys)+bot[c]*ys)*(1-0.3*xs**2)
    im=Image.fromarray(a.clip(0,255).astype(np.uint8)).convert("RGBA"); d=ImageDraw.Draw(im)
    d.rectangle((0,0,W,8),fill=(226,0,21,255)); return im
PANEL=build_panel()
def gear_sprite(r,teeth,alpha):
    sz=int(r*2.6); im=Image.new("RGBA",(sz,sz),(0,0,0,0)); d=ImageDraw.Draw(im); n=teeth*4; pts=[]
    for i in range(n):
        a=i*2*math.pi/n; rr=r*1.12 if i%4 in (0,1) else r; pts.append((sz/2+rr*math.cos(a),sz/2+rr*math.sin(a)))
    d.polygon(pts,fill=(255,255,255,alpha)); k=r*0.55; d.ellipse((sz/2-k,sz/2-k,sz/2+k,sz/2+k),fill=(0,0,0,0)); return im
GEAR1=gear_sprite(300,16,16); GEAR2=gear_sprite(380,20,12)

# ================= FX SPRITES =================
def puff_sprite(R=80):
    y,x=np.mgrid[-R:R,-R:R]; r=np.sqrt(x*x+y*y)/R; a=np.clip(1-r,0,1)**1.4*255
    im=np.zeros((2*R,2*R,4),np.uint8); im[...,0]=92; im[...,1]=92; im[...,2]=102; im[...,3]=a.astype(np.uint8); return Image.fromarray(im)
PUFF=puff_sprite()
def star_sprite(sz=64,col=(255,255,255)):
    d=ImageDraw.Draw(Image.new("RGBA",(1,1))); im=Image.new("RGBA",(sz*4,sz*4),(0,0,0,0)); d=ImageDraw.Draw(im); c=sz*2; pts=[]
    for i in range(8):
        a=i*math.pi/4-math.pi/2; r=sz*1.9 if i%2==0 else sz*0.4; pts.append((c+r*math.cos(a),c+r*math.sin(a)))
    d.polygon(pts,fill=col+(255,)); return im.resize((sz*2,sz*2),Image.LANCZOS)
STAR=star_sprite(); STAR_Y=star_sprite(64,(255,230,120))
def sticker(text,size,fill,stroke=(30,10,10),sw=9):
    f=fd(size*2); tmp=Image.new("RGBA",(10,10)); bb=ImageDraw.Draw(tmp).textbbox((0,0),text,font=f,stroke_width=sw*2)
    w=bb[2]-bb[0]+40; h=bb[3]-bb[1]+40; im=Image.new("RGBA",(w,h),(0,0,0,0)); ImageDraw.Draw(im).text((20-bb[0],20-bb[1]),text,font=f,fill=fill,stroke_width=sw*2,stroke_fill=stroke)
    return im.resize((w//2,h//2),Image.LANCZOS)
def lamp_sprite():
    d=D(170,130); d.rr((0,0,170,130),22,(255,190,0,255),outline=(40,30,10,255),width=5)
    k=(40,30,10,255); d.rr((45,45,115,92),8,k); d.rr((58,32,100,48),4,k); d.rr((30,58,45,82),3,k); d.rr((116,52,138,60),3,k); d.rr((116,52,126,92),3,k)
    d.rr((70,60,92,76),4,(255,190,0,255)); return d.out()
def qbubble():
    d=D(150,170); d.ell((5,5,145,135),WHITE,outline=(40,20,20,255),width=5); d.poly([(45,120),(35,165),(85,128)],WHITE)
    d.text((75,70),"?",fl(90*S),RED); return d.out()
LAMP=lamp_sprite(); QB=qbubble()

# ================= SERVICE ICONS =================
def make_icon(kind,label):
    d=D(170,190); d.rr((0,0,170,190),22,(255,255,255,245)); d.rr((0,0,170,40),22,RED); d.rr((0,22,170,40),0,RED)
    DK=(48,54,70,255); cx,cy=85,98
    if kind=="engine":
        d.rr((38,84,132,128),8,DK); d.rr((50,66,122,86),6,(90,98,116,255))
        for x in (58,80,102): d.rr((x,52,x+12,68),3,(150,158,172,255))
        d.rr((26,94,40,118),4,(90,98,116,255)); d.rr((130,96,146,112),4,(90,98,116,255)); d.rr((38,100,132,106),0,RED)
    elif kind=="brake":
        d.ell((44,58,126,140),DK); d.ell((66,80,104,118),(205,210,220,255)); d.ell((80,94,90,104),DK)
        for k in range(8):
            a=math.radians(k*45+20); d.line([(85+22*math.cos(a),99+22*math.sin(a)),(85+34*math.cos(a),99+34*math.sin(a))],(150,156,168,255),4)
        d.poly([(108,66),(136,86),(136,114),(108,134),(100,120),(120,102),(100,80)],RED)
    elif kind=="battery":
        d.rr((40,72,130,134),8,DK); d.rr((54,58,70,74),3,RED); d.rr((100,58,116,74),3,(90,98,116,255))
        d.poly([(90,80),(70,108),(85,108),(78,130),(104,98),(90,98),(98,80)],(255,205,40,255))
    elif kind=="ac":
        for k in range(6):
            a=math.radians(k*60); ex,ey=cx+40*math.cos(a),cy+40*math.sin(a); d.line([(cx,cy),(ex,ey)],(40,150,220,255),6)
            for s in (-1,1):
                b=a+s*0.7; d.line([(cx+26*math.cos(a),cy+26*math.sin(a)),(cx+26*math.cos(a)+14*math.cos(b),cy+26*math.sin(a)+14*math.sin(b))],(40,150,220,255),5)
        d.ell((cx-7,cy-7,cx+7,cy+7),(40,150,220,255))
    else:
        d.poly([(85,58),(58,104),(112,104)],(240,170,30,255)); d.ell((55,86,115,142),(240,170,30,255)); d.ell((68,100,78,118),(255,235,170,255))
    f=fd(S*34)
    while f.getlength(label)>150*S: f=fd(f.size-2)
    d.text((85,166),label,f,NAVY); return d.out()
ICONS=[make_icon("engine","इंजन"),make_icon("brake","ब्रेक"),make_icon("battery","बैटरी"),make_icon("ac","एसी"),make_icon("oil","तेल-फ़िल्टर")]
STK={k:sticker(*v) for k,v in {"khat":("खट-खट!",110,(255,214,64)),"dhuan":("धुआँ!",120,(255,255,255)),"chee":("चीं...!",110,(255,120,90)),"wah":("वाह!",130,(255,214,64)),"makkhan":("मक्खन!",120,(255,240,150)),"ribbon":("आज ही आओ सा!",86,(255,255,255),(150,0,14),6)}.items()}
print("scene sprites ok",flush=True)
# ================= TIMING =================
BND=[0,ST[1]-0.25,ST[2]-0.3,ST[3]-0.25,ST[4]-0.25,ST[5]-0.25]
tC0=ST[2]-0.3; tE0=ST[4]-0.25; tE1=ST[5]-0.35
def speedE(t):
    if t<tE0: return 0.0
    if t<tE1: return 1100*eo3((t-tE0)/0.7)
    return 1100*(1-cl((t-tE1)/1.4))**2
CAM=np.zeros(NF+3); acc=0.0
for f in range(NF+3):
    t=f/FPS
    if t<tC0: CAM[f]=0
    elif t<tC0+1.6: CAM[f]=1600*eo3((t-tC0)/1.6)
    else:
        if t>=tE0: acc+=speedE(t)/FPS
        CAM[f]=1600+acc
CAM_END=CAM[-1]
# lip-sync
sr=24000; track=np.zeros(int(END*sr)+sr)
for i in range(6):
    w,_=sf.read(TD+f"L{i+1}.wav"); a=int(ST[i]*sr); track[a:a+len(w)]+=w
VEN=np.zeros(NF+3)
for f in range(NF+3):
    c=int(f/FPS*sr); seg=track[max(0,c-400):c+400]; VEN[f]=np.sqrt(np.mean(seg**2)) if len(seg) else 0
VEN=VEN/(np.percentile(VEN[VEN>0.002],95)+1e-9); MST=np.zeros(NF+3,int); prev=0
for f in range(NF+3):
    v=VEN[f]; s=0 if v<0.10 else 1 if v<0.38 else 2 if v<0.75 else 3
    if s<prev: s=max(s,prev-1)
    MST[f]=s; prev=s
# captions
CAP={1:["राम राम सा!","नीमकाथाना वालो,","गाड़ी में कोई दिक्कत","है के?"],2:["आवाज़ करे,","धुआँ छोड़े,","ब्रेक ढीली पड़े...","तो देर मत","करो!"],
3:["आ जाओ गुरुजी मोटर्स!","बॉश","ऑथराइज़्ड","कार सर्विस,","म्हारे यहाँ।"],4:["इंजन की जाँच,","ब्रेक, बैटरी,","एसी,","तेल-फ़िल्टर,","सब एक ही जगह।"],
5:["फेर देखो,","गाड़ी चलेगी","एकदम","मक्खन!"],6:["गुरुजी मोटर्स,","नीमकाथाना। गाड़ी की सेहत,","बॉश के भरोसे!","आज ही आओ सा!"]}
CAPW={}
for i in range(1,7):
    assert len(CAP[i])==len(SEG[i]),(i,len(CAP[i]),len(SEG[i]))
    words=[]
    for chunk,(a,b) in zip(CAP[i],SEG[i]):
        ws=chunk.split(); tot=sum(len(x) for x in ws); cum=0
        for x in ws:
            t0=ST[i-1]+a+(b-a)*cum/tot; cum+=len(x); words.append((x,t0,ST[i-1]+a+(b-a)*cum/tot))
    for size in range(60,38,-2):
        f=fd(size); rows=[[]]; cur=0
        for k,(x,_,_) in enumerate(words):
            wl=f.getlength(x+" ")
            if cur+wl>880 and rows[-1]: rows.append([]); cur=0
            rows[-1].append(k); cur+=wl
        if len(rows)<=2: break
    CAPW[i]=(words,rows,size)
def draw_caption(cv,t):
    for i in range(1,7):
        if ST[i-1]-0.15<=t<=EN[i-1]+0.5:
            words,rows,size=CAPW[i]; f=fd(size); lay=Image.new("RGBA",(960,140),(0,0,0,0)); d=ImageDraw.Draw(lay)
            d.rounded_rectangle((0,0,959,139),radius=34,fill=(12,6,16,175))
            n=len(rows); lh=size*1.25; y0=70-(n-1)*lh/2
            for r,row in enumerate(rows):
                tw=sum(f.getlength(words[k][0]+" ") for k in row)-f.getlength(" "); x=480-tw/2
                for k in row:
                    x_,t0,t1=words[k]; cur=t0<=t<t1+0.05
                    d.text((x,y0+r*lh),x_,font=f,fill=(255,214,64,255) if cur else (255,255,255,255),anchor="lm"); x+=f.getlength(x_+" ")
            a=min(1,(t-(ST[i-1]-0.15))/0.15,(EN[i-1]+0.5-t)/0.25); blit(cv,lay,60,950,cl(a)); return
# ================= SCENE =================
STICKERS=[("khat",ST[1]+0.5,260,520,-8),("dhuan",ST[1]+1.9,820,470,7),("chee",ST[1]+3.2,540,560,3),("wah",ST[4]+0.7,280,520,-7),("makkhan",ST[4]+1.9,790,560,6)]
ITEM_T=[0.04,1.26,1.75,2.36,2.97]
RG=random.Random(9); SPARK=[(RG.uniform(140,940),RG.uniform(620,900),RG.random()) for _ in range(14)]
def draw_scene(f,t,sidx):
    sc=SKY.copy(); c=CAM[f]
    off=(c*0.12)%1440; blit(sc,DUNE,-off,640); blit(sc,DUNE,1440-off,640)
    off=(c*0.3)%1440; blit(sc,HAV,-off,480); blit(sc,HAV,1440-off,480)
    d=ImageDraw.Draw(sc); d.rectangle((0,860,W,880),fill=(214,172,122,255)); d.rectangle((0,880,W,SCH),fill=(44,42,54,255))
    for k in range(-1,8): x=k*180-(c%180); d.rectangle((x,926,x+90,932),fill=(232,232,232,255))
    for wx in (1670,70+CAM_END):
        sx=wx-c
        if -940<sx<W:
            blit(sc,BLD,sx,230)
            g=0.0
            if sidx==2 and t>ST[2]+2.0: g=max(0,1-(t-(ST[2]+2.0))/0.9)
            if sidx==5: g=0.18+0.12*math.sin(t*5)
            if g>0: blit(sc,SIGNGLOW,sx,230,g)
            for i in range(24):
                col=(255,236,150,255) if (i+int(t*4))%2==0 else (170,125,60,255); bx=sx+70+i*34.5; d.ellipse((bx-5,244,bx+5,254),fill=col)
    d.ellipse((140,912,940,940),fill=(30,28,38,255))
    carx,gy=540.0,915.0; dx=dy=0.0; tilt=0.0; hood=0.0; shine=None
    if sidx==0: dy=0.8*math.sin(t*40)
    if sidx==1:
        rg=random.Random(f); dx=rg.uniform(-5,5); dy=rg.uniform(-3,3); tilt=rg.uniform(-1.2,1.2); hood=6+3*math.sin(t*30)
    tilt+=-3*math.sin(math.pi*cl((t-(ST[2]+0.85))/0.6))+1.4*math.sin(math.pi*cl((t-tE0)/0.7))-2.5*math.sin(math.pi*cl((t-tE1)/1.4))
    if sidx==3: hood=55*eob((t-BND[3])/0.6)*(1-cl((t-(ST[4]-0.7))/0.4))
    if sidx==4: dy=3*math.sin(2*math.pi*4*t)
    if sidx==4 and t>ST[4]+0.3: shine=((t-ST[4])%1.8)/1.8
    if sidx==5: shine=((t-ST[5])%2.2)/2.2
    draw_car(sc,carx+dx,gy+dy,(-c/56*57.2958)%360,hood,tilt,shine)
    if sidx==1:
        for i in range(int((BND[2]-BND[1])/0.1)+10):
            tb=BND[1]+i*0.1; age=t-tb
            if 0<=age<1.8:
                rg=random.Random(i); px=850+45*age+14*math.sin(3*age+i)+rg.uniform(-10,10); py=762-150*age; s_=0.5+1.0*age
                blit(sc,scaled(PUFF,s_),px-PUFF.width*s_/2,py-PUFF.height*s_/2,0.75*(1-age/1.8))
        for k in range(6):
            age=t-(BND[1]+0.5+k*0.8)
            if 0<=age<0.2:
                rg=random.Random(k*7)
                for _ in range(8):
                    a=rg.uniform(-2.8,-0.3); L=70*age/0.2; d.line([(845,770),(845+L*math.cos(a),770+L*math.sin(a))],fill=(255,222,90,255),width=4)
        if int(t*4)%2==0: blit(sc,LAMP,455,455)
    if sidx==0:
        a=eo3((t-0.3)/0.5)*(1-cl((t-(BND[1]-0.4))/0.3))
        if a>0:
            lay=Image.new("RGBA",(W,260),(0,0,0,0)); ld=ImageDraw.Draw(lay)
            ld.text((543,83),"GURUJI MOTORS",font=fl(92),fill=(150,0,14,int(255*a)),anchor="mm"); ld.text((540,80),"GURUJI MOTORS",font=fl(92),fill=(255,255,255,int(255*a)),anchor="mm")
            ld.text((540,160),"BOSCH AUTHORISED CAR SERVICE",font=fl(36),fill=(255,214,120,int(255*a)),anchor="mm"); blit(sc,lay,0,90)
        age=t-(ST[0]+3.1)
        if 0<=age and sidx==0: s_=eob(age/0.4); blit(sc,scaled(QB,max(0.05,s_)),780-QB.width*s_/2,540-QB.height*s_/2)
    if sidx==3:
        fade=1-cl((t-(BND[4]-0.3))/0.3)
        for i,tr in enumerate(ITEM_T):
            age=t-(ST[3]+tr)
            if age>=0:
                s_=max(0.05,eob(age/0.4)); x=540+(i-2)*195; y=565; sp=scaled(ICONS[i],s_); blit(sc,sp,x-sp.width/2,y-sp.height/2,fade)
                if age>0.5 and fade>0.5:
                    d.ellipse((x+52,y-96,x+86,y-62),fill=(40,170,90,255)); d.line([(x+60,y-79),(x+66,y-72),(x+78,y-88)],fill=(255,255,255,255),width=5)
    for key,t0,x,y,rot in STICKERS:
        age=t-t0
        if 0<=age<1.6 and ((key in("khat","dhuan","chee") and sidx==1) or (key in("wah","makkhan") and sidx==4)):
            s_=max(0.05,eob(age/0.35))*(1 if age<1.2 else 1-(age-1.2)/0.4); sp=scaled(STK[key],s_).rotate(rot,resample=Image.BICUBIC,expand=True); blit(sc,sp,x-sp.width/2,y-sp.height/2)
    if sidx in(4,5) and t>ST[4]+0.5:
        for x,y,ph in SPARK:
            s_=0.2+0.35*abs(math.sin(2*math.pi*(t*1.1+ph))); blit(sc,scaled(STAR_Y,s_),x-STAR_Y.width*s_/2,y-STAR_Y.height*s_/2,0.9)
    if sidx==5 and t>ST[5]+3.4:
        s_=eob((t-ST[5]-3.4)/0.4)*(1+0.05*math.sin(t*8)); sp=scaled(STK["ribbon"],max(0.05,s_)); blit(sc,sp,540-sp.width/2,150-sp.height/2)
    return sc
# ================= GURUJI =================
def pose(t,sidx):
    s=ST; sn=math.sin; pi=math.pi
    if sidx==0: return ("spanner",158+16*sn(2*pi*2.4*t),"open",18,"open",0,-5)
    if sidx==1: return ("open",150+12*sn(2*pi*3*t),"open",150+12*sn(2*pi*3*t+1),"wide",16,-8)
    if sidx==2:
        late=t>s[2]+1.5
        return ("spanner",150,"thumb" if late else "open",(148+5*sn(2*pi*2*t)) if late else 20,"open",0,-3)
    if sidx==3: return ("spanner",145+6*sn(2*pi*1.5*t),"open",145+6*sn(2*pi*1.5*t+1),"open",0,-4)
    if sidx==4: return ("spanner",162+4*sn(2*pi*2*t),"thumb",148+6*sn(2*pi*2.2*t),"happy" if s[4]+0.5<t<s[4]+2.8 else "open",0,-9)
    return ("spanner",155+18*sn(2*pi*2.6*t),"open",155+18*sn(2*pi*2.6*t+pi),"happy" if t>EN[5]-0.6 else "open",0,-8)
ST_={"R":None,"L":None}
def draw_guruji(cv,f,t,sidx):
    kR,aR,kL,aL,eye,bang,bdy=pose(t,sidx)
    ST_["R"]=aR if ST_["R"] is None else ST_["R"]+(aR-ST_["R"])*0.25
    ST_["L"]=aL if ST_["L"] is None else ST_["L"]+(aL-ST_["L"])*0.25
    oy=(1-eob((t-0.1)/0.8))*700+6*math.sin(2*math.pi*t/1.7)
    blit(cv,BODY,150,1510+oy)
    for k,ang,px in ((kR,-ST_["R"],270),(kL,ST_["L"],810)):
        r=ARMS[k].rotate(ang,resample=Image.BICUBIC,center=(470,470)); blit(cv,r,px-470,1700+oy-470)
    hd=HEAD.copy()
    es="blink" if (t%3.3)<0.12 and t>1 else eye
    hd.alpha_composite(EYES[es],(80,250))
    for spr,ang,x in ((BROW_L,bang,75),(BROW_R,-bang,205)):
        b=spr.rotate(ang,resample=Image.BICUBIC); hd.alpha_composite(b,(x,220+bdy))
    hd.alpha_composite(MOUTH[MST[f] if es!="happy" or MST[f]>0 else 0],(155,428)) if True else None
    hd.alpha_composite(MOUS)
    ra=1.8*math.sin(2*math.pi*t/2.3)+(2.5*math.sin(2*math.pi*t*3) if sidx==1 else 0)
    hd=hd.rotate(ra,resample=Image.BICUBIC,center=(210,430))
    blit(cv,hd,330,1100+oy+3*min(1.5,VEN[f]))
def render(f):
    t=f/FPS; sidx=max(i for i,b in enumerate(BND) if t>=b)
    cv=Image.new("RGBA",(W,H),(0,0,0,255)); cv.alpha_composite(draw_scene(f,t,sidx),(0,0)); cv.alpha_composite(PANEL,(0,SCH))
    blit(cv,GEAR1.rotate(t*8,resample=Image.BILINEAR),620,1000); blit(cv,GEAR2.rotate(-t*6,resample=Image.BILINEAR),-330,1350)
    draw_guruji(cv,f,t,sidx); draw_caption(cv,t)
    ImageDraw.Draw(cv).rectangle((0,0,int(W*t/END),8),fill=(226,0,21,255))
    return cv.convert("RGB")
if __name__=="__main__":
    if len(sys.argv)>1 and sys.argv[1]=="test":
        ts=[float(x) for x in sys.argv[2:]]; ims=[]
        for tt in ts:
            f=int(tt*FPS); ST_["R"]=ST_["L"]=None
            for k in range(max(0,f-6),f): render(k)
            ims.append(render(f).resize((360,640)))
        m=Image.new("RGB",(360*len(ims),640))
        for i,im in enumerate(ims): m.paste(im,(i*360,0))
        m.save("/home/claude/vid/test.png"); print("saved")
    else:
        out="/home/claude/vid/silent.mp4"
        ff=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-c:v","libx264","-pix_fmt","yuv420p","-crf","19","-preset","medium",out],stdin=subprocess.PIPE)
        for f in range(NF):
            ff.stdin.write(render(f).tobytes())
            if f%60==0: print(f,NF,flush=True)
        ff.stdin.close(); ff.wait(); print("DONE",flush=True)
