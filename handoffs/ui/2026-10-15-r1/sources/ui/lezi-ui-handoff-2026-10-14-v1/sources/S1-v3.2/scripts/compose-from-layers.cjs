const fs=require('node:fs'),path=require('node:path');
const sharp=require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/sharp');
(async()=>{
 const root=path.resolve(__dirname,'..'),p=JSON.parse(fs.readFileSync(path.join(root,'evidence/edit-parameters.json'),'utf8'));
 const {data,info}=await sharp(path.join(root,p.background_layer)).ensureAlpha().raw().toBuffer({resolveWithObject:true});const out=Buffer.from(data);
 for(const c of p.controls){const ink=await sharp(path.join(root,c.scaled_layer)).ensureAlpha().raw().toBuffer();
  for(let y=0;y<c.height;y++)for(let x=0;x<c.width;x++){const s=(y*c.width+x)*4,k=((c.y+y)*info.width+c.x+x)*4,a=ink[s+3]/255;if(a)for(let ch=0;ch<3;ch++)out[k+ch]=Math.round(out[k+ch]*(1-a)+ink[s+ch]*a);}
 }
 const current=await sharp(path.join(root,p.current_candidate)).ensureAlpha().raw().toBuffer();if(!out.equals(current))throw new Error('Recomposition differs');
 const d=path.join(root,'rerenders');fs.mkdirSync(d,{recursive:true});await sharp(out,{raw:{width:info.width,height:info.height,channels:4}}).png().toFile(path.join(d,'lezi-settings-S1-v3_2.png'));console.log(JSON.stringify({pixel_equal:true}));
})().catch(e=>{console.error(e);process.exitCode=1;});

