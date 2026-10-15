// Preserve the archived base and extracted original controls. State does not change outer size.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const sharp=require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/sharp');
const root=path.resolve(__dirname,'..'), prior=path.resolve(root,'../s1-v3_1-source');
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const expected='ebba7e68642fb9fb7c7e59b1b8891830f61749bcbe8faaa990e62a8a22a8365c';
const lum=(a,k)=>.2126*a[k]+.7152*a[k+1]+.0722*a[k+2];
const w=61,h=61,n=w*h,target=28,threshold=160;
function lanczos(t){t=Math.abs(t);if(t<1e-10)return 1;if(t>=3)return 0;return Math.sin(Math.PI*t)*Math.sin(Math.PI*t/3)/(Math.PI*Math.PI*t*t/3);}
function resample(ink,scale){
 const out=Buffer.alloc(n*4),support=3/scale;
 for(let y=0;y<h;y++)for(let x=0;x<w;x++){
  const sx=30+(x-30)/scale,sy=30+(y-30)/scale;let weightSum=0,alpha=0;const color=[0,0,0];
  for(let yy=Math.ceil(sy-support);yy<=Math.floor(sy+support);yy++)for(let xx=Math.ceil(sx-support);xx<=Math.floor(sx+support);xx++){
   const wt=lanczos((yy-sy)*scale)*lanczos((xx-sx)*scale);weightSum+=wt;
   if(xx<0||yy<0||xx>=w||yy>=h)continue;
   const k=(yy*w+xx)*4,a=ink[k+3]/255;alpha+=wt*a;for(let c=0;c<3;c++)color[c]+=wt*a*ink[k+c];
  }
  const k=(y*w+x)*4;out[k+3]=Math.round(Math.max(0,Math.min(1,alpha/weightSum))*255);
  if(out[k+3])for(let c=0;c<3;c++)out[k+c]=Math.max(0,Math.min(255,Math.round(color[c]/alpha)));
 }
 return out;
}
function paintOn(base,ink,c,W){
 for(let y=0;y<h;y++)for(let x=0;x<w;x++){
  const s=(y*w+x)*4,k=((c.y+y)*W+c.x+x)*4,a=ink[s+3]/255;
  if(a)for(let ch=0;ch<3;ch++)base[k+ch]=Math.round(base[k+ch]*(1-a)+ink[s+ch]*a);
 }
}
function measure(full,c,W){
 let ax=999,ay=999,bx=-1,by=-1;
 for(let y=0;y<h;y++)for(let x=0;x<w;x++){const k=((c.y+y)*W+c.x+x)*4;if(lum(full,k)<threshold){ax=Math.min(ax,x);ay=Math.min(ay,y);bx=Math.max(bx,x);by=Math.max(by,y);}}
 return {width:bx-ax+1,height:by-ay+1,outer_diameter_px:Math.max(bx-ax+1,by-ay+1)};
}
(async()=>{
 for(const d of ['source','layers','background-layers','preview','evidence'])fs.mkdirSync(path.join(root,d),{recursive:true});
 const sourcePath=path.join(root,'source/lezi-settings-S1-v3_1.png'),sourceBytes=fs.readFileSync(sourcePath);
 if(hash(sourceBytes)!==expected)throw new Error('Baseline digest mismatch');
 const {data:source,info}=await sharp(sourceBytes).ensureAlpha().raw().toBuffer({resolveWithObject:true});
 const original=await sharp(path.join(prior,'source/lezi-settings-S1-v3.png')).ensureAlpha().raw().toBuffer();
 const base=await sharp(path.join(prior,'background-layers/s1-v3-enabled-controls-removed-estimated.png')).ensureAlpha().raw().toBuffer();
 const params=JSON.parse(fs.readFileSync(path.join(prior,'evidence/edit-parameters.json'),'utf8'));
 const controls=params.controls.map(c=>({...c,state:'on',old_scale:0.85,scale:0.85}));
 const allowed=Buffer.alloc(info.width*info.height);
 const oldAllowed=await sharp(path.join(prior,'evidence/allowed-control-footprints.png')).toColourspace('b-w').raw().toBuffer();
 oldAllowed.copy(allowed);
 for(const c of controls)fs.copyFileSync(path.join(prior,c.source_layer),path.join(root,c.source_layer));
 for(const c of [{id:'regular_reduce_off_ink',cx:355,cy:485},{id:'short_reduce_off_ink',cx:733,cy:461}]){
  c.x=c.cx-30;c.y=c.cy-30;c.width=w;c.height=h;c.state='off';
  const roi=Buffer.alloc(n*4),mask=new Uint8Array(n),queue=[];
  for(let y=0;y<h;y++)for(let x=0;x<w;x++){const k=((c.y+y)*info.width+c.x+x)*4,p=(y*w+x)*4;original.copy(roi,p,k,k+4);}
  // Isolated hollow-circle ROI; seed dense original brush pixels, not the empty center.
  for(let y=6;y<h-6;y++)for(let x=6;x<w-6;x++){const p=y*w+x;if(lum(roi,p*4)<130){mask[p]=1;queue.push(p);}}
  if(queue.length<40)throw new Error('Hollow-control ink unavailable');
  for(let at=0;at<queue.length;at++){const p=queue[at],x=p%w,y=Math.floor(p/w);
   for(let dy=-1;dy<=1;dy++)for(let dx=-1;dx<=1;dx++){const xx=x+dx,yy=y+dy;if(xx<0||yy<0||xx>=w||yy>=h)continue;const q=yy*w+xx;if(!mask[q]&&lum(roi,q*4)<205){mask[q]=1;queue.push(q);}}
  }
  const erase=new Uint8Array(mask);
  for(let y=1;y<h-1;y++)for(let x=1;x<w-1;x++)if(mask[y*w+x])for(let dy=-1;dy<=1;dy++)for(let dx=-1;dx<=1;dx++)erase[(y+dy)*w+x+dx]=1;
  let minX=99,minY=99,maxX=-1,maxY=-1,pixelCount=0;
  for(let y=0;y<h;y++)for(let x=0;x<w;x++)if(erase[y*w+x]){minX=Math.min(minX,x);maxX=Math.max(maxX,x);minY=Math.min(minY,y);maxY=Math.max(maxY,y);pixelCount++;}
  if(minX<5||minY<5||maxX>55||maxY>55)throw new Error('Unexpected hollow footprint');
  const sums=[0,0,0],paper=new Float64Array(n*3);let count=0;
  for(let p=0;p<n;p++)if(!erase[p]){count++;for(let ch=0;ch<3;ch++)sums[ch]+=roi[p*4+ch];}
  for(let p=0;p<n;p++)for(let ch=0;ch<3;ch++)paper[p*3+ch]=erase[p]?sums[ch]/count:roi[p*4+ch];
  for(let pass=0;pass<1400;pass++)for(let y=1;y<h-1;y++)for(let x=1;x<w-1;x++){const p=y*w+x;if(!erase[p])continue;for(let ch=0;ch<3;ch++)paper[p*3+ch]=(paper[(p-1)*3+ch]+paper[(p+1)*3+ch]+paper[(p-w)*3+ch]+paper[(p+w)*3+ch])/4;}
  const ink=Buffer.alloc(n*4);
  for(let y=0;y<h;y++)for(let x=0;x<w;x++){
   const p=y*w+x,k=((c.y+y)*info.width+c.x+x)*4;
   if(!erase[p])continue;
   for(let ch=0;ch<3;ch++){base[k+ch]=Math.round(paper[p*3+ch]);ink[p*4+ch]=roi[p*4+ch];}
   ink[p*4+3]=255;allowed[(c.y+y)*info.width+c.x+x]=255;
  }
  c.source_layer='layers/'+c.id+'-original.png';c.scale=.82;c.old_scale=1;
  c.hidden_background_estimated=true;c.estimated_pixel_count=pixelCount;
  c.original_ink_footprint_bounds={x:c.x+minX,y:c.y+minY,width:maxX-minX+1,height:maxY-minY+1};
  await sharp(ink,{raw:{width:w,height:h,channels:4}}).png().toFile(path.join(root,c.source_layer));
  controls.push(c);
 }
 const result=Buffer.from(base),regions=[];
 for(const c of controls){
  const ink=await sharp(path.join(root,c.source_layer)).ensureAlpha().raw().toBuffer();
  let selected=null,bestDistance=Infinity;
  // Keep the existing 85% result whenever its visible outer extent already matches.
  // Otherwise use only uniform scaling of the original extracted raster.
  const trials=[c.scale];
  for(let step=1;step<=50;step++)trials.push(c.scale+step*.001,c.scale-step*.001);
  for(const scale of trials){
   const scaled=resample(ink,scale),scratch=Buffer.from(base);paintOn(scratch,scaled,c,info.width);const m=measure(scratch,c,info.width);
   if(m.outer_diameter_px===target && Math.abs(scale-c.scale)<bestDistance){selected={scaled,scale,m};bestDistance=Math.abs(scale-c.scale);break;}
  }
  if(!selected)throw new Error('Unable to match common diameter without stretching');
  c.scale=selected.scale;c.actual_ink_bounds=selected.m;c.scaled_layer='layers/'+c.id+'-matched-outer.png';c.geometric_center_shift=[0,0];
  await sharp(selected.scaled,{raw:{width:w,height:h,channels:4}}).png().toFile(path.join(root,c.scaled_layer));
  paintOn(result,selected.scaled,c,info.width);
  const b=c.original_ink_footprint_bounds;regions.push({id:c.id,x:b.x-2,y:b.y-2,width:b.width+4,height:b.height+4});
  for(let y=0;y<h;y++)for(let x=0;x<w;x++){
   const k=(y*w+x)*4;if(!selected.scaled[k+3])continue;
   const gx=c.x+x,gy=c.y+y;if(gx<b.x-2||gy<b.y-2||gx>=b.x+b.width+2||gy>=b.y+b.height+2)throw new Error('Ink outside allowed fringe');
   allowed[gy*info.width+gx]=255;
  }
 }
 // Validate original extraction plus the immutable prior base reconstruct S1-v3.
 const restored=Buffer.from(base);
 for(const c of controls){const ink=await sharp(path.join(root,c.source_layer)).ensureAlpha().raw().toBuffer();paintOn(restored,ink,c,info.width);}
 if(!restored.equals(original))throw new Error('Original layers fail exact reconstruction');
 let changed=0,outside=0;
 for(let p=0;p<info.width*info.height;p++){const k=p*4;if(source[k]===result[k]&&source[k+1]===result[k+1]&&source[k+2]===result[k+2]&&source[k+3]===result[k+3])continue;changed++;if(!allowed[p])outside++;}
 if(outside)throw new Error('Protected pixels changed');
 const output=path.join(root,'preview/lezi-settings-S1-v3_2.png');
 await sharp(result,{raw:{width:info.width,height:info.height,channels:4}}).png().toFile(output);
 await sharp(base,{raw:{width:info.width,height:info.height,channels:4}}).png().toFile(path.join(root,'background-layers/s1-v3-all-controls-removed-estimated.png'));
 await sharp(allowed,{raw:{width:info.width,height:info.height,channels:1}}).toColourspace('b-w').png().toFile(path.join(root,'evidence/allowed-control-footprints.png'));
 const evidence={schema:'lezi.toggle_same_outer_size.v1',version:'S1-v3.2',source_version:'S1-v3.1',source_sha256:expected,output_sha256:hash(fs.readFileSync(output)),width:info.width,height:info.height,
 user_statement:'开启与关闭图案墨圈保持同样大小，因为机制是墨圈填满，所以空白墨圈跟全黑墨圈保持同样外圈大小',
 intent:'Keep the reduced size from the preceding request; ON and OFF have a shared outer diameter, only interior ink fill changes in the intended mechanism',
 common_visible_outer_diameter_px:target,measurement_luminance_threshold:threshold,scale_method:'original raster, uniform geometric scaling; no stretching or redrawing',
 all_six_outer_diameters_equal:true,controls,regions,changed_pixels:changed,changed_pixels_outside_authorized_mask:outside,source_unchanged:hash(fs.readFileSync(sourcePath))===expected,
 source_layers_reconstruct_original_exactly:true,header_unchanged:true,text_unchanged:true,background_layer:'background-layers/s1-v3-all-controls-removed-estimated.png',
 background_restoration:'The archived ON-state base is reused unchanged. OFF-state stroke-hidden paper is locally estimated once; paper visible in the hollow center is preserved unless the resized ring covers it.',
 allowed_mask:'evidence/allowed-control-footprints.png',current_candidate:'preview/lezi-settings-S1-v3_2.png',approval:'pending_user_review',runtime_acceptance:'not_run'};
 fs.writeFileSync(path.join(root,'evidence/edit-parameters.json'),JSON.stringify(evidence,null,2)+'\n');console.log(JSON.stringify(evidence));
})().catch(e=>{console.error(e);process.exitCode=1;});

