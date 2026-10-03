from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

W,H=960,210
BG=(2,11,16); BORDER=(0,185,217); CYAN=(0,229,255); WHITE=(245,250,255); MUTED=(110,150,160)
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf'
font=ImageFont.truetype(FONT,14); small=ImageFont.truetype(FONT,10); iconfont=ImageFont.truetype(FONT,17)
items=[
 ('C','C',(0,89,156)),('C++','C++',(8,118,185)),('Java','☕',(231,111,0)),('Python','🐍',(55,118,171)),('JavaScript','JS',(217,197,0)),
 ('HTML5','5',(227,79,38)),('CSS3','3',(21,114,182)),('Flask','⚗',(25,25,25)),('MongoDB','◆',(71,162,72)),('Git','⎇',(240,80,50)),('GitHub','●',(48,54,61)),
 ('NumPy','N',(77,171,207)),('Pandas','P',(86,61,124)),('scikit-learn','ML',(247,147,30))]
rows=[items[:5],items[5:11],items[11:]]
frames=[]
# Static SVG-like raster; logos are symbol marks alongside names for reliable GitHub rendering.
im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
d.rounded_rectangle((1,1,W-2,H-2),radius=9,outline=BORDER,width=2)
# heading accent
for ri,row in enumerate(rows):
    widths=[]
    for name,icon,color in row:
        widths.append(max(125, len(name)*11+42))
    gap=12; total=sum(widths)+gap*(len(row)-1); x=(W-total)/2; y=30+ri*52
    for (name,icon,color),ww in zip(row,widths):
        d.rounded_rectangle((x,y,x+ww,y+36),radius=7,fill=color,outline=CYAN if name in ('Java','Python','JavaScript','GitHub') else None,width=1)
        d.text((x+16,y+9),icon,font=iconfont,fill=WHITE)
        d.text((x+43,y+9),name,font=font,fill=WHITE)
        x+=ww+gap
d.text((W/2,184),'Languages  •  Web  •  Data  •  ML  •  Tools',font=small,fill=MUTED,anchor='ma')
im.save('tech-stack.png')
# Also provide a compact SVG fallback with the same symbol-logo treatment.
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="960" height="210" viewBox="0 0 960 210">',f'<rect x="1" y="1" width="958" height="208" rx="9" fill="#020b10" stroke="#00b9d9" stroke-width="2"/>']
for ri,row in enumerate(rows):
    widths=[max(125,len(name)*11+42) for name,_,_ in row]; gap=12; total=sum(widths)+gap*(len(row)-1); x=(W-total)/2; y=30+ri*52
    for (name,icon,color),ww in zip(row,widths):
        c='#%02x%02x%02x'%color
        svg.append(f'<rect x="{x:.1f}" y="{y}" width="{ww}" height="36" rx="7" fill="{c}"/>')
        svg.append(f'<text x="{x+16:.1f}" y="{y+24}" font-family="DejaVu Sans,Arial" font-size="16" font-weight="700" fill="#fff">{icon}</text>')
        svg.append(f'<text x="{x+43:.1f}" y="{y+23}" font-family="DejaVu Sans,Arial" font-size="14" font-weight="700" fill="#fff">{name}</text>')
        x+=ww+gap
svg.append('<text x="480" y="194" text-anchor="middle" font-family="monospace" font-size="10" fill="#6e96a0">Languages • Web • Data • ML • Tools</text></svg>')
Path('tech-stack.svg').write_text(''.join(svg),encoding='utf-8')
print('Wrote tech-stack.svg and tech-stack.png')
