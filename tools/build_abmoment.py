#!/usr/bin/env python3
"""Génère les pages HTML statiques du site ABmoment (abmoment/*.html).

Les en-têtes, pieds de page et coordonnées sont définis une seule fois ici.
Usage : python3 tools/build_abmoment.py
"""
from pathlib import Path
import json

OUT = Path(__file__).resolve().parent.parent / 'abmoment'
SITE = 'https://www.abmoment.com'

CENTRE = {
    'name': 'ABmoment',
    'tagline': 'Centre de kinésithérapie et de bien-être',
    'street': 'Rue Hancart 12', 'zip': '1030', 'city': 'Schaerbeek',
    'tel': '+32487137651', 'tel_h': '0487 13 76 51',
    'email': 'Aydinbozok1000@gmail.com',
    'insta': 'https://www.instagram.com/centre.abmoment/',
    'tiktok': 'https://www.tiktok.com/@aydinbozokk_',
    'facebook': '',
}
TEAM = [
    {'id': 'simon', 'name': 'Simon Cano', 'role': 'Kinésithérapeute', 'tel': '+32471627142', 'tel_h': '+32 471 62 71 42', 'img': 'assets/img/portrait-simon.jpg',
     'bio': "Rééducation, douleurs musculaires et articulaires, récupération après une blessure : Simon vous accompagne avec un suivi adapté à votre corps et à vos objectifs."},
    {'id': 'julie', 'name': 'Julie Thiebaut', 'role': 'Kinésithérapeute', 'tel': '+32456953798', 'tel_h': '+32 456 95 37 98', 'img': 'assets/img/portrait-julie.jpg',
     'bio': "Julie prend en charge vos douleurs et votre rééducation avec écoute et précision, pour vous aider à retrouver une mobilité confortable au quotidien."},
    {'id': 'kubra', 'name': 'Kübra Bozok', 'role': 'Neuropsychologue et psychologue clinicienne', 'tel': '+32488839401', 'tel_h': '+32 488 83 94 01', 'img': '',
     'bio': "Neuropsychologue et psychologue clinicienne, Kübra réalise des bilans neuropsychologiques, des bilans TDAH et des bilans de QI, et accompagne les patients dont la mémoire, l'attention ou la concentration posent difficulté."},
]
FOUNDER = {'id': 'aydin', 'name': 'Aydin Bozok', 'role': 'Fondateur · séance ABmoment', 'tel': '+32487137651', 'tel_h': '0487 13 76 51', 'img': 'assets/img/portrait-aydin.jpg',
           'bio': [
               "Créateur d’ABmoment, je m’investis chaque jour avec passion, détermination et engagement pour faire de notre centre un lieu où chaque patient se sent écouté, accompagné et en confiance.",
               "Toujours présent et attentif, j’ai à cœur d’offrir à chacun la meilleure prise en charge possible, en plaçant l’humain, la qualité des soins et le bien-être au centre de mes priorités.",
               "ABmoment, c’est avant tout une vision : celle d’une approche pluridisciplinaire où compétence, écoute et bienveillance se rencontrent.",
               "Merci à tous nos patients pour leur confiance et à toute notre équipe de faire vivre cette belle aventure au quotidien. Et ce n’est que le début !"]}
# Horaires réels (fiche Google du centre)
HOURS = [('Lundi au samedi', '10h00 à 18h00'), ('Dimanche', 'Fermé')]

PAGES = [('index.html', 'Accueil'), ('soins.html', 'Nos soins'), ('neuropsychologie.html', 'Neuropsychologie'), ('equipe.html', "L'équipe"), ('contact.html', 'Rendez-vous')]


def ic(name, extra=''):
    return f'<i class="ic{extra}" style="--i:url(icons/{name}.svg)" aria-hidden="true"></i>'


def wa(tel):
    return 'https://wa.me/' + tel.lstrip('+')


def schema():
    data = {
        '@context': 'https://schema.org', '@type': ['Physiotherapy', 'MedicalBusiness'],
        'name': 'ABmoment', 'description': 'Centre de kinésithérapie et de bien-être à Schaerbeek, Bruxelles : kinésithérapie conventionnée, séance ABmoment (techniques ostéopathiques, ventouses, pressothérapie et massage) et neuropsychologie.',
        'url': SITE, 'logo': SITE + '/assets/img/logo.png', 'telephone': CENTRE['tel'], 'email': CENTRE['email'],
        'address': {'@type': 'PostalAddress', 'streetAddress': CENTRE['street'], 'postalCode': CENTRE['zip'], 'addressLocality': CENTRE['city'], 'addressRegion': 'Bruxelles', 'addressCountry': 'BE'},
        'areaServed': ['Schaerbeek', 'Bruxelles', 'Saint-Josse-ten-Noode', 'Evere', 'Bruxelles-Ville'],
        'medicalSpecialty': ['Physiotherapy', 'Neurologic'],
        'availableService': [{'@type': 'MedicalTherapy', 'name': n} for n in ['Kinésithérapie', 'Séance ABmoment : techniques ostéopathiques, ventouses, pressothérapie et massage', 'Bilan neuropsychologique', 'Bilan TDAH', 'Bilan de QI']],
        'founder': {'@type': 'Person', 'name': FOUNDER['name']},
        'openingHoursSpecification': [{'@type': 'OpeningHoursSpecification', 'dayOfWeek': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'], 'opens': '10:00', 'closes': '18:00'}],
        'employee': [{'@type': 'Person', 'name': m['name'], 'jobTitle': m['role'], 'telephone': m['tel']} for m in TEAM + [FOUNDER]],
        'sameAs': [CENTRE['insta'], CENTRE['tiktok']],
        'vatID': 'BE1021837986',
    }
    return json.dumps(data, ensure_ascii=False, indent=1)


def head(file, title, desc):
    return f'''<!DOCTYPE html>
<html lang="fr-BE">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="format-detection" content="telephone=no">
<title>{title}</title>
<meta name="description" content="{desc}">
<!-- Retirer noindex une fois le site en ligne sur abmoment.com -->
<meta name="robots" content="noindex, nofollow">
<link rel="canonical" href="{SITE}/{'' if file == 'index.html' else file}">
<meta name="theme-color" content="#f7f6f3">
<meta property="og:type" content="website">
<meta property="og:locale" content="fr_BE">
<meta property="og:site_name" content="ABmoment">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="assets/img/og.jpg">
<link rel="icon" href="assets/img/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
<link rel="preload" href="assets/fonts/manrope.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/hanken-grotesk.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/site.css">
<script type="application/ld+json">{schema()}</script>
</head>
<body>
<script>document.documentElement.classList.add('js');</script>
<a class="skip" href="#main">Aller au contenu</a>
'''


def header(file):
    cur = ' aria-current="page"'
    links = ''.join(f'<li><a href="{f}"{cur if f == file else ""}>{n}</a></li>' for f, n in PAGES[1:])
    mlinks = ''.join(f'<a href="{f}">{n}</a>' for f, n in PAGES)
    return f'''<header class="hdr">
  <div class="wrap">
    <a href="index.html" class="brand" aria-label="ABmoment, accueil"><img class="brand-logo" src="assets/img/logo.png" alt="" width="56" height="48"><span>ABmoment<small>Kinésithérapie et <span class="nw">bien-être</span></small></span></a>
    <nav aria-label="Navigation principale"><ul class="nav">{links}</ul></nav>
    <a href="contact.html" class="btn btn-accent btn-sm">Prendre rendez-vous</a>
    <button class="menu-btn" aria-label="Ouvrir le menu" aria-expanded="false" aria-controls="mnav">{ic('list')}</button>
  </div>
</header>
<div class="mnav" id="mnav" role="dialog" aria-modal="true" aria-label="Menu">
  <button class="mnav-close" aria-label="Fermer le menu">{ic('x')}</button>
  {mlinks}
  <a href="tel:{CENTRE['tel']}" class="btn btn-accent">{ic('phone')} {CENTRE['tel_h']}</a>
</div>
<main id="main">
'''


def footer():
    soc = f'<li><a href="{CENTRE["insta"]}" target="_blank" rel="noopener">Instagram</a></li><li><a href="{CENTRE["tiktok"]}" target="_blank" rel="noopener">TikTok</a></li>'
    if CENTRE['facebook']:
        soc += f'<li><a href="{CENTRE["facebook"]}" target="_blank" rel="noopener">Facebook</a></li>'
    return f'''</main>
<footer class="ftr">
  <div class="wrap">
    <div class="ftr-grid">
      <div>
        <a href="index.html" class="brand"><img class="brand-logo" src="assets/img/logo.png" alt="" width="56" height="48"><span>ABmoment<small>Kinésithérapie et <span class="nw">bien-être</span></small></span></a>
        <p style="margin-top:16px;max-width:34ch">Centre de kinésithérapie et de bien-être à Schaerbeek, au service des patients de tout Bruxelles.</p>
      </div>
      <div><h2>Le centre</h2><ul>{''.join(f'<li><a href="{f}">{n}</a></li>' for f, n in PAGES[1:])}</ul></div>
      <div><h2>Contact</h2><ul><li>{CENTRE['street']}</li><li>{CENTRE['zip']} {CENTRE['city']}</li><li><a href="tel:{CENTRE['tel']}">{CENTRE['tel_h']}</a></li><li><a href="mailto:{CENTRE['email']}">E-mail</a></li></ul></div>
      <div><h2>Suivez-nous</h2><ul>{soc}</ul></div>
    </div>
    <div class="legal"><span>© 2026 ABmoment · BCE 1021.837.986 · <a href="mentions-legales.html">Mentions légales</a></span><span>Site conçu par <a href="https://webxl.be" target="_blank" rel="noopener">WEBXL</a></span></div>
  </div>
</footer>
<script type="importmap">{{ "imports": {{ "three": "./assets/vendor/three.module.min.js" }} }}</script>
<script type="module" src="assets/site.js"></script>
</body>
</html>
'''


def book_band(title='Prenez <span class="nw">rendez-vous</span>', text="Appelez le centre ou contactez directement votre praticien, par téléphone ou WhatsApp."):
    return f'''<section style="padding-top:0"><div class="wrap"><div class="band rv">
  <div><h2 class="h2">{title}</h2><p class="sub">{text}</p></div>
  <div class="cta" style="margin-top:0"><a href="tel:{CENTRE['tel']}" class="btn btn-accent">{ic('phone')} {CENTRE['tel_h']}</a><a href="contact.html" class="btn btn-line">Tous les contacts</a></div>
</div></div></section>
'''


SOINS = [
    ('kine', 'person-simple-run', 'Séance de kinésithérapie', 'Avec Julie Thiebaut et Simon Cano',
     "Rééducation et traitement des douleurs musculaires et articulaires, après une blessure, une opération ou en cas de douleurs installées.",
     ['Mal de dos, nuque et épaules', 'Rééducation après blessure ou opération', 'Entorses, tendinites et douleurs articulaires', 'Récupération des sportifs'],
     'Conventionnée INAMI : remboursement par la mutuelle sur prescription médicale.', 'assets/img/seance-kine.jpg', 'Julie Thiebaut, kinésithérapeute, mobilise la jambe d’une patiente au centre ABmoment'),
    ('seance', 'hand-palm', 'Séance ABmoment', 'Avec Aydin Bozok',
     "Un soin complet en une seule séance : techniques ostéopathiques, thérapie par ventouses, pressothérapie et massage, combinés selon vos besoins pour relâcher les tensions et retrouver de la mobilité.",
     ['Techniques ostéopathiques : déblocage articulaire', 'Thérapie par ventouses', 'Pressothérapie des jambes', 'Massage de détente ou sportif'],
     'Séance non conventionnée : pas de remboursement INAMI.', 'assets/img/centre-salle.jpg', 'Salle de soin du centre ABmoment avec table de traitement'),
]


GEO = (50.86402, 4.37245)
MAPS_URL = 'https://www.google.com/maps/search/?api=1&amp;query=Rue+Hancart+12,+1030+Schaerbeek'


def map_frame(h=340):
    return f'<a class="map rv" style="--h:{h}px" href="{MAPS_URL}" target="_blank" rel="noopener" aria-label="Ouvrir l’itinéraire vers ABmoment, {CENTRE["street"]}, dans Google Maps"><img src="assets/img/carte-abmoment.webp" alt="Plan du quartier : le centre ABmoment au {CENTRE["street"]}, {CENTRE["zip"]} {CENTRE["city"]}" width="1400" height="900" loading="lazy"><span class="map-cta">{ic("map-pin")} Ouvrir dans Google Maps</span></a>'


def find_us():
    return f'''<section style="padding-top:0" aria-labelledby="map-title">
  <div class="wrap find-us">
    <div>
      <p class="kicker rv">Nous trouver</p>
      <h2 class="h2 rv" id="map-title">Au cœur de Schaerbeek</h2>
      <p class="sub rv">{CENTRE['street']}, {CENTRE['zip']} {CENTRE['city']}. Facile d’accès en transports en commun.</p>
      <div class="cta rv"><a class="btn btn-accent" href="{MAPS_URL}" target="_blank" rel="noopener">{ic('map-pin')} Itinéraire</a><a class="btn btn-line" href="contact.html">Tous les contacts</a></div>
    </div>
    {map_frame(380)}
  </div>
</section>
'''


GOOGLE_REVIEWS = 'https://share.google/crhWTFDIozYlheTbz'
REVIEWS = [
    ('Anissa', "Habituée à venir une fois par mois au cabinet, je tenais à te remercier sincèrement pour ton accompagnement et pour toutes ces séances qui m’ont fait énormément de bien. Mais par-dessus tout, je tiens à te remercier pour ta gentillesse, ton accueil chaleureux, ta bienveillance et ton écoute. C’est toujours un plaisir de venir au cabinet. Un grand merci pour tout !"),
    ('Aurélien Tieleman', 'Bon praticien et bel humain. Je recommande.'),
    ('Serhat Yvz', 'Tres profesionnel, resultat garantie apres traitement'),
]


def reviews_block():
    stars = '<span class="stars" aria-label="5 étoiles sur 5">★★★★★</span>'
    cards = ''.join(f'''<figure class="review rv">{stars}<blockquote>« {t} »</blockquote><figcaption><span class="avatar" aria-hidden="true">{n[0]}</span>{n}<small>Avis Google</small></figcaption></figure>''' for n, t in REVIEWS)
    return f'''<section style="padding-top:0" aria-labelledby="reviews-title">
  <div class="wrap">
    <p class="kicker rv">Avis Google</p>
    <h2 class="h2 rv" id="reviews-title">Ce que disent nos patients</h2>
    <div class="reviews">{cards}</div>
    <p class="rv" style="margin-top:28px"><a class="btn btn-line" href="{GOOGLE_REVIEWS}" target="_blank" rel="noopener">Voir tous nos avis sur Google {ic('arrow-up-right')}</a></p>
  </div>
</section>
'''


def index():
    cards = ''.join(f'''<a class="card rv" href="soins.html#{s[0]}">{ic(s[1])}<h3>{s[2]}</h3><span class="role">{s[3]}</span><p>{s[4]}</p><span class="more">Découvrir {ic('arrow-right')}</span></a>''' for s in SOINS)
    cards += f'''<a class="card rv" href="neuropsychologie.html">{ic('brain')}<h3>Neuropsychologie</h3><span class="role">Avec Kübra Bozok</span><p>Bilans TDAH, bilans de QI et bilans neuropsychologiques, avec un accompagnement adapté. Consultations conventionnées.</p><span class="more">Découvrir {ic('arrow-right')}</span></a>'''
    def tcard(m):
        fig = f'<img src="{m["img"]}" alt="{m["name"]}, {m["role"].lower()}" width="880" height="1100" loading="lazy">' if m['img'] else '<div class="monogram" aria-hidden="true">KB</div>'
        return f'''<a class="tcard rv" href="equipe.html#{m['id']}"><figure>{fig}</figure><span class="role">{m['role']}</span><h3>{m['name']}</h3></a>'''
    team = ''.join(tcard(m) for m in [FOUNDER] + TEAM)
    return head('index.html', 'ABmoment | Centre de kinésithérapie et de bien-être à Schaerbeek, Bruxelles',
                'ABmoment, centre de kinésithérapie et de bien-être à Schaerbeek (Bruxelles) : kinésithérapie conventionnée, séance ABmoment (ostéopathie, ventouses, pressothérapie, massage) et neuropsychologie.') + header('index.html') + f'''
<section class="hero" style="padding:0" aria-labelledby="hero-title">
  <div class="wrap">
    <div>
      <p class="kicker rv">ABmoment, Bruxelles</p>
      <h1 id="hero-title" class="rv">Centre de kinésithérapie et de <em class="nw">bien-être</em> à Schaerbeek</h1>
      <p class="lead rv">Kinésithérapie conventionnée, séance ABmoment et neuropsychologie, réunies dans un même centre lumineux à Schaerbeek.</p>
      <div class="cta rv"><a href="contact.html" class="btn btn-accent">Prendre rendez-vous</a><a href="soins.html" class="btn btn-line">Nos soins</a></div>
      <div class="facts rv"><div><strong>4 praticiens</strong>Kinés, soins et psychologie</div><div><strong>Conventionné</strong>Kiné et psychologie</div><div><strong>Schaerbeek</strong>{CENTRE['street']}</div></div>
    </div>
    <div class="body3d" data-body3d="hero"><img src="assets/img/corps-3d.webp" alt="Corps humain anatomique en 3D, muscles et tendons" width="700" height="1300" fetchpriority="high"><canvas aria-hidden="true"></canvas><p class="turn-hint" aria-hidden="true">{ic("hand-palm")} Faites-le pivoter</p></div>
  </div>
</section>

<section aria-labelledby="soins-title">
  <div class="wrap">
    <h2 class="h2 rv" id="soins-title">Des soins pour tout le corps</h2>
    <p class="sub rv">Une approche globale qui associe techniques modernes et traditionnelles, adaptée à chaque patient : sportifs, personnes souffrant de douleurs ou simple besoin de récupérer.</p>
    <div class="cards">{cards}</div>
  </div>
</section>

<section style="padding-top:0" aria-labelledby="centre-title">
  <div class="wrap photo-split">
    <div class="spine3d rv" data-spine3d><img src="assets/img/colonne-3d.webp" alt="Colonne vertébrale et bassin en 3D, disques intervertébraux en bleu" width="600" height="800" loading="lazy"><canvas aria-hidden="true"></canvas></div>
    <div>
      <p class="kicker rv">Le centre</p>
      <h2 class="h2 rv" id="centre-title">Le savoir-faire, l’écoute et la précision</h2>
      <p class="sub rv">Un centre lumineux et apaisant à Schaerbeek, où chaque patient est pris en charge dans sa globalité : sportifs, personnes qui souffrent de douleurs, ou simple besoin de récupérer.</p>
      <p class="quote rv" style="margin-top:32px">« Le corps s’apaise lorsque l’on écoute enfin ce qu’il murmure. »</p>
    </div>
  </div>
</section>

<section style="padding-top:0" aria-labelledby="gal-title">
  <div class="wrap">
    <h2 class="h2 rv" id="gal-title">Le centre en images</h2>
    <div class="gallery">
      <figure class="g-wide rv"><img src="assets/img/equipe-groupe.jpg" alt="Julie Thiebaut, Aydin Bozok et Simon Cano dans le centre ABmoment" width="1170" height="1040" loading="lazy"></figure>
      <figure class="rv"><img src="assets/img/seance-kine.jpg" alt="Séance de kinésithérapie au centre ABmoment" width="900" height="1200" loading="lazy"></figure>
      <figure class="rv"><img src="assets/img/centre-salle.jpg" alt="Salle de soin avec table de traitement" width="1000" height="1190" loading="lazy"></figure>
      <figure class="rv"><img src="assets/img/centre-exercice.jpg" alt="Espace d’exercices : espalier, élastiques, ballon et kettlebells" width="1000" height="1230" loading="lazy"></figure>
    </div>
  </div>
</section>

<section style="padding-top:0" aria-labelledby="team-title">
  <div class="wrap">
    <h2 class="h2 rv" id="team-title">Une équipe de spécialistes</h2>
    <p class="sub rv">Deux kinésithérapeutes conventionnés, une neuropsychologue et psychologue clinicienne, et {FOUNDER['name']}, fondateur du centre.</p>
    <div class="tcards">{team}</div>
  </div>
</section>
''' + reviews_block() + find_us() + book_band() + footer()


ZONES = [('Nuque et tête', 'Tensions cervicales, raideurs de la nuque et maux de tête liés aux tensions musculaires.', 'f', [(50, 17.5)]),
         ('Épaules', 'Douleurs, tendinites et manque de mobilité de l’épaule.', 'f', [(32, 22.5), (68, 22.5)]),
         ('Dos', 'Lombalgies, dorsalgies et douleurs liées à la posture ou au travail.', 'b', [(50, 30), (50, 42)]),
         ('Bras et poignets', 'Coudes, avant-bras et poignets sollicités par le sport ou le travail.', 'f', [(16, 44), (84, 44)]),
         ('Hanches et bassin', 'Raideurs, douleurs et rééducation de la hanche.', 'f', [(39, 51), (61, 51)]),
         ('Genoux et jambes', 'Entorses, ligaments, rééducation du genou et jambes lourdes.', 'f', [(41, 70), (59, 70)])]


def zones_block():
    items = ''.join(f'<li><button type="button" class="zbtn" data-z="{i}" data-v="{v}" aria-pressed="{str(i == 0).lower()}"><span class="n">0{i + 1}</span><span><b>{t}</b><span>{d}</span></span></button></li>' for i, (t, d, v, _) in enumerate(ZONES))
    return f'''<section style="padding-top:40px" aria-labelledby="zones-title">
  <div class="wrap zones2">
    <div class="zbody rv body3d" data-body3d="zones"><img src="assets/img/corps-3d.webp" alt="Corps humain anatomique en 3D : les muscles de la zone choisie s’éclairent" width="700" height="1300" loading="lazy"><canvas aria-hidden="true"></canvas></div>
    <div class="zhead">
      <p class="kicker rv">Zones traitées</p>
      <h2 class="h2 rv" id="zones-title">Là où vous avez mal</h2>
      <p class="sub rv">Choisissez une zone : les muscles concernés s’éclairent sur le corps.</p>
    </div>
    <ul class="zlist rv">{items}</ul>
  </div>
</section>
'''


def soins():
    blocks = ''
    for sid, icon, title, who, desc, items, refund, img, alt in SOINS:
        blocks += f'''<article class="soin soin-photo rv" id="{sid}"><figure><img src="{img}" alt="{alt}" width="900" height="1200" loading="lazy"></figure><div><h2>{ic(icon)}{title}</h2><span class="role">{who}</span><p>{desc}</p><ul>{''.join(f'<li>{x}</li>' for x in items)}</ul><p class="refund">{ic('check')} {refund}</p></div></article>'''
    blocks += f'''<article class="soin rv" id="neuro"><h2>{ic('brain')}Neuropsychologie</h2><div><span class="role">Avec Kübra Bozok, neuropsychologue et psychologue clinicienne</span><p>Bilans et accompagnement des fonctions cognitives : mémoire, attention et concentration.</p><ul><li>Bilan neuropsychologique</li><li>Bilan TDAH</li><li>Bilan de QI</li><li>Suivi et remédiation cognitive</li></ul><p class="refund">{ic('check')} Consultations conventionnées : remboursement selon les conditions de votre mutuelle.</p><p style="margin-top:16px"><a href="neuropsychologie.html" class="btn btn-line btn-sm">En savoir plus</a></p></div></article>'''
    return head('soins.html', 'Nos soins | Kinésithérapie conventionnée et séance ABmoment à Schaerbeek | ABmoment',
                'Kinésithérapie conventionnée avec Julie Thiebaut et Simon Cano, séance ABmoment avec Aydin Bozok (techniques ostéopathiques, ventouses, pressothérapie et massage) et neuropsychologie à Schaerbeek, Bruxelles.') + header('soins.html') + f'''
<section style="padding-bottom:40px">
  <div class="wrap">
    <p class="kicker rv">Nos soins</p>
    <h1 class="rv">Kinésithérapie et <em class="nw">bien-être</em> à Schaerbeek</h1>
    <p class="lead rv">Chaque séance commence par un échange sur vos douleurs et vos objectifs. Le traitement est ensuite adapté à vous.</p>
    <div class="cta rv"><a href="contact.html" class="btn btn-accent">Prendre rendez-vous</a><a href="#refund-title" class="btn btn-line">Remboursement</a></div>
  </div>
</section>
<section style="padding-top:20px">
  <div class="wrap">
    {blocks}
  </div>
</section>
<section style="padding-top:0" aria-labelledby="refund-title">
  <div class="wrap">
    <h2 class="h2 rv" id="refund-title">Remboursement et prescription</h2>
    <div class="cards">
      <div class="card rv">{ic('person-simple-run')}<h3>Kinésithérapie</h3><p><strong>Conventionnée INAMI.</strong> Avec une prescription de votre médecin, une partie de la séance est remboursée par votre mutuelle. Pensez à apporter votre prescription et votre carte d’identité.</p></div>
      <div class="card rv">{ic('brain')}<h3>Psychologie et neuropsychologie</h3><p><strong>Conventionnée.</strong> Les conditions de remboursement dépendent de votre mutuelle : renseignez-vous auprès d’elle ou posez la question à Kübra Bozok.</p></div>
      <div class="card rv">{ic('hand-palm')}<h3>Séance ABmoment</h3><p><strong>Non conventionnée.</strong> La séance avec Aydin Bozok n’est pas remboursée par l’INAMI. Aucune prescription n’est nécessaire.</p></div>
    </div>
  </div>
</section>
''' + zones_block() + book_band() + footer()


def neuro():
    k = TEAM[2]
    return head('neuropsychologie.html', 'Neuropsychologue à Schaerbeek, Bruxelles | Bilan TDAH, bilan de QI | ABmoment',
                'Kübra Bozok, neuropsychologue et psychologue clinicienne au centre ABmoment à Schaerbeek : bilan neuropsychologique, bilan TDAH, bilan de QI et accompagnement.') + header('neuropsychologie.html') + f'''
<section style="padding:0" aria-labelledby="hero-title">
  <div class="wrap">
    <div class="neuro-hero rv">
      <div>
      <p class="kicker">Neuropsychologie</p>
      <h1 id="hero-title">Comprendre le fonctionnement de votre <em>cerveau</em></h1>
      <p class="lead">Avec Kübra Bozok, neuropsychologue et psychologue clinicienne : bilans neuropsychologiques, bilans TDAH et bilans de QI, pour comprendre et accompagner la mémoire, l’attention et la concentration.</p>
      <ul class="chips" aria-label="Bilans proposés"><li>Bilan TDAH</li><li>Bilan de QI</li><li>Bilan neuropsychologique</li><li>Mémoire</li><li>Attention</li></ul>
      <div class="cta"><a href="tel:{k['tel']}" class="btn btn-accent">{ic('phone')} Appeler Kübra Bozok</a><a href="{wa(k['tel'])}" class="btn btn-line" target="_blank" rel="noopener">{ic('whatsapp-logo')} WhatsApp</a></div>
      </div>
      <div class="brain" data-tilt><div class="brain-in"><img src="assets/img/cerveau.jpg" alt="Cerveau humain parcouru de connexions neuronales bleues" width="1100" height="1275"><span class="brain-glow" aria-hidden="true"></span></div></div>
    </div>
  </div>
</section>
<section aria-labelledby="bilans-title">
  <div class="wrap">
    <h2 class="h2 rv" id="bilans-title">Les bilans proposés</h2>
    <p class="sub rv">Chaque bilan commence par un entretien, se poursuit par des tests standardisés et se termine par une restitution claire des résultats.</p>
    <div class="cards">
      <div class="card rv">{ic('lightning')}<h3>Bilan TDAH</h3><p>Évaluation de l’attention, de l’impulsivité et de l’agitation, pour objectiver un trouble du déficit de l’attention avec ou sans hyperactivité.</p></div>
      <div class="card rv">{ic('chart-bar')}<h3>Bilan de QI</h3><p>Évaluation du fonctionnement intellectuel par des tests reconnus : difficultés scolaires, suspicion de haut potentiel ou orientation.</p></div>
      <div class="card rv">{ic('brain')}<h3>Bilan neuropsychologique</h3><p>Profil complet de la mémoire, de l’attention, du langage et des fonctions exécutives, avec des pistes d’accompagnement.</p></div>
    </div>
  </div>
</section>
<section style="padding-top:0" aria-labelledby="why-title">
  <div class="wrap">
    <h2 class="h2 rv" id="why-title">Quand consulter ?</h2>
    <div class="cards">
      <div class="card rv">{ic('brain')}<h3>Mémoire</h3><p>Oublis fréquents, difficulté à retenir de nouvelles informations ou inquiétude face à des changements.</p></div>
      <div class="card rv">{ic('sparkle')}<h3>Attention et concentration</h3><p>Difficulté à rester concentré, distractibilité, fatigue mentale au travail ou à l'école.</p></div>
      <div class="card rv">{ic('heartbeat')}<h3>Après un événement neurologique</h3><p>Évaluation et accompagnement après un traumatisme crânien, un AVC ou une autre atteinte neurologique.</p></div>
    </div>
  </div>
</section>
<section style="padding-top:0" aria-labelledby="bilan-title">
  <div class="wrap">
    <article class="soin rv"><h2 id="bilan-title">{ic('calendar-check')}Le bilan neuropsychologique</h2><div><p>Un entretien, puis des tests adaptés permettent de dresser un profil précis de vos forces et de vos difficultés. Les résultats vous sont expliqués et orientent la suite de l'accompagnement.</p><ul><li>Entretien et anamnèse</li><li>Tests standardisés</li><li>Restitution et conseils</li><li>Suivi et remédiation cognitive si nécessaire</li></ul></div></article>
    <article class="soin rv"><h2>{ic('phone')}{k['name']}</h2><div><p>{k['bio']}</p><div class="cta" style="margin-top:20px"><a href="tel:{k['tel']}" class="chip">{ic('phone')} {k['tel_h']}</a><a href="{wa(k['tel'])}" class="chip" target="_blank" rel="noopener">{ic('whatsapp-logo')} WhatsApp</a></div></div></article>
  </div>
</section>
''' + book_band('Un <span class="nw">rendez-vous</span> en neuropsychologie', f"Contactez directement Kübra Bozok au {k['tel_h']}, ou le centre au {CENTRE['tel_h']}.") + footer()


def equipe():
    cards = ''
    for m in TEAM:
        fig = f'<figure><img src="{m["img"]}" alt="{m["name"]}, {m["role"].lower()} au centre ABmoment" width="880" height="1100" loading="lazy"></figure>' if m['img'] else f'<div class="monogram" aria-hidden="true">KB</div>'
        cards += f'''<article class="member rv" id="{m['id']}">{fig}<div class="info"><span class="role">{m['role']}</span><h3>{m['name']}</h3><p>{m['bio']}</p><p class="refund">{ic('check')} Conventionné{'e' if m['id'] != 'simon' else ''}</p><div class="contacts"><a href="tel:{m['tel']}" class="chip">{ic('phone')} {m['tel_h']}</a><a href="{wa(m['tel'])}" class="chip" target="_blank" rel="noopener">{ic('whatsapp-logo')} WhatsApp</a></div></div></article>'''
    f = FOUNDER
    bio = ''.join(f'<p>{x}</p>' for x in f['bio'])
    founder = f'''<article class="founder2 rv" id="{f['id']}"><figure><img src="{f['img']}" alt="{f['name']}, fondateur d’ABmoment" width="880" height="1100" loading="lazy"></figure><div><span class="role">{f['role']}</span><h2 class="h2">{f['name']}</h2><div class="bio">{bio}</div><p class="refund">{ic('hand-palm')} Séance ABmoment : techniques ostéopathiques, ventouses, pressothérapie et massage, en un seul soin. Non conventionnée.</p><div class="contacts"><a href="tel:{f['tel']}" class="chip">{ic('phone')} {f['tel_h']}</a><a href="{wa(f['tel'])}" class="chip" target="_blank" rel="noopener">{ic('whatsapp-logo')} WhatsApp</a></div></div></article>'''
    return head('equipe.html', "L'équipe | Kinésithérapeutes, neuropsychologue et séance ABmoment à Schaerbeek | ABmoment",
                "Découvrez l'équipe du centre ABmoment à Schaerbeek : Aydin Bozok, fondateur, Simon Cano et Julie Thiebaut, kinésithérapeutes conventionnés, et Kübra Bozok, neuropsychologue et psychologue clinicienne.") + header('equipe.html') + f'''
<section style="padding-bottom:20px">
  <div class="wrap">
    <p class="kicker rv">L'équipe</p>
    <h1 class="rv">Des praticiens à votre <em>écoute</em></h1>
    <p class="lead rv">Quatre professionnels réunis dans un même centre, pour une prise en charge cohérente de votre corps et de votre esprit.</p>
    <figure class="team-photo rv"><img src="assets/img/equipe-groupe.jpg" alt="Julie Thiebaut, Aydin Bozok et Simon Cano dans le centre ABmoment" width="1170" height="1040" fetchpriority="high"></figure>
    {founder}
    <div class="team">{cards}</div>
  </div>
</section>
''' + book_band() + footer()


def contact():
    people = ''.join(f'''<div class="person"><div><strong>{m['name']}</strong><small>{m['role']} · {m['tel_h']}</small></div><div class="acts"><a class="icon-btn" href="tel:{m['tel']}" aria-label="Appeler {m['name']}">{ic('phone')}</a><a class="icon-btn" href="{wa(m['tel'])}" target="_blank" rel="noopener" aria-label="WhatsApp {m['name']}">{ic('whatsapp-logo')}</a></div></div>''' for m in [{'name': 'Le centre ABmoment', 'role': 'Accueil', 'tel': CENTRE['tel'], 'tel_h': CENTRE['tel_h']}] + TEAM)
    hours = ''.join(f'<span>{d}</span><span>{h}</span>' for d, h in HOURS)
    soc = f'<a class="chip" href="{CENTRE["insta"]}" target="_blank" rel="noopener">{ic("instagram-logo")} @centre.abmoment</a><a class="chip" href="{CENTRE["tiktok"]}" target="_blank" rel="noopener">{ic("tiktok-logo")} TikTok</a>'
    if CENTRE['facebook']:
        soc += f'<a class="chip" href="{CENTRE["facebook"]}" target="_blank" rel="noopener">{ic("facebook-logo")} Facebook</a>'
    maps = MAPS_URL
    return head('contact.html', 'Prendre rendez-vous | Kinésithérapeute à Schaerbeek | ABmoment',
                f"Prenez rendez-vous au centre ABmoment, {CENTRE['street']}, {CENTRE['zip']} {CENTRE['city']} : par téléphone ou WhatsApp, au {CENTRE['tel_h']} ou directement avec votre praticien.") + header('contact.html') + f'''
<section>
  <div class="wrap">
    <p class="kicker rv">Rendez-vous</p>
    <h1 class="rv">Prenez <em>rendez-vous</em></h1>
    <p class="lead rv">Appelez ou écrivez sur WhatsApp au centre, ou directement au praticien de votre choix. Vous pouvez aussi nous écrire sur Instagram.</p>
    <div class="contact-grid">
      <div class="panel rv"><h3>Par téléphone ou WhatsApp</h3><div class="people">{people}</div></div>
      <div style="display:grid;gap:24px">
        <div class="panel rv"><h3>Adresse</h3><p>{CENTRE['street']}<br>{CENTRE['zip']} {CENTRE['city']}, Bruxelles</p>{map_frame(260)}</div>
        <div class="panel rv"><h3>Horaires</h3><div class="hours">{hours}</div><p class="note">Sur rendez-vous.</p></div>
        <div class="panel rv"><h3>Réseaux sociaux</h3><div class="socials">{soc}</div></div>
      </div>
    </div>
  </div>
</section>
''' + footer()


def legal():
    return head('mentions-legales.html', 'Mentions légales | ABmoment', 'Mentions légales du site du centre ABmoment à Schaerbeek.') + header('') + f'''
<section><div class="wrap" style="max-width:760px">
  <h1>Mentions légales</h1>
  <p class="lead">Éditeur : ABmoment, {CENTRE['street']}, {CENTRE['zip']} {CENTRE['city']}, Belgique. Téléphone : {CENTRE['tel_h']}. E-mail : {CENTRE['email']}.</p>
  <p class="sub">Numéro d'entreprise (BCE) : BE 1021.837.986.</p>
  <p class="sub">Hébergement : Cloudflare, Inc., 101 Townsend Street, San Francisco, CA 94107, États-Unis.</p>
  <p class="sub">Modèle anatomique 3D : <a href="https://github.com/lucgrn3/anatomy-models" target="_blank" rel="noopener">anatomy-models</a> (d’après Z-Anatomy, BodyParts3D et NIH 3D), licence <a href="https://creativecommons.org/licenses/by-sa/4.0/deed.fr" target="_blank" rel="noopener">CC BY-SA 4.0</a>, couleurs modifiées.</p>
  <p class="sub">Ce site n'utilise aucun cookie ni outil de mesure d'audience. Plan : © contributeurs OpenStreetMap. Les informations publiées ont un but informatif et ne remplacent pas une consultation.</p>
</div></section>
''' + footer()


def main():
    files = {'index.html': index(), 'soins.html': soins(), 'neuropsychologie.html': neuro(), 'equipe.html': equipe(), 'contact.html': contact(), 'mentions-legales.html': legal()}
    for name, html in files.items():
        (OUT / name).write_text(html, encoding='utf-8')
    (OUT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{SITE}/{"" if f == "index.html" else f}</loc></url>\n' for f in files) + '</urlset>\n', encoding='utf-8')
    (OUT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n', encoding='utf-8')
    print('ok', ', '.join(files))


if __name__ == '__main__':
    main()
