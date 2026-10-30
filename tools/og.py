# Usage: python og.py <Bricolage.ttf> <out.svg>, then render with VectorCraft.
# Builds og.svg (1200x630) with Bricolage text converted to paths; VectorCraft renders the PNG.
import sys
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

SRC, OUT = sys.argv[1], sys.argv[2]
_cache = {}

def font(wght, opsz=48):
    key = (wght, opsz)
    if key not in _cache:
        f = TTFont(SRC)
        _cache[key] = instantiateVariableFont(f, {"wght": wght, "opsz": opsz, "wdth": 100})
    return _cache[key]

def text(s, x, y, size, wght, fill, anchor="start", opsz=48):
    f = font(wght, opsz)
    cmap, gs, hmtx = f.getBestCmap(), f.getGlyphSet(), f["hmtx"]
    upm = f["head"].unitsPerEm
    sc = size / upm
    width = sum(hmtx[cmap[ord(c)]][0] for c in s) * sc
    if anchor == "middle":
        x -= width / 2
    pen = SVGPathPen(gs)
    cx = 0
    for c in s:
        g = cmap[ord(c)]
        gs[g].draw(TransformPen(pen, (sc, 0, 0, -sc, x + cx * sc, y)))
        cx += hmtx[g][0]
    return f'<path fill="{fill}" d="{pen.getCommands()}"/>', width

BG, TEXT, MUTED, LIGHT, MUSTARD, EXT, INK = "#141414", "#ededeb", "#a3a29e", "#ecebe8", "#dcb664", "#4a4947", "#1d1d1f"
parts, widths = [], {}

def add(key, *a, **k):
    p, w = text(*a, **k)
    parts.append(p)
    widths[key] = round(w)

pride = ["#e40303", "#ff8c00", "#ffed00", "#008026", "#004dff", "#750787"]
parts.append("".join(f'<rect x="{i*200}" y="0" width="200" height="8" fill="{c}"/>' for i, c in enumerate(pride)))

# left column
parts.append(f'<rect x="80" y="84" width="64" height="64" rx="15" fill="{LIGHT}"/>')
add("cg", "cg", 112, 127, 30, 800, INK, anchor="middle")
add("name", "Christian Groth", 76, 318, 80, 800, TEXT, opsz=72)
add("role", "Software Architect & Engineer", 80, 376, 34, 600, MUSTARD)
add("c1", "Shipped today, still changeable tomorrow.", 80, 466, 30, 500, MUTED)
add("url", "chrgroth.de", 80, 566, 24, 700, TEXT)

# right: mini system context
edges = [((980, 218), (980, 340)), ((885, 302), (930, 340)), ((1075, 302), (1030, 340)),
         ((885, 470), (930, 430)), ((1075, 470), (1030, 430))]
parts.append("".join(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="{MUTED}" stroke-width="2" stroke-dasharray="6 6"/>' for a, b in edges))

def node(x, y, w, h, fill, ink, title, kind, rx=10, tsize=17):
    parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"/>')
    add(title, title, x + w / 2, y + h / 2 + 2, tsize, 700, ink, anchor="middle")
    add(title + "-k", kind, x + w / 2, y + h / 2 + 19, 12, 400, ink, anchor="middle")

parts.append(f'<circle cx="980" cy="142" r="19" fill="{MUSTARD}"/>')
node(920, 164, 120, 54, MUSTARD, "#2a2210", "Visitor", "[Person]", rx=16)
node(820, 250, 130, 52, MUSTARD, "#2a2210", "Teams", "[Person]")
node(1010, 250, 130, 52, MUSTARD, "#2a2210", "Business", "[Person]")
node(890, 340, 180, 90, LIGHT, INK, "Christian Groth", "[Software System]", rx=12, tsize=19)
node(820, 470, 130, 52, EXT, TEXT, "Production", "[External System]")
node(1010, 470, 130, 52, EXT, TEXT, "Platform & Ops", "[External System]")

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">'
       f'<rect width="1200" height="630" fill="{BG}"/>' + "".join(parts) + "</svg>")
open(OUT, "w", encoding="utf-8").write(svg)
print(widths)
