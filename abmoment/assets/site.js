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

// Corps anatomique 3D : chargé après l'affichage, quand il approche de l'écran
const bodies = document.querySelectorAll('[data-body3d]');
const zbtns = document.querySelectorAll('.zbtn');
let zoneApi = null, cur = 0, auto = !reduce, timer;
const showZone = i => {
  cur = i;
  zbtns.forEach(b => b.setAttribute('aria-pressed', String(+b.dataset.z === i)));
  zoneApi?.setZone(i, zbtns[i].dataset.v === 'b');
};
zbtns.forEach(b => {
  b.addEventListener('click', () => { auto = false; showZone(+b.dataset.z); });
  b.addEventListener('pointerenter', e => { if (e.pointerType === 'mouse') { auto = false; showZone(+b.dataset.z); } });
});
const zones2 = document.querySelector('.zones2');
if (zones2) new IntersectionObserver(([e]) => {
  clearInterval(timer);
  if (e.isIntersecting) timer = setInterval(() => auto && showZone((cur + 1) % zbtns.length), 3200);
}, { threshold: .3 }).observe(zones2);

const webgl = (() => { try { return !!document.createElement('canvas').getContext('webgl2'); } catch { return false; } })();
bodies.forEach(box => {
  if (!webgl) return;
  const zones = box.dataset.body3d === 'zones';
  new IntersectionObserver(([e], o) => {
    if (!e.isIntersecting) return; o.disconnect();
    import('./body3d.js').then(m => m.mountBody(box.querySelector('canvas'), { reduce, onReady: () => box.classList.add('ready') }))
      .then(api => { if (zones) { zoneApi = api; showZone(cur); } })
      .catch(() => {});
  }, { rootMargin: '300px 0px' }).observe(box);
  box.addEventListener('touched', () => { box.classList.add('touched'); if (zones) auto = false; });
});
