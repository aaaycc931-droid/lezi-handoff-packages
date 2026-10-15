import json,pathlib,hashlib
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
root=pathlib.Path(__file__).resolve().parent; fp=root/'fonts/LongCang-Regular.ttf'; font=TTFont(fp); cmap=font.getBestCmap(); gs=font.getGlyphSet(); glyphs={}
for char in sorted(set('等待对方加入本机设备：我的手机取消等待')):
    if ord(char) not in cmap:raise ValueError('Missing real glyph '+char)
    name=cmap[ord(char)];g=gs[name];sp=SVGPathPen(gs);bp=BoundsPen(gs);g.draw(sp);g.draw(bp)
    glyphs[char]={'path':sp.getCommands(),'advance':font['hmtx'][name][0],'bounds':bp.bounds}
(root/'layers/real-glyphs.json').write_text(json.dumps({'family':font['name'].getDebugName(1),'units_per_em':font['head'].unitsPerEm,'font_sha256':hashlib.sha256(fp.read_bytes()).hexdigest(),'glyphs':glyphs},ensure_ascii=False,indent=2)+'\n')
