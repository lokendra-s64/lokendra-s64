from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math

W, H = 960, 180
BG = (2, 11, 16)
CYAN = (0, 229, 255)
GREEN = (0, 255, 136)
WHITE = (230, 247, 255)
DIM = (92, 125, 138)

FONT_PATHS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]
FONT_MONO = next(p for p in FONT_PATHS if Path(p).exists())
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

def font(size, bold=False):
    p = FONT_MONO if bold else FONT_REG
    return ImageFont.truetype(p, size)

def centered(draw, y, text, fnt, fill):
    box = draw.textbbox((0, 0), text, font=fnt)
    x = (W - (box[2]-box[0]))/2
    draw.text((x, y), text, font=fnt, fill=fill)

def frame(title, subtitle, cursor=True, phase=0):
    im = Image.new("RGB", (W,H), BG)
    d = ImageDraw.Draw(im)
    # cyan-only frame; no green border
    d.rounded_rectangle((1,1,W-2,H-2), radius=9, outline=CYAN, width=2)
    # subtle HUD corners, cyan only
    for pts in [((12,30),(12,12),(30,12)), ((W-30,12),(W-12,12),(W-12,30)), ((12,H-30),(12,H-12),(30,H-12)), ((W-30,H-12),(W-12,H-12),(W-12,H-30))]:
        d.line([pts[0],pts[1],pts[2]], fill=CYAN, width=2)
    d.text((18,18), "> lokendra-s64", font=font(12), fill=CYAN)
    d.text((140,18), "/ README.md", font=font(12), fill=WHITE)
    # pencil
    d.line((925,43,945,23), fill=DIM, width=3)
    d.line((927,47,918,50), fill=DIM, width=3)
    d.line((938,29,946,37), fill=DIM, width=2)
    centered(d, 43, title, font(30, True), CYAN)
    # animated subtitle
    prefix = "> "
    sub = prefix + subtitle
    f = font(17, True)
    box = d.textbbox((0,0), sub, font=f)
    x = (W-(box[2]-box[0]))/2
    d.text((x,92), sub, font=f, fill=GREEN)
    if cursor:
        d.rectangle((x+(box[2]-box[0])+7,95,x+(box[2]-box[0])+15,114), fill=GREEN)
    # tiny status line
    centered(d, 135, "SYSTEM // PROFILE ONLINE", font(10), DIM)
    return im

titles = ["B.Tech CSE Student", "Java + DSA Learner", "AI / ML Explorer", "Software Developer"]
subs = ["Learning | Building | Improving ...", "Coding | Solving | Growing ...", "Data | Models | Experiments ...", "Designing | Debugging | Deploying ..."]
frames=[]
for phase in range(32):
    idx = (phase // 8) % len(titles)
    frames.append(frame(titles[idx], subs[idx], phase % 8 != 7, phase))

out = Path("hero.gif")
frames[0].save(out, save_all=True, append_images=frames[1:], duration=180, loop=0, disposal=2)
print("Wrote", out)
