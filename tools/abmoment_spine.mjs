import { NodeIO } from '@gltf-transform/core';
import { ALL_EXTENSIONS } from '@gltf-transform/extensions';
import { prune, meshopt } from '@gltf-transform/functions';
import { MeshoptDecoder, MeshoptEncoder } from 'meshoptimizer';
import fs from 'fs';
await MeshoptDecoder.ready; await MeshoptEncoder.ready;
const io = new NodeIO().registerExtensions(ALL_EXTENSIONS).registerDependencies({ 'meshopt.decoder': MeshoptDecoder, 'meshopt.encoder': MeshoptEncoder });
const idx = JSON.parse(fs.readFileSync(process.argv[2] + '/index.json')).nodes;
const keepBones = new Set(Object.entries(idx).filter(([k, v]) => v.layer === 'bones' && (
  (k.endsWith('.m') && Math.abs(v.c[0]) < .01 && v.c[1] > .8 && v.c[1] < 1.58 && v.c[2] < .02) || k.startsWith('ta2-1307.'))).map(([k]) => k));
const keepDiscs = new Set(Object.entries(idx).filter(([k]) => k.startsWith('ta2-x-intervertebral-disc')).map(([k]) => k));
for (const [file, keep, out] of [['bones.glb', keepBones, 'spine-bones.glb'], ['ligaments.glb', keepDiscs, 'spine-discs.glb']]) {
  const doc = await io.read(process.argv[2] + '/' + file);
  let kept = 0;
  for (const n of doc.getRoot().listNodes()) { if (n.getMesh() && !keep.has(n.getName())) n.dispose(); else if (n.getMesh()) kept++; }
  await doc.transform(prune(), meshopt({ encoder: MeshoptEncoder, level: 'high' }));
  await io.write(process.argv[3] + '/' + out, doc);
  console.log(out, kept, fs.statSync(process.argv[3] + '/' + out).size);
}
