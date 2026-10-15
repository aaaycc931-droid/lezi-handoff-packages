const sharp=require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/sharp');
const fs=require('node:fs'),crypto=require('node:crypto');
const base='/workspace/scratch/384cae71d8cb/lezi-bluetooth-B1-v1.png';
const edit='/workspace/scratch/384cae71d8cb/generated_images/exec-d97b3cc8-38cd-48c3-97d5-d7ba09f0443b.png';
const output='/workspace/scratch/384cae71d8cb/lezi-bluetooth-B2-v1.png';
const digest=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
(async()=>{
 if(digest(base)!=='bce5413e4a0c484457124e642ce815a1494f09ba1109d6096c2a0fa499b91806')throw new Error('Approved B1 changed');
 const a=await sharp(base).removeAlpha().raw().toBuffer({resolveWithObject:true});
 const b=await sharp(edit).removeAlpha().raw().toBuffer({resolveWithObject:true});
 if(a.info.width!==b.info.width||a.info.height!==b.info.height)throw new Error('Editor dimensions differ');
 const {width:w,height:h}=a.info,result=Buffer.from(a.data);
 const regions=[{id:'status_text',x:140,y:470,width:625,height:118},
 {id:'primary_action_text',x:201,y:733,width:454,height:124},
 {id:'remove_join_action',x:69,y:957,width:717,height:283}];
 const lum=(buf,k)=>.2126*buf[k]+.7152*buf[k+1]+.0722*buf[k+2];
 let foregroundPixels=0;
 for(const r of regions){
  const mask=new Uint8Array(r.width*r.height);
  for(let j=0;j<r.height;j++)for(let i=0;i<r.width;i++){
   const k=((r.y+j)*w+r.x+i)*3;let ink=false;
   if(r.id==='remove_join_action'){
    const R=a.data[k],G=a.data[k+1],B=a.data[k+2];
    ink=R-G>12&&R-B>16&&G<222;
   }else ink=lum(a.data,k)<195||lum(b.data,k)<195;
   if(ink)mask[j*r.width+i]=1;
  }
  const expanded=new Uint8Array(mask);
  for(let j=0;j<r.height;j++)for(let i=0;i<r.width;i++){
   if(!mask[j*r.width+i])continue;
   for(let dy=-2;dy<=2;dy++)for(let dx=-2;dx<=2;dx++){
    const x=i+dx,y=j+dy;if(x>=0&&y>=0&&x<r.width&&y<r.height)expanded[y*r.width+x]=1;
   }
  }
  for(let j=0;j<r.height;j++)for(let i=0;i<r.width;i++){
   if(!expanded[j*r.width+i])continue;
   const k=((r.y+j)*w+r.x+i)*3;
   for(let c=0;c<3;c++)result[k+c]=b.data[k+c];
   foregroundPixels++;
  }
 }
 await sharp(result,{raw:{width:w,height:h,channels:3}}).png().toFile(output);
 const check=await sharp(output).removeAlpha().raw().toBuffer();
 let changed=0,outside=0;
 for(let y=0;y<h;y++)for(let x=0;x<w;x++){
  const k=(y*w+x)*3;if(a.data[k]===check[k]&&a.data[k+1]===check[k+1]&&a.data[k+2]===check[k+2])continue;
  changed++;if(!regions.some(r=>x>=r.x&&y>=r.y&&x<r.x+r.width&&y<r.y+r.height))outside++;
 }
 if(outside)throw new Error('Unexpected changes outside the state-content areas');
 if(digest(base)!=='bce5413e4a0c484457124e642ce815a1494f09ba1109d6096c2a0fa499b91806')throw new Error('B1 original altered');
 const receipt={version:'B2-v1',depicted_state:'Bluetooth disabled',source_approved_version:'B1-v1',source_sha256:digest(base),output_sha256:digest(output),width:w,height:h,regions,foregroundPixels,changedPixels:changed,changedPixelsOutsideStateRegions:outside,approved_source_unchanged:true,protected:'Title, eyebrow, back arrow, blue frame, footer help/landscape, and all pixels outside three state-content regions',design_approval:'pending',runtime_acceptance:'not_run'};
 fs.writeFileSync('/workspace/scratch/384cae71d8cb/b2-v1-pixel-check.json',JSON.stringify(receipt,null,2)+'\n');
 console.log(JSON.stringify(receipt));
})().catch(e=>{console.error(e);process.exitCode=1;});
