import argparse, hashlib, json
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen

p = Path(__file__).resolve().parent
ap = argparse.ArgumentParser()
ap.add_argument('--baseline', type=Path, required=True)
a = ap.parse_args()
params = json.loads((p/'parameters.json').read_text())
fp = a.baseline/'fonts/LongCang-Regular.ttf'
digest = hashlib.sha256(fp.read_bytes()).hexdigest()
assert digest == params['font']['sha256'], 'Font identity mismatch'
font = TTFont(fp); cmap = font.getBestCmap(); gs = font.getGlyphSet(); glyphs = {}
for c in sorted(set(''.join(e['text'] for e in params['lines']))):
    if ord(c) not in cmap: raise ValueError('Missing glyph '+c)
    name = cmap[ord(c)]; g = gs[name]; sp = SVGPathPen(gs); bp = BoundsPen(gs)
    g.draw(sp); g.draw(bp)
    glyphs[c] = {'path':sp.getCommands(),'advance':font['hmtx'][name][0],'bounds':bp.bounds}
(p/'layers/real-glyphs.json').write_text(json.dumps({'family':font['name'].getDebugName(1),'units_per_em':font['head'].unitsPerEm,'font_sha256':digest,'glyphs':glyphs},ensure_ascii=False,indent=2)+'\n')
