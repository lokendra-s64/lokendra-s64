from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

W, H = 960, 180
BG = (2, 11, 16)
CYAN = (0, 229, 255)
GREEN = (0, 255, 136)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"


def font(size, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)


def draw_base(d):
    # Keep the existing cyan terminal-style box, but intentionally remove
    # the repository filename and edit/pencil glyph from the header.
    d.rounded_rectangle((1, 1, W - 2, H - 2), radius=9, outline=CYAN, width=2)
    corners = [
        ((12, 30), (12, 12), (30, 12)),
        ((W - 30, 12), (W - 12, 12), (W - 12, 30)),
        ((12, H - 30), (12, H - 12), (30, H - 12)),
        ((W - 30, H - 12), (W - 12, H - 12), (W - 12, H - 30)),
    ]
    for pts in corners:
        d.line([pts[0], pts[1], pts[2]], fill=CYAN, width=2)


def centered(draw, y, text, fnt, fill):
    box = draw.textbbox((0, 0), text, font=fnt)
    width = box[2] - box[0]
    x = (W - width) / 2
    draw.text((x, y), text, font=fnt, fill=fill)
    return x, width


def frame(title, subtitle, title_visible, subtitle_visible, cursor=True):
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    draw_base(d)

    title_font = font(30, True)
    sub_font = font(17, True)

    shown_title = title[:title_visible]
    shown_sub = subtitle[:subtitle_visible]

    if shown_title:
        x, width = centered(d, 43, shown_title, title_font, CYAN)
        if cursor and subtitle_visible == 0:
            d.rectangle((x + width + 7, 50, x + width + 15, 69), fill=CYAN)

    if shown_sub:
        x, width = centered(d, 92, "> " + shown_sub, sub_font, GREEN)
        if cursor:
            d.rectangle((x + width + 7, 95, x + width + 15, 114), fill=GREEN)

    return im


# Typewriter animation matching the supplied reference video:
# blank -> title types in -> subtitle types in -> pause -> reset -> next message.
titles = [
    "B.Tech CSE Student",
    "Java + DSA Learner",
    "AI / ML Explorer",
    "Software Developer",
]
subs = [
    "Learning | Building | Improving ...",
    "Coding | Solving | Growing ...",
    "Data | Models | Experiments ...",
    "Designing | Debugging | Deploying ...",
]

frames = []
for title, subtitle in zip(titles, subs):
    # blank lead-in
    for _ in range(4):
        frames.append(frame(title, subtitle, 0, 0, False))

    # title typewriter
    for n in range(1, len(title) + 1):
        frames.append(frame(title, subtitle, n, 0, True))

    # short pause with title
    for _ in range(5):
        frames.append(frame(title, subtitle, len(title), 0, True))

    # subtitle typewriter
    for n in range(1, len(subtitle) + 1):
        frames.append(frame(title, subtitle, len(title), n, True))

    # readable hold
    for i in range(18):
        frames.append(frame(title, subtitle, len(title), len(subtitle), i % 4 != 3))

    # blank before next message
    for _ in range(5):
        frames.append(frame(title, subtitle, 0, 0, False))

out = Path("hero.gif")
frames[0].save(
    out,
    save_all=True,
    append_images=frames[1:],
    duration=55,
    loop=0,
    disposal=2,
    optimize=True,
)
print("Wrote", out, "frames:", len(frames))
