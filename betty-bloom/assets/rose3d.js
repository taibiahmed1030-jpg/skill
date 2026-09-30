// Rose éternelle sous cloche, entièrement générée en 3D (aucun modèle externe)
import * as THREE from 'three';
import { RoomEnvironment } from './vendor/RoomEnvironment.js';

export function mountRose(canvas, { reduce = false, mobile = false } = {}) {
  let renderer;
  try { renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true, powerPreference: 'high-performance' }); }
  catch (e) { return null; }
  renderer.setPixelRatio(Math.min(devicePixelRatio, mobile ? 1.5 : 1.75));
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.05;

  const scene = new THREE.Scene();
  const pmrem = new THREE.PMREMGenerator(renderer);
  scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
  scene.environmentIntensity = 0.45;
  pmrem.dispose();

  const camera = new THREE.PerspectiveCamera(28, 1, 0.1, 50);
  camera.position.set(0, 2.9, 8.9);
  camera.lookAt(0, 1.5, 0);

  scene.add(new THREE.HemisphereLight(0xffe9f0, 0x1a1012, 0.25));
  const key = new THREE.DirectionalLight(0xfff1ea, 1.5); key.position.set(-3, 5, 4); scene.add(key);
  const rim = new THREE.DirectionalLight(0xffc4d6, 1.6); rim.position.set(3, 3, -4); scene.add(rim);
  const inner = new THREE.PointLight(0xff8fb1, 4, 3.2, 1.5); inner.position.set(0, 1.25, 0.35); scene.add(inner);

  const all = new THREE.Group(); scene.add(all);

  /* Socle noir avec anneau or rose */
  const blackMat = new THREE.MeshPhysicalMaterial({ color: 0x0f0d0e, roughness: 0.28, metalness: 0.2, clearcoat: 1, clearcoatRoughness: 0.12 });
  const goldMat = new THREE.MeshPhysicalMaterial({ color: 0xe9b7a7, roughness: 0.22, metalness: 1 });
  const base = new THREE.Mesh(new THREE.CylinderGeometry(1.08, 1.2, 0.36, 96), blackMat); base.position.y = 0.18;
  const ring = new THREE.Mesh(new THREE.TorusGeometry(1.1, 0.022, 16, 128), goldMat); ring.rotation.x = Math.PI / 2; ring.position.y = 0.3;
  const foot = new THREE.Mesh(new THREE.TorusGeometry(1.19, 0.018, 16, 128), goldMat); foot.rotation.x = Math.PI / 2; foot.position.y = 0.02;
  all.add(base, ring, foot);

  /* Pétale : surface bombée dont la pointe s'enroule vers l'extérieur */
  function petalGeo(w, h, cup, curl) {
    const g = new THREE.PlaneGeometry(1, 1, 14, 16);
    const p = g.attributes.position;
    for (let i = 0; i < p.count; i++) {
      const x = p.getX(i), y = p.getY(i) + 0.5;
      const taper = Math.pow(Math.sin(Math.PI * (0.07 + 0.83 * Math.pow(y, 0.6))), 0.5);
      const X = x * w * taper;
      const Z = -cup * X * X + curl * Math.pow(Math.max(0, y - 0.55), 2) * 3.2 - 0.04 * Math.sin(Math.PI * y);
      p.setXYZ(i, X, y * h, Z);
    }
    g.computeVertexNormals();
    return g;
  }

  const petalColors = ['#8e1240', '#b3205a', '#cc3a72', '#de5a8b', '#ea7aa2'].map(c => new THREE.Color(c));
  const petalMats = petalColors.map(c => new THREE.MeshPhysicalMaterial({
    color: c, roughness: 0.55, sheen: 0.55, sheenRoughness: 0.5, sheenColor: new THREE.Color('#ff8fb4'),
    side: THREE.DoubleSide, clearcoat: 0.15, clearcoatRoughness: 0.6,
  }));

  const rose = new THREE.Group();
  const N = 34;
  const tiltOf = t => 0.03 + 0.58 * Math.pow(t, 1.6);
  for (let i = 0; i < N; i++) {
    const t = i / (N - 1);
    const s = 0.28 + 0.86 * Math.pow(t, 0.85);
    const pivot = new THREE.Group();
    pivot.rotation.y = i * 2.39996;
    const petal = new THREE.Mesh(
      petalGeo(0.36 * s + 0.1, 0.32 * s + 0.17, 2.8 - 1.1 * t, 0.01 + 0.16 * t),
      petalMats[Math.min(4, Math.floor(t * 5))]
    );
    petal.position.set(0, -0.05 * t, 0.01 + 0.07 * t);
    petal.rotation.x = tiltOf(t);
    pivot.add(petal);
    rose.add(pivot);
  }
  const greenMat = new THREE.MeshPhysicalMaterial({ color: 0x1f3d27, roughness: 0.6, sheen: 0.2, sheenColor: new THREE.Color(0x6fa37a), side: THREE.DoubleSide });
  const sepal = new THREE.Mesh(new THREE.ConeGeometry(0.12, 0.22, 24), greenMat); sepal.rotation.x = Math.PI; sepal.position.y = -0.1;
  rose.add(sepal);
  rose.position.y = 1.5;
  if (reduce) rose.scale.setScalar(1.35);
  all.add(rose);

  const stem = new THREE.Mesh(new THREE.CylinderGeometry(0.022, 0.03, 1.28, 16), greenMat); stem.position.y = 0.98; all.add(stem);
  const leafGeo = petalGeo(0.3, 0.46, 0.6, 0.12);
  [[0.95, 0.9, 1.0], [0.75, -1.1, 3.9]].forEach(([y, tilt, rot]) => {
    const pv = new THREE.Group(); pv.position.y = y; pv.rotation.y = rot;
    const leaf = new THREE.Mesh(leafGeo, greenMat); leaf.rotation.x = Math.abs(tilt); leaf.rotation.z = tilt > 0 ? 0.2 : -0.2;
    pv.add(leaf); all.add(pv);
  });
  // pétales tombés sur le socle
  [[0.45, 0.2, 0.6], [-0.35, 0.45, 2.1], [0.15, -0.5, 4.2]].forEach(([x, z, r]) => {
    const fp = new THREE.Mesh(petalGeo(0.2, 0.26, 1.2, 0.2), petalMats[3]);
    fp.position.set(x, 0.37, z); fp.rotation.set(-Math.PI / 2 + 0.25, r, 0); all.add(fp);
  });

  /* Guirlande lumineuse : petites LED et halo (sans post-traitement) */
  const gc = document.createElement('canvas'); gc.width = gc.height = 64;
  const gx = gc.getContext('2d'); const grad = gx.createRadialGradient(32, 32, 0, 32, 32, 32);
  grad.addColorStop(0, 'rgba(255,240,215,1)'); grad.addColorStop(0.25, 'rgba(255,210,170,.55)'); grad.addColorStop(1, 'rgba(255,190,160,0)');
  gx.fillStyle = grad; gx.fillRect(0, 0, 64, 64);
  const glowTex = new THREE.CanvasTexture(gc);
  const leds = [];
  const ledCount = mobile ? 16 : 22;
  for (let i = 0; i < ledCount; i++) {
    const a = i / ledCount;
    const sp = new THREE.Sprite(new THREE.SpriteMaterial({ map: glowTex, blending: THREE.AdditiveBlending, depthWrite: false, transparent: true }));
    const ang = a * Math.PI * 7, rad = 0.8 + 0.06 * Math.sin(a * 9);
    sp.position.set(Math.cos(ang) * rad, 0.45 + a * 2.1, Math.sin(ang) * rad);
    sp.scale.setScalar(0.14);
    sp.userData.phase = Math.random() * Math.PI * 2;
    leds.push(sp); all.add(sp);
  }
  const halo = new THREE.Sprite(new THREE.SpriteMaterial({ map: glowTex, color: 0xff7fa6, blending: THREE.AdditiveBlending, depthWrite: false, transparent: true, opacity: 0.55 }));
  halo.scale.setScalar(2.4); halo.position.set(0, 1.6, -0.3); all.add(halo);

  /* Cloche en verre */
  // verre : reflets très légers + liseré lumineux sur les bords (effet de Fresnel)
  const glass = new THREE.MeshPhysicalMaterial({
    color: 0xffffff, roughness: 0.04, metalness: 0, transparent: true, opacity: 0.08,
    clearcoat: 1, clearcoatRoughness: 0.02, envMapIntensity: 2.2, depthWrite: false,
  });
  const rimMat = new THREE.ShaderMaterial({
    transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, side: THREE.DoubleSide,
    uniforms: { tint: { value: new THREE.Color(0xffe3ec) } },
    vertexShader: 'varying vec3 vN; varying vec3 vV; void main(){ vec4 mv = modelViewMatrix * vec4(position,1.0); vN = normalize(normalMatrix * normal); vV = normalize(-mv.xyz); gl_Position = projectionMatrix * mv; }',
    fragmentShader: 'uniform vec3 tint; varying vec3 vN; varying vec3 vV; void main(){ float f = pow(1.0 - abs(dot(vN, vV)), 3.0); gl_FragColor = vec4(tint * f * 0.9, f * 0.9); }',
  });
  const domeH = 2.35, domeR = 0.98;
  const tube = new THREE.Mesh(new THREE.CylinderGeometry(domeR, domeR, domeH, 96, 1, true), glass); tube.position.y = 0.36 + domeH / 2;
  const cap = new THREE.Mesh(new THREE.SphereGeometry(domeR, 96, 32, 0, Math.PI * 2, 0, Math.PI / 2), glass); cap.position.y = 0.36 + domeH;
  const knob = new THREE.Mesh(new THREE.SphereGeometry(0.09, 32, 16), goldMat); knob.position.y = 0.36 + domeH + domeR + 0.05;
  const tubeRim = new THREE.Mesh(tube.geometry, rimMat); tubeRim.position.copy(tube.position);
  const capRim = new THREE.Mesh(cap.geometry, rimMat); capRim.position.copy(cap.position);
  tube.renderOrder = cap.renderOrder = tubeRim.renderOrder = capRim.renderOrder = 2;
  all.add(tube, cap, tubeRim, capRim, knob);

  /* Pétales qui flottent autour de la cloche */
  const floaters = [];
  for (let i = 0; i < (mobile ? 5 : 9); i++) {
    const fp = new THREE.Mesh(petalGeo(0.16, 0.22, 1.3, 0.25), petalMats[2 + (i % 3)]);
    fp.userData = { r: 1.5 + Math.random() * 0.9, a: Math.random() * Math.PI * 2, y: Math.random() * 3.4, sp: 0.15 + Math.random() * 0.2, spin: Math.random() * 2 };
    floaters.push(fp); all.add(fp);
  }

  function resize() {
    const w = canvas.clientWidth, h = canvas.clientHeight;
    if (!w || !h) return;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.position.z = w / h < 0.8 ? 10.5 : 9.2;
    camera.updateProjectionMatrix();
  }
  resize();
  new ResizeObserver(resize).observe(canvas);

  const pointer = { x: 0, y: 0, tx: 0, ty: 0 };
  addEventListener('pointermove', e => { pointer.tx = (e.clientX / innerWidth) * 2 - 1; pointer.ty = (e.clientY / innerHeight) * 2 - 1; }, { passive: true });

  let visible = true;
  new IntersectionObserver(([e]) => { visible = e.isIntersecting; }).observe(canvas);

  // Ouverture : la rose s'épanouit au chargement
  const bloom = { v: reduce ? 1 : 0 };
  const start = performance.now();
  const clock = new THREE.Clock();

  function frame() {
    requestAnimationFrame(frame);
    if (!visible || document.hidden) return;
    const t = clock.getElapsedTime();
    if (!reduce) {
      bloom.v = Math.min(1, (performance.now() - start) / 2200);
      const e = 1 - Math.pow(1 - bloom.v, 3);
      rose.scale.setScalar(0.8 + 0.55 * e);
      rose.children.forEach((pv, i) => { const p = pv.children[0]; if (p && pv !== sepal) p.rotation.x = tiltOf(i / (N - 1)) * (0.3 + 0.7 * e); });
      pointer.x += (pointer.tx - pointer.x) * 0.05; pointer.y += (pointer.ty - pointer.y) * 0.05;
      all.rotation.y = t * 0.18 + pointer.x * 0.5;
      all.rotation.x = pointer.y * 0.06;
      rose.rotation.z = Math.sin(t * 0.7) * 0.025;
      leds.forEach(l => { const k = 0.6 + 0.4 * Math.sin(t * 2.2 + l.userData.phase); l.material.opacity = k; l.scale.setScalar(0.1 + 0.05 * k); });
      inner.intensity = 4 + Math.sin(t * 1.3) * 0.8;
      floaters.forEach(f => {
        const d = f.userData; d.y -= d.sp * 0.008; if (d.y < -0.2) d.y = 3.6;
        d.a += 0.002;
        f.position.set(Math.cos(d.a) * d.r, d.y, Math.sin(d.a) * d.r);
        f.rotation.set(t * d.sp + d.spin, t * 0.5 + d.spin, 0.3);
      });
    }
    renderer.render(scene, camera);
  }
  renderer.compile(scene, camera);
  frame();
  return { setTint(hex) { const c = new THREE.Color(hex); petalMats.forEach((m, i) => m.color.copy(c).offsetHSL(0, 0, (i - 2) * 0.06)); } };
}
