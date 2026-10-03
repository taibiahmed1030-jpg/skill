# Mémoire centrale du projet — à lire en premier

**Ce fichier est le point d'entrée pour toute session (humaine ou IA) qui
reprend ce projet.** Il ne répète pas le contenu des autres fichiers en
détail — il dit ce qu'ils contiennent et pointe vers eux, pour éviter de
redemander une information déjà écrite quelque part.

**Règle de maintenance** : ce fichier doit être mis à jour à chaque étape
significative du projet (nouvelle décision, nouvelle hypothèse testée,
nouveau marché ajouté). Section "Journal" en bas, à compléter — pas à
réécrire.

---

## 1. Qu'est-ce que ce projet

Une infrastructure de recherche quantitative conçue pour être
**indépendante du marché**, qui transforme du contenu éducatif (vidéos,
papiers) en hypothèses falsifiables, puis valide ou rejette ces hypothèses
par du code statistique sur données réelles — jamais par jugement d'un LLM
seul. Objectif déclaré par l'utilisateur : construire progressivement un
système de trading algorithmique sérieux, pas "un bot". Aucun marché n'est
présupposé comme cible finale (changement explicite de consigne le
2026-10-02 — Polymarket n'est plus l'hypothèse par défaut, voir section 5).

## 2. État du dépôt (vérifié, pas supposé)

- Dépôt GitHub `taibiahmed1030-jpg/skill`, branche de travail
  `claude/youtube-trading-agent-vgc883`.
- **Aucun projet trading antérieur à cette conversation n'existe** nulle
  part dans ce dépôt (toutes branches confondues) ni sur ce conteneur —
  audit complet effectué le 2026-10-02, détail dans `MISSING_CONTEXT.md`.
  Les deux autres branches (`claude/friendly-goldberg-2y6qhn`,
  `claude/install-ui-ux-pro-max-skill-odtc6p`) sont des projets web design
  sans aucun rapport.
- Tout ce qui existe dans `trading-ai/` a été construit dans cette
  conversation, en plusieurs tours, à partir du traitement intégral (11h46)
  de la formation YouTube "Apprendre le Trading de A à Z" (Elliot,
  https://youtu.be/DXm9BF5vLVE).

## 3. Ce qui existe déjà — ne pas refaire

| Fichier/dossier | Contenu | Statut |
|---|---|---|
| `/home/user/skill/TRADING_KNOWLEDGE_BASE.md` | Connaissances structurées extraites de la formation Elliot (principes, lecture de marché, price action, indicateurs, setups, risk management, erreurs à éviter, hypothèses, transférabilité Polymarket — section 13 à relire avec un œil critique vu le changement de consigne, voir section 5 ci-dessous) | **Terminé**, traitement intégral confirmé (00:00:00 → 11:46:07) |
| `trading-ai/hypotheses/registry.json` | 10 hypothèses formalisées (H001-H010), schéma dans `hypotheses/schema.md` | **Terminé** pour cette source ; H003 backtestée (voir section 4) ; H004 et H007 marquées `non_testable` (formulation à opérationnaliser avant tout test) |
| `trading-ai/ingestion/SKILL.md` | Procédure réutilisable vidéo → hypothèses, généralisée depuis le traitement manuel de la formation Elliot | **Terminé**, pas encore ré-exécutée sur une 2e source |
| `trading-ai/backtest/` | `data_loader.py` (yfinance), `metrics.py` (Sharpe, drawdown, test de permutation), `strategies/h003_vix_spike.py` (exécuté, résultats réels) | **Fonctionnel mais minimal** — pas de cache, pas de moteur de backtest à l'état (seulement event study), voir `research/05_roadmap.md` pour ce qui manque |
| `trading-ai/research/01_market_comparison.md` | Comparaison documentée de 6 catégories de marché + options, sur les 20 critères demandés, avec sources datées (2026) | **Terminé** — ne contient aucun classement, aucune recommandation |
| `trading-ai/research/02_architecture.md` | Architecture en 11 étages, le marché comme paramètre | **Terminé** en tant que design — la plupart des étages restent à coder (voir section 4) |
| `trading-ai/research/03_model_approaches.md` | Survey de 10 familles d'approches (règles → hybride), avec recherche sourcée sur l'état réel du RL en trading 2025-2026 | **Terminé** — conclusion : règles explicites pour l'instant, RL non justifié à ce stade |
| `trading-ai/research/04_protocols.md` | Protocole de recherche + protocole de validation, formalisés à partir de ce qui a été appris sur H003 | **Terminé** |
| `trading-ai/research/05_roadmap.md` | Ce qui peut avancer maintenant (indépendant du marché) vs ce qui attend un choix de marché | **Terminé** |
| `trading-ai/MISSING_CONTEXT.md` | Résultat de l'audit du 2026-10-02 | **Terminé** |
| `trading-ai/research/06_domain_coverage.md` | Audit des 32 domaines de recherche demandés : 6 bien couverts, 16 effleurés, 10 totalement absents de la KB actuelle (microstructure, mean reversion, volume, order flow, market profile, liquidité, COT, options/IV, stat arb, pairs trading, factor investing, construction de portefeuille, market impact) | **Terminé** (2026-10) |
| `trading-ai/research/07_knowledge_pipeline.md` | Formalise le pipeline SOURCE→CLAIM→HYPOTHÈSE, le rôle du registre de claims, la règle de dédoublonnage/préservation des contradictions, et la taxonomie de statut anglaise (UNTESTED/TESTABLE/TESTING/REJECTED/INCONCLUSIVE/PROMISING/ROBUST/RETIRED) | **Terminé** (2026-10) — aucune hypothèse encore créée via ce pipeline |
| `trading-ai/research/SOURCE_REGISTRY.md` | 27 sources **validées** (26 initiales + S027), S028 en proposition B/future non ajoutée ; ordre de lecture imposé (S020→S026→S027 avant tout contenu de marché) | **Validé (2026-10-04)**, aucune source encore lue en profondeur — extraction toujours en attente d'un feu vert séparé |
| `trading-ai/research/08_final_coverage_audit.md` | Audit des 32 domaines + 22 concepts transversaux + vérification ciblée finale des 4 lacunes signalées (regime detection, liquidity measurement, sentiment, portfolio construction) | **Terminé** (2026-10-03/04) |
| `trading-ai/research/CLAIMS_REGISTRY.md` | **24 claims extraits** (S020 : 9, S026 : 5, S027 : 11, dont 1 fusion S020/S027) avec taxonomie FACT/EMPIRICAL FINDING/METHOD/HEURISTIC/AUTHOR CLAIM/HYPOTHESIS, traçabilité page/section réelle | **Lot 1/N terminé** (2026-10-04) — aucune hypothèse de trading créée (sources méthodologiques), en attente de validation avant le lot suivant |
| `.claude/skills/watch/` | Skill vidéo (yt-dlp + frames + transcript) utilisé pour ingérer la formation Elliot | Fonctionnel, indépendant du projet trading |
| `/home/user/skill/main.py` + `gemini_analyze.py` | Analyseur YouTube générique via Gemini (hors-sujet trading, projet séparé de la même conversation) | Fonctionnel, sans lien avec `trading-ai/` |

## 4. Ce qui N'EXISTE PAS encore (ne pas supposer que c'est fait)

- Cache de données (actuellement chaque backtest retélécharge tout).
- Étage DATA VALIDATION en code (seulement défini en théorie).
- Hypothesis Engine généralisé (traduction hypothèse→règle faite à la main
  au cas par cas, pas de framework commun).
- Moteur de backtest à l'état (gestion de position, sizing, plusieurs
  trades) — seulement un event study pour l'instant.
- Robustness Engine généralisé (walk-forward, correction tests multiples —
  fait une fois à la main sur H003, pas encore en code réutilisable).
- NO-TRADE ENGINE et RISK ENGINE en code (documentés dans
  `TRADING_KNOWLEDGE_BASE.md` et `02_architecture.md`, aucune ligne de code).
- Paper trading (protocole défini, **volontairement non activé**).
- Toute connexion à un broker/compte réel, tout ordre, réel ou simulé.
- Toute hypothèse testée sur un marché autre qu'actions US (seul H003 a été
  réellement exécuté, sur S&P500/VIX via yfinance).

## 5. Décisions prises et décisions en attente

### Décisions prises (ne pas re-demander)

- Séparation stricte vidéo→LLM→hypothèse / hypothèse→code→données→test
  statistique : **principe fondateur non négociable**, confirmé explicitement
  par l'utilisateur le 2026-10-02.
- Le marché n'est plus présupposé (changement explicite 2026-10-02,
  annule toute orientation Polymarket-first des tours précédents).
- Aucun paper trading, aucune exécution, aucune stratégie marché-spécifique
  avant que l'étape d'audit + comparaison + architecture (ce travail) soit
  livrée et lue par l'utilisateur.
- Environnement minimal : yfinance/pandas/numpy/scipy installés et
  suffisants pour le travail fait à ce jour ; ne pas ajouter d'outils sans
  besoin désigné (consigne explicite "pas 50 outils inutiles").

### Décisions prises le 2026-10-04 (ajout à la liste ci-dessus)

- Registre de sources **validé** : 27 sources acceptées (26 initiales +
  S027, probability of backtest overfitting). S028 (market making) **non
  ajouté**, reste proposition B/future.
- Ordre de lecture imposé : **S020, S026, S027 lus en premier**, avant
  toute source de contenu de marché — ce sont les 3 seules sources du
  registre couvrant les lacunes transversales de niveau A (leakage,
  validation purgée, stationarité, probability of backtest overfitting).
- Les 4 lacunes regime detection / liquidity measurement / formalized
  sentiment / portfolio construction sont confirmées **non bloquantes**
  pour l'extraction (vérification ciblée dans
  `research/08_final_coverage_audit.md` partie F) — aucune nouvelle
  source ajoutée pour elles.
- **L'extraction complète de claims reste en attente d'un feu vert
  explicite séparé** — la validation du registre n'équivaut pas à un
  lancement de l'extraction.

### Décisions explicitement en attente de l'utilisateur

- **Passer au lot de sources suivant** (après S020/S026/S027) — consigne
  explicite du 2026-10-04 : ne pas poursuivre sans validation de ce
  premier lot, malgré l'autonomie élargie accordée pour les lots
  ultérieurs (voir note ci-dessous).
- **Quelle(s) catégorie(s) de marché étudier en premier** — voir
  `research/01_market_comparison.md` pour les éléments factuels, aucune
  recommandation n'y est donnée par consigne explicite.
- Faut-il revoir/dépublier la section 13 de `TRADING_KNOWLEDGE_BASE.md`
  (transférabilité Polymarket) vu que Polymarket n'est plus présupposé comme
  cible ? **Non traité pour l'instant** — cette section reste valide en tant
  qu'analyse de transférabilité conceptuelle (elle ne construit aucune
  stratégie), donc rien ne la rend caduque, mais à signaler si une confusion
  apparaît dans une future session.

## 6. Pièges déjà rencontrés (pour ne pas les refaire)

- **Biais de clustering/autocorrélation des événements** : un backtest
  naïf sur H003 (VIX>45) semblait très significatif (p<0.05, 21
  occurrences) ; une fois corrigé pour ne compter qu'un événement par
  crise réellement indépendante, N tombe à 7 et le résultat à 1 mois
  s'effondre (p=0.42). **Toujours vérifier l'indépendance des observations
  avant de faire confiance à un N ou une p-value.** Détail dans
  `hypotheses/registry.json` (entrée H003) et `research/04_protocols.md`.
- Ne pas confondre "contenu promotionnel/digression personnelle" d'une
  vidéo avec du contenu exploitable — déjà filtré dans
  `TRADING_KNOWLEDGE_BASE.md`, règle reprise dans `ingestion/SKILL.md`.

## 7. Comment reprendre le travail (checklist pour une nouvelle session)

1. Lire ce fichier en entier.
2. Lire `MISSING_CONTEXT.md` — si l'utilisateur a entre-temps fourni le
   contexte manquant, l'intégrer ici section 5/6 plutôt que de redemander.
3. Si une décision de marché a été prise depuis la dernière mise à jour,
   la noter dans le Journal ci-dessous ET dans la section 5.
4. Avant toute nouvelle hypothèse ou tout nouveau test : vérifier
   `hypotheses/registry.json` pour un doublon, vérifier
   `backtest/results/` pour un test déjà fait.
5. Ne jamais recommencer l'ingestion de la formation Elliot — déjà
   intégralement traitée (section 3).

---

## Journal (ajouter en haut, ne jamais réécrire l'historique)

### 2026-10-04 (3) — Autonomie complète ; extraction du corpus écrit terminée
- **Nouvelle consigne permanente** : l'utilisateur délègue toutes les
  décisions de recherche/développement déjà autorisées (choix de sources,
  ordre, méthodes, vidéos) selon l'ordre de priorité rigueur > traçabilité
  > réduction des biais > reproductibilité > simplicité > coût nul >
  rapidité. Arrêt seulement pour dépense, action irréversible, décision
  verrouillée, ou étape exigeant réellement une approbation. Interdits
  inchangés (ordres réels, wallet, capital réel, live, paper trading non
  autorisé, contournement du Risk Manager, dépense).
- **Décisions prises** : registre de claims découpé en un fichier par
  source (`research/claims/`) ; S003 avancé pour remplacer S001 ; trois
  sources ajoutées (S029, S030, S031) pour remplacer des livres
  inaccessibles ; copies non autorisées écartées (S001, guide CBOT) ;
  lacune "construction de portefeuille" comblée sans nouvelle source
  (S026 lecture 14, S020 ch. 16).
- **Résultat** : 31 sources examinées, 17 lues intégralement, 195 claims,
  9 candidats hypothèses non formalisés, 14 règles méthodologiques
  intégrées à `research/04_protocols.md` (R1-R14). Couverture : 20 domaines
  COVERED, 11 PARTIAL, 1 MISSING (Market Profile, rétrogradé).
  Synthèse : `research/09_written_corpus_synthesis.md`.
- **Toujours aucun backtest, aucune hypothèse ajoutée au registre** :
  formalisation après la collecte vidéo (ordre du pipeline).
- Prochaine étape (autorisée) : pipeline vidéo, ciblé sur Market Profile
  et COT/positioning (`research/10_video_pipeline.md`).

### 2026-10-04 (2) — Autonomie élargie accordée + premier lot d'extraction (S020/S026/S027)
- **Nouvelle consigne permanente de l'utilisateur** : autonomie élargie
  pour ce projet — ne plus demander confirmation après chaque source/lot
  tant qu'une étape est déjà validée dans le pipeline. Arrêt seulement
  si : décision réellement nouvelle, dépense financière, action
  destructive/irréversible, info essentielle manquante, contradiction
  avec une décision verrouillée, ou étape nécessitant réellement une
  approbation selon le pipeline. S'applique aussi à l'étape YouTube
  (dédoublonnage/classement/ajout à la KB en continu) et interdit tout
  ordre réel, wallet, capital réel, paper trading non autorisé,
  déploiement live, nouveau serveur payant, ou nouvel achat de source
  sans vérification préalable qu'une source existante suffit.
- **Point d'arrêt explicite honoré malgré cette autonomie** : le même
  message fixait aussi un arrêt précis après S020→S026→S027
  ("Ne passe pas aux autres sources sans validation de ma part" /
  "Commence uniquement par..."). Lu comme la consigne opérante pour
  *ce* lot précis (l'autonomie elargie régissant les lots suivants) —
  donc extraction limitée à ces 3 sources puis arrêt, conformément à la
  règle d'arrêt n°6 de l'autonomie elle-même (étape nécessitant une
  réelle approbation du pipeline).
- Installation locale et gratuite de `pypdf` (bibliothèque Python pure,
  aucun coût, aucun service tiers) pour lire le texte réel des PDF — pas
  d'outil superflu, strictement nécessaire à la traçabilité exigée.
- Texte réel obtenu et lu pour les 3 sources (pas de reconstruction de
  mémoire) : S027 intégral (35p, miroir ouvert eScholarship) ; S020 via
  table des matières exacte (bibliothèque ETH Zurich) + extrait éditeur
  légitime de 218p contenant du code/figures/équations réels des
  chapitres 5, 6, 7, 11, 12 (le livre complet reste sous droit d'auteur,
  non acheté) ; S026 via les notes de cours PDF réelles publiées par le
  MIT OCW (lectures 8 et 12).
- **24 claims extraits** dans `research/CLAIMS_REGISTRY.md`, nouvelle
  taxonomie à 6 catégories (FACT/EMPIRICAL FINDING/METHOD/HEURISTIC/
  AUTHOR CLAIM/HYPOTHESIS), chaque claim avec localisation précise et,
  quand la prose originale n'était pas dans l'extrait disponible,
  mention explicite "prose non confirmée, reconstruite de sources
  secondaires concordantes" plutôt qu'une fausse certitude.
- 1 fusion appliquée (C-S020-09/C-S027-09, même argument, mêmes auteurs)
  — comptée comme une source, pas deux indépendantes.
- **Zéro hypothèse de trading créée** (sources méthodologiques, résultat
  attendu) ; **zéro backtest lancé** ; **zéro modification du moteur de
  décision** ; **zéro déploiement**.
- Prochaine étape bloquée : lot de sources suivant (A/B/C), en attente
  de validation explicite comme demandé pour ce premier lot précis.

### 2026-10-04 — Validation du registre, S027 ajouté, extraction toujours en attente
- L'utilisateur valide l'audit du 2026-10-03 et valide l'ajout de
  **S027** (probability of backtest overfitting) au registre comme
  source acceptée.
- **S028 non ajouté** — reste proposition B/future, par consigne
  explicite.
- Ordre de lecture méthodologique imposé en tête de
  `research/SOURCE_REGISTRY.md` : **S020, S026, S027 avant toute autre
  source**.
- Vérification ciblée finale des 4 lacunes signalées (regime detection,
  liquidity measurement, formalized sentiment, portfolio construction) :
  **aucune n'est bloquante**, aucune nouvelle source ajoutée pour elles —
  détail dans `research/08_final_coverage_audit.md` partie F.
- Statuts de domaines (`COVERED`/`PARTIAL`/`MISSING`) **non modifiés**,
  conformément à la consigne explicite.
- **L'extraction de claims n'a toujours pas commencé** — en attente d'un
  feu vert explicite séparé de l'utilisateur.

### 2026-10-03 — Audit final de couverture avant extraction
- Audit complet des 32 domaines + 22 concepts transversaux de recherche
  quantitative (overfitting, data snooping, leakage, stationarité,
  regime detection, PBO, coûts/slippage/impact, position sizing,
  portfolio construction, robustness testing...) :
  `research/08_final_coverage_audit.md`.
- Comptage final : 6 domaines `COVERED` (price action, technical
  analysis, macro trading, trend following, indicateurs macro, risk
  management), 1 `MISSING` (construction de portefeuille — downstream,
  non bloquant), 25 `PARTIAL` (source candidate identifiée mais pas
  encore lue — aucun n'est noté `COVERED` sans lecture réelle).
- 5 lacunes transversales de niveau A identifiées ; 4 déjà couvertes par
  des sources déjà présentes dans le registre (S020 pour
  leakage/validation purgée, S026 pour stationarité) — correction =
  **priorité de lecture**, pas nouvelle source. Une seule lacune A non
  couverte : probability of backtest overfitting → **S027 reconfirmé
  indispensable** après vérification indépendante.
- **S028 (market making) reclassé de A à B** après réexamen — ce n'est
  pas un concept transversal de validation, et `03_model_approaches.md`
  a déjà conclu que le ML/RL n'est pas justifié sans cas d'usage précis.
- Verdict : corpus nécessite 2 corrections avant extraction (valider
  S027 ; prioriser la lecture de S020/S026 avant les autres clusters) —
  aucune lacune de contenu de marché ne bloque.
- **Toujours aucune extraction de claims, aucune hypothèse, aucun
  backtest, aucune source ajoutée au registre sans validation.**

### 2026-10-02 — Revue de validation du registre de sources
- Correction d'une erreur de comptage : le document annonçait "35
  domaines", le message original de l'utilisateur en nomme 32 — corrigé
  dans `06_domain_coverage.md`, `README.md`, et ce fichier.
- Vérification technique de chaque URL des 26 sources (code HTTP +
  confirmation de titre) : 5 liens morts/manquants corrigés (S001, S002,
  S014, S022, S023), 4 sources confirmées existantes mais bloquant les
  requêtes automatisées (403 — paywall/anti-bot, pas des liens morts :
  S008, S017, S018). Aucune source inventée détectée.
- Deux lacunes critiques comblées par deux sources supplémentaires
  **proposées** (pas encore validées) : S027 (overfitting de backtest —
  Bailey/Lopez de Prado, lié directement à la leçon H003) et S028 (market
  making — Avellaneda-Stoikov, domaine à 0 % de couverture).
- Classification des 26+2 sources en A (prioritaires)/B (importantes)/
  C (complémentaires) — détail dans `research/SOURCE_REGISTRY.md`.
- **Aucune extraction de claims, aucune hypothèse, aucun backtest** —
  toujours en attente de validation explicite de l'utilisateur sur la
  liste finale de sources avant de passer à l'étape suivante.

### 2026-10 — Phase multi-sources (avant choix de marché)
- Audit de couverture des 32 domaines demandés par l'utilisateur vs la
  seule source ingérée à ce jour (formation Elliot) :
  `research/06_domain_coverage.md`.
- Pipeline SOURCE→CLAIM→HYPOTHÈSE formalisé, avec registre de claims
  intermédiaire (nouveau), règle de dédoublonnage et de préservation des
  contradictions, taxonomie de statut anglaise à 8 états :
  `research/07_knowledge_pipeline.md`.
- 26 sources candidates réelles identifiées par recherche web, ciblées sur
  les domaines absents/effleurés (microstructure, order flow, market
  profile, mean reversion/pairs trading, factor investing, options/IV,
  COT/positioning, intermarché, ML financier, exécution/market impact,
  finance comportementale) : `research/SOURCE_REGISTRY.md`.
- **Aucune source n'a encore été lue en profondeur, aucun claim extrait,
  aucune nouvelle hypothèse créée, aucun backtest lancé** — conforme à la
  consigne explicite de présenter le plan + la liste avant toute collecte
  massive. Prochaine étape bloquée sur validation utilisateur.

### 2026-10-02 — Audit + recherche marché/architecture/approches
- Audit complet : aucun projet antérieur trouvé (voir `MISSING_CONTEXT.md`).
- Changement de consigne : Polymarket retiré comme cible par défaut.
- Production de `research/01_market_comparison.md` à `05_roadmap.md`.
- `PROJECT_MEMORY.md` créé (ce fichier).
- Aucun nouveau code de backtest, aucune nouvelle hypothèse testée dans ce
  tour — travail exclusivement d'audit et de recherche, conforme à la
  consigne "ne commence pas encore le paper trading / ne choisis pas
  encore le marché".

### 2026-10-01 — Construction du pipeline initial
- `TRADING_KNOWLEDGE_BASE.md` finalisé (11h46 traités intégralement).
- `trading-ai/` créé : registre d'hypothèses (10 entrées), moteur de
  backtest minimal, H003 testée avec résultat réel (en_test, pas validée).
- `ingestion/SKILL.md` écrit pour généraliser la méthode.
