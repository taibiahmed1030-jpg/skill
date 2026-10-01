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

### Décisions explicitement en attente de l'utilisateur

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
