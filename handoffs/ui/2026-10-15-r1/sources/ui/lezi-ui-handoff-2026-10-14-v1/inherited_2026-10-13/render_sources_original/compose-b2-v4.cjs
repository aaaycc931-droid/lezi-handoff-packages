const sharp=require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/sharp');
const fs=require('node:fs'),crypto=require('node:crypto');
const root='/workspace/scratch/100914f15bb1';
const source=root+'/handoff/ui-return/images/lezi-bluetooth-B2-v1.png',output=root+'/lezi-bluetooth-B2-v4.png';
const sha=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const expected='e501e1c965fe37a54176f912c2d3641a55206e9105ff40d9b47aa24f805fc112';
const data=JSON.parse(fs.readFileSync(root+'/b2-v4-real-glyphs.json','utf8'));
const regions=[{id:'eyebrow',x:290,y:207,width:271,height:75},
 {id:'title',x:202,y:278,width:448,height:164},
 {id:'status',x:193,y:477,width:468,height:118},
 {id:'primary_label',x:204,y:730,width:450,height:132}];
const lines=[
 {id:'eyebrow',text:'面对面对局',cx:426,cy:248,maxWidth:227,maxHeight:48,fill:'#12120f'},
 {id:'title',text:'蓝牙对局',cx:426,cy:360,maxWidth:405,maxHeight:139,fill:'#10110e'},
 {id:'status_1',text:'蓝牙当前处于关闭状态，',cx:426,cy:514,maxWidth:447,maxHeight:44,fill:'#12120f'},
 {id:'status_2',text:'请先开启蓝牙。',cx:426,cy:569,maxWidth:286,maxHeight:44,fill:'#12120f'},
 {id:'primary_label',text:'开启蓝牙',cx:426,cy:793,maxWidth:365,maxHeight:108,fill:'#123754'}
];
function realText(line){
 let advance=0,minX=Infinity,minY=Infinity,maxX=-Infinity,maxY=-Infinity;
 const children=[];
 for(const char of line.text){
  const g=data.glyphs[char];if(!g)throw new Error('Missing real glyph '+char);
  const [x0,y0,x1,y1]=g.bounds;
  minX=Math.min(minX,advance+x0);maxX=Math.max(maxX,advance+x1);
  minY=Math.min(minY,y0);maxY=Math.max(maxY,y1);
  children.push(`<path transform="translate(${advance} 0)" d="${g.path}"/>`);
  advance+=g.advance;
 }
 const s=Math.min(line.maxWidth/(maxX-minX),line.maxHeight/(maxY-minY));
 line.actualInkBounds={width:(maxX-minX)*s,height:(maxY-minY)*s};
 line.font_size_px=s*data.units_per_em;
 return `<g fill="${line.fill}" transform="translate(${line.cx-s*(minX+maxX)/2} ${line.cy+s*(minY+maxY)/2}) scale(${s} ${-s})">${children.join('')}</g>`;
}
function restoreInkFootprints(buf,w,r){
 const rw=r.width,rh=r.height,n=rw*rh;
 const mask=new Uint8Array(n);
 const offset=i=>((r.y+Math.floor(i/rw))*w+r.x+i%rw)*3;
 for(let i=0;i<n;i++){
  const k=offset(i),lum=.2126*buf[k]+.7152*buf[k+1]+.0722*buf[k+2];
  if(lum<150){
   const px=i%rw,py=Math.floor(i/rw);
   for(let dy=-3;dy<=3;dy++)for(let dx=-3;dx<=3;dx++){
    const x=px+dx,y=py+dy;
    if(x>=0&&y>=0&&x<rw&&y<rh)mask[y*rw+x]=1;
   }
  }
 }
 // Estimate only background hidden by removed glyphs. Retain all known pixels.
 const values=new Float64Array(n*3),seen=new Uint8Array(n),queue=new Int32Array(n);
 let head=0,tail=0;
 for(let i=0;i<n;i++){
  const k=offset(i);for(let c=0;c<3;c++)values[i*3+c]=buf[k+c];
  if(!mask[i]){queue[tail++]=i;seen[i]=1;}
 }
 const neighbors=i=>{
  const ns=[],x=i%rw,y=Math.floor(i/rw);
  if(x>0)ns.push(i-1);if(x<rw-1)ns.push(i+1);
  if(y>0)ns.push(i-rw);if(y<rh-1)ns.push(i+rw);return ns;
 };
 while(head<tail){
  const i=queue[head++];for(const j of neighbors(i))if(!seen[j]){
   seen[j]=1;queue[tail++]=j;
   for(let c=0;c<3;c++)values[j*3+c]=values[i*3+c];
  }
 }
 const masked=[];for(let i=0;i<n;i++)if(mask[i])masked.push([i,neighbors(i)]);
 for(let pass=0;pass<350;pass++)for(const [i,ns] of masked){
  for(let c=0;c<3;c++){
   let sum=0;for(const j of ns)sum+=values[j*3+c];values[i*3+c]=sum/ns.length;
  }
 }
 for(const [i] of masked){const k=offset(i);for(let c=0;c<3;c++)buf[k+c]=Math.round(values[i*3+c]);}
 return masked.length;
}
(async()=>{
 if(sha(source)!==expected)throw new Error('Candidate source differs');
 const a=await sharp(source).removeAlpha().raw().toBuffer({resolveWithObject:true});
 const {width:w,height:h}=a.info,restored=Buffer.from(a.data);
 const restoreCounts=regions.map(r=>({id:r.id,estimatedHiddenBackgroundPixels:restoreInkFootprints(restored,w,r)}));
 const svg=`<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}">${lines.map(realText).join('')}</svg>`;
 fs.writeFileSync(root+'/b2-v4-real-text-layer.svg',svg);
 await sharp(restored,{raw:{width:w,height:h,channels:3}}).composite([{input:Buffer.from(svg)}]).png().toFile(output);
 const result=await sharp(output).removeAlpha().raw().toBuffer();
 let changed=0,outside=0;
 for(let y=0;y<h;y++)for(let x=0;x<w;x++){
  const k=(y*w+x)*3;if(a.data[k]===result[k]&&a.data[k+1]===result[k+1]&&a.data[k+2]===result[k+2])continue;
  changed++;if(!regions.some(r=>x>=r.x&&y>=r.y&&x<r.x+r.width&&y<r.y+r.height))outside++;
 }
 if(outside)throw new Error('Pixels changed outside allowed text regions: '+outside);
 if(sha(source)!==expected)throw new Error('Input was altered');
 const evidence={version:'B2-v4',source_version:'B2-v1',source_sha256:sha(source),output_sha256:sha(output),width:w,height:h,regions,lines,changed_pixels:changed,changed_pixels_outside_text_regions:outside,source_unchanged:true,restoreCounts,font_family:data.family,font_face_index:data.face_index,font_file_sha256:data.font_sha256,glyph_source:'Original font outlines; no generative glyphs, synthetic weight, stretched glyphs, or added stroke ornament.',hidden_background_note:'Pixels hidden by prior text estimated locally only within old glyph footprints; visible background outside four text regions is unchanged.',artwork_approval:'pending',runtime_acceptance:'not_run',font_file_modified:false};
 fs.writeFileSync(root+'/b2-v4-font-pixel-check.json',JSON.stringify(evidence,null,2)+'\n');
 console.log(JSON.stringify(evidence));
})().catch(e=>{console.error(e);process.exitCode=1;});
