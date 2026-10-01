# Trading AI — pipeline connaissance → hypothèse → validation empirique

## Le problème que ce projet résout

Donner à une IA des heures de formations/vidéos de trading pour qu'elle
"devienne bonne en trading" a deux défauts : (1) ça consomme énormément de
tokens si on relit le contenu brut à chaque fois, (2) une IA peut prendre
une affirmation de formateur pour une vérité sans la challenger.

Ce projet sépare les deux métiers qui étaient mélangés :

| Métier | Qui le fait | Coût | Rigueur |
|---|---|---|---|
| Lire une vidéo et en extraire des idées | LLM, **une seule fois** par source | Payé une fois, jamais revécu | Force une séparation affirmation/hypothèse (voir `TRADING_KNOWLEDGE_BASE.md`) |
| Décider si une idée est rentable | Code déterministe sur données réelles | Quasi gratuit, répétable à volonté | Statistique (p-value, indépendance des événements, stabilité par sous-période) |

**Aucune IA ne décide seule qu'une stratégie est bonne.** Elle formalise des
hypothèses (étape 1) ; seul le backtest tranche (étape 2) ; et même un
backtest favorable doit passer par du paper trading avant tout capital réel
(étape 3). C'est la même discipline que celle enseignée dans la formation
source elle-même (démo → petit risque réel → scaling), appliquée à un
pipeline automatisé plutôt qu'à un humain.

## Structure

```
trading-ai/
├── ingestion/          Process réutilisable : vidéo → hypothèses structurées
│   └── SKILL.md
├── hypotheses/          Le registre persistant — la mémoire qui compound
│   ├── registry.json    10 hypothèses déjà extraites de la formation Elliot
│   └── schema.md         Règles de promotion de statut (jamais décidées "à l'instinct")
└── backtest/            Le moteur empirique — du code, pas du jugement LLM
    ├── data_loader.py    Source de données interchangeable (yfinance par défaut)
    ├── metrics.py        Sharpe, drawdown, test de permutation
    ├── strategies/        Un script de test par hypothèse (ex: H003 déjà exécuté)
    ├── results/            Sorties JSON brutes, conservées pour audit
    └── README.md           Règles de rigueur + procédure paper trading
```

## État actuel (2026-10-01)

- 10 hypothèses dans le registre, extraites de *"Apprendre le Trading de A à
  Z"* (Elliot, 11h46, intégralement traitée).
- 1 hypothèse (H003 — spike VIX > 45) déjà backtestée sur données réelles
  1990-2026 : résultat brut trompeur (biais de clustering corrigé), statut
  `en_test` avec un signal directionnel à N=7 épisodes indépendants — **pas
  encore assez pour valider**, à surveiller sur les prochaines crises.
- Marché cible pas encore tranché par l'utilisateur (Forex/actions/crypto vs
  Polymarket vs les deux) — le pipeline d'ingestion et le registre sont
  agnostiques au marché ; seul `backtest/data_loader.py` doit changer selon
  la décision.

## Prochaines étapes possibles

1. Trancher le marché cible pour orienter le moteur de backtest (voir
   `TRADING_KNOWLEDGE_BASE.md` section 13 pour la grille de transférabilité
   Polymarket déjà établie).
2. Backtester les hypothèses restantes qui ont des données librement
   disponibles (H001 yield curve, H002 Global M2, H008 sentiment retail si
   une source de données est trouvée).
3. Construire le harnais de paper trading une fois une première hypothèse
   atteint `validee`.
4. Industrialiser l'ingestion (étape manuelle aujourd'hui) en skill
   invocable directement sur une nouvelle URL YouTube.
