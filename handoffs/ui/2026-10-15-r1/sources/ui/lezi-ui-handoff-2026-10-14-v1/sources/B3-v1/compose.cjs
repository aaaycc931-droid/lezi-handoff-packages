const sharp=require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/sharp');
const fs=require('fs'),path=require('path'),crypto=require('crypto');const root=__dirname,w=852,h=1846;
const sha=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const source=path.join(root,'source/approved-B2-v4.png'),expected='0e15403ce826c21d1c3a5f3e73329a06fc9138ad20e2a5be1c0effd5f662fd08';
const font=JSON.parse(fs.readFileSync(path.join(root,'layers/real-glyphs.json')));
const entries=[
 {id:'waiting_status',text:'等待对方加入',cx:426,cy:514,maxWidth:385,maxHeight:46,fill:'#12120f'},
 {id:'device_name',text:'本机设备：我的手机',cx:426,cy:569,maxWidth:400,maxHeight:38,fill:'#12120f'},
 {id:'cancel_waiting',text:'取消等待',cx:426,cy:793,maxWidth:365,maxHeight:108,fill:'#123754'}
];
function realText(e){let advance=0,minX=Infinity,minY=Infinity,maxX=-Infinity,maxY=-Infinity;let children=[];
 for(const c of e.text){const g=font.glyphs[c];const [x0,y0,x1,y1]=g.bounds;minX=Math.min(minX,advance+x0);maxX=Math.max(maxX,advance+x1);minY=Math.min(minY,y0);maxY=Math.max(maxY,y1);children.push(`<path transform="translate(${advance} 0)" d="${g.path}"/>`);advance+=g.advance;}
 const s=Math.min(e.maxWidth/(maxX-minX),e.maxHeight/(maxY-minY));e.actual_ink_bounds={width:s*(maxX-minX),height:s*(maxY-minY)};e.font_size_px=s*font.units_per_em;
 return `<g fill="${e.fill}" transform="translate(${e.cx-s*(minX+maxX)/2} ${e.cy+s*(minY+maxY)/2}) scale(${s} ${-s})">${children.join('')}</g>`;
}
const wrap=body=>`<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}">${body}</svg>`;
(async()=>{
 if(sha(source)!==expected)throw new Error('Approved source identity mismatch');
 const original=await sharp(source).ensureAlpha().raw().toBuffer();const archived=await sharp(path.join(root,'source/b2-v4-estimated-base.png')).ensureAlpha().raw().toBuffer();
 const oldSvg=fs.readFileSync(path.join(root,'source/b2-v4-real-text-layer.svg'),'utf8');const groups=oldSvg.match(/<g\b[\s\S]*?<\/g>/g);if(groups.length!==5)throw new Error('Unexpected source layer structure');
 const recomposed=await sharp(path.join(root,'source/b2-v4-estimated-base.png')).composite([{input:Buffer.from(oldSvg)}]).ensureAlpha().raw().toBuffer();let recDiff=0;
 for(let i=0;i<w*h;i++){const k=i*4;if([0,1,2,3].some(c=>original[k+c]!==recomposed[k+c]))recDiff++;}if(recDiff)throw new Error('Archived layers fail approved baseline recomposition');
 const oldLocal=await sharp(Buffer.from(wrap(groups.slice(2).join('')))).ensureAlpha().raw().toBuffer();const base=Buffer.from(original),oldMask=Buffer.alloc(w*h),allowed=Buffer.alloc(w*h);
 for(let i=0;i<w*h;i++){const k=i*4;if(oldLocal[k+3]){oldMask[i]=255;for(let c=0;c<4;c++)base[k+c]=archived[k+c];}}
 await sharp(base,{raw:{width:w,height:h,channels:4}}).png().toFile(path.join(root,'background-layers/b3-fixed-local-base.png'));
 await sharp(oldMask,{raw:{width:w,height:h,channels:1}}).png().toFile(path.join(root,'evidence/old-text-mask.png'));
 const newGroups=entries.map(realText),newSvg=wrap(newGroups.join(''));fs.writeFileSync(path.join(root,'layers/b3-real-text-layer.svg'),newSvg);await sharp(Buffer.from(newSvg)).ensureAlpha().png().toFile(path.join(root,'layers/b3-real-text-layer.png'));
 for(let i=0;i<entries.length;i++){const s=wrap(newGroups[i]);fs.writeFileSync(path.join(root,'layers/'+entries[i].id+'.svg'),s);await sharp(Buffer.from(s)).ensureAlpha().png().toFile(path.join(root,'layers/'+entries[i].id+'.png'));}
 const text=await sharp(path.join(root,'layers/b3-real-text-layer.png')).ensureAlpha().raw().toBuffer();const out=Buffer.from(base);
 for(let i=0;i<w*h;i++){const k=i*4,a=text[k+3]/255;if(oldMask[i]||a)allowed[i]=255;if(a){for(let c=0;c<3;c++)out[k+c]=Math.round(base[k+c]*(1-a)+text[k+c]*a);out[k+3]=255;}}
 const output=path.join(root,'preview/lezi-bluetooth-B3-v1.png');await sharp(out,{raw:{width:w,height:h,channels:4}}).png().toFile(output);await sharp(allowed,{raw:{width:w,height:h,channels:1}}).png().toFile(path.join(root,'evidence/allowed-mask.png'));
 const regions=[{id:'waiting_and_device',x:193,y:477,width:468,height:118},{id:'cancel_waiting',x:204,y:730,width:450,height:132}];fs.writeFileSync(path.join(root,'evidence/regions.json'),JSON.stringify({regions},null,2)+'\n');
 const evidence={schema:'lezi.bluetooth_waiting_static_candidate.v1',version:'B3-v1',item_id:'UI002-BLUETOOTH-B3',depicted_state:'Host listening before first connection; waiting for a paired guest to join',source_version:'B2-v4',source_sha256:sha(source),output_sha256:sha(output),width:w,height:h,regions,lines:entries,font_family:font.family,font_sha256:font.font_sha256,font_modified:false,source_unchanged:sha(source)===expected,baseline_recomposition_pixel_differences:recDiff,new_background_estimation:false,background_provenance:'Reuses archived approved B2-v4 base solely under old text alpha; original hidden pixels were historically estimated. No repeated erase/inpaint/smoothing or whole-page regeneration.',protected_parts:['paper and landscape','back arrow','eyebrow and title','original blue ink frame','original footer pairing/autonavigation explanation'],device_name:'我的手机 is example fixture, not actual device name',interaction_spec:{cancel:'Cancel host waiting and return to B1 initial lobby',back:'Leave this waiting state and return through existing lobby flow; no forfeiture before first connection',connection_success:'Brief success then automatic hero selection; no ready button',countdown:'No hero timer before initial connection'},artwork_approval:'pending',runtime_acceptance:'not_run',bluetooth_device_acceptance:'not_run',product_code_changed:false,whole_page_regenerated:false};fs.writeFileSync(path.join(root,'evidence/revision.json'),JSON.stringify(evidence,null,2)+'\n');console.log(JSON.stringify({version:evidence.version,source_unchanged:evidence.source_unchanged,baseline_recomposition_pixel_differences:recDiff,output}));
})();
