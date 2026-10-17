const fs=require('fs'),path=require('path'),crypto=require('crypto');
const sharp=require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/sharp');
const root=__dirname,baseline=path.resolve(process.argv[2]||'');
if(!process.argv[2])throw Error('Usage: node compose.cjs /absolute/path/to/baseline');
const params=JSON.parse(fs.readFileSync(path.join(root,'parameters.json'))),{width:w,height:h}=params.canvas;
const font=JSON.parse(fs.readFileSync(path.join(root,'layers/real-glyphs.json')));
const expected={b4:'7c11e53aaa7c76b04e77ca60b59780ca4b61dfc251e541fea9df21a3ce38f72c',b5:'f01b1307f68d20e9c8d5f99c8fb913f9dbef01ec913dd42810000dea73c1a712',base:'13a513a067abb972ab8e0c898faeba92eb17952a1ecc955248e418c73b429a8f'};
const hash=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const raw=async p=>{const {data,info}=await sharp(p).ensureAlpha().raw().toBuffer({resolveWithObject:true});if(info.width!==w||info.height!==h)throw Error('Unexpected asset dimensions');return data;};
function compose(base,layer){const out=Buffer.from(base);for(let p=0;p<w*h;p++){const k=p*4,a=layer[k+3]/255;if(a){for(let c=0;c<3;c++)out[k+c]=Math.round(base[k+c]*(1-a)+layer[k+c]*a);out[k+3]=255;}}return out;}
function count(a,b){let n=0;for(let p=0;p<w*h;p++){const k=p*4;if([0,1,2,3].some(c=>a[k+c]!==b[k+c]))n++;}return n;}
function realText(e){let advance=0,minX=Infinity,minY=Infinity,maxX=-Infinity,maxY=-Infinity,children=[];
 for(const c of e.text){const g=font.glyphs[c];if(!g)throw Error('Missing glyph '+c);if(g.bounds){const[x0,y0,x1,y1]=g.bounds;minX=Math.min(minX,advance+x0);maxX=Math.max(maxX,advance+x1);minY=Math.min(minY,y0);maxY=Math.max(maxY,y1);children.push(`<path transform="translate(${advance} 0)" d="${g.path}"/>`);}advance+=g.advance;}
 const s=Math.min(e.maxWidth/(maxX-minX),e.maxHeight/(maxY-minY));e.actual_ink_bounds={width:s*(maxX-minX),height:s*(maxY-minY)};e.font_size_px=s*font.units_per_em;
 return `<g id="${e.id}" fill="${e.fill}" transform="translate(${e.cx-s*(minX+maxX)/2} ${e.cy+s*(minY+maxY)/2}) scale(${s} ${-s})">${children.join('')}</g>`;
}
(async()=>{
 const b4path=path.join(baseline,'images/lezi-bluetooth-B4-v1.png'),b5path=path.join(baseline,'images/lezi-bluetooth-B5-v1.png'),basepath=path.join(baseline,'sources/B4-v1/background-layers/b4-fixed-local-base.png');
 if(hash(b4path)!==expected.b4||hash(b5path)!==expected.b5||hash(basepath)!==expected.base||font.font_sha256!==params.font.sha256)throw Error('Frozen source identity mismatch');
 const b4=await raw(b4path),b5=await raw(b5path),base=await raw(basepath),oldText=await raw(path.join(baseline,'sources/B4-v1/layers/b4-real-text-layer.png')),oldControls=await raw(path.join(baseline,'sources/B4-v1/layers/selection-and-links.png'));
 const b4diff=count(compose(compose(base,oldControls),oldText),b4);
 const b5base=await raw(path.join(baseline,'sources/B5-v1/background-layers/b5-fixed-local-base.png')),b5text=await raw(path.join(baseline,'sources/B5-v1/layers/b5-empty-text-layer.png')),b5disabled=await raw(path.join(baseline,'sources/B5-v1/layers/connect-disabled.png'));
 const b5diff=count(compose(compose(b5base,b5text),b5disabled),b5);
 if(b4diff||b5diff)throw Error('Approved source recomposition mismatch');
 const entries=structuredClone(params.lines),groups=entries.map(realText),svg=`<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}">${groups.join('')}</svg>`;
 fs.writeFileSync(path.join(root,'layers/b8-real-text-layer.svg'),svg);
 const textpath=path.join(root,'layers/b8-real-text-layer.png');await sharp(Buffer.from(svg)).ensureAlpha().png().toFile(textpath);
 const approvedRoot=path.resolve(process.argv[3]||path.join(root,'../B7-v1'));
 const approvedPath=path.join(approvedRoot,'lezi-bluetooth-B7-v1.png');
 if(hash(approvedPath)!=='1ab53dbaec7936e720835425ec117e431a2bbf5385410ced7d898d222a03f74a')throw Error('Approved B7 identity mismatch');
 const approved=await raw(approvedPath),approvedText=await raw(path.join(approvedRoot,'layers/b7-real-text-layer.png'));
 const text=await raw(textpath),out=compose(base,text),allowed=Buffer.alloc(w*h);
 for(let p=0;p<w*h;p++)if(approvedText[p*4+3]||text[p*4+3])allowed[p]=255;
 await sharp(allowed,{raw:{width:w,height:h,channels:1}}).toColourspace('b-w').png().toFile(path.join(root,'evidence/allowed-mask.png'));
 fs.writeFileSync(path.join(root,'evidence/regions.json'),JSON.stringify({regions:params.regions},null,2)+'\n');
 const output=path.join(root,'lezi-bluetooth-B8-v1.png');await sharp(out,{raw:{width:w,height:h,channels:4}}).png().toFile(output);
 const evidence={schema:'lezi.bluetooth_permission_retry_static_candidate.v1',version:'B8-v1',source_version:'B4-v1',source_sha256:hash(b4path),output_sha256:hash(output),width:w,height:h,font_family:font.family,font_sha256:font.font_sha256,font_modified:false,lines:entries,approved_source_recomposition:{'B4-v1':b4diff,'B5-v1':b5diff},source_unchanged:hash(b4path)===expected.b4&&hash(b5path)===expected.b5&&hash(basepath)===expected.base,background:{reused_sha256:expected.base,new_estimation:false,historical_estimation:'Inherited B2 text-footprint estimates retained; not original hidden paper pixels'},whole_page_regenerated:false,resampling:false,approved_comparison_version:'B7-v1',approved_comparison_sha256:hash(approvedPath),changed_pixels:count(approved,out),changed_pixels_vs_B4:count(b4,out),mask_rule:params.mask_rule,fixture:params.fixture,actions:params.actions,artwork_approval:'pending_user_review',runtime_acceptance:'not_run',bluetooth_device_acceptance:'not_run',production_code_changed:false,game_rules_delta:0,scoring_frozen:true,NET:'paused'};
 fs.writeFileSync(path.join(root,'evidence/revision.json'),JSON.stringify(evidence,null,2)+'\n');
 console.log(JSON.stringify({output,sha256:evidence.output_sha256,recomposition:evidence.approved_source_recomposition,source_unchanged:evidence.source_unchanged,changed_pixels:evidence.changed_pixels}));
})().catch(e=>{console.error(e);process.exit(1);});
