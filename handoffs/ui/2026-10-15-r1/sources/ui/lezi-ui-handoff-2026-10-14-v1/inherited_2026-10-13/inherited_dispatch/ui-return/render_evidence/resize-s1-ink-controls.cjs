// Local raster refinement requested by the user. No image generation.
// Keep the complete source raster, alter only six original ink-control boxes.
const sharp=require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/sharp');
const fs=require('node:fs');
const crypto=require('node:crypto');
const source='/workspace/scratch/384cae71d8cb/generated_images/exec-90c9922e-b8a1-4929-a41e-ad02be041c2c.png';
const output='/workspace/scratch/384cae71d8cb/lezi-settings-S1-v2_1.png';
const digest=b=>crypto.createHash('sha256').update(b).digest('hex');
const luminance=(a,k)=>.2126*a[k]+.7152*a[k+1]+.0722*a[k+2];
(async()=>{
 const originalFile=fs.readFileSync(source);
 if(digest(originalFile)!=='c3044d21ff6c8c9b7a5a0915ed81b4a23c7d870da6c7090d39fa72982bbaf644')throw new Error('Unexpected input revision');
 const {data,info}=await sharp(source).removeAlpha().raw().toBuffer({resolveWithObject:true});
 const result=Buffer.from(data),boxes=[];
 const centers=[[355,345],[355,415],[355,485],[733,322],[733,391],[733,461]];
 for(const[cx,cy]of centers){
  let minX=Infinity,minY=Infinity,maxX=-Infinity,maxY=-Infinity;
  for(let y=cy-25;y<=cy+25;y++)for(let x=cx-25;x<=cx+25;x++){
   if(luminance(data,(y*info.width+x)*3)<160){minX=Math.min(minX,x);minY=Math.min(minY,y);maxX=Math.max(maxX,x);maxY=Math.max(maxY,y);}
  }
  const x=minX-3,y=minY-3,w=maxX-minX+7,h=maxY-minY+7;
  const n=w*h,roi=Buffer.alloc(n*3),candidate=new Uint8Array(n),mask=new Uint8Array(n),queue=[];
  for(let j=0;j<h;j++)for(let i=0;i<w;i++){
   const p=j*w+i,k=((y+j)*info.width+x+i)*3;
   data.copy(roi,p*3,k,k+3);
   candidate[p]=luminance(roi,p*3)<205?1:0;
   if(luminance(roi,p*3)<130){mask[p]=1;queue.push(p);}
  }
  // Flood only ink connected to the original control's dense ink.
  for(let at=0;at<queue.length;at++){
   const p=queue[at],px=p%w,py=Math.floor(p/w);
   for(let dy=-1;dy<=1;dy++)for(let dx=-1;dx<=1;dx++){
    const ix=px+dx,iy=py+dy;if(ix<0||iy<0||ix>=w||iy>=h)continue;
    const q=iy*w+ix;if(candidate[q]&&!mask[q]){mask[q]=1;queue.push(q);}
   }
  }
  const erase=new Uint8Array(mask);
  for(let j=1;j<h-1;j++)for(let i=1;i<w-1;i++){
   const p=j*w+i;if(!mask[p])continue;
   for(let dy=-1;dy<=1;dy++)for(let dx=-1;dx<=1;dx++)erase[(j+dy)*w+i+dx]=1;
  }
  // Estimate paper only where the old ink has to be removed. Untouched paper
  // and every pixel outside this original control box retain their source bytes.
  const paper=new Float64Array(n*3);let count=0,sums=[0,0,0];
  for(let p=0;p<n;p++)if(!erase[p]){count++;for(let c=0;c<3;c++)sums[c]+=roi[p*3+c];}
  if(!count)throw new Error('No local paper samples');
  for(let p=0;p<n;p++)for(let c=0;c<3;c++)paper[p*3+c]=erase[p]?sums[c]/count:roi[p*3+c];
  for(let pass=0;pass<800;pass++)for(let j=1;j<h-1;j++)for(let i=1;i<w-1;i++){
   const p=j*w+i;if(!erase[p])continue;
   for(let c=0;c<3;c++)paper[p*3+c]=(paper[(p-1)*3+c]+paper[(p+1)*3+c]+paper[(p-w)*3+c]+paper[(p+w)*3+c])/4;
  }
  const ink=Buffer.alloc(n*4);
  for(let p=0;p<n;p++){
   for(let c=0;c<3;c++)ink[p*4+c]=roi[p*3+c];
   ink[p*4+3]=erase[p]?255:0;
  }
  const nw=Math.round(w*.85),nh=Math.round(h*.85);
  const small=await sharp(ink,{raw:{width:w,height:h,channels:4}}).resize(nw,nh,{kernel:'lanczos3'}).raw().toBuffer();
  const offX=Math.floor((w-nw)/2),offY=Math.floor((h-nh)/2);
  for(let j=0;j<h;j++)for(let i=0;i<w;i++){
   const p=j*w+i,k=((y+j)*info.width+x+i)*3;
   if(erase[p])for(let c=0;c<3;c++)result[k+c]=Math.round(paper[p*3+c]);
  }
  for(let j=0;j<nh;j++)for(let i=0;i<nw;i++){
   const s=(j*nw+i)*4,a=small[s+3]/255;
   if(!a)continue;
   const k=((y+offY+j)*info.width+x+offX+i)*3;
   for(let c=0;c<3;c++)result[k+c]=Math.round(result[k+c]*(1-a)+small[s+c]*a);
  }
  boxes.push({x,y,w,h,scale:.85,raster_size:[nw,nh],center_shift_pixels:[(nw-w)/2+offX,(nh-h)/2+offY]});
 }
 await sharp(result,{raw:{width:info.width,height:info.height,channels:3}}).png().toFile(output);
 const decoded=await sharp(output).removeAlpha().raw().toBuffer();
 let changedPixels=0,outsideChanges=0;
 for(let y=0;y<info.height;y++)for(let x=0;x<info.width;x++){
  const k=(y*info.width+x)*3;
  if(data[k]===decoded[k]&&data[k+1]===decoded[k+1]&&data[k+2]===decoded[k+2])continue;
  changedPixels++;if(!boxes.some(b=>x>=b.x&&y>=b.y&&x<b.x+b.w&&y<b.y+b.h))outsideChanges++;
 }
 if(outsideChanges)throw new Error(`Unexpected outside changes: ${outsideChanges}`);
 if(digest(fs.readFileSync(source))!==digest(originalFile))throw new Error('Input altered');
 const receipt={version:'S1-v2.1',source_sha256:digest(originalFile),output_sha256:digest(fs.readFileSync(output)),source,output,width:info.width,height:info.height,scope:'Only six ink-control bounding boxes',scale:.85,boxes,changedPixels,changedPixelsOutsideControlBoxes:outsideChanges,source_unchanged:true,header_text_unchanged:true,approval:'pending',runtime_acceptance:'not_run'};
 fs.writeFileSync('/workspace/scratch/384cae71d8cb/s1-v2_1-pixel-check.json',JSON.stringify(receipt,null,2)+'\n');
 console.log(JSON.stringify(receipt));
})().catch(e=>{console.error(e);process.exitCode=1;});
