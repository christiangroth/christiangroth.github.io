# Builds favicon.svg and apple-touch-icon.svg ("cg" monogram, text as Bricolage paths); VectorCraft renders the PNG.
import sys
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

SRC, OUT = sys.argv[1], sys.argv[2]
f = instantiateVariableFont(TTFont(SRC), {"wght": 800, "opsz": 48, "wdth": 100})
cmap, gs, hmtx, upm = f.getBestCmap(), f.getGlyphSet(), f["hmtx"], f["head"].unitsPerEm


def text(s, cx, y, size, fill):
    sc = size / upm
    x = cx - sum(hmtx[cmap[ord(c)]][0] for c in s) * sc / 2
    pen, adv = SVGPathPen(gs), 0
    for c in s:
        g = cmap[ord(c)]
        gs[g].draw(TransformPen(pen, (sc, 0, 0, -sc, x + adv * sc, y)))
        adv += hmtx[g][0]
    return f'<path fill="{fill}" d="{pen.getCommands()}"/>'


GRAPHITE, LIGHT, MUSTARD = "#2b2a29", "#ecebe8", "#dcb664"

# tab icon: rounded graphite tile, light letters, mustard underline; flips to light tile in dark browsers
fav = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
       '<style>.t{fill:%s}.l{fill:%s}@media (prefers-color-scheme:dark){.t{fill:%s}.l{fill:%s}}</style>'
       '<rect class="t" width="64" height="64" rx="15"/>' % (GRAPHITE, LIGHT, LIGHT, GRAPHITE)
       + text("cg", 32, 41, 34, "x").replace('fill="x"', 'class="l"')
       + f'<rect x="20" y="49" width="24" height="4" rx="2" fill="{MUSTARD}"/></svg>')
open(OUT + "/favicon.svg", "w", encoding="utf-8").write(fav)

# home screen icon: full-bleed, iOS rounds the corners itself
touch = ('<svg xmlns="http://www.w3.org/2000/svg" width="180" height="180" viewBox="0 0 180 180">'
         f'<rect width="180" height="180" fill="{GRAPHITE}"/>'
         + text("cg", 90, 112, 92, LIGHT)
         + f'<rect x="58" y="134" width="64" height="9" rx="4.5" fill="{MUSTARD}"/></svg>')
open(OUT + "/apple-touch-icon.svg", "w", encoding="utf-8").write(touch)
print("ok")
