// Le « AB » du logo ABmoment en 3D : lettres Bodoni bleu marine laqué sur un socle en marbre blanc
import * as THREE from 'three';
import { RoomEnvironment } from './vendor/RoomEnvironment.js';

const NAVY = 0x002043;

function marbleTexture() {
  const c = document.createElement('canvas'); c.width = c.height = 512;
  const g = c.getContext('2d');
  g.fillStyle = '#f4f3f0'; g.fillRect(0, 0, 512, 512);
  // veines grises fines, comme le marbre du centre
  for (let v = 0; v < 9; v++) {
    g.strokeStyle = `rgba(110,114,122,${0.25 + Math.random() * 0.3})`;
    g.lineWidth = 0.6 + Math.random() * 1.6;
    g.beginPath();
    let x = Math.random() * 512, y = -10;
    g.moveTo(x, y);
    while (y < 530) { x += (Math.random() - 0.4) * 40; y += 18 + Math.random() * 26; g.lineTo(x, y); }
    g.stroke();
  }
  const t = new THREE.CanvasTexture(c); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.colorSpace = THREE.SRGBColorSpace;
  return t;
}

function buildShapes(contours) {
  const area = pts => pts.reduce((s, p, i) => { const q = pts[(i + 1) % pts.length]; return s + p[0] * q[1] - q[0] * p[1]; }, 0) / 2;
  const inside = (pt, poly) => {
    let c = false;
    for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) {
      const [xi, yi] = poly[i], [xj, yj] = poly[j];
      if ((yi > pt[1]) !== (yj > pt[1]) && pt[0] < ((xj - xi) * (pt[1] - yi)) / (yj - yi) + xi) c = !c;
    }
    return c;
  };
  const withArea = contours.map(c => ({ c, a: area(c) }));
  const outerSign = Math.sign(withArea.reduce((m, x) => (Math.abs(x.a) > Math.abs(m.a) ? x : m)).a);
  const outers = withArea.filter(x => Math.sign(x.a) === outerSign);
  const holes = withArea.filter(x => Math.sign(x.a) !== outerSign);
  return outers.map(o => {
    const s = new THREE.Shape(o.c.map(([x, y]) => new THREE.Vector2(x, y)));
    holes.filter(h => inside(h.c[0], o.c)).forEach(h => s.holes.push(new THREE.Path(h.c.map(([x, y]) => new THREE.Vector2(x, y)))));
    return s;
  });
}

export async function mountLogo(canvas, { reduce = false, mobile = false } = {}) {
  let renderer;
  try { renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true, powerPreference: 'high-performance' }); }
  catch (e) { return null; }
  const glyphs = await fetch(new URL('./ab-glyphs.json', import.meta.url)).then(r => r.json());

  renderer.setPixelRatio(Math.min(devicePixelRatio, mobile ? 1.7 : 2));
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.0;
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;

  const scene = new THREE.Scene();
  const pmrem = new THREE.PMREMGenerator(renderer);
  scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.03).texture;
  scene.environmentIntensity = 0.85;
  pmrem.dispose();

  const camera = new THREE.PerspectiveCamera(26, 1, 0.1, 50);
  camera.position.set(0, 1.35, 7.4);
  camera.lookAt(0, 0.5, 0);

  const key = new THREE.DirectionalLight(0xffffff, 2.2);
  key.position.set(-1.6, 5, 2.4); key.castShadow = true;
  key.shadow.mapSize.set(mobile ? 1024 : 2048, mobile ? 1024 : 2048);
  Object.assign(key.shadow.camera, { left: -4, right: 4, top: 3, bottom: -2, near: 0.5, far: 14 });
  key.shadow.radius = 8; key.shadow.bias = -0.0004;
  scene.add(key);
  const rim = new THREE.DirectionalLight(0xdbe6ff, 1.6); rim.position.set(3, 2.5, -3); scene.add(rim);
  scene.add(new THREE.HemisphereLight(0xffffff, 0xd9d6d0, 0.35));

  // Lettres : laque bleu marine, arêtes biseautées qui accrochent la lumière
  const shapes = [...buildShapes(glyphs.A), ...buildShapes(glyphs.B)];
  const geo = new THREE.ExtrudeGeometry(shapes, { depth: 0.2, bevelEnabled: true, bevelThickness: 0.02, bevelSize: 0.008, bevelSegments: 5, curveSegments: 6 });
  geo.computeBoundingBox();
  const bb = geo.boundingBox; const w = bb.max.x - bb.min.x;
  geo.translate(-(bb.min.x + w / 2), -bb.min.y, -0.1);
  const lacquer = new THREE.MeshPhysicalMaterial({ color: NAVY, roughness: 0.28, metalness: 0.15, clearcoat: 1, clearcoatRoughness: 0.06, envMapIntensity: 1.1 });
  const letters = new THREE.Mesh(geo, lacquer);
  letters.castShadow = true; letters.receiveShadow = true;
  const scale = 1.9 / w;
  letters.scale.setScalar(scale);

  // Socle en marbre blanc
  const marble = new THREE.MeshPhysicalMaterial({ map: marbleTexture(), roughness: 0.18, metalness: 0, clearcoat: 0.6, clearcoatRoughness: 0.15 });
  const plinth = new THREE.Mesh(new THREE.CylinderGeometry(1.18, 1.22, 0.2, 128), marble);
  plinth.position.y = -0.1; plinth.receiveShadow = true; plinth.castShadow = true;
  const edge = new THREE.Mesh(new THREE.TorusGeometry(1.185, 0.007, 8, 160), new THREE.MeshPhysicalMaterial({ color: NAVY, roughness: 0.3 }));
  edge.rotation.x = Math.PI / 2; edge.position.y = 0.002;

  // Ombre douce au sol
  const floor = new THREE.Mesh(new THREE.PlaneGeometry(12, 12), new THREE.ShadowMaterial({ opacity: 0.16 }));
  floor.rotation.x = -Math.PI / 2; floor.position.y = -0.2; floor.receiveShadow = true;

  const piece = new THREE.Group(); piece.add(letters);
  const stage = new THREE.Group(); stage.add(piece, plinth, edge);
  scene.add(stage, floor);

  function resize() {
    const cw = canvas.clientWidth, ch = canvas.clientHeight; if (!cw || !ch) return;
    renderer.setSize(cw, ch, false); camera.aspect = cw / ch;
    camera.position.z = cw / ch < 0.9 ? 8.6 : 7.4;
    camera.updateProjectionMatrix();
  }
  resize(); new ResizeObserver(resize).observe(canvas);

  const pointer = { x: 0, y: 0, tx: 0, ty: 0 };
  addEventListener('pointermove', e => { pointer.tx = (e.clientX / innerWidth) * 2 - 1; pointer.ty = (e.clientY / innerHeight) * 2 - 1; }, { passive: true });
  let visible = true;
  new IntersectionObserver(([e]) => { visible = e.isIntersecting; }).observe(canvas);

  const clock = new THREE.Clock();
  const start = performance.now();
  renderer.compile(scene, camera);
  (function frame() {
    requestAnimationFrame(frame);
    if (!visible || document.hidden) return;
    const t = clock.getElapsedTime();
    pointer.x += (pointer.tx - pointer.x) * 0.05; pointer.y += (pointer.ty - pointer.y) * 0.05;
    if (!reduce) {
      // Entrée : les lettres montent doucement sur le socle
      const e = 1 - Math.pow(1 - Math.min(1, (performance.now() - start) / 1600), 3);
      piece.position.y = -0.5 * (1 - e);
      letters.material.opacity = 1;
      stage.rotation.y = -0.35 + Math.sin(t * 0.35) * 0.32 + pointer.x * 0.35;
      stage.rotation.x = pointer.y * 0.04;
    } else stage.rotation.y = -0.3;
    renderer.render(scene, camera);
  })();
  return {};
}
