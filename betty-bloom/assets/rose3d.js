// Rose éternelle sous cloche, entièrement générée en 3D (aucun modèle externe)
import * as THREE from 'three';
import { RoomEnvironment } from './vendor/RoomEnvironment.js';

export function mountRose(canvas, { reduce = false, mobile = false } = {}) {
  let renderer;
  try { renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true, powerPreference: 'high-performance' }); }
  catch (e) { return null; }
  renderer.setPixelRatio(Math.min(devicePixelRatio, mobile ? 1.6 : 2));
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.1;
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;

  const scene = new THREE.Scene();
  const pmrem = new THREE.PMREMGenerator(renderer);
  scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
  scene.environmentIntensity = 0.4;
  pmrem.dispose();

  const camera = new THREE.PerspectiveCamera(26, 1, 0.1, 50);
  camera.position.set(0, 3.1, 9.4);
  camera.lookAt(0, 1.5, 0);

  // Éclairage : lumière chaude principale (avec ombres douces), contre-jour rose, lueur intérieure
  scene.add(new THREE.HemisphereLight(0xfff0f4, 0x1a0e12, 0.2));
  const key = new THREE.DirectionalLight(0xfff2e8, 2.1);
  key.position.set(-2.5, 6, 3.5);
  key.castShadow = true;
  key.shadow.mapSize.set(mobile ? 512 : 1024, mobile ? 512 : 1024);
  Object.assign(key.shadow.camera, { left: -1.6, right: 1.6, top: 3, bottom: -0.2, near: 1, far: 14 });
  key.shadow.radius = 6; key.shadow.bias = -0.0005;
  scene.add(key);
  const rim = new THREE.DirectionalLight(0xffb8cf, 2.2); rim.position.set(3, 3.5, -4); scene.add(rim);
  const fill = new THREE.DirectionalLight(0xffe4ec, 0.6); fill.position.set(3, 1, 5); scene.add(fill);
  const inner = new THREE.PointLight(0xff7fa6, 3, 2.6, 1.6); inner.position.set(0, 1.9, 0.5); scene.add(inner);

  const all = new THREE.Group(); scene.add(all);
  let seed = 7; const rnd = () => ((seed = (seed * 16807) % 2147483647) / 2147483647);

  /* ---------- Socle noir laqué, anneaux or rose ---------- */
  const blackMat = new THREE.MeshPhysicalMaterial({ color: 0x0f0d0e, roughness: 0.25, metalness: 0.15, clearcoat: 1, clearcoatRoughness: 0.08 });
  const topMat = new THREE.MeshPhysicalMaterial({ color: 0x151213, roughness: 0.55, metalness: 0.1 });
  const goldMat = new THREE.MeshPhysicalMaterial({ color: 0xe9b7a7, roughness: 0.2, metalness: 1 });
  const base = new THREE.Mesh(new THREE.CylinderGeometry(1.08, 1.2, 0.36, 128), blackMat); base.position.y = 0.18;
  const top = new THREE.Mesh(new THREE.CircleGeometry(1.0, 96), topMat); top.rotation.x = -Math.PI / 2; top.position.y = 0.362; top.receiveShadow = true;
  const ring = new THREE.Mesh(new THREE.TorusGeometry(1.1, 0.022, 16, 160), goldMat); ring.rotation.x = Math.PI / 2; ring.position.y = 0.3;
  const foot = new THREE.Mesh(new THREE.TorusGeometry(1.19, 0.018, 16, 160), goldMat); foot.rotation.x = Math.PI / 2; foot.position.y = 0.02;
  all.add(base, top, ring, foot);

  /* ---------- Pétale : large, arrondi, creusé, bords qui s'enroulent ---------- */
  const cA = new THREE.Color(), cB = new THREE.Color(), cV = new THREE.Color();
  function petalGeo({ w, h, cup, curl, roll, baseCol, tipCol }) {
    const g = new THREE.PlaneGeometry(1, 1, 20, 24);
    g.translate(0, 0.5, 0);
    const p = g.attributes.position, colors = new Float32Array(p.count * 3);
    cA.set(baseCol); cB.set(tipCol);
    for (let i = 0; i < p.count; i++) {
      const x = p.getX(i), y = p.getY(i), ax = Math.abs(2 * x);
      const prof = Math.sqrt(Math.max(0, 1 - Math.pow((y - 0.62) / 0.64, 2)));   // étroit à la base, large et arrondi en haut
      const X = x * w * (0.25 + 0.75 * prof);
      const Y = y * h * (1 - 0.34 * Math.pow(ax, 2) * Math.pow(y, 2.5));        // coins arrondis
      const Z = -cup * X * X                                                    // creux qui enveloppe le coeur
        + curl * Math.pow(y, 2.6) * h                                           // la pointe s'ouvre vers l'extérieur
        + roll * ax * ax * Math.pow(y, 2.2) * h                                 // les bords se retournent
        + 0.012 * Math.sin(y * 9 + x * 6) * y;                                  // petites ondulations naturelles
      p.setXYZ(i, X, Y, Z);
      const k = THREE.MathUtils.smoothstep(y, 0.05, 0.85);
      cV.copy(cA).lerp(cB, k).multiplyScalar(1 - 0.12 * Math.pow(ax, 3) * y);  // bords légèrement plus foncés
      colors.set([cV.r, cV.g, cV.b], i * 3);
    }
    g.setAttribute('color', new THREE.BufferAttribute(colors, 3));
    g.computeVertexNormals();
    return g;
  }

  const petalMat = new THREE.MeshPhysicalMaterial({
    vertexColors: true, roughness: 0.58, sheen: 0.35, sheenRoughness: 0.5, sheenColor: new THREE.Color('#ff7aa3'),
    side: THREE.DoubleSide, emissive: new THREE.Color('#3a0718'), emissiveIntensity: 0.4,
  });

  /* ---------- La rose : bouton serré en spirale, puis pétales qui s'ouvrent ---------- */
  const rose = new THREE.Group();
  const N = 32, petals = [];
  const lerp = THREE.MathUtils.lerp;
  for (let i = 0; i < N; i++) {
    const t = i / (N - 1), j = 0.92 + rnd() * 0.16;
    const pivot = new THREE.Group();
    pivot.rotation.y = i * 2.39996 + rnd() * 0.25;
    const geo = petalGeo({
      w: (0.2 + 0.46 * Math.pow(t, 0.85)) * j,
      h: (0.36 + 0.24 * Math.pow(t, 0.7)) * j,
      cup: lerp(5.4, 2.1, Math.pow(t, 0.6)),
      curl: lerp(-0.02, 0.26, Math.pow(t, 1.4)),
      roll: lerp(0, 0.22, Math.max(0, t - 0.3) / 0.7),
      baseCol: t < 0.3 ? '#d9406f' : '#f19ab6',
      tipCol: t < 0.3 ? '#9c1242' : t < 0.65 ? '#d0336a' : '#e2588a',
    });
    const petal = new THREE.Mesh(geo, petalMat);
    petal.castShadow = true;
    petal.position.set(0, -0.08 * t, lerp(0.004, 0.085, t));
    petal.rotation.z = (rnd() - 0.5) * 0.14;
    petal.userData.tilt = lerp(0.0, 0.74, Math.pow(t, 1.8)) + (rnd() - 0.5) * 0.06;
    petal.rotation.x = petal.userData.tilt;
    pivot.add(petal); rose.add(pivot); petals.push(petal);
  }

  /* ---------- Sépales, tige courbée, épines, feuilles dentelées ---------- */
  const greenMat = new THREE.MeshPhysicalMaterial({ vertexColors: true, roughness: 0.55, sheen: 0.3, sheenColor: new THREE.Color(0x8fc79b), side: THREE.DoubleSide });
  function leafGeo(len, wid, fold, bend, c1 = '#2f6a3c', c2 = '#1d4526') {
    const g = new THREE.PlaneGeometry(1, 1, 12, 20); g.translate(0, 0.5, 0);
    const p = g.attributes.position, colors = new Float32Array(p.count * 3);
    cA.set(c1); cB.set(c2);
    for (let i = 0; i < p.count; i++) {
      const x = p.getX(i), y = p.getY(i), ax = Math.abs(2 * x);
      const prof = Math.pow(Math.sin(Math.PI * Math.min(1, y * 1.02)), 0.8) * (1 + 0.07 * Math.sin(y * 46) * ax);
      const X = x * wid * prof;
      p.setXYZ(i, X, y * len, -Math.abs(X) * fold + bend * y * y * len);
      cV.copy(cA).lerp(cB, ax * 0.8); colors.set([cV.r, cV.g, cV.b], i * 3);
    }
    g.setAttribute('color', new THREE.BufferAttribute(colors, 3));
    g.computeVertexNormals();
    return g;
  }
  const sepalGeo = leafGeo(0.3, 0.09, 0.6, 0.4, '#3d7a47', '#24502d');
  for (let i = 0; i < 5; i++) {
    const pv = new THREE.Group(); pv.rotation.y = i * (Math.PI * 2 / 5) + 0.3;
    const s = new THREE.Mesh(sepalGeo, greenMat); s.position.set(0, -0.06, 0.05); s.rotation.x = 2.1 + rnd() * 0.3; s.castShadow = true;
    pv.add(s); rose.add(pv);
  }
  const hip = new THREE.Mesh(new THREE.SphereGeometry(0.09, 24, 16), greenMat); hip.scale.set(1, 1.2, 1); hip.position.y = -0.1;
  const hipGeo = hip.geometry; const hc = new Float32Array(hipGeo.attributes.position.count * 3).fill(0); for (let i = 0; i < hc.length; i += 3) { hc[i] = 0.2; hc[i + 1] = 0.42; hc[i + 2] = 0.25; }
  hipGeo.setAttribute('color', new THREE.BufferAttribute(hc, 3));
  rose.add(hip);
  rose.position.set(0.02, 1.66, 0);
  all.add(rose);

  const stemCurve = new THREE.CatmullRomCurve3([
    new THREE.Vector3(0, 0.36, 0), new THREE.Vector3(0.05, 0.75, 0.02), new THREE.Vector3(-0.03, 1.15, -0.01), new THREE.Vector3(0.02, 1.52, 0),
  ]);
  const stemGeo = new THREE.TubeGeometry(stemCurve, 48, 0.03, 12, false);
  const sc = new Float32Array(stemGeo.attributes.position.count * 3); for (let i = 0; i < sc.length; i += 3) { sc[i] = 0.1; sc[i + 1] = 0.24; sc[i + 2] = 0.13; }
  stemGeo.setAttribute('color', new THREE.BufferAttribute(sc, 3));
  const stem = new THREE.Mesh(stemGeo, greenMat); stem.castShadow = true; all.add(stem);
  const thornMat = new THREE.MeshPhysicalMaterial({ color: 0x5a3b2c, roughness: 0.5 });
  [[0.62, 0.4], [0.9, 2.6], [1.2, 4.4], [1.38, 1.3]].forEach(([u, a]) => {
    const pt = stemCurve.getPoint((u - 0.36) / 1.16);
    const th = new THREE.Mesh(new THREE.ConeGeometry(0.014, 0.07, 8), thornMat);
    th.position.set(pt.x + Math.cos(a) * 0.026, pt.y, pt.z + Math.sin(a) * 0.026);
    th.rotation.set(Math.sin(a) * 1.2, 0, -Math.cos(a) * 1.2 - 0.3); all.add(th);
  });
  const leafG = leafGeo(0.5, 0.28, 0.35, 0.2);
  const smallLeafG = leafGeo(0.36, 0.2, 0.35, 0.16);
  [[0.8, 0.9, 1], [1.05, 3.9, -1]].forEach(([y, rot, side]) => {
    const pv = new THREE.Group(); pv.position.y = y; pv.rotation.y = rot;
    const petiole = new THREE.Mesh(new THREE.CylinderGeometry(0.008, 0.01, 0.18, 6), new THREE.MeshStandardMaterial({ color: 0x2b5a35, roughness: 0.6 })); petiole.rotation.z = -1.0 * side; petiole.position.set(0.07 * side, 0.04, 0);
    pv.add(petiole);
    [[0, 0, leafG], [0.6, 0.12, smallLeafG], [-0.6, 0.12, smallLeafG]].forEach(([spread, off, g]) => {
      const l = new THREE.Mesh(g, greenMat);
      l.position.set(0.14 * side + off * 0.3 * side, 0.08 + off * 0.2, 0);
      l.rotation.set(0.3, 0, -1.25 * side + spread * 0.6); l.castShadow = true;
      pv.add(l);
    });
    all.add(pv);
  });
  // pétales tombés sur le socle
  const fallenMat = petalMat;
  [[0.48, 0.18, 0.6], [-0.4, 0.42, 2.1], [0.12, -0.52, 4.2], [-0.55, -0.2, 5.3]].forEach(([x, z, r], i) => {
    const fp = new THREE.Mesh(petalGeo({ w: 0.24, h: 0.28, cup: 1.4, curl: 0.25, roll: 0.3, baseCol: '#f19ab6', tipCol: i % 2 ? '#c92f62' : '#e2588a' }), fallenMat);
    fp.position.set(x, 0.38, z); fp.rotation.set(-Math.PI / 2 + 0.2, r, 0); fp.castShadow = true; all.add(fp);
  });

  /* ---------- Guirlande lumineuse et halo (sans post-traitement) ---------- */
  const gc = document.createElement('canvas'); gc.width = gc.height = 64;
  const gx = gc.getContext('2d'); const grad = gx.createRadialGradient(32, 32, 0, 32, 32, 32);
  grad.addColorStop(0, 'rgba(255,244,222,1)'); grad.addColorStop(0.22, 'rgba(255,214,176,.6)'); grad.addColorStop(1, 'rgba(255,190,160,0)');
  gx.fillStyle = grad; gx.fillRect(0, 0, 64, 64);
  const glowTex = new THREE.CanvasTexture(gc);
  const leds = [];
  const ledCount = mobile ? 16 : 24;
  for (let i = 0; i < ledCount; i++) {
    const a = i / ledCount;
    const sp = new THREE.Sprite(new THREE.SpriteMaterial({ map: glowTex, blending: THREE.AdditiveBlending, depthWrite: false, transparent: true }));
    const ang = a * Math.PI * 7, rad = 0.82 + 0.05 * Math.sin(a * 9);
    sp.position.set(Math.cos(ang) * rad, 0.5 + a * 2.2, Math.sin(ang) * rad);
    sp.userData.phase = rnd() * Math.PI * 2;
    leds.push(sp); all.add(sp);
  }
  const halo = new THREE.Sprite(new THREE.SpriteMaterial({ map: glowTex, color: 0xff6f9c, blending: THREE.AdditiveBlending, depthWrite: false, transparent: true, opacity: 0.45 }));
  halo.scale.setScalar(2.6); halo.position.set(0, 1.7, -0.5); all.add(halo);

  /* ---------- Cloche en verre : reflets légers, liseré et reflets verticaux ---------- */
  const glass = new THREE.MeshPhysicalMaterial({
    color: 0xffffff, roughness: 0.03, metalness: 0, transparent: true, opacity: 0.07,
    clearcoat: 1, clearcoatRoughness: 0.02, envMapIntensity: 2.4, depthWrite: false,
  });
  const rimMat = new THREE.ShaderMaterial({
    transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, side: THREE.DoubleSide,
    uniforms: { tint: { value: new THREE.Color(0xffe6ee) } },
    vertexShader: 'varying vec3 vN; varying vec3 vV; void main(){ vec4 mv = modelViewMatrix * vec4(position,1.0); vN = normalize(normalMatrix * normal); vV = normalize(-mv.xyz); gl_Position = projectionMatrix * mv; }',
    fragmentShader: `uniform vec3 tint; varying vec3 vN; varying vec3 vV;
      void main(){
        float f = pow(1.0 - abs(dot(vN, vV)), 3.0) * 0.85;
        float streak = pow(max(0.0, vN.x * 0.9 + vN.y * 0.1), 60.0) * 0.55 + pow(max(0.0, -vN.x), 90.0) * 0.25;
        float a = f + streak;
        gl_FragColor = vec4(tint * a, a);
      }`,
  });
  const domeH = 2.4, domeR = 0.98;
  const tube = new THREE.Mesh(new THREE.CylinderGeometry(domeR, domeR, domeH, 128, 1, true), glass); tube.position.y = 0.36 + domeH / 2;
  const cap = new THREE.Mesh(new THREE.SphereGeometry(domeR, 128, 40, 0, Math.PI * 2, 0, Math.PI / 2), glass); cap.position.y = 0.36 + domeH;
  const tubeRim = new THREE.Mesh(tube.geometry, rimMat); tubeRim.position.copy(tube.position);
  const capRim = new THREE.Mesh(cap.geometry, rimMat); capRim.position.copy(cap.position);
  const knob = new THREE.Mesh(new THREE.SphereGeometry(0.09, 32, 16), goldMat); knob.position.y = 0.36 + domeH + domeR + 0.05;
  tube.renderOrder = cap.renderOrder = tubeRim.renderOrder = capRim.renderOrder = 2;
  all.add(tube, cap, tubeRim, capRim, knob);

  /* ---------- Pétales qui flottent autour de la cloche ---------- */
  const floaters = [];
  for (let i = 0; i < (mobile ? 5 : 9); i++) {
    const fp = new THREE.Mesh(petalGeo({ w: 0.18, h: 0.22, cup: 1.5, curl: 0.2, roll: 0.25, baseCol: '#f19ab6', tipCol: '#d0336a' }), petalMat);
    fp.userData = { r: 1.5 + rnd() * 0.9, a: rnd() * Math.PI * 2, y: rnd() * 3.4, sp: 0.15 + rnd() * 0.2, spin: rnd() * 2 };
    floaters.push(fp); all.add(fp);
  }

  function resize() {
    const w = canvas.clientWidth, h = canvas.clientHeight;
    if (!w || !h) return;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.position.z = w / h < 0.8 ? 11 : 9.4;
    camera.updateProjectionMatrix();
  }
  resize();
  new ResizeObserver(resize).observe(canvas);

  const pointer = { x: 0, y: 0, tx: 0, ty: 0 };
  addEventListener('pointermove', e => { pointer.tx = (e.clientX / innerWidth) * 2 - 1; pointer.ty = (e.clientY / innerHeight) * 2 - 1; }, { passive: true });

  let visible = true;
  new IntersectionObserver(([e]) => { visible = e.isIntersecting; }).observe(canvas);

  const start = performance.now();
  const clock = new THREE.Clock();
  if (reduce) rose.scale.setScalar(1.3);

  function frame() {
    requestAnimationFrame(frame);
    if (!visible || document.hidden) return;
    const t = clock.getElapsedTime();
    if (!reduce) {
      // Ouverture de la rose au chargement
      const e = 1 - Math.pow(1 - Math.min(1, (performance.now() - start) / 2600), 3);
      rose.scale.setScalar(1.0 + 0.3 * e);
      petals.forEach(p => { p.rotation.x = p.userData.tilt * (0.25 + 0.75 * e) + Math.sin(t * 0.9 + p.parent.rotation.y) * 0.012; });
      pointer.x += (pointer.tx - pointer.x) * 0.05; pointer.y += (pointer.ty - pointer.y) * 0.05;
      all.rotation.y = t * 0.16 + pointer.x * 0.5;
      all.rotation.x = pointer.y * 0.05;
      rose.rotation.z = Math.sin(t * 0.7) * 0.02;
      leds.forEach(l => { const k = 0.55 + 0.45 * Math.sin(t * 2.2 + l.userData.phase); l.material.opacity = k; l.scale.setScalar(0.09 + 0.05 * k); });
      inner.intensity = 3 + Math.sin(t * 1.3) * 0.6;
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
  return {};
}
