"""Read original font outlines; does not edit images or alter the font."""
import json, pathlib, hashlib
from fontTools.ttLib import TTCollection
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
root=pathlib.Path('/workspace/scratch/384cae71d8cb')
font_path=root/'real-font-source/extracted/usr/share/fonts/truetype/arphic/ukai.ttc'
font=TTCollection(font_path).fonts[0]
cmap=font.getBestCmap(); gs=font.getGlyphSet(); upm=font['head'].unitsPerEm
texts=['面对面对局','蓝牙对局','蓝牙当前处于关闭状态，','请先开启蓝牙。','开启蓝牙']
glyphs={}
for char in set(''.join(texts)):
    name=cmap[ord(char)]; glyph=gs[name]
    pen=SVGPathPen(gs); glyph.draw(pen)
    bp=BoundsPen(gs); glyph.draw(bp)
    glyphs[char]={'name':name,'path':pen.getCommands(),'advance':font['hmtx'][name][0],'bounds':bp.bounds}
data={'family':font['name'].getDebugName(1),'face_index':0,'units_per_em':upm,'font_sha256':hashlib.sha256(font_path.read_bytes()).hexdigest(),'glyphs':glyphs}
(root/'b2-v3-real-glyphs.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'font':data['family'],'glyph_count':len(glyphs),'upm':upm,'source_file_unchanged':True}))
