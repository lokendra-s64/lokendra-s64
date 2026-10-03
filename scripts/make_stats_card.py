from pathlib import Path
import json, html

W,H=960,250
BG="#020b10"; BORDER="#00b9d9"; CYAN="#00e5ff"; GREEN="#00ff88"; PINK="#ff4fb3"; WHITE="#e6f7ff"; MUTED="#7aa5b2"

def esc(s): return html.escape(str(s))

def card(x,y,w,h,fill="#06141b",stroke="#123743",r=10):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>'

def text(x,y,s,size=14,fill=WHITE,weight="600",anchor="start",family="DejaVu Sans Mono,monospace"):
    return f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{esc(s)}</text>'

def icon(x,y,s,fill): return text(x,y,s,20,fill,"700","middle","DejaVu Sans,Arial")

p=Path(__import__('sys').argv[1]); out=Path(__import__('sys').argv[2]); d=json.loads(p.read_text())
stars=d.get('stars',0); commits=d.get('commits',0); prs=d.get('pull_requests',0); issues=d.get('issues',0); total=d.get('total_contributions',0); current=d.get('current_streak',0); longest=d.get('longest_streak',0)
svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">', f'<rect width="{W}" height="{H}" rx="12" fill="{BG}"/>', f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="12" fill="none" stroke="{BORDER}" stroke-width="2"/>']
# title
svg += [text(22,34,"Lokendra's GitHub Stats",17,CYAN,"800"), text(938,34,"LIVE",10,GREEN,"800","end")]
# left stats
svg.append(card(18,50,335,182))
rows=[("★","Total Stars",stars,PINK),("◉","Total Commits",commits,CYAN),("⑂","Total PRs",prs,"#b57cff"),("●","Total Issues",issues,GREEN),("▣","Contributions",total,CYAN)]
for i,(ic,label,val,col) in enumerate(rows):
    y=82+i*29; svg += [icon(38,y-3,ic,col), text(58,y,label,13,WHITE,"650"), text(320,y,str(val),14,WHITE,"800","end")]
# total ring
cx=495; cy=142; r=55; svg += [f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#12323b" stroke-width="11"/>', f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{GREEN}" stroke-width="11" stroke-linecap="round" stroke-dasharray="{min(2*3.14159*r, max(25,total)*4)} {2*3.14159*r}" transform="rotate(-90 {cx} {cy})"/>', icon(cx,cy+5,"◉",CYAN), text(cx,cy+36,str(total),28,WHITE,"900","middle"), text(cx,cy+55,"Total Contributions",11,CYAN,"700","middle")]
# dividers and streaks
svg += [f'<line x1="650" y1="58" x2="650" y2="225" stroke="{BORDER}" stroke-width="1.5"/>', f'<line x1="805" y1="58" x2="805" y2="225" stroke="{BORDER}" stroke-width="1.5"/>']
svg += [icon(728,91,"♨",GREEN), text(728,132,str(current),32,PINK,"900","middle"), text(728,154,"CURRENT STREAK",11,CYAN,"800","middle"), text(728,174,"days",11,WHITE,"600","middle"), text(728,204,"GitHub GraphQL • live",9,GREEN,"700","middle")]
svg += [icon(883,91,"★",PINK), text(883,132,str(longest),32,PINK,"900","middle"), text(883,154,"LONGEST STREAK",11,CYAN,"800","middle"), text(883,174,"days",11,WHITE,"600","middle"), text(883,204,"GitHub GraphQL • live",9,GREEN,"700","middle")]
svg.append('</svg>'); out.write_text(''.join(svg),encoding='utf-8')
