"""Read original font outlines; does not edit images or alter the font."""
import json, pathlib, hashlib
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
root=pathlib.Path('/workspace/scratch/100914f15bb1')
font_path=root/'LongCang-Regular.ttf'
font=TTFont(font_path)
cmap=font.getBestCmap(); gs=font.getGlyphSet(); upm=font['head'].unitsPerEm
texts=['设置', '音效', '开启', '触感反馈', '开启', '减少动画', '关闭', '游戏模式', '现有揭棋', '查看基础开局', '恢复默认', '设置', '音效', '开启', '触感反馈', '开启', '减少动画', '关闭', '游戏模式', '现有揭棋', '恢复默认', '乐子象棋设置页S1-v3']
glyphs={}
for char in set(''.join(texts)):
    name=cmap[ord(char)]; glyph=gs[name]
    pen=SVGPathPen(gs); glyph.draw(pen)
    bp=BoundsPen(gs); glyph.draw(bp)
    glyphs[char]={'name':name,'path':pen.getCommands(),'advance':font['hmtx'][name][0],'bounds':bp.bounds}
data={'family':font['name'].getDebugName(1),'face_index':0,'units_per_em':upm,'font_sha256':hashlib.sha256(font_path.read_bytes()).hexdigest(),'glyphs':glyphs}
(root/'s1-v3-real-glyphs.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'font':data['family'],'glyph_count':len(glyphs),'upm':upm,'source_file_unchanged':True}))
