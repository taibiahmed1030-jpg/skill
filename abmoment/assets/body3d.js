// Corps anatomique 3D (muscles + os), rendu façon planche médicale.
// Modèle : lucgrn3/anatomy-models (Z-Anatomy, BodyParts3D…), CC BY-SA 4.0.
import * as THREE from 'three';
import { GLTFLoader } from './vendor/jsm/loaders/GLTFLoader.js';
import { MeshoptDecoder } from './vendor/jsm/libs/meshopt_decoder.module.js';
import { mergeGeometries } from './vendor/jsm/utils/BufferGeometryUtils.js';
import { RoomEnvironment } from './vendor/jsm/environments/RoomEnvironment.js';

const base = new URL('./models/', import.meta.url);
let assets = null;
function loadAssets() {
  if (!assets) {
    const L = new GLTFLoader().setMeshoptDecoder(MeshoptDecoder);
    assets = Promise.all([L.loadAsync(new URL('muscles.glb', base).href), L.loadAsync(new URL('bones.glb', base).href)]);
  }
  return assets;
}

// Zone d'un muscle d'après la position de son centre (hauteur relative, écart à l'axe, face/dos)
function zoneOf(h, ax, back) {
  if (h > .845 && ax < .11) return 0;               // nuque et tête
  if (h > .76 && ax >= .11 && ax < .23) return 1;   // épaules
  if (ax >= .14 && h <= .8) return 3;               // bras et poignets
  if (back && h > .56 && h <= .845 && ax < .14) return 2; // dos
  if (h > .43 && h <= .58 && ax < .17) return 4;    // hanches et bassin
  if (h <= .43) return 5;                           // genoux et jambes
  return -1;
}

function buildMuscles(scene) {
  scene.updateMatrixWorld(true);
  const box = new THREE.Box3().setFromObject(scene), size = box.getSize(new THREE.Vector3()), ctr = box.getCenter(new THREE.Vector3());
  const geos = [], v = new THREE.Vector3(), mean = new THREE.Vector3(), d = new THREE.Vector3();
  scene.traverse(o => {
    if (!o.isMesh) return;
    const g = o.geometry.clone(); g.applyMatrix4(o.matrixWorld);
    for (const k of Object.keys(g.attributes)) if (k !== 'position' && k !== 'normal') g.deleteAttribute(k);
    if (!g.attributes.normal) g.computeVertexNormals();
    const P = g.attributes.position, n = P.count;
    mean.set(0, 0, 0); for (let i = 0; i < n; i++) mean.add(v.fromBufferAttribute(P, i)); mean.divideScalar(n);
    let xx = 0, xy = 0, xz = 0, yy = 0, yz = 0, zz = 0;
    for (let i = 0; i < n; i++) { v.fromBufferAttribute(P, i).sub(mean); xx += v.x * v.x; xy += v.x * v.y; xz += v.x * v.z; yy += v.y * v.y; yz += v.y * v.z; zz += v.z * v.z; }
    d.set(1, 1, 1).normalize();
    for (let it = 0; it < 20; it++) d.set(xx * d.x + xy * d.y + xz * d.z, xy * d.x + yy * d.y + yz * d.z, xz * d.x + yz * d.y + zz * d.z).normalize();
    let tmin = 1e9, tmax = -1e9, rmax = 0;
    for (let i = 0; i < n; i++) { const t = v.fromBufferAttribute(P, i).sub(mean).dot(d); tmin = Math.min(tmin, t); tmax = Math.max(tmax, t); rmax = Math.max(rmax, v.addScaledVector(d, -t).length()); }
    const L = (tmax - tmin) / 2, mid = mean.clone().addScaledVector(d, (tmax + tmin) / 2), elong = L / Math.max(rmax, 1e-4);
    const zone = zoneOf((mean.y - box.min.y) / size.y, Math.abs(mean.x - ctr.x), mean.z < ctr.z);
    const tint = .9 + Math.random() * .2;
    const F = new Float32Array(n * 4), C = new Float32Array(n * 4), Z = new Float32Array(n);
    for (let i = 0; i < n; i++) { F.set([d.x, d.y, d.z, tint], i * 4); C.set([mid.x, mid.y, mid.z, elong > 2.2 ? L : -L], i * 4); Z[i] = zone; }
    g.setAttribute('fdir', new THREE.BufferAttribute(F, 4));
    g.setAttribute('mctr', new THREE.BufferAttribute(C, 4));
    g.setAttribute('mzone', new THREE.BufferAttribute(Z, 1));
    geos.push(g);
  });
  return { geo: mergeGeometries(geos, false), box };
}

function muscleMaterial(uniforms) {
  const m = new THREE.MeshPhysicalMaterial({ color: '#a03f30', roughness: .55, clearcoat: .15, clearcoatRoughness: .5, sheen: .5, sheenColor: new THREE.Color('#ff9c86'), sheenRoughness: .5 });
  m.onBeforeCompile = sh => {
    Object.assign(sh.uniforms, uniforms);
    sh.vertexShader = sh.vertexShader
      .replace('#include <common>', '#include <common>\nattribute vec4 fdir; attribute vec4 mctr; attribute float mzone; varying vec4 vF; varying vec3 vP; varying vec4 vC; varying float vZ;')
      .replace('#include <begin_vertex>', '#include <begin_vertex>\nvF = fdir; vP = position; vC = mctr; vZ = mzone;');
    sh.fragmentShader = sh.fragmentShader
      .replace('#include <common>', `#include <common>
uniform float uZone; uniform float uTime; uniform float uHl;
varying vec4 vF; varying vec3 vP; varying vec4 vC; varying float vZ;
float h3(vec3 p){ p = fract(p * vec3(.1031, .1030, .0973)); p += dot(p, p.yxz + 33.33); return fract((p.x + p.y) * p.z); }
float vn(vec3 x){ vec3 i = floor(x), f = fract(x); f = f * f * (3.0 - 2.0 * f);
  return mix(mix(mix(h3(i), h3(i + vec3(1,0,0)), f.x), mix(h3(i + vec3(0,1,0)), h3(i + vec3(1,1,0)), f.x), f.y),
             mix(mix(h3(i + vec3(0,0,1)), h3(i + vec3(1,0,1)), f.x), mix(h3(i + vec3(0,1,1)), h3(i + vec3(1,1,1)), f.x), f.y), f.z); }
float fib(vec3 p, vec3 d){ vec3 q = p - d * dot(p, d) * .985;
  float f = vn(q * 420.0) * .55 + vn(q * 170.0) * .45;
  return mix(.5, f, clamp(1.4 - length(fwidth(q * 420.0)) * .5, 0.0, 1.0)); }`)
      .replace('#include <color_fragment>', `#include <color_fragment>
  vec3 fd = normalize(vF.xyz);
  float fh = fib(vP, fd);
  float tt = vC.w > 0.0 ? abs(dot(vP - vC.xyz, fd)) / vC.w : 0.0;
  float tendon = smoothstep(.62, .9, tt);
  vec3 musc = diffuseColor.rgb * vF.w * mix(.84, 1.1, fh);
  diffuseColor.rgb = mix(musc, vec3(.93, .88, .82) * mix(.96, 1.02, fh), tendon);
  float crease = clamp(length(fwidth(vNormal)) * 2.2, 0.0, 1.0); diffuseColor.rgb *= 1.0 - crease * .5;
  float hl = uHl * (1.0 - step(.5, abs(vZ - uZone)));
  diffuseColor.rgb = mix(diffuseColor.rgb, vec3(.06, .26, .78), hl * .8);`)
      .replace('#include <emissivemap_fragment>', `#include <emissivemap_fragment>
  totalEmissiveRadiance += vec3(.02, .14, .5) * hl * (.45 + .25 * sin(uTime * 3.0));`);
  };
  return m;
}

export async function mountBody(canvas, { reduce = false, interactive = true, onReady } = {}) {
  const r = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true, powerPreference: 'high-performance' });
  r.setPixelRatio(Math.min(devicePixelRatio, 2));
  r.toneMapping = THREE.ACESFilmicToneMapping;
  const scene = new THREE.Scene();
  const pm = new THREE.PMREMGenerator(r);
  scene.environment = pm.fromScene(new RoomEnvironment(), .04).texture; scene.environmentIntensity = .7;
  const key = new THREE.DirectionalLight('#fff3e8', 2.6); key.position.set(2.5, 3, 3);
  const fill = new THREE.DirectionalLight('#ffffff', .5); fill.position.set(-3, 1, 2);
  const rim = new THREE.DirectionalLight('#dfe9ff', 1.6); rim.position.set(-3, 2, -3);
  const cam = new THREE.PerspectiveCamera(20, 1, .05, 50);
  cam.add(key, fill, rim); scene.add(cam); // lumière studio fixe par rapport à la caméra

  const [m, b] = await loadAssets();
  const uniforms = { uZone: { value: -1 }, uTime: { value: 0 }, uHl: { value: 0 } };
  const { geo, box } = buildMuscles(m.scene);
  const muscles = new THREE.Mesh(geo, muscleMaterial(uniforms));
  const bones = b.scene.clone(true);
  const boneMat = new THREE.MeshPhysicalMaterial({ color: '#eee6d8', roughness: .55, clearcoat: .2 });
  bones.traverse(o => { if (o.isMesh) o.material = boneMat; });
  const body = new THREE.Group(); body.add(bones, muscles);
  const ctr = box.getCenter(new THREE.Vector3()), size = box.getSize(new THREE.Vector3());
  body.position.sub(ctr);
  const pivot = new THREE.Group(); pivot.add(body); scene.add(pivot);
  const dist = size.y * 3.1;
  cam.position.set(0, size.y * .02, dist); cam.lookAt(0, 0, 0);

  const resize = () => {
    const w = canvas.clientWidth, h = canvas.clientHeight; if (!w || !h) return;
    r.setSize(w, h, false); cam.aspect = w / h;
    // le corps entier doit tenir en hauteur comme en largeur
    const fitH = size.y * 1.06, fitW = size.x * 1.15 / cam.aspect;
    cam.fov = THREE.MathUtils.radToDeg(2 * Math.atan(Math.max(fitH, fitW) / 2 / dist));
    cam.updateProjectionMatrix();
  };
  resize(); new ResizeObserver(resize).observe(canvas);

  let yaw = 0, vel = 0, target = null, drag = null, idle = 2, visible = true, last = performance.now();
  const auto = reduce ? 0 : .35;
  if (interactive) {
    canvas.addEventListener('pointerdown', e => { drag = { x: e.clientX, y: yaw, t: e.timeStamp, lx: e.clientX }; target = null; canvas.setPointerCapture(e.pointerId); canvas.classList.add('drag'); canvas.dispatchEvent(new CustomEvent('touched', { bubbles: true })); });
    canvas.addEventListener('pointermove', e => {
      if (!drag) return; const k = 6 / canvas.clientWidth;
      yaw = drag.y + (e.clientX - drag.x) * k;
      const dt = Math.max(1, e.timeStamp - drag.t) / 1000; vel = (e.clientX - drag.lx) * k / dt; drag.t = e.timeStamp; drag.lx = e.clientX;
    });
    const end = () => { if (!drag) return; drag = null; idle = 0; canvas.classList.remove('drag'); vel = Math.max(-6, Math.min(6, vel)); };
    canvas.addEventListener('pointerup', end); canvas.addEventListener('pointercancel', end);
  }
  new IntersectionObserver(([e]) => { visible = e.isIntersecting; }).observe(canvas);

  const loop = t => {
    requestAnimationFrame(loop);
    const dt = Math.min(.05, (t - last) / 1000); last = t;
    if (!visible) return;
    if (!drag) {
      idle += dt;
      if (target !== null) {
        // rotation vers la face ou le dos pour montrer une zone
        const diff = Math.atan2(Math.sin(target - yaw), Math.cos(target - yaw));
        yaw += diff * Math.min(1, dt * 5); vel = 0;
      } else {
        vel += ((idle > 1.5 ? auto : 0) - vel) * Math.min(1, dt * 2);
        yaw += vel * dt;
      }
    }
    pivot.rotation.y = yaw;
    uniforms.uTime.value = t / 1000;
    uniforms.uHl.value += ((uniforms.uZone.value >= 0 ? 1 : 0) - uniforms.uHl.value) * Math.min(1, dt * 5);
    r.render(scene, cam);
  };
  r.render(scene, cam);
  requestAnimationFrame(loop);
  onReady?.();
  return {
    setZone(z, back) { uniforms.uZone.value = z; target = back ? Math.PI : 0; },
    free() { target = null; idle = 0; }
  };
}
