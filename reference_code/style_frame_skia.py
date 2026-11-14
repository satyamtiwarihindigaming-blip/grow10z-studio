import skia, math, random, numpy as np
from PIL import Image, ImageDraw, ImageFont
W,H=1080,1920
def C(r,g,b,a=255): return skia.ColorSetARGB(a,r,g,b)
surf=skia.Surface(W,H); cv=surf.getCanvas(); rg=random.Random(11)
def P(**k): return skia.Paint(AntiAlias=True,**k)
def lin(p0,p1,cols,pos=None): return skia.GradientShader.MakeLinear([p0,p1],cols,pos)
def rad(c,r,cols,pos=None): return skia.GradientShader.MakeRadial(c,r,cols,pos)
def blur(s): return skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle,s)
def R(l,t,r,b): return skia.Rect.MakeLTRB(l,t,r,b)
# sky
cv.drawRect(R(0,0,W,H),P(Shader=lin((0,0),(0,1050),[C(5,8,26),C(18,28,68),C(70,92,135)],[0,0.55,1])))
for _ in range(260):
    x,y=rg.uniform(0,W),rg.uniform(0,900)**1; a=int(rg.uniform(90,255)*(1-y/1100)); r=rg.choice((1,1,1.4,2))
    cv.drawCircle(x,y,r,P(Color=C(255,250,230,max(40,a))))
# moon + glow
cv.drawCircle(760,470,260,P(Shader=rad((760,470),260,[C(200,215,255,90),C(200,215,255,0)]),MaskFilter=blur(30)))
cv.drawCircle(760,470,150,P(Shader=lin((660,380),(860,560),[C(250,246,226),C(214,214,200)])))
for (dx,dy,r,a) in [(-40,-30,28,40),(30,40,36,34),(-20,60,18,30),(60,-50,20,28)]: cv.drawCircle(760+dx,470+dy,r,P(Color=C(150,150,150,a)))
# hills
def hill(base,amp,fr,ph,col):
    p=skia.Path(); p.moveTo(0,H)
    for x in range(0,W+8,8): p.lineTo(x,base+amp*math.sin(x*fr+ph)+amp*0.5*math.sin(x*fr*2.3+ph*1.7))
    p.lineTo(W,H); p.close(); cv.drawPath(p,P(Color=col))
hill(930,40,0.006,0.5,C(18,30,62)); hill(980,28,0.009,2.0,C(11,18,42))
# mist
cv.drawRect(R(0,900,W,1180),P(Shader=lin((0,900),(0,1180),[C(170,190,230,0),C(170,190,230,60),C(170,190,230,0)],[0,0.5,1])))
# ground + road
cv.drawRect(R(0,1000,W,H),P(Shader=lin((0,1000),(0,H),[C(10,16,30),C(5,8,16)])))
road=skia.Path(); road.moveTo(525,1000); road.lineTo(555,1000); road.lineTo(1010,H); road.lineTo(70,H); road.close()
cv.drawPath(road,P(Shader=lin((0,1000),(0,H),[C(30,34,50),C(14,16,24)])))
for i in range(9):
    t0=(i/9)**1.8; t1=((i+0.5)/9)**1.8; y0=1000+t0*920; y1=1000+t1*920; w0=2+t0*14; w1=2+t1*14
    d=skia.Path(); d.moveTo(540-w0/2,y0); d.lineTo(540+w0/2,y0); d.lineTo(540+w1/2,y1); d.lineTo(540-w1/2,y1); d.close(); cv.drawPath(d,P(Color=C(200,190,150,150)))
# headlight cone (drawn before bus)
cone=skia.Path(); cone.moveTo(640,1432); cone.lineTo(1080,1330); cone.lineTo(1080,1640); cone.close()
cv.drawPath(cone,P(Shader=lin((640,1432),(1080,1432),[C(255,235,170,150),C(255,235,170,0)]),MaskFilter=blur(14)))
# bus
cv.drawRRect(skia.RRect.MakeRectXY(R(56,1252,656,1480),30,30),P(Color=C(0,0,0,110),MaskFilter=blur(14)))
cv.drawRRect(skia.RRect.MakeRectXY(R(60,1256,650,1474),26,26),P(Shader=lin((0,1256),(0,1474),[C(150,48,50),C(92,26,34)])))
cv.drawRect(R(62,1408,648,1426),P(Color=C(214,196,150)))
cv.drawRect(R(112,1244,540,1258),P(Color=C(40,24,28)))
for i in range(7):
    x=96+i*72; cv.drawRRect(skia.RRect.MakeRectXY(R(x-6,1284,x+62,1366),14,14),P(Color=C(255,205,110,110),MaskFilter=blur(10)))
    cv.drawRRect(skia.RRect.MakeRectXY(R(x,1290,x+56,1360),10,10),P(Shader=lin((0,1290),(0,1360),[C(255,226,150),C(240,170,80)])))
cv.drawRRect(skia.RRect.MakeRectXY(R(574,1290,636,1394),12,12),P(Shader=lin((0,1290),(0,1394),[C(210,232,255),C(120,150,190)])))
cv.drawRRect(skia.RRect.MakeRectXY(R(520,1262,632,1284),6,6),P(Color=C(255,176,60)))
cv.drawRect(R(560,1430,650,1460),P(Color=C(30,20,24)))
cv.drawCircle(646,1436,16,P(Color=C(255,246,200))); cv.drawCircle(646,1436,40,P(Shader=rad((646,1436),40,[C(255,240,180,160),C(255,240,180,0)])))
for cx in (190,500):
    cv.drawCircle(cx,1480,54,P(Color=C(10,10,14))); cv.drawCircle(cx,1480,26,P(Color=C(80,80,92))); cv.drawCircle(cx,1480,8,P(Color=C(30,30,36)))
# bus stop sign
cv.drawRect(R(796,1170,808,1520),P(Color=C(8,12,22))); cv.drawRRect(skia.RRect.MakeRectXY(R(764,1140,842,1196),6,6),P(Color=C(170,196,226,230)))
cv.drawRect(R(770,1160,836,1168),P(Color=C(10,20,40,180)))
# old woman (rim light + silhouette)
def woman(dx,col):
    p=skia.Path(); x=930+dx
    p.moveTo(x-8,1308); p.cubicTo(x-30,1330,x-62,1420,x-48,1520); p.lineTo(x+52,1520); p.cubicTo(x+60,1420,x+36,1330,x+14,1308); p.close(); return p,col
for dx,col in ((-5,C(255,196,120,150)),(0,C(5,7,16))):
    p,c_=woman(dx,col); cv.drawPath(p,P(Color=c_))
    cv.drawCircle(930+dx-1,1284,27,P(Color=c_))
cv.drawPath(skia.Path().moveTo(900,1300).lineTo(960,1300).lineTo(968,1318).lineTo(892,1318).close(),P(Color=C(5,7,16)))
# glowing tiffin
cv.drawCircle(905,1440,70,P(Shader=rad((905,1440),70,[C(255,196,90,170),C(255,196,90,0)])))
cv.drawRRect(skia.RRect.MakeRectXY(R(886,1420,926,1466),5,5),P(Shader=lin((0,1420),(0,1466),[C(255,222,130),C(230,150,50)])))
cv.drawRect(R(884,1436,928,1440),P(Color=C(120,70,20))); cv.drawRect(R(884,1450,928,1454),P(Color=C(120,70,20)))
cv.drawPath(skia.Path().moveTo(892,1420).quadTo(906,1396,920,1420),P(Color=C(255,222,130),Style=skia.Paint.kStroke_Style,StrokeWidth=4))
for _ in range(26):
    x=rg.gauss(900,150); y=rg.gauss(1380,120); cv.drawCircle(x,y,rg.choice((1.5,2,2.5)),P(Color=C(255,224,130,rg.randint(90,220)),MaskFilter=blur(1.2)))
# edge trees
for tx,sc in ((20,0.9),(1085,0.95),(-40,1.15)):
    cv.drawRect(R(tx-10*sc,1180,tx+10*sc,1700),P(Color=C(3,6,12)))
    for (dx,dy,r) in [(0,-0,150),(-90,60,110),(90,50,120),(10,-110,100)]: cv.drawCircle(tx+dx*sc,900+dy*sc,r*sc,P(Color=C(3,6,12)))
# vignette
cv.drawRect(R(0,0,W,H),P(Shader=rad((540,980),1250,[C(0,0,0,0),C(0,0,0,0),C(0,0,0,185)],[0,0.55,1])))
img=surf.makeImageSnapshot().convert(alphaType=skia.kUnpremul_AlphaType,colorType=skia.kRGBA_8888_ColorType)
im=Image.fromarray(img.toarray()).convert("RGB")
d=ImageDraw.Draw(im); FB="fonts/FreeSansBold.ttf"
def txt(s,cx,cy,sz,fill,stroke=(10,6,2),sw=8):
    f=ImageFont.truetype(FB,sz); d.text((cx,cy),s,font=f,fill=fill,anchor="mm",stroke_width=sw,stroke_fill=stroke)
txt("आख़िरी बस",540,250,190,(255,226,150),sw=10)
txt("भाग 1",540,400,70,(255,255,255),sw=6)
d.rounded_rectangle((190,1600,890,1740),radius=40,fill=(8,10,22,))
txt("आगे क्या होगा?",540,1670,90,(255,214,64),sw=6)
im.save("out/style_frame.png"); print("saved",im.size)
