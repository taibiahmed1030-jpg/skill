// Scènes 3D d'ABmoment, générées en code (aucun modèle externe) :
//  - mountBody  : silhouette humaine en fibres musculaires lumineuses
//  - mountBrain : cerveau en nuage de neurones reliés par des connexions bleues
import * as THREE from 'three';

const fiberVert = `
  attribute float u; attribute float seed; attribute float region;
  varying float vU; varying float vSeed; varying float vRegion; varying float vDepth;
  void main() {
    vU = u; vSeed = seed; vRegion = region;
    vec4 mv = modelViewMatrix * vec4(position, 1.0);
    vDepth = -mv.z;
    gl_Position = projectionMatrix * mv;
  }`;
const fiberFrag = `
  uniform float time; uniform float region; uniform float hl; uniform vec3 colA; uniform vec3 colB; uniform vec3 colHi;
  uniform float base; uniform float speed; uniform float near; uniform float far;
  varying float vU; varying float vSeed; varying float vRegion; varying float vDepth;
  void main() {
    float p = fract(vU * 0.9 - time * speed + vSeed);
    float pulse = smoothstep(0.1, 0.0, abs(p - 0.5)) ;
    float isHi = (abs(vRegion - region) < 0.5 ? 1.0 : 0.0) * hl;
    float depth = 1.0 - smoothstep(near, far, vDepth) * 0.75;
    vec3 c = mix(colA, colB, vU);
    c = mix(c, colHi, isHi * 0.85);
    float a = (base + pulse * 0.9 + isHi * 0.55) * depth;
    gl_FragColor = vec4(c * a, a);
  }`;

function glowTexture(r, g, b) {
  const c = document.createElement('canvas'); c.width = c.height = 64;
  const x = c.getContext('2d'); const gr = x.createRadialGradient(32, 32, 0, 32, 32, 32);
  gr.addColorStop(0, `rgba(${r},${g},${b},1)`); gr.addColorStop(0.3, `rgba(${r},${g},${b},.35)`); gr.addColorStop(1, `rgba(${r},${g},${b},0)`);
  x.fillStyle = gr; x.fillRect(0, 0, 64, 64);
  return new THREE.CanvasTexture(c);
}

function setup(canvas, { mobile, fov = 30, z = 9 }) {
  let renderer;
  try { renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true, powerPreference: 'high-performance' }); }
  catch (e) { return null; }
  renderer.setPixelRatio(Math.min(devicePixelRatio, mobile ? 1.6 : 2));
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(fov, 1, 0.1, 60);
  camera.position.set(0, 0, z);
  const resize = () => {
    const w = canvas.clientWidth, h = canvas.clientHeight; if (!w || !h) return;
    renderer.setSize(w, h, false); camera.aspect = w / h; camera.updateProjectionMatrix();
  };
  resize(); new ResizeObserver(resize).observe(canvas);
  const pointer = { x: 0, y: 0, tx: 0, ty: 0 };
  addEventListener('pointermove', e => { pointer.tx = (e.clientX / innerWidth) * 2 - 1; pointer.ty = (e.clientY / innerHeight) * 2 - 1; }, { passive: true });
  let visible = true;
  new IntersectionObserver(([e]) => { visible = e.isIntersecting; }).observe(canvas);
  return { renderer, scene, camera, pointer, isVisible: () => visible && !document.hidden };
}

/* ======================= Corps en fibres musculaires ======================= */
export function mountBody(canvas, { reduce = false, mobile = false } = {}) {
  const S = setup(canvas, { mobile, fov: 28, z: 9.2 });
  if (!S) return null;
  const { renderer, scene, camera, pointer } = S;

  // Régions : 0 tête/cou, 1 épaules, 2 dos/tronc, 3 bras, 4 hanches, 5 jambes/genoux
  const pos = [], uArr = [], seedArr = [], regArr = [];
  const tmp = new THREE.Vector3(), axis = new THREE.Vector3(), uDir = new THREE.Vector3(), vDir = new THREE.Vector3();
  const density = mobile ? 0.6 : 1;

  function pushFiber(points, region, seed) {
    for (let i = 0; i < points.length - 1; i++) {
      const a = points[i], b = points[i + 1];
      pos.push(a.x, a.y, a.z, b.x, b.y, b.z);
      uArr.push(i / (points.length - 1), (i + 1) / (points.length - 1));
      const rg = typeof region === 'function' ? region(i / (points.length - 1)) : region;
      seedArr.push(seed, seed); regArr.push(rg, rg);
    }
  }

  // Muscle long : fibres qui se rejoignent aux tendons, ventre musculaire bombé, légère torsion
  function muscle(a, b, r0, r1, { n = 26, bulge = 0.3, twist = 0.5, depth = 1, region = 2, phase = 0, belly = 0.5 } = {}) {
    const A = new THREE.Vector3(...a), B = new THREE.Vector3(...b);
    axis.subVectors(B, A).normalize();
    uDir.set(1, 0, 0); if (Math.abs(axis.dot(uDir)) > 0.9) uDir.set(0, 0, 1);
    vDir.crossVectors(axis, uDir).normalize(); uDir.crossVectors(vDir, axis).normalize();
    const N = Math.round(n * density), M = 22;
    for (let f = 0; f < N; f++) {
      const th0 = (f / N) * Math.PI * 2 + phase, jitter = (Math.random() - 0.5) * 0.12, pts = [];
      for (let k = 0; k <= M; k++) {
        const t = k / M;
        const shape = Math.pow(Math.sin(Math.PI * Math.min(1, Math.max(0, (t - belly + 0.5)))), 0.7);
        const r = THREE.MathUtils.lerp(r0, r1, t) * (0.45 + 0.55 * Math.pow(Math.sin(Math.PI * t), 0.55)) * (1 + bulge * shape);
        const th = th0 + twist * (t - 0.5) + jitter;
        tmp.copy(A).lerp(B, t).addScaledVector(uDir, Math.cos(th) * r).addScaledVector(vDir, Math.sin(th) * r * depth);
        pts.push(tmp.clone());
      }
      pushFiber(pts, region, Math.random());
    }
  }

  // Tronc : section elliptique qui varie des épaules aux hanches
  const torsoProfile = y => {
    const k = (y - 0.02) / (1.16 - 0.02); // 0 hanches -> 1 épaules
    const w = 0.33 - 0.07 * Math.sin(Math.PI * Math.min(1, k * 1.25)) + 0.12 * Math.pow(Math.max(0, k - 0.55) / 0.45, 1.4);
    const d = 0.19 - 0.02 * Math.sin(Math.PI * k) + 0.02 * k;
    return [w, d];
  };
  const TN = Math.round(64 * density), TM = 34;
  for (let f = 0; f < TN; f++) {
    const th0 = (f / TN) * Math.PI * 2, pts = [];
    const back = Math.sin(th0) < 0;
    for (let k = 0; k <= TM; k++) {
      const t = k / TM, y = THREE.MathUtils.lerp(0.02, 1.16, t);
      const [w, d] = torsoProfile(y);
      const th = th0 + (back ? -1 : 1) * 0.35 * Math.sin(Math.PI * t) * Math.cos(th0);
      pts.push(new THREE.Vector3(Math.cos(th) * w, y, Math.sin(th) * d));
    }
    // région : bas du tronc = hanches (4), reste = dos/tronc (2)
    pushFiber(pts, t => (t < 0.22 ? 4 : 2), Math.random());
  }
  // Pectoraux : éventail du sternum vers l'épaule
  for (const side of [-1, 1]) {
    const n = Math.round(14 * density);
    for (let f = 0; f < n; f++) {
      const s = f / (n - 1), pts = [];
      const start = new THREE.Vector3(0.02 * side, 0.62 + s * 0.42, 0.2), end = new THREE.Vector3(0.4 * side, 1.02, 0.12);
      const mid = new THREE.Vector3(0.22 * side, 0.8 + s * 0.2, 0.27);
      const curve = new THREE.QuadraticBezierCurve3(start, mid, end);
      pushFiber(curve.getPoints(18), 1, Math.random());
    }
    // Trapèzes : de la nuque vers l'épaule
    for (let f = 0; f < Math.round(8 * density); f++) {
      const s = f / 7;
      const curve = new THREE.QuadraticBezierCurve3(new THREE.Vector3(0.03 * side, 1.3 - s * 0.35, -0.08 - s * 0.05), new THREE.Vector3(0.2 * side, 1.2 - s * 0.1, -0.12), new THREE.Vector3(0.44 * side, 1.12, -0.02));
      pushFiber(curve.getPoints(16), 1, Math.random());
    }
    // Deltoïdes
    muscle([0.4 * side, 1.18, 0], [0.5 * side, 0.82, 0], 0.12, 0.06, { n: 22, bulge: 0.35, twist: 0.3 * side, region: 1, belly: 0.4 });
    // Bras, avant-bras, mains
    muscle([0.47 * side, 1.02, 0], [0.56 * side, 0.45, 0.02], 0.085, 0.065, { n: 20, bulge: 0.35, twist: 0.6 * side, region: 3 });
    muscle([0.57 * side, 0.42, 0.03], [0.63 * side, -0.16, 0.08], 0.068, 0.04, { n: 18, bulge: 0.35, twist: 0.9 * side, region: 3, belly: 0.35 });
    muscle([0.63 * side, -0.18, 0.08], [0.65 * side, -0.4, 0.1], 0.045, 0.03, { n: 10, bulge: 0.2, twist: 0.2, region: 3 });
    // Cuisses, mollets, pieds
    muscle([0.17 * side, 0.08, 0], [0.2 * side, -0.84, 0.02], 0.15, 0.085, { n: 28, bulge: 0.25, twist: -0.5 * side, region: 4, belly: 0.4 });
    muscle([0.2 * side, -0.9, 0.02], [0.21 * side, -1.64, -0.02], 0.09, 0.045, { n: 22, bulge: 0.4, twist: 0.4 * side, region: 5, belly: 0.3 });
    muscle([0.21 * side, -1.68, -0.02], [0.23 * side, -1.73, 0.2], 0.05, 0.035, { n: 10, bulge: 0.1, twist: 0, region: 5 });
    // Genou : anneaux autour de la rotule
    for (let rr = 0; rr < 3; rr++) {
      const pts = []; for (let k = 0; k <= 40; k++) { const a = (k / 40) * Math.PI * 2; pts.push(new THREE.Vector3(0.2 * side + Math.cos(a) * (0.08 + rr * 0.012), -0.87 + rr * 0.01, 0.02 + Math.sin(a) * (0.08 + rr * 0.012))); }
      pushFiber(pts, 5, Math.random());
    }
  }
  // Cou
  muscle([0, 1.18, 0], [0, 1.36, 0.01], 0.085, 0.07, { n: 16, bulge: 0.15, twist: 0.4, region: 0 });
  // Tête : méridiens et parallèles
  for (let m = 0; m < Math.round(14 * density); m++) {
    const a0 = (m / 14) * Math.PI, pts = [];
    for (let k = 0; k <= 40; k++) { const b = (k / 40) * Math.PI * 2; pts.push(new THREE.Vector3(Math.cos(b) * Math.cos(a0) * 0.17, 1.56 + Math.sin(b) * 0.215, Math.cos(b) * Math.sin(a0) * 0.19)); }
    pushFiber(pts, 0, Math.random());
  }
  for (let p = 1; p < 6; p++) {
    const y = -0.8 + p * 0.27, rad = Math.sqrt(1 - y * y), pts = [];
    for (let k = 0; k <= 40; k++) { const b = (k / 40) * Math.PI * 2; pts.push(new THREE.Vector3(Math.cos(b) * rad * 0.17, 1.56 + y * 0.215, Math.sin(b) * rad * 0.19)); }
    pushFiber(pts, 0, Math.random());
  }
  // Colonne vertébrale lumineuse (vue de dos)
  const spine = [];
  for (let v = 0; v < 22; v++) spine.push(new THREE.Vector3(0, 0.08 + v * 0.058, -0.17 - 0.03 * Math.sin((v / 21) * Math.PI)));

  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
  geo.setAttribute('u', new THREE.Float32BufferAttribute(uArr, 1));
  geo.setAttribute('seed', new THREE.Float32BufferAttribute(seedArr, 1));
  geo.setAttribute('region', new THREE.Float32BufferAttribute(regArr, 1));
  const uniforms = {
    time: { value: 0 }, region: { value: -1 }, hl: { value: 0 },
    colA: { value: new THREE.Color('#ff4a3d') }, colB: { value: new THREE.Color('#ff9f84') }, colHi: { value: new THREE.Color('#ffe7c9') },
    base: { value: 0.34 }, speed: { value: 0.22 }, near: { value: 7.6 }, far: { value: 10.6 },
  };
  const mat = new THREE.ShaderMaterial({ vertexShader: fiberVert, fragmentShader: fiberFrag, uniforms, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending });
  const body = new THREE.LineSegments(geo, mat);

  const vertMat = new THREE.SpriteMaterial({ map: glowTexture(255, 210, 180), blending: THREE.AdditiveBlending, depthWrite: false, transparent: true, opacity: 0.3 });
  const spineGroup = new THREE.Group();
  spine.forEach((p, i) => { const s = new THREE.Sprite(vertMat); s.position.copy(p); s.scale.setScalar(0.07 + 0.015 * Math.sin(i)); spineGroup.add(s); });

  // Halo sur la zone mise en avant
  const halo = new THREE.Sprite(new THREE.SpriteMaterial({ map: glowTexture(255, 120, 100), blending: THREE.AdditiveBlending, depthWrite: false, transparent: true, opacity: 0 }));
  halo.scale.setScalar(1.1);
  const centers = [[0, 1.45, 0], [0.42, 1.08, 0], [0, 0.75, -0.1], [0.56, 0.4, 0], [0, 0.1, 0], [0.2, -0.87, 0.05]];

  const fig = new THREE.Group(); fig.add(body, spineGroup, halo);
  fig.position.y = 0.05;
  scene.add(fig);

  // Sol : cercles concentriques discrets
  const ringMat = new THREE.LineBasicMaterial({ color: 0xff7a64, transparent: true, opacity: 0.12 });
  for (let i = 1; i <= 4; i++) {
    const pts = []; for (let k = 0; k <= 96; k++) { const a = (k / 96) * Math.PI * 2; pts.push(new THREE.Vector3(Math.cos(a) * i * 0.32, -1.76, Math.sin(a) * i * 0.32)); }
    const ring = new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts), ringMat); fig.add(ring);
  }

  let targetRegion = -1, hlTarget = 0;
  const clock = new THREE.Clock();
  const start = performance.now();
  (function frame() {
    requestAnimationFrame(frame);
    if (!S.isVisible()) return;
    const t = clock.getElapsedTime();
    uniforms.time.value = reduce ? 0 : t;
    pointer.x += (pointer.tx - pointer.x) * 0.05; pointer.y += (pointer.ty - pointer.y) * 0.05;
    if (!reduce) {
      fig.rotation.y = Math.sin(t * 0.25) * 0.5 + pointer.x * 0.5 + (targetRegion === 2 ? Math.PI : 0) * 0;
      fig.rotation.x = pointer.y * 0.06;
      const intro = Math.min(1, (performance.now() - start) / 1800);
      uniforms.base.value = 0.34 * intro;
    }
    uniforms.hl.value += (hlTarget - uniforms.hl.value) * 0.08;
    halo.material.opacity = uniforms.hl.value * 0.55;
    renderer.render(scene, camera);
  })();

  return {
    // Met une zone du corps en lumière (0 tête, 1 épaules, 2 dos, 3 bras, 4 hanches, 5 genoux) ou -1 pour aucune
    setRegion(i) {
      targetRegion = i; hlTarget = i < 0 ? 0 : 1;
      if (i >= 0) { uniforms.region.value = i; halo.position.set(...centers[i]); }
    },
  };
}

/* ======================= Cerveau et connexions neuronales ======================= */
export function mountBrain(canvas, { reduce = false, mobile = false } = {}) {
  const S = setup(canvas, { mobile, fov: 30, z: 7.4 });
  if (!S) return null;
  const { renderer, scene, camera, pointer } = S;

  // Bruit simple pour dessiner les circonvolutions
  const fold = (x, y, z) => 0.055 * Math.sin(9 * x + 3 * Math.sin(5 * y)) * Math.cos(8 * y + 2 * z) + 0.03 * Math.sin(14 * z + 6 * x);
  const nodes = [];
  const N = mobile ? 900 : 1500;
  function sampleHemisphere(side, count) {
    for (let i = 0; i < count; i++) {
      // direction aléatoire, hémisphère aplati côté médian
      let x = Math.random() * 2 - 1, y = Math.random() * 2 - 1, z = Math.random() * 2 - 1;
      const l = Math.hypot(x, y, z) || 1; x /= l; y /= l; z /= l;
      if (x * side < -0.25) x = -0.25 * side + (x + 0.25 * side) * 0.15;
      const r = 1 + fold(x, y, z);
      // profil latéral : dôme en haut, lobe temporal qui descend vers l'avant, base plus plate à l'arrière
      const ry = y > 0 ? 0.84 - 0.12 * Math.max(0, -z) : 0.34 + 0.34 * Math.exp(-((z - 0.3) * (z - 0.3)) / 0.18);
      nodes.push(new THREE.Vector3(side * 0.44 + x * 0.78 * r, y * ry * r + 0.12, z * 1.25 * r));
    }
  }
  sampleHemisphere(-1, N / 2); sampleHemisphere(1, N / 2);
  // Cervelet et tronc cérébral
  for (let i = 0; i < N * 0.12; i++) {
    let x = Math.random() * 2 - 1, y = Math.random() * 2 - 1, z = Math.random() * 2 - 1; const l = Math.hypot(x, y, z) || 1;
    nodes.push(new THREE.Vector3(x / l * 0.6, -0.42 + y / l * 0.26, -0.92 + z / l * 0.34));
  }
  for (let i = 0; i < 50; i++) nodes.push(new THREE.Vector3((Math.random() - 0.5) * 0.16, -0.3 - i * 0.02, -0.45 - i * 0.004 + (Math.random() - 0.5) * 0.12));

  // Points (neurones)
  const pGeo = new THREE.BufferGeometry().setFromPoints(nodes);
  const sizes = new Float32Array(nodes.length).map(() => 0.5 + Math.random());
  pGeo.setAttribute('size', new THREE.BufferAttribute(sizes, 1));
  const pMat = new THREE.ShaderMaterial({
    transparent: true, depthWrite: false, blending: THREE.AdditiveBlending,
    uniforms: { time: { value: 0 }, pr: { value: renderer.getPixelRatio() } },
    vertexShader: `attribute float size; uniform float time; uniform float pr; varying float vA;
      void main(){ vec4 mv = modelViewMatrix * vec4(position,1.0); float tw = 0.6 + 0.4 * sin(time * 2.0 + position.x * 7.0 + position.z * 5.0);
      vA = tw * (1.0 - smoothstep(6.0, 9.0, -mv.z) * 0.7); gl_PointSize = size * 5.0 * pr * (6.0 / -mv.z); gl_Position = projectionMatrix * mv; }`,
    fragmentShader: `varying float vA; void main(){ float d = length(gl_PointCoord - 0.5); float a = smoothstep(0.5, 0.0, d) * vA; gl_FragColor = vec4(vec3(0.55, 0.85, 1.0) * a, a); }`,
  });
  const points = new THREE.Points(pGeo, pMat);

  // Connexions courtes entre neurones voisins
  const pos = [], uA = [], sA = [];
  const maxD = 0.24;
  for (let i = 0; i < nodes.length; i++) {
    let links = 0;
    for (let j = i + 1; j < nodes.length && links < 3; j++) {
      if (nodes[i].distanceTo(nodes[j]) < maxD && Math.random() < 0.5) {
        pos.push(nodes[i].x, nodes[i].y, nodes[i].z, nodes[j].x, nodes[j].y, nodes[j].z);
        uA.push(0, 1); const s = Math.random(); sA.push(s, s); links++;
      }
    }
  }
  // Grandes connexions (faisceaux) entre régions éloignées, en arc
  const arcs = mobile ? 50 : 90;
  for (let k = 0; k < arcs; k++) {
    const a = nodes[(Math.random() * nodes.length) | 0], b = nodes[(Math.random() * nodes.length) | 0];
    if (a.distanceTo(b) < 0.9) continue;
    const mid = a.clone().add(b).multiplyScalar(0.5).multiplyScalar(0.55);
    const pts = new THREE.QuadraticBezierCurve3(a, mid, b).getPoints(24); const s = Math.random();
    for (let i = 0; i < pts.length - 1; i++) { pos.push(pts[i].x, pts[i].y, pts[i].z, pts[i + 1].x, pts[i + 1].y, pts[i + 1].z); uA.push(i / 24, (i + 1) / 24); sA.push(s, s); }
  }
  const lGeo = new THREE.BufferGeometry();
  lGeo.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
  lGeo.setAttribute('u', new THREE.Float32BufferAttribute(uA, 1));
  lGeo.setAttribute('seed', new THREE.Float32BufferAttribute(sA, 1));
  lGeo.setAttribute('region', new THREE.Float32BufferAttribute(new Float32Array(uA.length), 1));
  const uniforms = {
    time: { value: 0 }, region: { value: -1 }, hl: { value: 0 },
    colA: { value: new THREE.Color('#1f7cff') }, colB: { value: new THREE.Color('#6fe3ff') }, colHi: { value: new THREE.Color('#ffffff') },
    base: { value: 0.22 }, speed: { value: 0.45 }, near: { value: 6.2 }, far: { value: 9 },
  };
  const lines = new THREE.LineSegments(lGeo, new THREE.ShaderMaterial({ vertexShader: fiberVert, fragmentShader: fiberFrag, uniforms, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending }));

  const halo = new THREE.Sprite(new THREE.SpriteMaterial({ map: glowTexture(40, 120, 255), blending: THREE.AdditiveBlending, depthWrite: false, transparent: true, opacity: 0.35 }));
  halo.scale.setScalar(3.1); halo.position.z = -0.6;

  const brain = new THREE.Group(); brain.add(halo, lines, points);
  brain.rotation.set(0.12, -1.2, 0);
  scene.add(brain);

  const clock = new THREE.Clock();
  (function frame() {
    requestAnimationFrame(frame);
    if (!S.isVisible()) return;
    const t = clock.getElapsedTime();
    uniforms.time.value = reduce ? 0 : t; pMat.uniforms.time.value = reduce ? 0 : t;
    pointer.x += (pointer.tx - pointer.x) * 0.05; pointer.y += (pointer.ty - pointer.y) * 0.05;
    if (!reduce) { brain.rotation.y = -1.2 + Math.sin(t * 0.2) * 0.5 + pointer.x * 0.4; brain.rotation.x = 0.15 + pointer.y * 0.12; }
    renderer.render(scene, camera);
  })();
  return {};
}
