#!/usr/bin/env python3
"""Recompose B10 faithfully from existing approved UI assets; source input is read-only."""
import argparse, hashlib, io, json
from pathlib import Path
import numpy as np
from PIL import Image
import cairosvg
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen

P=Path(__file__).resolve().parent
cfg=json.loads((P/"parameters.json").read_text(encoding="utf-8"))
ap=argparse.ArgumentParser()
for name in ("base","font","approved-b9","out"): ap.add_argument("--"+name,required=True)
a=ap.parse_args()
base_path,font_path,old_path,out_path=map(Path,[a.base,a.font,a.approved_b8,a.out])
digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert digest(base_path)==cfg["background_sha256"],"Approved background mismatch"
assert digest(font_path)==cfg["font_sha256"],"Long Cang font mismatch"
assert digest(old_path)==cfg["approved_predecessor"]["sha256"],"B9 approved preview mismatch"
font=TTFont(font_path)
cmap=font.getBestCmap()
gs=font.getGlyphSet()
def render(lines):
    shapes=[]
    for e in lines:
        advance=0
        minx=miny=float("inf");maxx=maxy=-float("inf")
        children=[]
        for c in e["text"]:
            name=cmap[ord(c)];g=gs[name]
            sp=SVGPathPen(gs);bp=BoundsPen(gs)
            g.draw(sp);g.draw(bp)
            if bp.bounds:
                x0,y0,x1,y1=bp.bounds
                minx=min(minx,advance+x0);maxx=max(maxx,advance+x1)
                miny=min(miny,y0);maxy=max(maxy,y1)
                children.append(f'<path transform="translate({advance} 0)" d="{sp.getCommands()}"/>')
            advance+=font["hmtx"][name][0]
        scale=min(e["maxWidth"]/(maxx-minx),e["maxHeight"]/(maxy-miny))
        tx=e["cx"]-scale*(minx+maxx)/2
        ty=e["cy"]+scale*(miny+maxy)/2
        shapes.append(f'<g id="{e["id"]}" fill="{e["fill"]}" transform="translate({tx} {ty}) scale({scale} {-scale})">{"".join(children)}</g>')
    W,H=cfg["canvas"]["width"],cfg["canvas"]["height"]
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{"".join(shapes)}</svg>'
    layer=Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode()))).convert("RGBA")
    return svg,layer
svg,new_layer=render(cfg["lines"])
old_lines=[
  {
    "id": "permission_status",
    "text": "蓝牙权限已被永久拒绝",
    "cx": 426,
    "cy": 514,
    "maxWidth": 565,
    "maxHeight": 48,
    "fill": "#12120f"
  },
  {
    "id": "permission_reason_1",
    "text": "请在系统设置中开启附近设备权限，",
    "cx": 426,
    "cy": 577,
    "maxWidth": 560,
    "maxHeight": 34,
    "fill": "#12120f"
  },
  {
    "id": "permission_reason_2",
    "text": "返回游戏后重新进入蓝牙对局。",
    "cx": 426,
    "cy": 627,
    "maxWidth": 560,
    "maxHeight": 34,
    "fill": "#12120f"
  },
  {
    "id": "open_app_settings",
    "text": "前往系统设置",
    "cx": 426,
    "cy": 793,
    "maxWidth": 460,
    "maxHeight": 108,
    "fill": "#123754"
  }
]
_,old_layer=render(old_lines)
image=Image.alpha_composite(Image.open(base_path).convert("RGBA"),new_layer)
old=np.array(Image.open(old_path).convert("RGBA"))
old_recomposed=np.array(Image.alpha_composite(Image.open(base_path).convert("RGBA"),old_layer))
assert np.array_equal(old_recomposed,old),"Approved B9 cannot be exactly recomposed"
new=np.array(image)
mask=(np.array(new_layer)[:,:,3]>0)|(np.array(old_layer)[:,:,3]>0)
changed=np.any(old!=new,axis=2)
allowed=np.zeros(mask.shape,dtype=bool)
for r in cfg['regions']:
    allowed[r['y']:r['y']+r['height'],r['x']:r['x']+r['width']]=True
assert int((changed & ~(mask & allowed)).sum())==0,"Approved protected pixels changed"
out_path.parent.mkdir(parents=True,exist_ok=True)
image.save(out_path,format="PNG",compress_level=9)
out_path.with_suffix(".text.svg").write_text(svg,encoding="utf-8")
assert digest(out_path)==cfg["local_preview_sha256"],"B10 candidate SHA mismatch"
print(json.dumps({"candidate":"B10-v1","preview_sha256":digest(out_path),
                  "protected_pixel_changes":0,"changed_pixels":int(changed.sum()),
                  "approval":"pending_user_review","runtime":"not_run"},ensure_ascii=False))
