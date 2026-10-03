import json, sys
from pathlib import Path

BG='#020b10'; PANEL='#06131a'; BORDER='#00b9d9'; CYAN='#00e5ff'; GREEN='#00ff88'; PINK='#ff4fa3'; WHITE='#f2fbff'; MUTED='#91a9b2'; PURPLE='#a970ff'
FONT='SFMono-Regular, Consolas, monospace'
W,H=960,250

def esc(x): return str(x).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
def text(x,y,s,size=13,fill=WHITE,weight='normal',anchor='start'):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{FONT}" font-size="{size}px" font-weight="{weight}" fill="{fill}">{esc(s)}</text>'

def icon(x,y,kind,color):
    if kind=='github':
        path='M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27s1.36.09 2 .27c1.53-1.03 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8Z'
        return f'<circle cx="{x}" cy="{y}" r="27" fill="none" stroke="{color}" stroke-width="2"/><g transform="translate({x-13},{y-13}) scale(1.6)"><path d="{path}" fill="{color}"/></g>'
    if kind=='fire': return f'<text x="{x}" y="{y+12}" text-anchor="middle" font-family="Arial" font-size="38" fill="{color}">♨</text>'
    if kind=='star': return f'<text x="{x}" y="{y+12}" text-anchor="middle" font-family="Arial" font-size="42" fill="{color}">★</text>'
    return ''

def main():
    path=sys.argv[1] if len(sys.argv)>1 else 'data/contributions.json'; out=sys.argv[2] if len(sys.argv)>2 else 'stats-card.svg'
    d=json.loads(Path(path).read_text(encoding='utf-8'))
    total=int(d.get('total_contributions',0)); commits=int(d.get('commits',0)); prs=int(d.get('pull_requests',0)); issues=int(d.get('issues',0)); stars=int(d.get('stars',0)); current=int(d.get('current_streak',0)); longest=int(d.get('longest_streak',0)); updated=d.get('generated_at','')[:10] or 'live'
    circ=2*3.1415926535*52; pct=min(1,current/max(longest,1)) if longest else 0; dash=circ*pct
    p=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',f'<rect x="1" y="1" width="958" height="248" rx="9" fill="{BG}" stroke="{BORDER}" stroke-width="2"/>',f'<rect x="16" y="18" width="315" height="214" rx="8" fill="{PANEL}" stroke="#124b5b"/>',f'<text x="34" y="47" font-family="{FONT}" font-size="17" font-weight="700" fill="{CYAN}">Lokendra&apos;s GitHub Stats</text>']
    rows=[('★','Total Stars',stars,PINK),('◉','Total Commits',commits,CYAN),('⑂','Total PRs',prs,PURPLE),('●','Total Issues',issues,GREEN),('▣','Contributions',total,CYAN)]
    for i,(sym,label,val,col) in enumerate(rows):
        y=78+i*29; p.append(text(36,y,sym,16,col,'bold')); p.append(text(62,y,label,13,WHITE,'bold')); p.append(text(285,y,f'{val:,}',15,WHITE,'bold','end'))
    # center ring / total contributions
    cx,cy=470,125
    p += [f'<circle cx="{cx}" cy="{cy}" r="52" fill="none" stroke="#153743" stroke-width="11"/>',f'<circle cx="{cx}" cy="{cy}" r="52" fill="none" stroke="{GREEN}" stroke-width="11" stroke-linecap="round" stroke-dasharray="{dash:.1f} {circ:.1f}" transform="rotate(-90 {cx} {cy})"/>',icon(cx,cy-18,'github',CYAN),text(cx,cy+34,f'{total:,}',30,CYAN,'bold','middle'),text(cx,cy+58,'Total Contributions',12,WHITE,'bold','middle'),text(cx,cy+76,f'Updated {updated}',9,MUTED,'normal','middle')]
    # dividers
    p += [f'<line x1="610" y1="28" x2="610" y2="220" stroke="{BORDER}" opacity="0.8"/>',f'<line x1="790" y1="28" x2="790" y2="220" stroke="{BORDER}" opacity="0.8"/>']
    # current streak
    p += [icon(700,58,'fire',GREEN),text(700,106,f'{current}',36,PINK,'bold','middle'),text(700,133,'CURRENT STREAK',13,CYAN,'bold','middle'),text(700,154,'days',12,WHITE,'normal','middle'),text(700,180,'GitHub GraphQL • live',10,GREEN,'bold','middle')]
    # longest streak
    p += [icon(875,58,'star',PINK),text(875,106,f'{longest}',36,PINK,'bold','middle'),text(875,133,'LONGEST STREAK',13,CYAN,'bold','middle'),text(875,154,'days',12,WHITE,'normal','middle'),text(875,180,'GitHub GraphQL • live',10,GREEN,'bold','middle')]
    # small live indicator
    p.append(f'<circle cx="928" cy="28" r="5" fill="{GREEN}"/><text x="914" y="33" text-anchor="end" font-family="{FONT}" font-size="9" fill="{GREEN}">LIVE</text>')
    p.append('</svg>')
    Path(out).write_text(''.join(p),encoding='utf-8')
if __name__=='__main__': main()
