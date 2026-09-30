import { T } from './i18n.js';

const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
const store = {
  get(k, d) { try { const v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch (e) { return d; } },
  set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} },
};
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

/* ---------- Réglages de la boutique (à confirmer avec Betty Bloom) ---------- */
const CUTOFF_HOUR = 14; // commande avant 14 h = livraison le jour même
// Codes postaux livrés gratuitement : Bruxelles-Capitale + communes à environ 25 km
const ZONE = new Set([
  ...Array.from({ length: 300 }, (_, i) => String(1000 + i)),
  '1300','1310','1320','1330','1331','1332','1340','1341','1342','1380','1410','1420','1640','1650','1700','1701','1702','1703',
  '1730','1731','1740','1741','1745','1750','1755','1760','1761','1780','1785','1790','1800','1820','1830','1831','1840',
  '1850','1851','1852','1853','1860','1861','1880','1910','1930','1932','1933','1950','1970','1980','1981','1982',
  '2800','2812','2830','3000','3001','3010','3012','3018','3020','3060','3061','3070','3071','3078','3080',
]);

let lang = store.get('bb-lang', (navigator.language || 'fr').toLowerCase().startsWith('nl') ? 'nl' : 'fr');
let cart = store.get('bb-cart', []);
let C; // catalogue
const t = k => (T[lang] && T[lang][k]) ?? T.fr[k] ?? k;
const L = o => (o ? (o[lang] ?? o.fr) : '');
const money = n => new Intl.NumberFormat(lang === 'nl' ? 'nl-BE' : 'fr-BE', { style: 'currency', currency: 'EUR', minimumFractionDigits: n % 1 ? 2 : 0 }).format(n);
const product = id => C.products.find(p => p.id === id);
const extra = id => C.extras.find(e => e.id === id);

function unitPrice(it) {
  const ex = (it.extras || []).reduce((s, id) => s + (extra(id)?.price || 0), 0);
  if (it.id === 'custom') {
    const b = C.custom.bases.find(x => x.id === it.custom.base);
    return (b?.price || 0) + (C.custom.sizes[it.size] || 0) + ex;
  }
  return (product(it.id)?.sizes[it.size] || 0) + ex;
}
const minPrice = p => Math.min(...Object.values(p.sizes));
const cartTotal = () => cart.reduce((s, it) => s + unitPrice(it) * it.qty, 0);
function itemName(it) {
  if (it.id === 'custom') {
    const b = C.custom.bases.find(x => x.id === it.custom.base), c = C.custom.colors.find(x => x.id === it.custom.color);
    return `${t('custom_name')} : ${L(b)}, ${L(c).toLowerCase()}`;
  }
  return L(product(it.id));
}
const itemImg = it => it.id === 'custom' ? C.custom.bases.find(x => x.id === it.custom.base)?.img : product(it.id)?.img;
const itemDetail = it => [it.size !== 'u' ? L(C.sizes[it.size]) : '', ...(it.extras || []).map(id => L(extra(id)))].filter(Boolean).join(', ');

/* ---------- Langue ---------- */
function applyLang() {
  document.documentElement.lang = lang === 'nl' ? 'nl-BE' : 'fr-BE';
  $$('[data-i18n]').forEach(el => { el.textContent = t(el.dataset.i18n); });
  $$('[data-i18n-ph]').forEach(el => { el.placeholder = t(el.dataset.i18nPh); });
  $$('[data-i18n-aria]').forEach(el => { el.setAttribute('aria-label', t(el.dataset.i18nAria)); });
  $$('.lang button').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.lang === lang)));
  if (C) { renderCats(); renderShop(); renderFavs(); renderCart(); }
}
$$('.lang button').forEach(b => b.addEventListener('click', () => { lang = b.dataset.lang; store.set('bb-lang', lang); applyLang(); }));

/* ---------- Univers, boutique, coups de coeur ---------- */
let filter = 'all';
function renderCats() {
  $('#cats').innerHTML = C.categories.map(c => `
    <a class="cat" href="#boutique" data-cat="${c.id}">
      <img src="${c.img}" alt="" loading="lazy" width="460" height="224">
      <div class="cat-body"><h3>${esc(L(c))}</h3><p>${esc(lang === 'nl' ? c.dnl : c.dfr)}</p><span class="btn btn-pink btn-sm">${t('discover')}</span></div>
    </a>`).join('');
  $$('#cats .cat').forEach(a => a.addEventListener('click', () => { filter = a.dataset.cat; renderShop(); }));
  $$('[data-nav-cat]').forEach(a => { a.textContent = L(C.categories.find(c => c.id === a.dataset.navCat)); });
}
function card(p) {
  return `<article class="prod" data-id="${p.id}">
    <button class="prod-img" data-open="${p.id}" aria-label="${esc(L(p))}"><img src="${p.img}" alt="${esc(L(p))}" loading="lazy" width="430" height="410"></button>
    <div class="prod-body"><h3>${esc(L(p))}</h3><p>${t('from')} <strong>${money(minPrice(p))}</strong></p>
    <button class="btn btn-dark btn-sm" data-open="${p.id}">${t('choose')}</button></div></article>`;
}
function renderShop() {
  $('#tabs').innerHTML = [{ id: 'all' }, ...C.categories].map(c =>
    `<button role="tab" aria-selected="${filter === c.id}" data-f="${c.id}">${c.id === 'all' ? t('all') : esc(L(c))}</button>`).join('');
  $$('#tabs button').forEach(b => b.addEventListener('click', () => { filter = b.dataset.f; renderShop(); }));
  $('#grid').innerHTML = C.products.filter(p => filter === 'all' || p.cat === filter).map(card).join('');
  bindOpen($('#grid'));
}
function renderFavs() { $('#favs').innerHTML = C.products.filter(p => p.fav).map(card).join(''); bindOpen($('#favs')); }
function bindOpen(root) { $$('[data-open]', root).forEach(b => b.addEventListener('click', () => openProduct(b.dataset.open))); }

/* ---------- Fiche produit ---------- */
const pm = $('#pmodal');
function openProduct(id) {
  const p = product(id); if (!p) return;
  const sizes = Object.keys(p.sizes);
  pm.innerHTML = `
    <button class="x" data-close aria-label="${t('close')}"></button>
    <div class="pm-grid">
      <div class="pm-img"><img src="${p.img}" alt="${esc(L(p))}" width="430" height="410"></div>
      <form class="pm-body" method="dialog">
        <p class="eyebrow">${esc(L(C.categories.find(c => c.id === p.cat)))}</p>
        <h2>${esc(L(p))}</h2>
        <p class="pm-desc">${esc(lang === 'nl' ? p.dnl : p.dfr)}</p>
        ${sizes.length > 1 ? `<fieldset><legend>${t('size')}</legend><div class="chips">${sizes.map((s, i) =>
          `<label class="chip"><input type="radio" name="size" value="${s}" ${i === 0 ? 'checked' : ''}><span>${esc(L(C.sizes[s]))}<b>${money(p.sizes[s])}</b></span></label>`).join('')}</div></fieldset>`
          : `<input type="hidden" name="size" value="${sizes[0]}">`}
        <fieldset><legend>${t('extras_t')}</legend><div class="extras">${C.extras.map(e =>
          `<label class="ex"><input type="checkbox" name="extra" value="${e.id}"><span>${esc(L(e))}</span><b>+${money(e.price)}</b></label>`).join('')}</div></fieldset>
        <div class="pm-foot">
          <div class="qty"><button type="button" data-q="-1" aria-label="-">−</button><output name="q">1</output><button type="button" data-q="1" aria-label="+">+</button></div>
          <button class="btn btn-dark" type="submit"><span>${t('add')}</span> <span class="pm-price"></span></button>
        </div>
      </form>
    </div>`;
  const f = $('form', pm); let q = 1;
  const price = () => { const it = { id, size: f.size.value, extras: $$('input[name=extra]:checked', f).map(i => i.value) }; $('.pm-price', pm).textContent = money(unitPrice(it) * q); return it; };
  f.addEventListener('change', price);
  $$('[data-q]', pm).forEach(b => b.addEventListener('click', () => { q = Math.max(1, Math.min(20, q + +b.dataset.q)); f.q.value = q; price(); }));
  f.addEventListener('submit', e => { e.preventDefault(); addToCart({ ...price(), qty: q }); pm.close(); });
  price();
  pm.showModal();
}

/* ---------- Panier ---------- */
const drawer = $('#cart');
function addToCart(it) {
  it.extras = (it.extras || []).slice().sort();
  const key = JSON.stringify([it.id, it.size, it.extras, it.custom || null]);
  const found = cart.find(c => c.key === key);
  if (found) found.qty += it.qty; else cart.push({ ...it, key });
  store.set('bb-cart', cart); renderCart(); toast(t('toast_added')); bump();
}
function renderCart() {
  const n = cart.reduce((s, i) => s + i.qty, 0);
  $$('.cart-count').forEach(el => { el.textContent = n; el.hidden = n === 0; });
  const list = $('#cart-list');
  if (!cart.length) {
    list.innerHTML = `<div class="cart-empty"><p>${t('empty')}</p><a href="#boutique" class="btn btn-dark" data-close-cart>${t('empty_cta')}</a></div>`;
  } else {
    list.innerHTML = cart.map((it, i) => `
      <div class="line">
        <img src="${itemImg(it)}" alt="" width="72" height="72">
        <div class="line-body"><strong>${esc(itemName(it))}</strong><small>${esc(itemDetail(it))}</small>
          <div class="line-foot"><div class="qty sm"><button data-dq="${i}|-1" aria-label="-">−</button><output>${it.qty}</output><button data-dq="${i}|1" aria-label="+">+</button></div>
          <button class="link" data-rm="${i}">${t('remove')}</button></div></div>
        <b>${money(unitPrice(it) * it.qty)}</b>
      </div>`).join('');
  }
  $('#cart-sub').textContent = money(cartTotal());
  $('#cart-total').textContent = money(cartTotal());
  $('#go-checkout').disabled = !cart.length;
  $$('[data-dq]', list).forEach(b => b.addEventListener('click', () => {
    const [i, d] = b.dataset.dq.split('|').map(Number); cart[i].qty += d; if (cart[i].qty < 1) cart.splice(i, 1);
    store.set('bb-cart', cart); renderCart();
  }));
  $$('[data-rm]', list).forEach(b => b.addEventListener('click', () => { cart.splice(+b.dataset.rm, 1); store.set('bb-cart', cart); renderCart(); }));
  $$('[data-close-cart]', list).forEach(a => a.addEventListener('click', closeCart));
}
function openCart() { drawer.showModal(); }
function closeCart() { drawer.close(); }
$$('[data-open-cart]').forEach(b => b.addEventListener('click', openCart));
function bump() { $$('.cart-btn').forEach(b => { b.classList.remove('bump'); void b.offsetWidth; b.classList.add('bump'); }); }

/* ---------- Commande : réception, date, coordonnées, paiement ---------- */
const co = $('#checkout');
const order = store.get('bb-order', { mode: 'delivery', date: '', slot: 'am', recipient: {}, customer: {}, message: '', note: '' });
let coStep = 1;
function todayISO(d = new Date()) { const z = new Date(d.getTime() - d.getTimezoneOffset() * 60000); return z.toISOString().slice(0, 10); }
function minDate(mode) {
  const d = new Date(); if (d.getHours() >= CUTOFF_HOUR) d.setDate(d.getDate() + 1);
  if (mode === 'delivery' && d.getDay() === 0) d.setDate(d.getDate() + 1);
  return todayISO(d);
}
function fmtDate(iso) { return new Date(iso + 'T12:00').toLocaleDateString(lang === 'nl' ? 'nl-BE' : 'fr-BE', { weekday: 'long', day: 'numeric', month: 'long' }); }
const slotLabel = (s, iso) => s === 'pm' && iso && new Date(iso + 'T12:00').getDay() === 0 ? t('slot_pm_sun') : t('slot_' + s);

function openCheckout() { closeCart(); coStep = 1; renderCheckout(); co.showModal(); }
$('#go-checkout').addEventListener('click', openCheckout);

function field(name, label, value, attrs = '') {
  return `<div class="field"><label for="co-${name}">${label}</label><input id="co-${name}" name="${name}" value="${esc(value || '')}" ${attrs}></div>`;
}
function renderCheckout() {
  const steps = [t('cs1'), t('cs2'), t('cs3'), t('cs4')];
  const r = order.recipient, c = order.customer;
  let body = '';
  if (coStep === 1) body = `
    <div class="modes" role="radiogroup">
      ${['delivery', 'pickup'].map(m => `<label class="mode"><input type="radio" name="mode" value="${m}" ${order.mode === m ? 'checked' : ''}>
        <span><strong>${t('mode_' + m)}</strong><small>${t('mode_' + m + '_d')}</small></span><b>${t('free')}</b></label>`).join('')}
    </div>
    <div class="addr" ${order.mode === 'pickup' ? 'hidden' : ''}>
      <div class="row2">${field('rname', t('recip_name'), r.name, 'autocomplete="name"')}${field('rphone', t('recip_phone'), r.phone, 'type="tel" autocomplete="tel"')}</div>
      ${field('raddress', t('address'), r.address, 'autocomplete="street-address"')}
      <div class="row2">${field('rzip', t('zip'), r.zip, 'inputmode="numeric" maxlength="4" autocomplete="postal-code"')}${field('rcity', t('city'), r.city, 'autocomplete="address-level2"')}</div>
      <p class="zone" id="zone" role="status"></p>
    </div>`;
  if (coStep === 2) body = `
    <div class="field"><label for="co-date">${t('date')}</label><input id="co-date" name="date" type="date" min="${minDate(order.mode)}" value="${esc(order.date && order.date >= minDate(order.mode) ? order.date : minDate(order.mode))}"></div>
    <fieldset><legend>${t('slot')}</legend><div class="slots">${['am', 'mid', 'pm'].map(s =>
      `<label class="chip"><input type="radio" name="slot" value="${s}" ${order.slot === s ? 'checked' : ''}><span>${slotLabel(s, order.date)}</span></label>`).join('')}</div></fieldset>
    <p class="hint">${t('cutoff_note')}</p><p class="err" id="date-err" role="alert"></p>`;
  if (coStep === 3) body = `
    <div class="row2">${field('cname', t('your_name'), c.name, 'autocomplete="name"')}${field('cphone', t('your_phone'), c.phone, 'type="tel" autocomplete="tel"')}</div>
    ${field('cemail', t('your_email'), c.email, 'type="email" autocomplete="email"')}
    <div class="field"><label for="co-message">${t('card_msg')}</label><textarea id="co-message" name="message" maxlength="250" placeholder="${esc(t('card_ph'))}">${esc(order.message)}</textarea></div>
    <div class="field"><label for="co-note">${t('note')}</label><input id="co-note" name="note" value="${esc(order.note)}"></div>`;
  if (coStep === 4) body = `
    <div class="recap">
      ${cart.map(it => `<div class="rl"><span>${it.qty} × ${esc(itemName(it))}<small>${esc(itemDetail(it))}</small></span><b>${money(unitPrice(it) * it.qty)}</b></div>`).join('')}
      <div class="rl"><span>${t('delivery')}</span><b>${t('free')}</b></div>
      <div class="rl total"><span>${t('total')}</span><b>${money(cartTotal())}</b></div>
    </div>
    <dl class="recap-info">
      <div><dt>${t('recap_mode')}</dt><dd>${order.mode === 'pickup' ? t('mode_pickup') : esc(`${t('mode_delivery')} : ${r.address}, ${r.zip} ${r.city}`)}</dd></div>
      <div><dt>${t('recap_when')}</dt><dd>${esc(fmtDate(order.date))}, ${esc(slotLabel(order.slot, order.date))}</dd></div>
      ${order.mode === 'delivery' ? `<div><dt>${t('recap_to')}</dt><dd>${esc(r.name)}</dd></div>` : ''}
      ${order.message ? `<div><dt>${t('recap_msg')}</dt><dd>« ${esc(order.message)} »</dd></div>` : ''}
    </dl>
    <label class="cgv"><input type="checkbox" name="cgv" required> <span>${t('cgv_accept')} <a href="cgv.html" target="_blank" rel="noopener">CGV</a></span></label>`;
  co.innerHTML = `
    <form class="co" novalidate>
      <header class="co-head"><h2>${t('co_title')}</h2><button type="button" class="x" data-close aria-label="${t('close')}"></button></header>
      <ol class="co-steps">${steps.map((s, i) => `<li class="${i + 1 < coStep ? 'done' : i + 1 === coStep ? 'on' : ''}"><i>${i + 1}</i>${s}</li>`).join('')}</ol>
      <div class="co-body">${body}<p class="err" id="co-err" role="alert"></p></div>
      <footer class="co-foot">
        ${coStep > 1 ? `<button type="button" class="btn btn-line" data-back>${t('back')}</button>` : '<span></span>'}
        <button type="submit" class="btn btn-dark">${coStep < 4 ? t('next') : `${t('pay')} ${money(cartTotal())}`}</button>
      </footer>
    </form>`;
  const f = $('form', co);
  $('[data-back]', co)?.addEventListener('click', () => { coStep--; renderCheckout(); });
  $('[data-close]', co).addEventListener('click', () => co.close());
  if (coStep === 1) {
    const zone = () => { const z = (f.rzip.value || '').trim(); const el = $('#zone'); if (z.length < 4) { el.textContent = ''; el.className = 'zone'; return; } const ok = ZONE.has(z); el.textContent = ok ? t('zone_ok') : t('zone_ko'); el.className = 'zone ' + (ok ? 'ok' : 'ko'); };
    $$('input[name=mode]', f).forEach(i => i.addEventListener('change', () => { order.mode = f.mode.value; $('.addr', f).hidden = order.mode === 'pickup'; }));
    f.rzip.addEventListener('input', zone); zone();
  }
  if (coStep === 2) {
    const check = () => { const d = f.date.value; const sun = d && new Date(d + 'T12:00').getDay() === 0; $('#date-err').textContent = order.mode === 'delivery' && sun ? t('sunday_no') : ''; order.date = d; $$('.slots .chip span', f).forEach((s, i) => { s.textContent = slotLabel(['am', 'mid', 'pm'][i], d); }); return !(order.mode === 'delivery' && sun); };
    f.date.addEventListener('change', check); check();
  }
  f.addEventListener('submit', e => { e.preventDefault(); next(f); });
  $('input, textarea', $('.co-body', co))?.focus({ preventScroll: true });
}
function need(f, names) {
  let ok = true;
  names.forEach(n => { const el = f[n]; const bad = !el.value.trim(); el.setAttribute('aria-invalid', String(bad)); if (bad && ok) { el.focus(); ok = false; } });
  if (!ok) $('#co-err').textContent = t('err_required');
  return ok;
}
function next(f) {
  $('#co-err').textContent = '';
  if (coStep === 1) {
    order.mode = f.mode.value;
    if (order.mode === 'delivery') {
      if (!need(f, ['rname', 'rphone', 'raddress', 'rzip', 'rcity'])) return;
      if (!ZONE.has(f.rzip.value.trim())) { $('#co-err').textContent = t('zone_ko'); f.rzip.focus(); return; }
      order.recipient = { name: f.rname.value.trim(), phone: f.rphone.value.trim(), address: f.raddress.value.trim(), zip: f.rzip.value.trim(), city: f.rcity.value.trim() };
    }
  }
  if (coStep === 2) {
    if (!f.date.value || f.date.value < minDate(order.mode)) { f.date.value = minDate(order.mode); }
    order.date = f.date.value; order.slot = f.slot.value;
    if (order.mode === 'delivery' && new Date(order.date + 'T12:00').getDay() === 0) { $('#date-err').textContent = t('sunday_no'); return; }
  }
  if (coStep === 3) {
    if (!need(f, ['cname', 'cphone', 'cemail'])) return;
    if (!/^\S+@\S+\.\S+$/.test(f.cemail.value.trim())) { $('#co-err').textContent = t('err_email'); f.cemail.focus(); return; }
    order.customer = { name: f.cname.value.trim(), phone: f.cphone.value.trim(), email: f.cemail.value.trim() };
    order.message = f.message.value.trim(); order.note = f.note.value.trim();
  }
  store.set('bb-order', order);
  if (coStep < 4) { coStep++; renderCheckout(); return; }
  if (!f.cgv.checked) { $('#co-err').textContent = t('err_required'); f.cgv.focus(); return; }
  pay();
}

/* ---------- Paiement : Stripe si configuré, sinon paiement de démonstration ---------- */
async function pay() {
  const btn = $('.co-foot .btn-dark', co); btn.disabled = true; btn.textContent = t('paying');
  const payload = { lang, items: cart.map(({ id, size, extras, qty, custom }) => ({ id, size, extras, qty, custom })), order };
  const summary = { ref: 'BB-' + Date.now().toString(36).toUpperCase().slice(-6), total: cartTotal(), lines: cart.map(it => ({ name: itemName(it), detail: itemDetail(it), qty: it.qty, price: unitPrice(it) * it.qty })), order, lang };
  try { sessionStorage.setItem('bb-last', JSON.stringify(summary)); } catch (e) {}
  try {
    const res = await fetch('/.netlify/functions/checkout', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
    if (res.ok) { const j = await res.json(); if (j.url) { location.href = j.url; return; } }
  } catch (e) { /* pas de serveur de paiement : mode démonstration */ }
  co.close(); demoPay(summary);
}
const pd = $('#paydemo');
function demoPay(summary) {
  pd.innerHTML = `
    <div class="pd">
      <button class="x" data-close aria-label="${t('close')}"></button>
      <p class="pd-brand">Betty Bloom Flowers</p>
      <h2>${t('demo_title')}</h2>
      <p class="pd-amount">${money(summary.total)}</p>
      <p class="pd-sub">${t('demo_sub')}</p>
      <div class="pd-methods">
        <button class="pm-bc" data-m>${t('pay_bancontact')}</button>
        <button class="pm-card" data-m>${t('pay_card')}</button>
        <button class="pm-apple" data-m>${t('pay_apple')}</button>
      </div>
      <p class="pd-status" role="status"></p>
    </div>`;
  $('[data-close]', pd).addEventListener('click', () => pd.close());
  $$('[data-m]', pd).forEach(b => b.addEventListener('click', () => {
    $$('[data-m]', pd).forEach(x => { x.disabled = true; });
    $('.pd-status', pd).textContent = t('processing');
    setTimeout(() => { location.href = 'merci.html?demo=1'; }, 1300);
  }));
  pd.showModal();
}

/* ---------- Créer mon cadeau ---------- */
const bd = $('#builder');
const gift = { base: 'bouquet', color: 'rose', size: 'm', extras: [], message: '' };
let bStep = 1;
function openBuilder() { bStep = 1; renderBuilder(); bd.showModal(); }
$$('[data-open-builder]').forEach(b => b.addEventListener('click', e => { e.preventDefault(); closeMenu(); openBuilder(); }));
function giftItem() { return { id: 'custom', size: gift.size, extras: gift.extras.slice(), custom: { base: gift.base, color: gift.color } }; }
function renderBuilder() {
  const titles = [t('b_s1'), t('b_s2'), t('b_s3'), t('b_s4'), t('b_s5')];
  const base = C.custom.bases.find(b => b.id === gift.base);
  let body = '';
  if (bStep === 1) body = `<div class="bases">${C.custom.bases.map(b => `
    <label class="base"><input type="radio" name="base" value="${b.id}" ${gift.base === b.id ? 'checked' : ''}>
    <img src="${b.img}" alt="" width="200" height="190"><span>${esc(L(b))}<b>${t('from')} ${money(b.price)}</b></span></label>`).join('')}</div>`;
  if (bStep === 2) body = `
    <fieldset><legend>${t('color')}</legend><div class="colors">${C.custom.colors.map(c => `
      <label class="color"><input type="radio" name="color" value="${c.id}" ${gift.color === c.id ? 'checked' : ''}><i style="background:${c.hex}"></i><span>${esc(L(c))}</span></label>`).join('')}</div></fieldset>
    <fieldset><legend>${t('size')}</legend><div class="chips">${['s', 'm', 'l'].map(s => `
      <label class="chip"><input type="radio" name="size" value="${s}" ${gift.size === s ? 'checked' : ''}><span>${esc(L(C.sizes[s]))}<b>${money(base.price + C.custom.sizes[s])}</b></span></label>`).join('')}</div></fieldset>`;
  if (bStep === 3) body = `<div class="extras">${C.extras.map(e => `
    <label class="ex"><input type="checkbox" name="extra" value="${e.id}" ${gift.extras.includes(e.id) ? 'checked' : ''}><span>${esc(L(e))}</span><b>+${money(e.price)}</b></label>`).join('')}</div>`;
  if (bStep === 4) body = `<div class="field"><label for="b-msg">${t('card_msg')}</label><textarea id="b-msg" name="message" maxlength="250" placeholder="${esc(t('card_ph'))}">${esc(gift.message)}</textarea></div><p class="hint">${t('b_msg_note')}</p>`;
  if (bStep === 5) { const it = giftItem(); body = `
    <div class="gift-sum"><img src="${base.img}" alt="" width="200" height="190">
      <div><h3>${esc(itemName(it))}</h3><p>${esc(itemDetail(it)) || ''}</p>${gift.message ? `<p class="msg">« ${esc(gift.message)} »</p>` : ''}<p class="gift-price">${money(unitPrice(it))}</p></div></div>`; }
  bd.innerHTML = `
    <form class="co" novalidate>
      <header class="co-head"><h2>${t('b_title')}</h2><button type="button" class="x" data-close aria-label="${t('close')}"></button></header>
      <ol class="co-steps five">${titles.map((s, i) => `<li class="${i + 1 < bStep ? 'done' : i + 1 === bStep ? 'on' : ''}"><i>${i + 1}</i>${s}</li>`).join('')}</ol>
      <div class="co-body"><h3 class="b-h">${titles[bStep - 1]}</h3>${body}</div>
      <footer class="co-foot">
        ${bStep > 1 ? `<button type="button" class="btn btn-line" data-back>${t('back')}</button>` : '<span></span>'}
        <button type="submit" class="btn btn-dark">${bStep < 5 ? `${t('next')} · ${money(unitPrice(giftItem()))}` : t('b_add')}</button>
      </footer>
    </form>`;
  const f = $('form', bd);
  $('[data-back]', bd)?.addEventListener('click', () => { save(f); bStep--; renderBuilder(); });
  $('[data-close]', bd).addEventListener('click', () => bd.close());
  f.addEventListener('change', () => { save(f); $('.co-foot .btn-dark', bd).textContent = bStep < 5 ? `${t('next')} · ${money(unitPrice(giftItem()))}` : t('b_add'); });
  f.addEventListener('submit', e => {
    e.preventDefault(); save(f);
    if (bStep < 5) { bStep++; renderBuilder(); return; }
    if (gift.message && !order.message) { order.message = gift.message; store.set('bb-order', order); }
    addToCart({ ...giftItem(), qty: 1 }); bd.close(); openCart();
  });
}
function save(f) {
  if (f.base) gift.base = f.base.value;
  if (f.color) gift.color = f.color.value;
  if (f.size) gift.size = f.size.value;
  if (bStep === 3) gift.extras = $$('input[name=extra]:checked', f).map(i => i.value);
  if (f.message) gift.message = f.message.value.trim();
}

/* ---------- Divers : fermeture des fenêtres, menu mobile, message ---------- */
$$('dialog').forEach(d => {
  d.addEventListener('click', e => { if (e.target === d || e.target.closest('[data-close]')) d.close(); });
});
const menu = $('#mmenu');
function closeMenu() { if (menu.open) menu.close(); }
$('#menu-btn').addEventListener('click', () => menu.showModal());
$$('a', menu).forEach(a => a.addEventListener('click', () => { if (a.dataset.navCat) { filter = a.dataset.navCat; renderShop(); } closeMenu(); }));
$$('.nav-cats a').forEach(a => a.addEventListener('click', () => { filter = a.dataset.navCat; renderShop(); }));
let toastTimer;
function toast(msg) { const el = $('#toast'); el.textContent = msg; el.classList.add('on'); clearTimeout(toastTimer); toastTimer = setTimeout(() => el.classList.remove('on'), 2200); }

/* ---------- Démarrage ---------- */
fetch('assets/catalog.json').then(r => r.json()).then(data => { C = data; applyLang(); }).catch(() => {});
applyLang();

// Apparition douce des sections
if (!matchMedia('(prefers-reduced-motion: reduce)').matches) {
  const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }), { threshold: 0.12 });
  $$('.rv').forEach(el => io.observe(el));
} else $$('.rv').forEach(el => el.classList.add('in'));

// Rose 3D : chargée après l'affichage du contenu
const rc = $('#rose');
if (rc) {
  const load = () => import('./rose3d.js').then(m => m.mountRose(rc, { reduce: matchMedia('(prefers-reduced-motion: reduce)').matches, mobile: matchMedia('(max-width: 900px)').matches })).catch(() => rc.remove());
  'requestIdleCallback' in window ? requestIdleCallback(load, { timeout: 1200 }) : setTimeout(load, 300);
}
