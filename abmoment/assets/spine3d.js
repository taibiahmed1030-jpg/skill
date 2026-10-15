// Colonne vertébrale 3D (vertèbres, bassin, disques), même modèle que le corps : CC BY-SA 4.0.
import * as THREE from 'three';
import { GLTFLoader } from './vendor/jsm/loaders/GLTFLoader.js';
import { MeshoptDecoder } from './vendor/jsm/libs/meshopt_decoder.module.js';
import { RoomEnvironment } from './vendor/jsm/environments/RoomEnvironment.js';

export async function mountSpine(canvas, { reduce = false, onReady } = {}) {
  const r = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
  r.setPixelRatio(Math.min(devicePixelRatio, 2)); r.toneMapping = THREE.ACESFilmicToneMapping;
  const scene = new THREE.Scene();
  scene.environment = new THREE.PMREMGenerator(r).fromScene(new RoomEnvironment(), .04).texture; scene.environmentIntensity = .6;
  const cam = new THREE.PerspectiveCamera(22, 1, .01, 50); scene.add(cam);
  const key = new THREE.DirectionalLight('#fff3e8', 2.4); key.position.set(2, 3, 3);
  const rim = new THREE.DirectionalLight('#cfe0ff', 2); rim.position.set(-3, 1, -2); cam.add(key, rim);

  const L = new GLTFLoader().setMeshoptDecoder(MeshoptDecoder), base = new URL('./models/', import.meta.url);
  const [b, d] = await Promise.all([L.loadAsync(new URL('spine-bones.glb', base).href), L.loadAsync(new URL('spine-discs.glb', base).href)]);
  const bone = new THREE.MeshPhysicalMaterial({ color: '#ece3d4', roughness: .45, clearcoat: .35, clearcoatRoughness: .4 });
  bone.onBeforeCompile = sh => { sh.fragmentShader = sh.fragmentShader.replace('#include <color_fragment>', `#include <color_fragment>
    diffuseColor.rgb *= 1.0 - clamp(length(fwidth(vNormal)) * 1.8, 0.0, 1.0) * .35;`); };
  const disc = new THREE.MeshPhysicalMaterial({ color: '#1f5fd6', emissive: '#1a56e0', emissiveIntensity: .5, roughness: .3, clearcoat: 1 });
  b.scene.traverse(o => { if (o.isMesh) { o.material = bone; if (!o.geometry.attributes.normal) o.geometry.computeVertexNormals(); } });
  d.scene.traverse(o => { if (o.isMesh) o.material = disc; });
  const g = new THREE.Group(); g.add(b.scene, d.scene);
  const box = new THREE.Box3().setFromObject(g), size = box.getSize(new THREE.Vector3());
  g.position.sub(box.getCenter(new THREE.Vector3()));
  const piv = new THREE.Group(); piv.add(g); scene.add(piv);
  const dist = size.y * 3.4; cam.position.set(0, 0, dist); cam.lookAt(0, 0, 0);

  const resize = () => {
    const w = canvas.clientWidth, h = canvas.clientHeight; if (!w || !h) return;
    r.setSize(w, h, false); cam.aspect = w / h;
    cam.fov = THREE.MathUtils.radToDeg(2 * Math.atan(Math.max(size.y * 1.08, size.x * 1.3 / cam.aspect) / 2 / dist));
    cam.updateProjectionMatrix();
  };
  resize(); new ResizeObserver(resize).observe(canvas);

  let yaw = .5, vel = 0, drag = null, idle = 2, visible = true, last = performance.now();
  canvas.addEventListener('pointerdown', e => { drag = { x: e.clientX, y: yaw, t: e.timeStamp, lx: e.clientX }; canvas.setPointerCapture(e.pointerId); canvas.classList.add('drag'); });
  canvas.addEventListener('pointermove', e => {
    if (!drag) return; const k = 6 / canvas.clientWidth;
    yaw = drag.y + (e.clientX - drag.x) * k;
    const dt = Math.max(1, e.timeStamp - drag.t) / 1000; vel = (e.clientX - drag.lx) * k / dt; drag.t = e.timeStamp; drag.lx = e.clientX;
  });
  const end = () => { if (!drag) return; drag = null; idle = 0; canvas.classList.remove('drag'); vel = Math.max(-6, Math.min(6, vel)); };
  canvas.addEventListener('pointerup', end); canvas.addEventListener('pointercancel', end);
  new IntersectionObserver(([e]) => { visible = e.isIntersecting; }).observe(canvas);

  const loop = t => {
    requestAnimationFrame(loop);
    const dt = Math.min(.05, (t - last) / 1000); last = t;
    if (!visible) return;
    if (!drag) { idle += dt; vel += ((idle > 1.5 && !reduce ? .4 : 0) - vel) * Math.min(1, dt * 2); yaw += vel * dt; }
    piv.rotation.y = yaw;
    disc.emissiveIntensity = reduce ? .5 : .4 + .25 * Math.sin(t / 600);
    r.render(scene, cam);
  };
  r.render(scene, cam); requestAnimationFrame(loop); onReady?.();
}
