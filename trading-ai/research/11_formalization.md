# Dédoublonnage, formalisation, testabilité et priorisation (2026-10-03)

Étape commune aux corpus écrit (`09_written_corpus_synthesis.md`) et vidéo
(`10_video_pipeline.md`). Résultat : **H011-H031** ajoutées à
`hypotheses/registry.json` (champs du §3 de `07_knowledge_pipeline.md`).
**Aucun test lancé à ce stade** ; les tests ne commencent qu'avec les
hypothèses priorisées au §5, selon un protocole écrit avant de charger les
données (§6).

## 1. Décisions de dédoublonnage

| Décision | Claims | Résultat |
|---|---|---|
| Fusion | C-S007-15 + C-S008-14 (pairs distance vs cointégration) | **H017** (une hypothèse comparative) |
| Fusion | C-V001-11 + C-V001-22 + C-V001-17 (extrêmes à un niveau mécanique : règlement, milieu du range, plus haut/bas de nuit manqué) | **H020**, trois niveaux pré-déclarés testés séparément avec correction pour 3 tests |
| Fusion | C-V001-08 + C-V001-09 (revisite du POC / des anomalies) | **H019** ; les anomalies restent non formalisées (aucune définition opérationnelle) |
| Fusion | C-V002-10 + C-V003-07 (changement de signe de la position nette) | **H029**, 2 sources indépendantes |
| Fusion | C-V003-10 + C-V002-11 (filtre COT de direction) | **H031** |
| Ajout de source à une hypothèse existante | C-V002-14 (petits traders du mauvais côté) → **H008** (positionnement retail contrarien) | Pas de nouvel ID ; opérationnalisation alternative gratuite via les « non reportables » du COT |
| Hypothèses contradictoires liées | C-V002-09 (extrêmes des commerciaux = retournement) vs C-V003-05/06 + C-S015-08 (suivre les non-commerciaux) | **H027** ↔ **H028** (`contredit_hypothese`) — à tester sur les mêmes données |
| Hypothèses concurrentes liées | C-S029-11 (prime de variance) vs H003 (niveau du VIX) | **H011** ↔ **H003** (`concurrente_de`) |
| Critique intégrée comme contrôle | C-S012-07 (exposition nette du TSMOM) | Variante neutralisée **obligatoire** dans H012 |

## 2. Claims [C] non formalisés en hypothèse (et pourquoi)

| Claim | Raison |
|---|---|
| C-V001-13 (cassure de liquidation tardive) | « Liquidation » non observable ; une version prix seule serait un autre énoncé que celui de la source |
| C-V001-14 (valeur chevauchante après cassure post-ABC) | « Sauf cassure rapide » non quantifié |
| C-V001-15 (signal de changement) | Pas de prédiction de rendement ni de condition de sortie |
| C-V001-21 (ATH nocturne « seldom lasting ») | Trop peu d'occurrences pour le seuil de 20 épisodes indépendants |
| C-V001-12, C-V001-19 (attribution comportementale) | Non testable (identité des participants inconnue) |
| C-V004-01/02/03 (perte d'objectivité du Market Profile) | Pas une hypothèse de trading : devient une **contrainte de conception** de H019-H026 (test par sous-période obligatoire) |

## 3. Testabilité (vérifiée le 2026-10-03)

Accès réel testé depuis l'environnement : rapports historiques CFTC (200),
bibliothèque K. French (200), Yahoo Finance (200) ; Stooq inaccessible.

| Statut | Hypothèses | Blocage éventuel |
|---|---|---|
| `TESTABLE` | H011, H012, H014, H015, H022, H027, H028, H029, H031 | H027-H031 : raccordement des séries continues Yahoo non documenté (R3) |
| `UNTESTED` (dépendance) | H013 | Après H012 |
| `UNTESTED` (données) | H016, H017 | Univers d'actions sans biais de survie non gratuit |
| `UNTESTED` (données) | H019-H021, H023-H026 | Historique intraday 30 min de futures avec séance de nuit et règlement : non gratuit au-delà de 60 jours (30 min) / 730 jours (60 min) chez Yahoo |
| `UNTESTED` (données à vérifier) | H030 | OI quotidien historique gratuit non confirmé (variante hebdomadaire possible via le COT) |
| `RETIRED` | H018 | Trades classés achat/vente non gratuits |

**Conséquence** : 7 des 8 hypothèses Market Profile sont bloquées par les
données ; seule H022 (ouverture/amplitude) est testable sur données
quotidiennes gratuites. Aucun achat de données n'est envisagé (consigne :
pas de dépense).

## 4. Critères de priorisation (fixés avant de choisir)

Dans l'ordre de priorité du projet (rigueur > qualité des données >
risque de biais > reproductibilité > simplicité > coût > rapidité) :

1. **Données gratuites, vérifiées, de qualité connue** (exclut toute
   hypothèse avec réserve de données non résolue en premier rang) ;
2. **Hors-échantillon réel disponible** par rapport à la source (période
   postérieure à la publication) ;
3. **Peu de degrés de liberté** (paramètres fixés par la source ou par
   nous a priori, peu de variantes → faible fardeau de tests multiples) ;
4. **Valeur d'arbitrage** : le test tranche un conflit ouvert du registre ;
5. **Infrastructure existante** (`backtest/data_loader.py`,
   `backtest/metrics.py`) ;
6. Nombre suffisant d'observations indépendantes (≥ 20).

## 5. Priorisation

| Rang | Hypothèse | 1 | 2 | 3 | 4 | 5 | 6 | Décision |
|---|---|---|---|---|---|---|---|---|
| 1 | **H011** prime de variance (vs H003) | ✓ | ✓ 2008+ | ✓ 1 régression | ✓ H003 vs C-S029-04 | ✓ | ✓ ~70 trimestres non chevauchants | **Tester en premier** |
| 2 | **H022** ouverture/amplitude (V001) | ✓ | ✓ (source non datée : test par sous-périodes) | ✓ 1 régression + 1 variante | ✗ | ✓ | ✓ milliers de jours | **Tester en second** — premier test d'une affirmation de praticien, coût minimal |
| 3 | **H027 ↔ H028** COT commerciaux | ✓ CFTC / réserve R3 | ✓ | ✗ marchés × horizons | ✓ V002 vs V003, S015 vs S017 | partiel | ✓ | **Troisième**, après mise au point du raccordement (R3) et pré-enregistrement de l'univers |
| 4 | H014, H015 facteurs French | ✓ | ✓ | ✓ | ✗ | ✓ | ✓ | Ensuite — testent des propriétés, pas des stratégies exploitables |
| 5 | H012 → H013 TSMOM ETF | ✓ | ✓ | moyen | ✓ S015 vs C-S012-07 | partiel | moyen (historique ETF court) | Ensuite |
| 6 | H029, H031 | ✓ / R3 | ✓ | ✗ | ✗ | partiel | ✓ | Après H027/H028 (même pipeline de données) |

Les hypothèses bloquées par les données (§3) ne sont pas priorisées.

## 6. Règles de test applicables aux trois premières hypothèses

- Protocole écrit **avant** de charger les données (fichier de
  pré-enregistrement par hypothèse dans `backtest/results/`), précisant :
  variable, horizon, période d'apprentissage/de contrôle, période de test,
  baseline, test statistique, seuils, variantes autorisées.
- Toutes les variantes essayées journalisées (R6) ; aucune décision prise
  sur la période de test (R5).
- Erreurs standard corrigées du chevauchement (R9), permutation/bootstrap
  (R10), coûts pour toute stratégie (R11-R13), gabarit R14.
- Aucun verdict ne promeut au-delà de `PROMISING` sans l'étape B complète
  (`04_protocols.md`).
