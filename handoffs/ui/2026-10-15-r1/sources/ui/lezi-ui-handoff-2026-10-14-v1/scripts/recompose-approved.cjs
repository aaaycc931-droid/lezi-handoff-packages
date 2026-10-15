// Read-only layer identity check; writes a JSON report, never overwrites artwork.
const fs=require('fs'),path=require('path'),crypto=require('crypto');
const sharp=process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES?require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/sharp'):require('sharp');
const root=path.resolve(__dirname,'..'),index=JSON.parse(fs.readFileSync(path.join(root,'layers/COMPOSITION_INDEX.json')));
async function raw(file){return await sharp(path.join(root,file)).ensureAlpha().raw().toBuffer({resolveWithObject:true});}
function blend(base,layer){const out=Buffer.from(base);for(let i=0;i<base.length;i+=4){const a=layer[i+3]/255;if(a){for(let c=0;c<3;c++)out[i+c]=Math.round(base[i+c]*(1-a)+layer[i+c]*a);out[i+3]=255;}}return out;}
(async()=>{
 const results=[];
 for(const item of index.entries){const bg=await raw(item.background),reference=await raw(item.approved_image);let out=Buffer.from(bg.data);
  if(item.kind==='sharp_svg')out=await sharp(path.join(root,item.background)).composite([{input:path.join(root,item.svg)}]).ensureAlpha().raw().toBuffer();
  else if(item.kind==='manual_layers')for(const file of item.layers){const layer=await raw(file);if(layer.data.length!==out.length)throw new Error('Layer size mismatch '+file);out=blend(out,layer.data);}
  else if(item.kind==='manual_patches')for(const patch of item.patches){const layer=await raw(patch.file);if(layer.info.width!==patch.width||layer.info.height!==patch.height)throw new Error('Patch size mismatch');for(let y=0;y<patch.height;y++)for(let x=0;x<patch.width;x++){const s=(y*patch.width+x)*4,k=((patch.y+y)*bg.info.width+patch.x+x)*4,a=layer.data[s+3]/255;if(a)for(let c=0;c<3;c++)out[k+c]=Math.round(out[k+c]*(1-a)+layer.data[s+c]*a);}}
  else throw new Error('Unknown composition type');
  if(reference.data.length!==out.length)throw new Error('Reference size mismatch');let changed=0;for(let i=0;i<out.length;i+=4)if([0,1,2,3].some(c=>out[i+c]!==reference.data[i+c]))changed++;
  results.push({version:item.version,width:bg.info.width,height:bg.info.height,decoded_rgba_changed_pixels:changed,passed:changed===0});
 }
 const report={schema:'lezi.approved_source_recomposition_check.v1',performed_at:new Date().toISOString(),conditions:'Current sharp decode; 8-bit RGBA; sources only, no resampling or background reconstruction',results,all_passed:results.every(x=>x.passed),not_runtime_or_aesthetic_acceptance:true};
 fs.mkdirSync(path.join(root,'verification'),{recursive:true});fs.writeFileSync(path.join(root,'verification/RECOMPOSITION.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report));if(!report.all_passed)process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1;});
