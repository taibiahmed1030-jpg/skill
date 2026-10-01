# Trading AI — pipeline connaissance → hypothèse → validation empirique

> **Reprise de travail ou nouvelle session : lire `PROJECT_MEMORY.md` en
> premier.** Ce README donne le pitch général ; `PROJECT_MEMORY.md` est la
> source de vérité à jour sur l'état du projet, les décisions prises et ce
> qui reste en attente.

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
├── PROJECT_MEMORY.md     Mémoire centrale — à lire en premier
├── MISSING_CONTEXT.md    Résultat de l'audit de contexte (2026-10-02)
├── research/             Comparaison marchés, architecture, approches, protocoles, roadmap, sources multi-domaines
│   ├── 01_market_comparison.md
│   ├── 02_architecture.md
│   ├── 03_model_approaches.md
│   ├── 04_protocols.md
│   ├── 05_roadmap.md
│   ├── 06_domain_coverage.md    Audit des 35 domaines demandés vs connaissances existantes
│   ├── 07_knowledge_pipeline.md Pipeline SOURCE→CLAIM→HYPOTHÈSE, registres, statuts
│   ├── SOURCE_REGISTRY.md       Sources candidates (en attente de validation)
│   └── CLAIMS_REGISTRY.md       Registre de claims (squelette, vide)
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

## État actuel — voir `PROJECT_MEMORY.md`

Ce fichier contient l'état détaillé et à jour (ce qui est fait, ce qui
manque, les décisions prises/en attente). Résumé ultra-court : pipeline
construit et fonctionnel sur un marché (actions US, via H003), **aucun
marché cible n'est présupposé** (changement de consigne du 2026-10-02 —
Polymarket n'est qu'une option parmi d'autres, voir `research/01_market_comparison.md`),
aucun paper trading ni exécution activés.
