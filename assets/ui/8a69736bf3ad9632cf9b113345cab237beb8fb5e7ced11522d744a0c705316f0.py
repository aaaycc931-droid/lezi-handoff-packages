import json,pathlib,hashlib
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
p=pathlib.Path(__file__).resolve().parent;fp=p/'fonts/LongCang-Regular.ttf';font=TTFont(fp);cmap=font.getBestCmap();gs=font.getGlyphSet();glyphs={}
for c in sorted(set('已配对设备朋友的手机地址：02:00:00:00:00:01连接设备重新检测打开系统蓝牙设置返回')):
 if ord(c) not in cmap:raise ValueError('Missing glyph '+c)
 name=cmap[ord(c)];g=gs[name];sp=SVGPathPen(gs);bp=BoundsPen(gs);g.draw(sp);g.draw(bp);glyphs[c]={'path':sp.getCommands(),'advance':font['hmtx'][name][0],'bounds':bp.bounds}
(p/'layers/real-glyphs.json').write_text(json.dumps({'family':font['name'].getDebugName(1),'units_per_em':font['head'].unitsPerEm,'font_sha256':hashlib.sha256(fp.read_bytes()).hexdigest(),'glyphs':glyphs},ensure_ascii=False,indent=2)+'\n')
