import sys
from pathlib import Path

DATA = {
    "name": "LOKENDRA SONWANI",
    "role": "B.Tech CSE Student",
    "now": "Learning Java + DSA",
    "focus": "AI / ML / Software Development",
    "stack": ["C", "C++", "Java", "Python", "JS"],
    "web": ["HTML", "CSS", "Flask", "MongoDB"],
    "edu": "B.Tech CSE, PSIT Kanpur",
    "grad": "2028",
    "loc": "Kanpur, India",
}
WIDTH = 500
FONT = "SFMono-Regular, Consolas, monospace"
BG, BORDER, LABEL, VALUE, ACCENT = "#020b10", "#00b9d9", "#c9d1d9", "#ffffff", "#00e5ff"
TITLEBAR_H, PAD_X, LINE_H = 34, 20, 23

def esc(s):
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

def build():
    rows = [
        ("os", "human@kanpur"), ("role", DATA["role"]), ("now", DATA["now"]),
        ("focus", DATA["focus"]), ("stack", " / ".join(DATA["stack"])),
        ("web", " / ".join(DATA["web"])), ("edu", DATA["edu"]),
        ("grad", DATA["grad"]), ("loc", DATA["loc"] + " 🇮🇳"),
    ]
    body_y = TITLEBAR_H + 34
    height = body_y + len(rows) * LINE_H + 20
    parts = []
    for i, (label, value) in enumerate(rows):
        y, begin = body_y + i*LINE_H, 0.25 + i*0.09
        parts.append(f'''<g opacity="1" transform="translate(0,0)">
  <text x="{PAD_X}" y="{y}" font-family="{FONT}" font-size="13px" fill="{LABEL}">{esc(label)}</text>
  <text x="{PAD_X+65}" y="{y}" font-family="{FONT}" font-size="13px" fill="{VALUE}">{esc(value)}</text>
  <animate attributeName="opacity" from="0" to="1" begin="{begin:.2f}s" dur="0.3s" fill="freeze"/>
  <animateTransform attributeName="transform" type="translate" from="-12 0" to="0 0" begin="{begin:.2f}s" dur="0.3s" fill="freeze"/>
</g>''')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {height}" width="{WIDTH}" height="{height}">
<rect width="100%" height="100%" rx="8" fill="{BG}" stroke="{BORDER}"/>
<rect width="100%" height="{TITLEBAR_H}" rx="8" fill="{BG}"/>
<rect y="{TITLEBAR_H-1}" width="100%" height="1" fill="{BORDER}"/>
<circle cx="20" cy="{TITLEBAR_H/2}" r="5" fill="#ff5f56"/>
<circle cx="38" cy="{TITLEBAR_H/2}" r="5" fill="#ffbd2e"/>
<circle cx="56" cy="{TITLEBAR_H/2}" r="5" fill="#27c93f"/>
<text x="{WIDTH/2}" y="{TITLEBAR_H/2+4}" text-anchor="middle" font-family="{FONT}" font-size="12px" fill="{LABEL}">neofetch</text>
<text x="{PAD_X}" y="{TITLEBAR_H+20}" font-family="{FONT}" font-size="15px" font-weight="bold" fill="{ACCENT}">{esc(DATA["name"])}
<animate attributeName="opacity" from="0" to="1" begin="0s" dur="0.3s" fill="freeze"/>
</text>
{''.join(parts)}
</svg>'''

def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "info-card.svg"
    Path(out).write_text(build(), encoding="utf-8")
    print("Wrote", out)

if __name__ == "__main__":
    main()
