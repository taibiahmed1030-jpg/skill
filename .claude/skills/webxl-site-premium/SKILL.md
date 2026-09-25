---
name: webxl-site-premium
description: Méthode WebXL pour créer un site web premium pour un client (vitrine, 3D, animations, SEO, performance, accessibilité, conformité FR). À utiliser dès qu'on crée ou refond un site client WebXL, une landing page, un site 3D/immersif ou un portfolio haut de gamme.
---

# WebXL — Site premium

Objectif : livrer un site qui se vend cher parce qu'il est **beau, rapide, trouvable sur Google et irréprochable techniquement**. La 3D et les animations sont un bonus au service du client, jamais au détriment du SEO ou de la vitesse.

Ce skill orchestre les autres skills du dépôt :
- `frontend-design` : direction artistique unique (pas de look "template IA").
- `3d-web-experience` : Three.js / React Three Fiber / Spline.
- `gsap-core`, `gsap-timeline`, `gsap-scrolltrigger`, `gsap-plugins`, `gsap-performance`, `gsap-react`, `gsap-frameworks`, `gsap-utils` : animations.
- Plugins (si installés) : `claude-seo` pour l'audit SEO, `playwright-skill` pour tester dans un vrai navigateur.

## 1. Brief (ne jamais sauter)

Avant d'écrire du code, obtenir ou proposer puis faire valider :
- Entreprise, secteur, ville/zone, cible, concurrents.
- Objectif n°1 du site (appels, devis, réservations, ventes).
- Pages voulues, contenus disponibles (logo, photos, textes), langue(s).
- Niveau "wow" : sobre / animé / 3D immersif. Budget et délai.
- Mots-clés visés (ex. "plombier Lyon 3").

Si une info manque, poser la question plutôt que d'inventer.

## 2. Direction artistique

Suivre `frontend-design` : plan de design (4–6 couleurs, typographies, layout en wireframe ASCII, principes), relecture contre le brief, puis code. Un seul élément "wow" par page ; le reste est calme et discipliné.

## 3. Stack

| Projet | Stack |
|---|---|
| Vitrine simple, rapide | Astro (HTML statique) + CSS moderne + GSAP |
| 3D / immersif | Astro ou Next.js + Three.js ou React Three Fiber + GSAP ScrollTrigger |
| E-commerce | Shopify, ou Next.js + solution de paiement |

Privilégier le rendu statique ou côté serveur (SSG/SSR) : le HTML doit contenir tout le contenu dès le chargement.

## 4. 3D sans casser le SEO ni la vitesse

- **HTML d'abord** : titres, textes, liens et images existent dans le HTML ; la 3D est une couche décorative au-dessus.
- Charger la 3D **après** l'affichage (import dynamique, `IntersectionObserver`, `requestIdleCallback`).
- Afficher une image statique (poster) à la place tant que la 3D n'est pas prête, sur mobile bas de gamme et si `prefers-reduced-motion`.
- Modèles en GLB compressé (Draco/Meshopt + textures WebP/KTX2), idéalement < 2–5 Mo au total, < 100k polygones.
- Limiter le `devicePixelRatio` (max 2), mettre en pause le rendu hors écran.

## 5. Animations

- Suivre `gsap-performance` : animer `transform` et `opacity` uniquement.
- Respecter `prefers-reduced-motion` avec `gsap.matchMedia()`.
- Une séquence d'entrée orchestrée plutôt que des fondus sur chaque section.

## 6. SEO (checklist obligatoire)

- `<title>` unique (50–60 car.) et `meta description` (140–160 car.) par page, avec mot-clé + ville.
- Une seule `<h1>` par page, hiérarchie `h2`/`h3` logique.
- URLs propres, `canonical`, `lang="fr"`, `hreflang` si multilingue.
- Données structurées JSON-LD : `Organization` ou `LocalBusiness` (sous-type précis : `Restaurant`, `Plumber`, `HairSalon`…), avec adresse, téléphone, horaires, `geo`, `sameAs`. Ajouter `FAQPage`, `Product`, `BreadcrumbList` si pertinent.
- Open Graph + Twitter Card (image 1200×630).
- `sitemap.xml`, `robots.txt`, favicon + manifest.
- Images : `alt` descriptif, formats AVIF/WebP, `width`/`height`, `loading="lazy"` sauf l'image principale (`fetchpriority="high"`).
- SEO local : nom, adresse, téléphone identiques partout ; rappeler au client de créer/optimiser sa fiche Google Business Profile.
- Si `claude-seo` est installé, lancer un audit avant livraison.

## 7. Performance (objectifs)

- Lighthouse ≥ 90 partout (Performance, Accessibilité, Bonnes pratiques, SEO) sur mobile.
- Core Web Vitals : LCP < 2,5 s, INP < 200 ms, CLS < 0,1.
- Polices : 2 familles max, `font-display: swap`, préchargement de la police principale, auto-hébergées si possible.
- JS minimal sur les pages sans 3D.

## 8. Accessibilité

- Contrastes WCAG AA, focus clavier visible, navigation au clavier complète.
- Balises sémantiques (`header`, `nav`, `main`, `footer`), labels sur tous les champs de formulaire.
- Canvas 3D : `aria-hidden="true"` si décoratif, sinon description textuelle.

## 9. Conformité France

- Page **Mentions légales** (éditeur, SIRET, hébergeur) et **Politique de confidentialité** (RGPD).
- Bandeau cookies conforme CNIL si outils de mesure ou traceurs non exemptés (refuser aussi simple qu'accepter).
- Formulaires : consentement explicite, pas de données collectées inutilement.

## 10. Vérification avant livraison

1. Tester en largeur mobile (375 px), tablette et bureau ; captures d'écran (via `playwright-skill` si disponible) et corriger ce qui cloche.
2. Lighthouse mobile + vérification des données structurées (Rich Results Test).
3. Tous les liens, formulaires et numéros cliquables (`tel:`, `mailto:`) fonctionnent.
4. Aucune erreur dans la console du navigateur.
5. Remettre au client : accès, mode d'emploi pour modifier les contenus, check-list Google Business Profile / Search Console.
