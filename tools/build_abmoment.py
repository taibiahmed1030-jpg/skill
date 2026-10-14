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
    'insta': 'https://www.instagram.com/ab.moment_/',
    'tiktok': 'https://www.tiktok.com/@aydinbozokk_',
    # TODO : lien de la page Facebook du centre (non fourni)
    'facebook': '',
}
TEAM = [
    {'id': 'simon', 'name': 'Simon Cano', 'role': 'Kinésithérapeute', 'tel': '+32471627142', 'tel_h': '+32 471 62 71 42', 'img': 'assets/img/equipe-simon.jpg',
     'bio': "Rééducation, douleurs musculaires et articulaires, récupération après une blessure : Simon vous accompagne avec un suivi adapté à votre corps et à vos objectifs."},
    {'id': 'julie', 'name': 'Julie Thiebaut', 'role': 'Kinésithérapeute', 'tel': '+32456953798', 'tel_h': '+32 456 95 37 98', 'img': 'assets/img/equipe-julie.jpg',
     'bio': "Julie prend en charge vos douleurs et votre rééducation avec écoute et précision, pour vous aider à retrouver une mobilité confortable au quotidien."},
    {'id': 'kubra', 'name': 'Kubra Bozok', 'role': 'Neuropsychologue', 'tel': '+32488839401', 'tel_h': '+32 488 83 94 01', 'img': '',
     'bio': "Kubra réalise des bilans neuropsychologiques et accompagne les patients dont la mémoire, l'attention ou la concentration posent difficulté."},
]
FOUNDER = {'name': 'Aydin Bozok', 'role': "Fondateur d'ABmoment"}
# Horaires provisoires (maquette) : à remplacer par les horaires réels du centre
HOURS = [('Lundi au vendredi', '8h00 à 20h00'), ('Samedi', '9h00 à 14h00'), ('Dimanche', 'Fermé')]
PRICE = {'amount': '60 €', 'duration': '1 heure'}

PAGES = [('index.html', 'Accueil'), ('soins.html', 'Nos soins'), ('neuropsychologie.html', 'Neuropsychologie'), ('equipe.html', "L'équipe"), ('contact.html', 'Rendez-vous')]


def ic(name, extra=''):
    return f'<i class="ic{extra}" style="--i:url(icons/{name}.svg)" aria-hidden="true"></i>'


def wa(tel):
    return 'https://wa.me/' + tel.lstrip('+')


def schema():
    data = {
        '@context': 'https://schema.org', '@type': ['Physiotherapy', 'MedicalBusiness'],
        'name': 'ABmoment', 'description': 'Centre de kinésithérapie et de bien-être à Schaerbeek, Bruxelles : kinésithérapie, ventouses, techniques ostéopathiques, pressothérapie, massothérapie et neuropsychologie.',
        'url': SITE, 'logo': SITE + '/assets/img/logo.png', 'telephone': CENTRE['tel'], 'email': CENTRE['email'],
        'address': {'@type': 'PostalAddress', 'streetAddress': CENTRE['street'], 'postalCode': CENTRE['zip'], 'addressLocality': CENTRE['city'], 'addressRegion': 'Bruxelles', 'addressCountry': 'BE'},
        'areaServed': ['Schaerbeek', 'Bruxelles', 'Saint-Josse-ten-Noode', 'Evere', 'Bruxelles-Ville'],
        'medicalSpecialty': ['Physiotherapy', 'Neurologic'],
        'availableService': [{'@type': 'MedicalTherapy', 'name': n} for n in ['Kinésithérapie', 'Thérapie par ventouses', 'Techniques ostéopathiques', 'Pressothérapie', 'Massothérapie', 'Bilan neuropsychologique']],
        'founder': {'@type': 'Person', 'name': FOUNDER['name']},
        'employee': [{'@type': 'Person', 'name': m['name'], 'jobTitle': m['role'], 'telephone': m['tel']} for m in TEAM],
        'sameAs': [CENTRE['insta'], CENTRE['tiktok']],
    }
    return json.dumps(data, ensure_ascii=False, indent=1)


def head(file, title, desc):
    return f'''<!DOCTYPE html>
<html lang="fr-BE">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<!-- Maquette WEBXL : retirer noindex et le bandeau .demo-bar à la mise en ligne réelle -->
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
<link rel="stylesheet" href="assets/site.css">
<script type="application/ld+json">{schema()}</script>
</head>
<body>
<script>document.documentElement.classList.add('js');</script>
<a class="skip" href="#main">Aller au contenu</a>
<div class="demo-bar">Maquette conçue par <strong>WEBXL</strong>. Horaires et certains textes provisoires.</div>
'''


def header(file):
    cur = ' aria-current="page"'
    links = ''.join(f'<li><a href="{f}"{cur if f == file else ""}>{n}</a></li>' for f, n in PAGES[1:])
    mlinks = ''.join(f'<a href="{f}">{n}</a>' for f, n in PAGES)
    return f'''<header class="hdr">
  <div class="wrap">
    <a href="index.html" class="brand" aria-label="ABmoment, accueil"><img class="brand-logo" src="assets/img/logo.png" alt="" width="56" height="48"><span>ABmoment<small>Kinésithérapie et bien-être</small></span></a>
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
        <a href="index.html" class="brand"><img class="brand-logo" src="assets/img/logo.png" alt="" width="56" height="48"><span>ABmoment<small>Kinésithérapie et bien-être</small></span></a>
        <p style="margin-top:16px;max-width:34ch">Centre de kinésithérapie et de bien-être à Schaerbeek, au service des patients de tout Bruxelles.</p>
      </div>
      <div><h2>Le centre</h2><ul>{''.join(f'<li><a href="{f}">{n}</a></li>' for f, n in PAGES[1:])}</ul></div>
      <div><h2>Contact</h2><ul><li>{CENTRE['street']}</li><li>{CENTRE['zip']} {CENTRE['city']}</li><li><a href="tel:{CENTRE['tel']}">{CENTRE['tel_h']}</a></li><li><a href="mailto:{CENTRE['email']}">E-mail</a></li></ul></div>
      <div><h2>Suivez-nous</h2><ul>{soc}</ul></div>
    </div>
    <div class="legal"><span>© 2026 ABmoment. <a href="mentions-legales.html">Mentions légales</a></span><span>Site conçu par <a href="https://webxl.be" target="_blank" rel="noopener">WEBXL</a></span></div>
  </div>
</footer>
<script type="module" src="assets/site.js"></script>
</body>
</html>
'''


def book_band(title='Prenez rendez-vous', text="Appelez le centre ou contactez directement votre praticien, par téléphone ou WhatsApp."):
    return f'''<section style="padding-top:0"><div class="wrap"><div class="band rv">
  <div><h2 class="h2">{title}</h2><p class="sub">{text}</p></div>
  <div class="cta" style="margin-top:0"><a href="tel:{CENTRE['tel']}" class="btn btn-accent">{ic('phone')} {CENTRE['tel_h']}</a><a href="contact.html" class="btn btn-line">Tous les contacts</a></div>
</div></div></section>
'''


SOINS = [
    ('kine', 'person-simple-run', 'Kinésithérapie', "Rééducation et traitement des douleurs musculaires et articulaires, après une blessure, une opération ou en cas de douleurs installées.",
     ['Mal de dos, nuque et épaules', 'Rééducation après blessure ou opération', 'Entorses, tendinites et douleurs articulaires', 'Récupération des sportifs']),
    ('ventouses', 'drop-half', 'Thérapie par ventouses', "Technique traditionnelle qui aspire doucement la peau pour relâcher les tensions musculaires et favoriser la récupération.",
     ['Tensions du dos et des épaules', 'Récupération après l’effort', 'Associée aux techniques manuelles']),
    ('osteo', 'hand-palm', 'Techniques ostéopathiques', "Mobilisations et techniques manuelles de déblocage articulaire pour retrouver de l’aisance dans le mouvement.",
     ['Raideurs et blocages articulaires', 'Mobilité du dos et du bassin', 'Approche manuelle et précise']),
    ('presso', 'wind', 'Pressothérapie', "Des bottes à compression pneumatique massent les jambes par vagues successives, pour une sensation de légèreté.",
     ['Jambes lourdes', 'Récupération sportive', 'Moment de détente']),
    ('masso', 'sparkle', 'Massothérapie', "Massages de détente ou massages sportifs, adaptés à vos tensions et à votre rythme.",
     ['Massage de détente', 'Massage sportif', 'Relâchement des tensions musculaires']),
]


def index():
    cards = ''.join(f'''<a class="card rv" href="soins.html#{s[0]}">{ic(s[1])}<h3>{s[2]}</h3><p>{s[3]}</p><span class="more">Découvrir {ic('arrow-right')}</span></a>''' for s in SOINS)
    cards += f'''<a class="card rv" href="neuropsychologie.html">{ic('brain')}<h3>Neuropsychologie</h3><p>Bilans de la mémoire, de l’attention et de la concentration, et accompagnement adapté.</p><span class="more">Découvrir {ic('arrow-right')}</span></a>'''
    team = ''.join(f'''<a class="card rv" href="equipe.html#{m['id']}"><span class="role">{m['role']}</span><h3>{m['name']}</h3><p>{m['bio']}</p><span class="more">Voir l'équipe {ic('arrow-right')}</span></a>''' for m in TEAM)
    return head('index.html', 'ABmoment | Centre de kinésithérapie et de bien-être à Schaerbeek, Bruxelles',
                'ABmoment, centre de kinésithérapie et de bien-être à Schaerbeek (Bruxelles) : kinésithérapie, ventouses, techniques ostéopathiques, pressothérapie, massothérapie et neuropsychologie.') + header('index.html') + f'''
<section class="hero" style="padding:0" aria-labelledby="hero-title">
  <div class="wrap">
    <div>
      <p class="kicker rv">ABmoment, Bruxelles</p>
      <h1 id="hero-title" class="rv">Centre de kinésithérapie et de <em>bien-être</em> à Schaerbeek</h1>
      <p class="lead rv">Kinésithérapie, ventouses, techniques ostéopathiques, pressothérapie, massothérapie et neuropsychologie, réunies dans un même centre.</p>
      <div class="cta rv"><a href="contact.html" class="btn btn-accent">Prendre rendez-vous</a><a href="soins.html" class="btn btn-line">Nos soins</a></div>
      <div class="facts rv"><div><strong>3 praticiens</strong>Kinés et neuropsychologue</div><div><strong>{PRICE['amount']}</strong>la séance d'{PRICE['duration']}</div><div><strong>Schaerbeek</strong>{CENTRE['street']}</div></div>
    </div>
    <div class="turn" data-frames="32" data-src="assets/img/corps-360/"><img src="assets/img/corps-360/00.webp" alt="Corps humain anatomique en fibres musculaires, en rotation à 360°" width="600" height="1430" fetchpriority="high"><canvas width="600" height="1430" aria-hidden="true"></canvas><p class="turn-hint" aria-hidden="true">{ic("hand-palm")} Faites-le pivoter</p></div>
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
    <img class="rv" src="assets/img/equipe-julie.jpg" alt="Julie Thiebaut, kinésithérapeute, et Aydin Bozok dans le centre ABmoment" width="1040" height="1298" loading="lazy">
    <div>
      <p class="kicker rv">Le centre</p>
      <h2 class="h2 rv" id="centre-title">Le savoir-faire, l’écoute et la précision</h2>
      <p class="sub rv">Un centre lumineux et apaisant à Schaerbeek, où chaque patient est pris en charge dans sa globalité : sportifs, personnes qui souffrent de douleurs, ou simple besoin de récupérer.</p>
      <p class="quote rv" style="margin-top:32px">« Le corps s’apaise lorsque l’on écoute enfin ce qu’il murmure. »</p>
    </div>
  </div>
</section>

<section style="padding-top:0" aria-labelledby="team-title">
  <div class="wrap">
    <h2 class="h2 rv" id="team-title">Une équipe de spécialistes</h2>
    <p class="sub rv">Deux kinésithérapeutes et une neuropsychologue, réunis par {FOUNDER['name']}, fondateur du centre.</p>
    <div class="cards">{team}</div>
  </div>
</section>
''' + book_band() + footer()


ZONES = [('Nuque et tête', 'Tensions cervicales, raideurs de la nuque et maux de tête liés aux tensions musculaires.', 'f', [(50, 17.5)]),
         ('Épaules', 'Douleurs, tendinites et manque de mobilité de l’épaule.', 'f', [(32, 22.5), (68, 22.5)]),
         ('Dos', 'Lombalgies, dorsalgies et douleurs liées à la posture ou au travail.', 'b', [(50, 30), (50, 42)]),
         ('Bras et poignets', 'Coudes, avant-bras et poignets sollicités par le sport ou le travail.', 'f', [(16, 44), (84, 44)]),
         ('Hanches et bassin', 'Raideurs, douleurs et rééducation de la hanche.', 'f', [(39, 51), (61, 51)]),
         ('Genoux et jambes', 'Entorses, ligaments, rééducation du genou et jambes lourdes.', 'f', [(41, 70), (59, 70)])]


def zones_block():
    spots = ''.join(f'<i class="spot" data-z="{i}" data-v="{z[2]}" style="--x:{x}%;--y:{y}%"></i>' for i, z in enumerate(ZONES) for x, y in z[3])
    items = ''.join(f'<li><button type="button" class="zbtn" data-z="{i}" data-v="{v}" aria-pressed="{str(i == 0).lower()}"><span class="n">0{i + 1}</span><span><b>{t}</b><span>{d}</span></span></button></li>' for i, (t, d, v, _) in enumerate(ZONES))
    return f'''<section style="padding-top:40px" aria-labelledby="zones-title">
  <div class="wrap zones2">
    <div class="zbody rv"><img src="assets/img/corps-360/00.webp" alt="Corps humain anatomique vu de face : la zone choisie s’éclaire" width="600" height="1430" loading="lazy"><img class="zback" src="assets/img/corps-360/16.webp" alt="" width="600" height="1430" loading="lazy">{spots}</div>
    <div class="zhead">
      <p class="kicker rv">Zones traitées</p>
      <h2 class="h2 rv" id="zones-title">Là où vous avez mal</h2>
      <p class="sub rv">Choisissez une zone : elle s’éclaire sur le corps.</p>
    </div>
    <ul class="zlist rv">{items}</ul>
  </div>
</section>
'''


def soins():
    blocks = ''.join(f'''<article class="soin rv" id="{s[0]}"><h2>{ic(s[1])}{s[2]}</h2><div><p>{s[3]}</p><ul>{''.join(f'<li>{x}</li>' for x in s[4])}</ul></div></article>''' for s in SOINS)
    blocks += f'''<article class="soin rv" id="neuro"><h2>{ic('brain')}Neuropsychologie</h2><div><p>Bilans et accompagnement des fonctions cognitives : mémoire, attention, concentration et organisation.</p><ul><li>Bilan neuropsychologique</li><li>Suivi et remédiation cognitive</li><li>Avec Kubra Bozok, neuropsychologue</li></ul><p style="margin-top:16px"><a href="neuropsychologie.html" class="btn btn-line btn-sm">En savoir plus</a></p></div></article>'''
    return head('soins.html', 'Nos soins | Kinésithérapie, ventouses, pressothérapie à Schaerbeek | ABmoment',
                'Kinésithérapie, thérapie par ventouses, techniques ostéopathiques, pressothérapie, massothérapie et neuropsychologie au centre ABmoment à Schaerbeek, Bruxelles.') + header('soins.html') + f'''
<section style="padding-bottom:40px">
  <div class="wrap">
    <p class="kicker rv">Nos soins</p>
    <h1 class="rv">Kinésithérapie et <em>bien-être</em> à Schaerbeek</h1>
    <p class="lead rv">Chaque séance commence par un échange sur vos douleurs et vos objectifs. Le traitement est ensuite adapté à vous.</p>
    <div class="price rv"><div><b>{PRICE['amount']}</b><p>La séance d'{PRICE['duration']}, au même tarif chez chacun de nos praticiens.</p></div><a href="contact.html" class="btn btn-accent">Prendre rendez-vous</a></div>
  </div>
</section>
<section style="padding-top:20px">
  <div class="wrap">
    <article class="soin rv" id="seance"><h2>{ic('heartbeat')}La séance ABmoment</h2><div><p>Notre traitement signature : la thérapie par ventouses associée aux techniques manuelles de déblocage articulaire, en une séance d'{PRICE['duration']}.</p><ul><li>Relâchement des tensions musculaires</li><li>Mobilité articulaire</li><li>Récupération et bien-être</li></ul></div></article>
    {blocks}
  </div>
</section>
''' + zones_block() + book_band() + footer()


def neuro():
    k = TEAM[2]
    return head('neuropsychologie.html', 'Neuropsychologue à Schaerbeek, Bruxelles | Bilan neuropsychologique | ABmoment',
                'Kubra Bozok, neuropsychologue au centre ABmoment à Schaerbeek : bilans neuropsychologiques de la mémoire, de l’attention et de la concentration, et accompagnement.') + header('neuropsychologie.html') + f'''
<section style="padding:0" aria-labelledby="hero-title">
  <div class="wrap">
    <div class="neuro-hero rv">
      <div>
      <p class="kicker">Neuropsychologie</p>
      <h1 id="hero-title">Comprendre le fonctionnement de votre <em>cerveau</em></h1>
      <p class="lead">La neuropsychologie évalue et accompagne les fonctions cognitives : mémoire, attention, concentration, langage et organisation.</p>
      <ul class="chips" aria-label="Fonctions évaluées"><li>Mémoire</li><li>Attention</li><li>Concentration</li><li>Langage</li><li>Organisation</li></ul>
      <div class="cta"><a href="tel:{k['tel']}" class="btn btn-accent">{ic('phone')} Appeler Kubra Bozok</a><a href="{wa(k['tel'])}" class="btn btn-line" target="_blank" rel="noopener">{ic('whatsapp-logo')} WhatsApp</a></div>
      </div>
      <div class="brain" data-tilt><div class="brain-in"><img src="assets/img/cerveau.jpg" alt="Cerveau humain parcouru de connexions neuronales bleues" width="1100" height="1275"><span class="brain-glow" aria-hidden="true"></span></div></div>
    </div>
  </div>
</section>
<section aria-labelledby="why-title">
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
''' + book_band('Un rendez-vous en neuropsychologie', f"Contactez directement Kubra Bozok au {k['tel_h']}, ou le centre au {CENTRE['tel_h']}.") + footer()


def equipe():
    cards = ''
    for m in TEAM:
        blue = m['id'] == 'kubra'
        fig = f'<figure><img src="{m["img"]}" alt="{m["name"]}, {m["role"].lower()}, avec {FOUNDER["name"]}, fondateur d\'ABmoment" width="1040" height="1300" loading="lazy"></figure><p class="caption">{m["name"]} (à droite) avec {FOUNDER["name"]}</p>' if m['img'] else f'<div class="monogram" aria-hidden="true">KB</div>'
        cards += f'''<article class="member rv" id="{m['id']}">{fig}<div class="info"><span class="role">{m['role']}</span><h3>{m['name']}</h3><p>{m['bio']}</p><div class="contacts"><a href="tel:{m['tel']}" class="chip">{ic('phone')} {m['tel_h']}</a><a href="{wa(m['tel'])}" class="chip" target="_blank" rel="noopener">{ic('whatsapp-logo')} WhatsApp</a></div></div></article>'''
    founder = f'''<article class="founder rv"><div><span class="role">{FOUNDER['role']}</span><h3>{FOUNDER['name']}</h3></div><div><p class="sub" style="margin-top:0">{FOUNDER['name']} a fondé ABmoment pour réunir, dans un même lieu, des praticiens qui partagent la même exigence : le savoir-faire, l'écoute et la précision.</p><div class="contacts" style="display:flex;flex-wrap:wrap;gap:8px;margin-top:16px"><a href="tel:{CENTRE['tel']}" class="chip">{ic('phone')} {CENTRE['tel_h']}</a><a href="{wa(CENTRE['tel'])}" class="chip" target="_blank" rel="noopener">{ic('whatsapp-logo')} WhatsApp</a></div></div></article>'''
    return head('equipe.html', "L'équipe | Kinésithérapeutes et neuropsychologue à Schaerbeek | ABmoment",
                "Découvrez l'équipe du centre ABmoment à Schaerbeek : Simon Cano et Julie Thiebaut, kinésithérapeutes, et Kubra Bozok, neuropsychologue.") + header('equipe.html') + f'''
<section style="padding-bottom:20px">
  <div class="wrap">
    <p class="kicker rv">L'équipe</p>
    <h1 class="rv">Des praticiens à votre <em>écoute</em></h1>
    <p class="lead rv">Trois spécialistes réunis dans un même centre, pour une prise en charge cohérente de votre corps et de votre esprit.</p>
    <div class="team">{cards}</div>
    {founder}
  </div>
</section>
''' + book_band() + footer()


def contact():
    people = ''.join(f'''<div class="person"><div><strong>{m['name']}</strong><small>{m['role']} · {m['tel_h']}</small></div><div class="acts"><a class="icon-btn" href="tel:{m['tel']}" aria-label="Appeler {m['name']}">{ic('phone')}</a><a class="icon-btn" href="{wa(m['tel'])}" target="_blank" rel="noopener" aria-label="WhatsApp {m['name']}">{ic('whatsapp-logo')}</a></div></div>''' for m in [{'name': 'Le centre ABmoment', 'role': 'Accueil', 'tel': CENTRE['tel'], 'tel_h': CENTRE['tel_h']}] + TEAM)
    hours = ''.join(f'<span>{d}</span><span>{h}</span>' for d, h in HOURS)
    soc = f'<a class="chip" href="{CENTRE["insta"]}" target="_blank" rel="noopener">{ic("instagram-logo")} @ab.moment_</a><a class="chip" href="{CENTRE["tiktok"]}" target="_blank" rel="noopener">{ic("tiktok-logo")} TikTok</a>'
    if CENTRE['facebook']:
        soc += f'<a class="chip" href="{CENTRE["facebook"]}" target="_blank" rel="noopener">{ic("facebook-logo")} Facebook</a>'
    maps = 'https://www.google.com/maps/search/?api=1&amp;query=Rue+Hancart+12,+1030+Schaerbeek'
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
        <div class="panel rv"><h3>Adresse</h3><p>{CENTRE['street']}<br>{CENTRE['zip']} {CENTRE['city']}, Bruxelles</p><p style="margin-top:14px"><a class="chip" href="{maps}" target="_blank" rel="noopener">{ic('map-pin')} Itinéraire</a></p></div>
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
  <!-- TODO : numéro d'entreprise (BCE), numéros INAMI des praticiens, hébergeur -->
  <p class="sub">Numéro d'entreprise et hébergeur : à compléter.</p>
  <p class="sub">Ce site n'utilise aucun cookie ni outil de mesure d'audience. Les informations publiées ont un but informatif et ne remplacent pas une consultation.</p>
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
