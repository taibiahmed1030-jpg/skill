# Audit de couverture — 32 domaines demandés vs connaissances existantes

**Correction du 2026-10-02** : ce document annonçait initialement "35
domaines" par erreur (artefact d'un résumé intermédiaire de session).
Vérification faite sur le message original verbatim de l'utilisateur
(phase "pipeline SOURCE→CLAIM→HYPOTHÈSE") : la liste contient exactement
**32 domaines nommés**, pas 35. Les 32 lignes du tableau ci-dessous
correspondent terme à terme à cette liste originale — aucun domaine n'a
été omis, le chiffre "35" était simplement faux.

**But** : avant de chercher de nouvelles sources, savoir précisément ce qui
est déjà couvert par `TRADING_KNOWLEDGE_BASE.md` (formation Elliot, seule
source ingérée à ce jour) pour prioriser la recherche sur les domaines
sous-couverts plutôt que de redemander la même chose sous un autre angle.
Évaluation faite en relisant les sections 1-14 du fichier, pas de mémoire.

Légende : ✅ couvert (au moins une connaissance structurée exploitable) ·
🟡 effleuré (mentionné mais pas structuré, pas assez pour une hypothèse
indépendante) · ❌ absent.

| # | Domaine | Statut | Où / pourquoi |
|---|---|---|---|
| 1 | Trading systématique (process, discipline) | ✅ | Section 1 (process en 6 étapes), section 9 (risk mgmt) |
| 2 | Quantitative trading (au sens recherche/stats) | 🟡 | Aucune méthode quanti dans la source elle-même ; couvert côté *infrastructure* par `03_model_approaches.md`, pas côté *contenu de marché* |
| 3 | Market microstructure | ❌ | Rien sur carnet d'ordres, bid/ask, formation du prix tick par tick |
| 4 | Price action | ✅ | Section 3, complète (bougies, S/R, trendlines, Fibonacci) |
| 5 | Technical analysis (classique) | ✅ | Sections 3-4 (indicateurs, patterns, MM, RSI) |
| 6 | Macro trading | ✅ | Section 2, large (cycles, régimes, CPI, yield curve, DXY, pétrole) |
| 7 | Momentum | 🟡 | Mentionné via RSI/divergences et "angle de trendline" mais pas de stratégie momentum formalisée |
| 8 | Mean reversion | ❌ | Aucune mention — la source est orientée trend-following/breakout |
| 9 | Trend following | ✅ | Section 3 (trading dans le sens de la tendance), section 5 (setups) |
| 10 | Volatilité | 🟡 | VIX traité comme indicateur de régime (section 2, H003) mais pas de stratégie de volatilité en tant que telle (pas d'options, pas de vol targeting) |
| 11 | Volume | ❌ | Jamais mentionné dans la source (ni volume profile, ni volume spike) |
| 12 | Order flow | ❌ | Absent |
| 13 | Market profile | ❌ | Absent |
| 14 | Liquidité (microstructure, pas macro) | ❌ | Seul le sens macro de "liquidité" (banques centrales) est traité, pas la liquidité de marché/carnet |
| 15 | Régimes de marché | 🟡 | 4 régimes macro (section 2) + régime de volatilité (VIX) — mais pas de détection de régime formalisée pour une stratégie |
| 16 | Sentiment | 🟡 | Risk-on/risk-off, rotations sectorielles (section 2) — pas d'indice de sentiment dédié (put/call ratio, AAII, etc.) |
| 17 | Positioning | 🟡 | "Overcrowded positioning" mentionné une fois (section 3, note Fibonacci) — pas structuré, c'est précisément H005 marquée `non_testable` par manque de données |
| 18 | COT (Commitment of Traders) | ❌ | Jamais cité explicitement |
| 19 | Options / volatilité implicite | ❌ | Absent (VIX est utilisé comme indicateur, jamais comme sous-jacent tradable) |
| 20 | Analyse intermarchés | 🟡 | "Chaîne de corrélation" dollar→pétrole→inflation→taux→obligations→actions (section 2, fin) — une ligne, pas développé |
| 21 | Indicateurs macroéconomiques | ✅ | Section 2, détaillé (growth/inflation/hybrid, leading/coincident/lagging) |
| 22 | Arbitrage statistique | ❌ | Absent |
| 23 | Pairs trading | ❌ | Absent (le "hedging via paire corrélée", section 5, est proche mais c'est une couverture de risque, pas un pairs trade spéculatif) |
| 24 | Factor investing | ❌ | Absent (pas de facteurs actions type value/quality/size) |
| 25 | ML appliqué aux marchés | 🟡 | Couvert côté architecture (`03_model_approaches.md`), pas de contenu domaine (quelles features marchent en pratique) |
| 26 | Prévision de séries temporelles | 🟡 | Idem — couvert côté famille de modèles, pas de connaissance marché spécifique |
| 27 | Construction de portefeuille | ❌ | Absent — la source traite un trade à la fois, jamais d'allocation multi-actifs |
| 28 | Risk management | ✅ | Section 9, complet (sizing, R, règles de perte) |
| 29 | Exécution | 🟡 | OCO/straddle (section 5), construction progressive de position (section 5) — mais rien sur l'exécution algorithmique (TWAP/VWAP, etc.) |
| 30 | Coûts de transaction | 🟡 | Mentionné uniquement comme principe général dans `04_protocols.md` étape C, pas de données chiffrées par marché pour la plupart des catégories (voir `01_market_comparison.md` pour les quelques ordres de grandeur déjà réunis) |
| 31 | Market impact | ❌ | Absent |
| 32 | Finance comportementale | 🟡 | Section 11 (erreurs à éviter) traite les biais du *trader*, pas les biais de marché agrégés (disposition effect au niveau prix, etc.) |

## Synthèse

- **Bien couvert (6/32)** : price action, technical analysis, macro
  trading, trend following, indicateurs macro, risk management. Tous issus
  d'une seule source généraliste (formation retail forex/indices) —
  cohérent et attendu, mais **aucun de ces domaines n'a de deuxième source
  indépendante** pour l'instant (aucun des 10 hypothèses actuelles n'a
  `nb_sources > 1`).
- **Totalement absent (10/32)** : market microstructure, mean reversion,
  volume, order flow, market profile, liquidité (sens microstructure), COT,
  options/IV, arbitrage statistique, pairs trading, factor investing,
  construction de portefeuille, market impact. **Priorité de recherche** —
  ce sont des familles d'idées entières sur lesquelles le projet n'a
  aujourd'hui aucune hypothèse possible.
- **Effleuré (16/32)** : à traiter en priorité secondaire — chercher une
  source qui structure ce qui n'est aujourd'hui qu'une ligne ou une
  observation qualitative (momentum, volatilité, régimes, sentiment,
  positioning, intermarché, ML/time-series, exécution, coûts, comportemental).

## Conséquence pour la recherche de sources (tâche suivante)

La recherche de sources candidates (`SOURCE_REGISTRY.md`) doit délibérément
sur-pondérer les domaines ❌ et 🟡 plutôt que de chercher une 2e vidéo
généraliste de price action/risk management — ce dernier domaine a déjà une
base solide et gagnerait peu à être dupliqué sans raison (règle de
non-redondance explicitement demandée par l'utilisateur).
