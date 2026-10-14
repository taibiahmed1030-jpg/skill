// Menu mobile et apparitions au scroll
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
const mobile = matchMedia('(max-width: 960px)').matches;

const mnav = document.getElementById('mnav');
const menuBtn = document.querySelector('.menu-btn');
function setMenu(open) {
  mnav.classList.toggle('open', open);
  menuBtn.setAttribute('aria-expanded', String(open));
  document.body.style.overflow = open ? 'hidden' : '';
  if (open) mnav.querySelector('a').focus(); else menuBtn.focus({ preventScroll: true });
}
menuBtn?.addEventListener('click', () => setMenu(true));
mnav?.querySelector('.mnav-close').addEventListener('click', () => setMenu(false));
mnav?.querySelectorAll('a').forEach(a => a.addEventListener('click', () => setMenu(false)));
addEventListener('keydown', e => { if (e.key === 'Escape' && mnav?.classList.contains('open')) setMenu(false); });

if (!reduce) {
  const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }), { threshold: 0.12 });
  document.querySelectorAll('.rv').forEach(el => io.observe(el));
} else document.querySelectorAll('.rv').forEach(el => el.classList.add('in'));

// Cerveau : légère profondeur qui suit la souris et le scroll
const tilts = [...document.querySelectorAll('[data-tilt]')];
if (tilts.length && !reduce) {
  const fine = matchMedia('(pointer: fine)').matches;
  let mx = 0, my = 0;
  if (fine) addEventListener('pointermove', e => { mx = e.clientX / innerWidth - .5; my = e.clientY / innerHeight - .5; }, { passive: true });
  const st = tilts.map(el => ({ el, inner: el.firstElementChild, glow: el.querySelector('.brain-glow'), rx: 0, ry: 0 }));
  const tick = t => {
    for (const s of st) {
      const r = s.el.getBoundingClientRect();
      if (r.bottom < 0 || r.top > innerHeight) continue;
      const p = (r.top + r.height / 2) / innerHeight - .5;
      const tx = fine ? my * -8 : Math.sin(t / 2600) * 3, ty = fine ? mx * 14 : Math.sin(t / 3200) * 8;
      s.rx += (tx + p * 6 - s.rx) * .06; s.ry += (ty - s.ry) * .06;
      s.inner.style.setProperty('--rx', s.rx.toFixed(2) + 'deg');
      s.inner.style.setProperty('--ry', s.ry.toFixed(2) + 'deg');
      s.inner.style.setProperty('--ty', (Math.sin(t / 1400) * 6).toFixed(1) + 'px');
      if (s.glow) { s.glow.style.setProperty('--gx', (50 + Math.sin(t / 1700) * 30).toFixed(1) + '%'); s.glow.style.setProperty('--gy', (45 + Math.cos(t / 2300) * 20).toFixed(1) + '%'); }
    }
    requestAnimationFrame(tick);
  };
  requestAnimationFrame(tick);
}

// Zones du corps : la zone choisie s'éclaire, défilement automatique tant qu'on n'a pas cliqué
const zbtns = document.querySelectorAll('.zbtn');
if (zbtns.length) {
  const spots = document.querySelectorAll('.spot'), zbody = document.querySelector('.zbody');
  let cur = 0, auto = !reduce, timer;
  const show = i => {
    cur = i;
    zbtns.forEach(b => b.setAttribute('aria-pressed', String(+b.dataset.z === i)));
    spots.forEach(s => s.classList.toggle('on', +s.dataset.z === i));
    zbody.classList.toggle('back', zbtns[i].dataset.v === 'b');
  };
  zbtns.forEach(b => {
    b.addEventListener('click', () => { auto = false; show(+b.dataset.z); });
    b.addEventListener('pointerenter', e => { if (e.pointerType === 'mouse') { auto = false; show(+b.dataset.z); } });
  });
  show(0);
  new IntersectionObserver(([e]) => {
    clearInterval(timer);
    if (e.isIntersecting) timer = setInterval(() => auto && show((cur + 1) % zbtns.length), 2600);
  }, { threshold: .3 }).observe(document.querySelector('.zones2'));
}

// Corps à 360° : images préparées, fondu entre deux vues voisines, rotation auto + glisser
const turn = document.querySelector('.turn');
if (turn) {
  const n = +turn.dataset.frames, base = turn.dataset.src, cv = turn.querySelector('canvas'), ctx = cv.getContext('2d');
  const imgs = Array.from({ length: n }, (_, i) => { const im = new Image(); im.decoding = 'async'; im.src = base + String(i).padStart(2, '0') + '.webp'; return im; });
  let pos = 0, vel = reduce ? 0 : n / 16, drag = null, last = performance.now(), idle = 0;
  // En rotation auto : courte pause sur chaque vue nette (face, 3/4, profil...), puis transition douce
  const K = 4, hold = .3, ease = x => x * x * x * (x * (x * 6 - 15) + 10);
  const shown = () => {
    if (drag || Math.abs(vel) > n / 10) return pos;
    const s = Math.floor(pos / K), f = pos / K - s;
    return (s + ease(Math.max(0, (f - hold) / (1 - hold)))) * K;
  };
  let disp = 0;
  const draw = () => {
    const q = disp, p = ((q % n) + n) % n, a = Math.floor(p), f = p - a, A = imgs[a], B = imgs[(a + 1) % n];
    ctx.globalAlpha = 1; ctx.drawImage(A, 0, 0, cv.width, cv.height);
    if (f > .01 && B.complete) { ctx.globalAlpha = f; ctx.drawImage(B, 0, 0, cv.width, cv.height); }
  };
  const loop = t => {
    const dt = Math.min(.05, (t - last) / 1000); last = t;
    if (!drag) {
      idle += dt;
      const auto = reduce ? 0 : n / 16;
      vel += ((idle > 1.2 ? auto : 0) - vel) * Math.min(1, dt * 2.5);
      pos += vel * dt;
    }
    disp += (shown() - disp) * Math.min(1, dt * (drag ? 25 : 8));
    draw(); requestAnimationFrame(loop);
  };
  Promise.all(imgs.map(im => im.decode().catch(() => {}))).then(() => {
    turn.classList.add('ready'); requestAnimationFrame(t => { last = t; loop(t); });
  });
  turn.addEventListener('pointerdown', e => { drag = { x: e.clientX, p: pos, t: e.timeStamp, lx: e.clientX }; turn.classList.add('drag', 'touched'); turn.setPointerCapture(e.pointerId); });
  turn.addEventListener('pointermove', e => {
    if (!drag) return;
    const k = n / turn.clientWidth * 1.1;
    pos = drag.p - (e.clientX - drag.x) * k;
    const dt = Math.max(1, e.timeStamp - drag.t) / 1000; vel = -(e.clientX - drag.lx) * k / dt; drag.t = e.timeStamp; drag.lx = e.clientX;
  });
  const end = () => { if (!drag) return; drag = null; idle = 0; turn.classList.remove('drag'); vel = Math.max(-n * 1.5, Math.min(n * 1.5, vel)); };
  turn.addEventListener('pointerup', end); turn.addEventListener('pointercancel', end);
}
