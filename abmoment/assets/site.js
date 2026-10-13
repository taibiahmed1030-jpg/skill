// Menu mobile, apparitions au scroll, et montage des scènes 3D
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

const logos = document.querySelectorAll('canvas[data-3d="logo"]');
if (logos.length) {
  const load = () => import('./logo3d.js').then(m => logos.forEach(c => m.mountLogo(c, { reduce, mobile }))).catch(() => {});
  'requestIdleCallback' in window ? requestIdleCallback(load, { timeout: 800 }) : setTimeout(load, 150);
}

// Modèle anatomique : chargé quand on approche de la section, puis piloté par la zone lue
const anat = document.querySelector('canvas[data-3d="anatomy"]');
if (anat) {
  const box = anat.parentElement;
  const zones = document.querySelectorAll('.zone');
  let api = null, current = -1;
  const zio = new IntersectionObserver(es => es.forEach(e => {
    if (!e.isIntersecting) return;
    current = +e.target.dataset.region;
    zones.forEach(z => z.classList.toggle('on', z === e.target));
    api?.setZone(current);
  }), { rootMargin: mobile ? '-62% 0px -22% 0px' : '-45% 0px -45% 0px' });
  zones.forEach(z => zio.observe(z));
  const near = new IntersectionObserver(([e], o) => {
    if (!e.isIntersecting) return; o.disconnect();
    import('./anatomy3d.js').then(m => m.mountAnatomy(anat, { reduce, mobile, onReady: () => box.classList.add('ready') }))
      .then(a => { api = a; if (current >= 0) api?.setZone(current); }).catch(() => {});
  }, { rootMargin: '800px 0px' });
  near.observe(anat);
}
