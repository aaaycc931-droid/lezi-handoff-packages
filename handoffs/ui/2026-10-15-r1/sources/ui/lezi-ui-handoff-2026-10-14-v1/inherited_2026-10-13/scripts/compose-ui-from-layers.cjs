// Recompose from archived base and text layers; never overwrite supplied review images.
const fs = require('node:fs');
const path = require('node:path');
const sharp = require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES ? process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/sharp' : 'sharp');
const root = path.resolve(process.argv[2] || path.join(__dirname, '..'));
(async () => {
  const config = JSON.parse(fs.readFileSync(path.join(root, 'layers/COMPOSITION_INDEX.json'), 'utf8'));
  fs.mkdirSync(path.join(root, 'rerenders'), {recursive:true});
  for (const item of config.items) {
    const output = path.join(root, 'rerenders', item.file_name);
    const bytes = await sharp(path.join(root, item.background_layer))
      .composite([{input:path.join(root,item.text_layer)}]).png().toBuffer();
    await sharp(bytes).raw().toBuffer();
    const temporary = output + '.writing';
    fs.writeFileSync(temporary, bytes);
    fs.renameSync(temporary, output);
    console.log(output);
  }
})().catch(error => {console.error(error);process.exitCode=1;});
