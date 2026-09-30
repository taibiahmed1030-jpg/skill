// Crée une session de paiement Stripe Checkout (Bancontact, carte, Apple Pay...).
// Les prix sont recalculés ici à partir du catalogue : le navigateur ne peut pas les modifier.
// Réglage Netlify requis : variable d'environnement STRIPE_SECRET_KEY (sk_test_... puis sk_live_...).
const catalog = require('../../assets/catalog.json');

const json = (status, body) => ({ statusCode: status, headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });

function priceOf(item) {
  const extras = (item.extras || []).map(id => catalog.extras.find(e => e.id === id)).filter(Boolean);
  const extraSum = extras.reduce((s, e) => s + e.price, 0);
  if (item.id === 'custom') {
    const base = catalog.custom.bases.find(b => b.id === item.custom?.base);
    const color = catalog.custom.colors.find(c => c.id === item.custom?.color);
    const sizeAdd = catalog.custom.sizes[item.size];
    if (!base || !color || sizeAdd === undefined) return null;
    return { unit: base.price + sizeAdd + extraSum, name: `Création sur mesure : ${base.fr}, ${color.fr.toLowerCase()} (${catalog.sizes[item.size].fr})`, extras };
  }
  const p = catalog.products.find(x => x.id === item.id);
  if (!p || p.sizes[item.size] === undefined) return null;
  const size = item.size === 'u' ? '' : ` (${catalog.sizes[item.size].fr})`;
  return { unit: p.sizes[item.size] + extraSum, name: p.fr + size, extras };
}

exports.handler = async (event) => {
  if (event.httpMethod !== 'POST') return json(405, { error: 'method' });
  const key = process.env.STRIPE_SECRET_KEY;
  if (!key) return json(501, { error: 'stripe-not-configured' });

  let data;
  try { data = JSON.parse(event.body || '{}'); } catch (e) { return json(400, { error: 'json' }); }
  const items = Array.isArray(data.items) ? data.items.slice(0, 30) : [];
  const o = data.order || {};
  if (!items.length) return json(400, { error: 'empty' });

  const origin = event.headers.origin || `https://${event.headers.host}`;
  const f = new URLSearchParams();
  f.append('mode', 'payment');
  f.append('locale', data.lang === 'nl' ? 'nl' : 'fr');
  f.append('success_url', `${origin}/merci.html?paid=1&session_id={CHECKOUT_SESSION_ID}`);
  f.append('cancel_url', `${origin}/#boutique`);
  if (o.customer?.email) f.append('customer_email', String(o.customer.email).slice(0, 200));

  let i = 0;
  for (const it of items) {
    const pr = priceOf(it);
    const qty = Math.max(1, Math.min(20, parseInt(it.qty, 10) || 1));
    if (!pr) return json(400, { error: 'item', id: it.id });
    const desc = pr.extras.map(e => e.fr).join(', ');
    f.append(`line_items[${i}][quantity]`, qty);
    f.append(`line_items[${i}][price_data][currency]`, 'eur');
    f.append(`line_items[${i}][price_data][unit_amount]`, Math.round(pr.unit * 100));
    f.append(`line_items[${i}][price_data][product_data][name]`, pr.name);
    if (desc) f.append(`line_items[${i}][price_data][product_data][description]`, `Avec : ${desc}`);
    i++;
  }

  // Détails de la commande, visibles par la fleuriste dans son tableau de bord Stripe
  const r = o.recipient || {}, c = o.customer || {};
  const meta = {
    reception: o.mode === 'pickup' ? 'Retrait en boutique' : 'Livraison',
    date: o.date, creneau: o.slot,
    destinataire: o.mode === 'pickup' ? '' : `${r.name || ''}, ${r.phone || ''}`,
    adresse: o.mode === 'pickup' ? '' : `${r.address || ''}, ${r.zip || ''} ${r.city || ''}`,
    client: `${c.name || ''}, ${c.phone || ''}`,
    message_carte: o.message, remarque: o.note,
  };
  for (const [k, v] of Object.entries(meta)) {
    if (!v) continue;
    f.append(`metadata[${k}]`, String(v).slice(0, 490));
    f.append(`payment_intent_data[metadata][${k}]`, String(v).slice(0, 490));
  }

  const res = await fetch('https://api.stripe.com/v1/checkout/sessions', {
    method: 'POST',
    headers: { Authorization: `Bearer ${key}`, 'Content-Type': 'application/x-www-form-urlencoded' },
    body: f,
  });
  const out = await res.json();
  if (!res.ok) return json(502, { error: 'stripe', message: out.error?.message });
  return json(200, { url: out.url });
};
