from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
import math

W, H = 960, 150
BG = (1, 8, 13)

font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
font_big = ImageFont.truetype(font_path, 25)


def wave_points(base, amp, phase, freq=58, drift=0):
    pts = []
    for x in range(-10, W + 11, 3):
        y = base + amp * math.sin(x / freq + phase + drift) + 3 * math.sin(x / 135 - phase * 0.55)
        pts.append((x, y))
    return pts


# Multiple green shades, with layered ribbons and glow rather than one thin line.
WAVES = [
    ((0, 255, 136), 7, 82, 0.95, 3),
    ((0, 225, 118), 10, 91, 1.05, 4),
    ((0, 190, 105), 13, 101, 1.15, 5),
    ((35, 155, 91), 8, 108, 1.30, 3),
    ((0, 255, 170), 5, 116, 1.48, 3),
    ((70, 120, 78), 11, 124, 1.62, 2),
]

frames = []
for phase_i in range(42):
    im = Image.new("RGB", (W, H), BG)

    # Soft glow layer.
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    for color, amp, base, speed, width in WAVES:
        pts = wave_points(base, amp, phase_i * 0.17 * speed, drift=phase_i * 0.06 * speed)
        gd.line(pts, fill=(*color, 105), width=width + 7, joint="curve")
    glow = glow.filter(ImageFilter.GaussianBlur(7))
    im = Image.alpha_composite(im.convert("RGBA"), glow).convert("RGB")
    d = ImageDraw.Draw(im)

    # Large readable footer slogan, above the wave field.
    slogan = "Learn. Build. Break. Fix. Repeat."
    box = d.textbbox((0, 0), slogan, font=font_big)
    sx = (W - (box[2] - box[0])) / 2
    d.text((sx, 7), slogan, font=font_big, fill=(0, 255, 136))
    cursor_x = sx + (box[2] - box[0]) + 8
    d.rectangle((cursor_x, 11, cursor_x + 8, 34), fill=(0, 255, 136))

    # Layered green wave ribbons.
    for color, amp, base, speed, width in WAVES:
        pts = wave_points(base, amp, phase_i * 0.17 * speed, drift=phase_i * 0.06 * speed)
        d.line(pts, fill=color, width=width, joint="curve")

    # A few moving green particles make the footer feel alive without clutter.
    for i in range(30):
        x = ((i * 71 + phase_i * 13) % (W + 50)) - 25
        y = 62 + 63 * (0.5 + 0.5 * math.sin(i * 1.31 + phase_i * 0.11))
        r = 1 if i % 3 else 2
        d.ellipse((x-r, y-r, x+r, y+r), fill=(0, 255, 136))

    frames.append(im)

out = Path("waves.gif")
frames[0].save(
    out,
    save_all=True,
    append_images=frames[1:],
    duration=85,
    loop=0,
    disposal=2,
    optimize=True,
)
print("Wrote", out, "frames:", len(frames))
