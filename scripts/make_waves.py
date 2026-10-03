from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math

W,H=960,150
BG=(1,8,13); CYAN=(0,229,255); GREEN=(0,255,136); WHITE=(230,247,255); DIM=(20,90,105)
font_path='/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf'
font_big=ImageFont.truetype(font_path,25)
font_small=ImageFont.truetype(font_path,10)

frames=[]
for phase in range(32):
    im=Image.new('RGB',(W,H),BG)
    d=ImageDraw.Draw(im)
    # slogan above waves, bigger and bright
    slogan='Learn. Build. Break. Fix. Repeat.'
    box=d.textbbox((0,0),slogan,font=font_big)
    sx=(W-(box[2]-box[0]))/2
    d.text((sx,8),slogan,font=font_big,fill=CYAN)
    # moving cursor
    cursor_x=sx+(box[2]-box[0])+8
    d.rectangle((cursor_x,12,cursor_x+8,35),fill=GREEN)
    # animated multi-wave field
    for wave,(color,amp,base,speed,width) in enumerate([(GREEN,14,68,1.0,2),(CYAN,10,78,1.4,2),(GREEN,7,88,1.8,1),(CYAN,5,95,2.2,1)]):
        pts=[]
        for x in range(0,W+1,4):
            y=base + amp*math.sin(x/55 + phase*0.30*speed + wave*1.2) + 2*math.sin(x/130 - phase*0.15)
            pts.append((x,y))
        d.line(pts,fill=color,width=width)
    # tiny moving particles
    for i in range(26):
        x=((i*47 + phase*11) % (W+40))-20
        y=62 + 40*math.sin(i*1.7 + phase*0.15)
        r=1 if i%3 else 2
        d.ellipse((x-r,y-r,x+r,y+r),fill=GREEN if i%2 else CYAN)
    # subtle bottom baseline
    d.line((0,125,W,125),fill=DIM,width=1)
    frames.append(im)

out=Path('waves.gif')
frames[0].save(out,save_all=True,append_images=frames[1:],duration=90,loop=0,disposal=2,optimize=True)
print('Wrote',out)
