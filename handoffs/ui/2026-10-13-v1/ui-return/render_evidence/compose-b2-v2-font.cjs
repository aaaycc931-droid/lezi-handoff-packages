const sharp=require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/sharp');
const fs=require('node:fs'),crypto=require('node:crypto');
const source='/workspace/scratch/384cae71d8cb/lezi-bluetooth-B2-v1.png';
const edit='/workspace/scratch/384cae71d8cb/generated_images/exec-ab2329ba-5dfb-4e50-afbe-2ef16ca4af6f.png';
const output='/workspace/scratch/384cae71d8cb/lezi-bluetooth-B2-v2.png';
const sha=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
(async()=>{
 if(sha(source)!=='e501e1c965fe37a54176f912c2d3641a55206e9105ff40d9b47aa24f805fc112')throw new Error('Source B2-v1 changed');
 const a=await sharp(source).removeAlpha().raw().toBuffer({resolveWithObject:true});
 const b=await sharp(edit).removeAlpha().raw().toBuffer({resolveWithObject:true});
 const {width:w,height:h}=a.info;
 if(w!==b.info.width||h!==b.info.height)throw new Error('Output dimensions differ');
 const result=Buffer.from(a.data);
 const regions=[{id:'eyebrow',x:290,y:207,width:271,height:75},
 {id:'title',x:202,y:278,width:448,height:164},
 {id:'status',x:193,y:477,width:468,height:118},
 {id:'primary_label',x:204,y:730,width:450,height:132}];
 const lum=(buf,k)=>.2126*buf[k]+.7152*buf[k+1]+.0722*buf[k+2];
 for(const r of regions){
  const mask=new Uint8Array(r.width*r.height);
  for(let j=0;j<r.height;j++)for(let i=0;i<r.width;i++){
   const k=((r.y+j)*w+r.x+i)*3;
   if(lum(a.data,k)<150||lum(b.data,k)<150)mask[j*r.width+i]=1;
  }
  const expanded=new Uint8Array(mask);
  for(let j=0;j<r.height;j++)for(let i=0;i<r.width;i++){
   if(!mask[j*r.width+i])continue;
   for(let dy=-2;dy<=2;dy++)for(let dx=-2;dx<=2;dx++){
    const x=i+dx,y=j+dy;
    if(x>=0&&y>=0&&x<r.width&&y<r.height)expanded[y*r.width+x]=1;
   }
  }
  for(let j=0;j<r.height;j++)for(let i=0;i<r.width;i++){
   if(!expanded[j*r.width+i])continue;
   const k=((r.y+j)*w+r.x+i)*3;
   for(let c=0;c<3;c++)result[k+c]=b.data[k+c];
  }
 }
 await sharp(result,{raw:{width:w,height:h,channels:3}}).png().toFile(output);
 const check=await sharp(output).removeAlpha().raw().toBuffer();
 let changed=0,outside=0;
 for(let y=0;y<h;y++)for(let x=0;x<w;x++){
  const k=(y*w+x)*3;if(a.data[k]===check[k]&&a.data[k+1]===check[k+1]&&a.data[k+2]===check[k+2])continue;
  changed++;if(!regions.some(r=>x>=r.x&&y>=r.y&&x<r.x+r.width&&y<r.y+r.height))outside++;
 }
 if(outside)throw new Error('Unexpected changes outside text regions');
 if(sha(source)!=='e501e1c965fe37a54176f912c2d3641a55206e9105ff40d9b47aa24f805fc112')throw new Error('Source altered');
 const record={version:'B2-v2',source_version:'B2-v1',source_sha256:sha(source),output_sha256:sha(output),width:w,height:h,regions,changedPixels:changed,changedPixelsOutsideTextRegions:outside,source_unchanged:true,layout_state_approval:'B2-v1 user-approved with typography feedback',new_font_appearance_approval:'pending',runtime_acceptance:'not_run',font_source_acceptance:'not_finalized'};
 fs.writeFileSync('/workspace/scratch/384cae71d8cb/b2-v2-font-pixel-check.json',JSON.stringify(record,null,2)+'\n');
 console.log(JSON.stringify(record));
})().catch(e=>{console.error(e);process.exitCode=1;});
