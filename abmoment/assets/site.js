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
