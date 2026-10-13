// Modèle anatomique 3D (Z-Anatomy, CC BY-SA 4.0) : corps musculaire en porcelaine,
// posé sur le socle en marbre, avec la zone décrite qui se colore en bleu marine.
import * as THREE from 'three';
import { GLTFLoader } from './vendor/loaders/GLTFLoader.js';
import { DRACOLoader } from './vendor/loaders/DRACOLoader.js';
import { RoomEnvironment } from './vendor/RoomEnvironment.js';

const NAVY = new THREE.Color(0x0b3a73);
// Zones (en mètres, pieds à y = 0) : centre, rayon, orientation du corps (0 face, PI dos)
const ZONES = [
  { c: [0, 1.52, -0.02], r: 0.13, turn: Math.PI },        // nuque et tête
  { c: [0.17, 1.4, 0], r: 0.13, turn: 0.5, both: true },   // épaules
  { c: [0, 1.12, -0.08], r: 0.24, turn: Math.PI },        // dos
  { c: [0.29, 1.05, 0], r: 0.2, turn: 0.6, both: true },   // bras et poignets
  { c: [0, 0.92, 0], r: 0.18, turn: 0.3 },                // hanches et bassin
  { c: [0.1, 0.5, 0.02], r: 0.14, turn: 0.2, both: true }, // genoux et jambes
];

export async function mountAnatomy(canvas, { reduce = false, mobile = false, onReady } = {}) {
  let renderer;
  try { renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true, powerPreference: 'high-performance' }); }
  catch (e) { return null; }
  renderer.setPixelRatio(Math.min(devicePixelRatio, mobile ? 1.5 : 2));
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;

  const scene = new THREE.Scene();
  const pmrem = new THREE.PMREMGenerator(renderer);
  scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.03).texture;
  scene.environmentIntensity = 0.55;
  pmrem.dispose();

  const camera = new THREE.PerspectiveCamera(24, 1, 0.05, 20);
  camera.position.set(0, 1.05, 4.6);
  camera.lookAt(0, 0.86, 0);

  const key = new THREE.DirectionalLight(0xffffff, 2.4);
  key.position.set(-1.5, 3.2, 2.2); key.castShadow = true;
  key.shadow.mapSize.set(mobile ? 1024 : 2048, mobile ? 1024 : 2048);
  Object.assign(key.shadow.camera, { left: -1, right: 1, top: 2, bottom: -0.2, near: 0.5, far: 8 });
  key.shadow.radius = 6; key.shadow.bias = -0.0003;
  scene.add(key);
  const rim = new THREE.DirectionalLight(0x9db8e6, 2.6); rim.position.set(1.8, 2, -2.2); scene.add(rim);
  scene.add(new THREE.HemisphereLight(0xffffff, 0xcfcac1, 0.3));

  // Matériau porcelaine partagé, avec mise en couleur de la zone active (calcul dans le shader)
  const uniforms = { uZone: { value: new THREE.Vector3(0, -10, 0) }, uZone2: { value: new THREE.Vector3(0, -10, 0) }, uR: { value: 0.1 }, uOn: { value: 0 }, uNavy: { value: NAVY } };
  const porcelain = new THREE.MeshPhysicalMaterial({ color: 0xe4ded4, roughness: 0.5, metalness: 0, sheen: 0.4, sheenRoughness: 0.6, sheenColor: new THREE.Color(0xffffff), clearcoat: 0.25, clearcoatRoughness: 0.4 });
  porcelain.onBeforeCompile = sh => {
    Object.assign(sh.uniforms, uniforms);
    sh.vertexShader = sh.vertexShader.replace('#include <common>', '#include <common>\nvarying vec3 vWorld;')
      .replace('#include <worldpos_vertex>', '#include <worldpos_vertex>\nvWorld = (modelMatrix * vec4(transformed, 1.0)).xyz;');
    sh.fragmentShader = sh.fragmentShader.replace('#include <common>', '#include <common>\nvarying vec3 vWorld; uniform vec3 uZone; uniform vec3 uZone2; uniform float uR; uniform float uOn; uniform vec3 uNavy;')
      .replace('#include <color_fragment>', `#include <color_fragment>
        float dz = min(distance(vWorld, uZone), distance(vWorld, uZone2));
        float k = (1.0 - smoothstep(uR * 0.55, uR, dz)) * uOn;
        diffuseColor.rgb = mix(diffuseColor.rgb, uNavy, k * 0.9);`);
  };
  porcelain.customProgramCacheKey = () => 'abm-porcelain';

  const draco = new DRACOLoader(); draco.setDecoderPath(new URL('./vendor/draco/', import.meta.url).href);
  const loader = new GLTFLoader(); loader.setDRACOLoader(draco);
  const file = 'muscular';
  const gltf = await loader.loadAsync(new URL(`./models/${file}.glb`, import.meta.url).href);
  const body = gltf.scene;
  body.traverse(o => { if (o.isMesh) { o.material = porcelain; o.castShadow = true; o.receiveShadow = true; } });

  // Socle en marbre identique à celui du logo
  const mc = document.createElement('canvas'); mc.width = mc.height = 512; const g = mc.getContext('2d');
  g.fillStyle = '#f4f3f0'; g.fillRect(0, 0, 512, 512);
  for (let v = 0; v < 9; v++) { g.strokeStyle = `rgba(110,114,122,${0.25 + Math.random() * 0.3})`; g.lineWidth = 0.6 + Math.random() * 1.6; g.beginPath(); let x = Math.random() * 512, y = -10; g.moveTo(x, y); while (y < 530) { x += (Math.random() - 0.4) * 40; y += 18 + Math.random() * 26; g.lineTo(x, y); } g.stroke(); }
  const mt = new THREE.CanvasTexture(mc); mt.colorSpace = THREE.SRGBColorSpace;
  const plinth = new THREE.Mesh(new THREE.CylinderGeometry(0.42, 0.44, 0.06, 96), new THREE.MeshPhysicalMaterial({ map: mt, roughness: 0.2, clearcoat: 0.6 }));
  plinth.position.y = -0.03; plinth.receiveShadow = true;
  const edge = new THREE.Mesh(new THREE.TorusGeometry(0.422, 0.003, 8, 120), new THREE.MeshPhysicalMaterial({ color: 0x002043 }));
  edge.rotation.x = Math.PI / 2; edge.position.y = 0.001;
  const floor = new THREE.Mesh(new THREE.PlaneGeometry(6, 6), new THREE.ShadowMaterial({ opacity: 0.14 }));
  floor.rotation.x = -Math.PI / 2; floor.position.y = -0.06; floor.receiveShadow = true;

  const turntable = new THREE.Group(); turntable.add(body);
  scene.add(turntable, plinth, edge, floor);

  function resize() {
    const w = canvas.clientWidth, h = canvas.clientHeight; if (!w || !h) return;
    renderer.setSize(w, h, false); camera.aspect = w / h;
    camera.position.z = w / h < 0.75 ? 5.6 : 4.6;
    camera.updateProjectionMatrix();
  }
  resize(); new ResizeObserver(resize).observe(canvas);

  const pointer = { x: 0, tx: 0 };
  addEventListener('pointermove', e => { pointer.tx = (e.clientX / innerWidth) * 2 - 1; }, { passive: true });
  let visible = true;
  new IntersectionObserver(([e]) => { visible = e.isIntersecting; }).observe(canvas);

  let targetTurn = 0.35, targetOn = 0;
  const zA = new THREE.Vector3(0, -10, 0), zB = new THREE.Vector3(0, -10, 0);
  const clock = new THREE.Clock();
  renderer.compile(scene, camera);
  onReady?.();
  (function frame() {
    requestAnimationFrame(frame);
    if (!visible || document.hidden) return;
    const t = clock.getElapsedTime();
    pointer.x += (pointer.tx - pointer.x) * 0.05;
    const idle = reduce ? 0 : Math.sin(t * 0.4) * 0.12;
    turntable.rotation.y += ((targetTurn + idle + pointer.x * 0.25) - turntable.rotation.y) * (reduce ? 1 : 0.045);
    uniforms.uOn.value += (targetOn - uniforms.uOn.value) * (reduce ? 1 : 0.08);
    turntable.updateMatrixWorld();
    uniforms.uZone.value.copy(zA).applyMatrix4(turntable.matrixWorld);
    uniforms.uZone2.value.copy(zB).applyMatrix4(turntable.matrixWorld);
    renderer.render(scene, camera);
  })();

  return {
    // i : 0 nuque, 1 épaules, 2 dos, 3 bras, 4 hanches, 5 genoux ; -1 pour aucune zone
    setZone(i) {
      const z = ZONES[i];
      if (!z) { targetOn = 0; return; }
      zA.set(...z.c);
      zB.set(z.both ? -z.c[0] : z.c[0], z.c[1], z.c[2]);
      uniforms.uR.value = z.r; targetOn = 1; targetTurn = z.turn;
    },
  };
}
