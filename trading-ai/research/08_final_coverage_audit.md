# Audit final de couverture — avant extraction de claims (2026-10-03)

**Portée** : ce document évalue si les 26 sources du registre + les 2
sources proposées (S027, S028) suffisent à construire une base de
connaissances exploitable pour générer puis tester des hypothèses
quantitatives, **avant** toute extraction de claims. Aucune extraction,
aucun claim, aucune modification de `TRADING_KNOWLEDGE_BASE.md` ni de
`CLAIMS_REGISTRY.md` n'a été faite pour produire cet audit.

**Sources consultées pour cet audit** : `06_domain_coverage.md`,
`SOURCE_REGISTRY.md`, `03_model_approaches.md`, `PROJECT_MEMORY.md`
(relus intégralement le 2026-10-03, pas depuis un résumé). **Il n'existe
aucun fichier `DECISIONS.md`** dans ce dépôt — les décisions prises/en
attente sont centralisées dans `PROJECT_MEMORY.md` section 5, qui a servi
de référence ici.

**Principe de notation** : `COVERED` est réservé aux domaines dont le
contenu a été **réellement extrait et vérifié** (aujourd'hui : uniquement
les 6 domaines issus de la formation Elliot, seule source déjà lue en
entier). Un domaine couvert seulement par une source *candidate* du
registre — identifiée, réelle, mais pas encore lue — est noté `PARTIAL`,
jamais `COVERED`, même si la source promet une couverture excellente.
C'est une application stricte de la consigne "si la couverture est
seulement superficielle, marquer PARTIAL plutôt que COVERED".

---

## A. Tableau des 32 domaines

| # | Domaine | Statut | Sources | Profondeur réelle | Suffisant pour claims testables | Ce qui manque exactement |
|---|---|---|---|---|---|---|
| 1 | Trading systématique | PARTIAL | Elliot §1/§9 (qualitatif) + S024, S025 (non lus) | Discipline narrative déjà extraite ; version quantitative promise mais non lue | Partiellement — domaine méta, pas un claim de marché en soi | Aucune lecture quanti encore faite |
| 2 | Quantitative trading | PARTIAL | S024, S025 (non lus) + `03_model_approaches.md` (synthèse interne déjà sourcée) | 2 livres dédiés identifiés, 0 % extrait | Oui, une fois lu | Lecture en attente |
| 3 | Market microstructure | PARTIAL | S001-S005 (non lus) | 5 sources solides (O'Hara, Bouchaud, Stoll, 2 papiers arXiv), aucune extraite | Oui (S004 donne une relation déjà quantifiée) | Lecture en attente |
| 4 | Price action | **COVERED** | Elliot §3 | Complet, a déjà produit des hypothèses réelles (H00x) | Oui, déjà fait | Aucune 2e source indépendante |
| 5 | Technical analysis | **COVERED** | Elliot §3-4 | Complet | Oui | Aucune 2e source indépendante |
| 6 | Macro trading | **COVERED** | Elliot §2 | Large mais entièrement tagué [E] (non académique, non vérifié indépendamment) | Oui mais confiance limitée par la source unique | Aucune source académique macro dans le registre |
| 7 | Momentum | PARTIAL | Elliot 🟡 + S014, S015, S016 (non lus) | 3 papiers fondateurs identifiés — un des domaines les mieux servis du registre | Oui, S015 directement actionnable avec l'outillage event-study existant | Lecture en attente |
| 8 | Mean reversion | PARTIAL | S007, S009 (non lus) | Méthodologie réplicable promise (distance approach, OU) | Oui | Lecture en attente |
| 9 | Trend following | **COVERED** | Elliot §3/§5 + S016 (non lu, renfort) | Déjà testable, hypothèses existantes | Oui | Cross-check contre AQR (S016) pas encore fait |
| 10 | Volatilité | PARTIAL | Elliot 🟡 (**H003 déjà testée**, statut `en_test`) + S013 (non lu) | Partagée : régime de volatilité déjà testé ; volatilité-comme-actif (options) totalement absente | Oui pour le régime (déjà fait) ; non pour le volet options | S013 à lire pour le volet options/IV |
| 11 | Volume | PARTIAL | S006 (non lu, praticien) | Source unique, même épistémologie qu'Elliot (formation, pas peer-reviewed) | Oui mais avec la même prudence que pour Elliot | Aucune source académique sur le volume |
| 12 | Order flow | PARTIAL | S004, S005 (non lus) | 2 papiers empiriques solides | Oui | Lecture en attente |
| 13 | Market profile | PARTIAL | S006 seul (non lu) | Source unique | Oui, même régime qu'Elliot | Aucun 2e angle |
| 14 | Liquidité (microstructure) | PARTIAL | S001, S003 (non lus, théorie générale) | Bonne théorie promise (spread, profondeur de marché) ; aucune métrique dédiée | Oui pour les concepts ; non pour un proxy chiffrable direct | Métrique de liquidité dédiée (ex. Amihud illiquidity ratio) absente du registre — **lacune confirmée (point 7)** |
| 15 | Régimes de marché | PARTIAL | Elliot 🟡 (4 régimes macro + VIX) | Qualitatif seulement, aucune détection formalisée | Non, pour un vrai modèle de régime | Source de regime-switching (ex. Hamilton/Markov-switching) absente — **lacune confirmée (point 7)** |
| 16 | Sentiment | PARTIAL | Elliot 🟡 (risk-on/risk-off) | Qualitatif seulement | Non, pour un indice de sentiment formel | Aucune source put/call ratio, AAII, etc. — **lacune confirmée (point 7)** |
| 17 | Positioning | PARTIAL | Elliot 🟡 (H005 `non_testable`) + S017, S018 (non lus, COT) | COT = positioning institutionnel concret et déjà testé par la littérature | Oui via COT une fois lu | Positioning retail (ex. IG Client Sentiment) toujours absent |
| 18 | COT | PARTIAL | S017, S018 (non lus) | Très solide — S017 teste directement le COT comme signal de trading | Oui, fort potentiel | Lecture en attente |
| 19 | Options / IV | PARTIAL | S013 seul (non lu) | Référence standard du domaine mais un seul angle | Oui | 2e angle plus quantitatif (prime de risque de variance) absent |
| 20 | Analyse intermarchés | PARTIAL | Elliot 🟡 (1 ligne) + S019 (non lu, praticien) | Promis bon mais source praticien seule | Oui, même épistémologie qu'Elliot | Aucune source académique |
| 21 | Indicateurs macro | **COVERED** | Elliot §2 | Détaillé | Oui mais tout [E] | Aucune source académique macro |
| 22 | Arbitrage statistique | PARTIAL | S007, S008, S009 (non lus) | 3 sources fortes (papier fondateur + revue de littérature + modèle stochastique) | Oui, très actionnable | Lecture en attente |
| 23 | Pairs trading | PARTIAL | S007, S008 (non lus) | Idem #22 | Oui | Lecture en attente |
| 24 | Factor investing | PARTIAL | S010, S011, S012 (non lus) | 3 sources institutionnelles/académiques solides | Oui | Lecture en attente |
| 25 | ML appliqué aux marchés | PARTIAL | `03_model_approaches.md` (déjà lu, sourcé) + S020 (non lu) | Architecture déjà claire ; contenu marché spécifique absent | Non prioritaire — le projet a déjà conclu que le ML n'est pas justifié à ce stade | Pas bloquant, décision déjà actée |
| 26 | Prévision de séries temporelles | PARTIAL | `03_model_approaches.md` + S026 (non lu, cours) | Idem #25 | Non prioritaire | Idem |
| 27 | Construction de portefeuille | **MISSING** | Rien de direct — S010/S011/S012/S026 ne font qu'effleurer tangentiellement | Aucun traitement dédié (Markowitz, Black-Litterman absents du registre) | Non | Source dédiée absente — **lacune confirmée (point 7)**, mais downstream (voir partie C) |
| 28 | Risk management | **COVERED** | Elliot §9 | Complet, concret, déjà opérationnel (sizing, R-multiples) | Oui, déjà utilisé dans les contraintes des hypothèses existantes | Aucune 2e source indépendante |
| 29 | Exécution | PARTIAL | Elliot 🟡 + S004, S005, S021 (non lus) | S021 = modèle fondateur directement quantifié | Oui, fort | Lecture en attente |
| 30 | Coûts de transaction | PARTIAL | Elliot 🟡 + `04_protocols.md` (interne) + `01_market_comparison.md` (déjà chiffré, à reverifier) + S021 (non lu) | Bon potentiel, chiffrage partiel déjà fait pour certains marchés | Oui, en partie déjà quantifié | Lecture de S021 en attente |
| 31 | Market impact | PARTIAL | S004, S021 (non lus) | Paire très solide (empirique + modèle fondateur) | Oui, fort | Lecture en attente |
| 32 | Finance comportementale | PARTIAL | Elliot 🟡 + S022, S023 (non lus) | S023 (disposition effect) directement opérationnalisable en hypothèse de prix | Oui, surtout via S023 | Lecture en attente |

**Comptage** : 6 `COVERED` (4, 5, 6, 9, 21, 28), 1 `MISSING` (27), 25
`PARTIAL`. Ce comptage diffère de celui de `06_domain_coverage.md`
(6 ✅ / 16 🟡 / 10 ❌) **parce que ce document-là évaluait la formation
Elliot seule, avant la construction du registre de sources** — pas une
contradiction, une mise à jour attendue. Les 10 domaines "❌ absent" de
l'ancien audit sont presque tous passés à `PARTIAL` ici car des sources
candidates réelles existent désormais pour eux — mais aucun n'est
`COVERED`, car rien n'a encore été lu.

---

## B. Tableau des concepts transversaux

| Concept | Statut actuel | Source(s) / couverture | Catégorie | Note |
|---|---|---|---|---|
| Overfitting | Opérationnel (pas via une source, via la pratique) | Leçon H003 déjà documentée et appliquée (`PROJECT_MEMORY.md` §6, `04_protocols.md`) ; S027 (non lu) renforcerait | B | Déjà appliqué une fois en situation réelle, pas seulement théorique |
| Data snooping | Partiel | `04_protocols.md` étape B (biais multiple-tests) + S011 (non lu, discute les biais de backtest momentum) | B | |
| Multiple testing | Partiel | `04_protocols.md` nomme la correction (Bonferroni/FDR) mais sans implémentation code | B | Gap d'implémentation, pas de lecture |
| P-hacking | Nommé seulement | Même famille que data snooping/multiple testing, pas de source dédiée | C | Déjà couvert fonctionnellement par les deux lignes au-dessus |
| Walk-forward validation | **Gap de code confirmé** (`PROJECT_MEMORY.md` §4 : "Robustness Engine... pas encore en code réutilisable") | S020 (non lu) couvre la méthode | B | C'est une capacité à construire, pas une lecture manquante |
| Purged / embargoed validation | Satisfait par une source déjà identifiée | **S020** (Lopez de Prado — créateur de cette méthode), non lu | A | Voir partie C — aucune nouvelle source nécessaire |
| Leakage | Satisfait par une source déjà identifiée | **S020** | A | Idem |
| Stationarity | Satisfait par une source déjà identifiée | **S026** (MIT OCW — "Time Series Analysis I/II/III" dans son programme confirmé) | A | Idem |
| Non-stationarity | Satisfait par une source déjà identifiée | **S026** | A | Idem |
| Regime detection | Gap confirmé (point 7) | Nommé comme famille dans `03_model_approaches.md`, aucune source dédiée | B | Pertinent surtout au stade validation/robustesse, pas à l'extraction |
| Statistical significance | **Déjà couvert, opérationnel** | `backtest/metrics.py` (test de permutation déjà codé et exécuté sur H003) | — | Pas un gap |
| Bootstrap / randomization | **Déjà couvert, opérationnel** | `backtest/metrics.py::permutation_test()` déjà exécuté | — | Pas un gap |
| Probability of backtest overfitting | **Gap réel, non satisfait par le corpus existant** | Seule source candidate : **S027**, non lu | **A** | Voir partie C — nouvelle source réellement nécessaire |
| Transaction costs | Partiel (= domaine 30) | Elliot 🟡 + `01_market_comparison.md` + S021 (non lu) | B | |
| Slippage | Partiel, implicite | Couvert conceptuellement par l'impact temporaire d'Almgren-Chriss (S021, non lu) | B | |
| Market impact | Partiel (= domaine 31) | S004, S021 (non lus) | B | |
| Liquidity | Partiel (= domaine 14) | S001, S003 (non lus) | B | |
| Execution | Partiel (= domaine 29) | Elliot 🟡 + S004, S005, S021 (non lus) | B | |
| Position sizing | **Déjà couvert, opérationnel** | Elliot §9 (R-multiples, règles de sizing), déjà utilisé dans les contraintes des hypothèses H00x | — | Pas un gap |
| Portfolio construction | Gap confirmé (= domaine 27, `MISSING`) | Aucune source dédiée | C | Downstream — ne devient pertinent qu'une fois plusieurs hypothèses validées |
| Correlation / dependence | Partiel | Elliot 🟡 (hedging via paire corrélée) + S007, S008, S009 (non lus, cointégration/distance) | B | |
| Robustness testing | Partiel, interne | `04_protocols.md` étape B défini ; seule la vérification d'indépendance a été réellement exercée sur H003 (sous-périodes et perturbation de paramètres pas encore faites) | B | Gap de pratique, pas de lecture |

---

## C. Lacunes classées A (indispensables avant extraction)

| Lacune | Le corpus actuel la couvre-t-il déjà ? | Conclusion |
|---|---|---|
| Purged / embargoed validation | **Oui** — S020 (déjà dans le registre, non encore lu) | Pas de nouvelle source nécessaire ; **prioriser la lecture de S020 tôt** dans l'ordre d'extraction, avant que des claims de time-series soient formalisés en hypothèses |
| Leakage | **Oui** — S020 | Idem |
| Stationarity | **Oui** — S026 (déjà dans le registre, non encore lu) | Pas de nouvelle source nécessaire ; **prioriser la lecture de S026 tôt** |
| Non-stationarity | **Oui** — S026 | Idem |
| Probability of backtest overfitting | **Non** — aucune autre source du registre (y compris S020) ne couvre ce cadre spécifique (biais de sélection parmi de multiples hypothèses testées, distinct de la validation croisée purgée) | **Nouvelle source réellement nécessaire** — voir partie D |

**Conclusion de la partie C** : sur 5 lacunes de niveau A identifiées, 4
sont déjà couvertes par des sources *déjà présentes* dans le registre
(S020, S026) — la correction nécessaire est une **priorité de lecture**,
pas un ajout. Une seule lacune A nécessite réellement une **nouvelle**
source.

### Vérification spécifique de S027 et S028 (consigne explicite de ne pas les supposer nécessaires)

- **S027 (Probability of Backtest Overfitting)** : réexaminé indépendamment de sa proposition initiale. **Confirmé A — réellement nécessaire.** Raison : le projet est sur le point de générer des dizaines d'hypothèses à partir de 26-28 sources hétérogènes, exactement le scénario où le biais de sélection "la meilleure hypothèse parmi N testées" devient réel — une généralisation à grande échelle de ce que la leçon H003 a montré sur un seul cas. Aucune autre source du corpus (y compris S020) ne fournit ce cadre spécifique (PBO / validation croisée symétrique combinatoire).
- **S028 (Avellaneda-Stoikov, market making)** : réexaminé indépendamment. **Reclassé de A à B.** Raison du changement : le market making est un domaine de marché spécifique (comme pairs trading ou factor investing), pas un concept transversal de validation statistique — il n'est donc pas "indispensable avant extraction" au même sens que les 5 lacunes ci-dessus. De plus, `03_model_approaches.md` (déjà produit par ce projet) a déjà conclu que le RL/ML n'est pas justifié à ce stade, sauf cas d'usage étroit précis (dont le market making est cité comme exemple) — aucun cas d'usage de ce type n'est actuellement sur la table. S028 reste une source de qualité pour combler un domaine à 0 %, mais elle peut attendre.

---

## D. Nouvelle source proposée (uniquement pour la lacune A non satisfaite)

**Une seule nouvelle source est proposée** à l'issue de cet audit — S027,
déjà identifiée lors de la revue précédente, reconfirmée ici après
vérification indépendante :

| Champ | Détail |
|---|---|
| Auteur(s) | David H. Bailey, Jonathan Borwein, Marcos López de Prado, Qiji Jim Zhu |
| Titre | The Probability of Backtest Overfitting |
| Année | 2017 (Journal of Computational Finance) |
| Type | Papier académique (peer-reviewed) |
| URL | https://escholarship.org/uc/item/4w1110bb (miroir ouvert UC) ; version citable également sur https://www.semanticscholar.org/paper/The-Probability-of-Backtest-Overfitting-Bailey-Borwein/b1233b4f5384f003e85c2e0eec1a2dfc08f624c5 |
| Accessibilité | **Open access via le miroir eScholarship** (bloque les requêtes automatisées type curl — comportement anti-bot déjà observé sur ce domaine, mais accessible à un navigateur humain) ; version éditeur (Journal of Computational Finance) payante |
| Lacune comblée | Probability of backtest overfitting (concept transversal A, partie B) — seule technique du corpus qui quantifie le risque d'avoir "trouvé" une stratégie par pur hasard de recherche multiple sur un grand nombre d'hypothèses testées |
| Pourquoi les sources actuelles ne suffisent pas | S020 (Lopez de Prado, déjà dans le registre) couvre le leakage et la validation croisée purgée/embargo, des techniques liées mais **distinctes** — aucune ne fournit le cadre PBO (combinatorially symmetric cross-validation) qui s'applique spécifiquement au risque de sélection parmi plusieurs hypothèses, risque que ce projet va rencontrer dès qu'il testera plusieurs hypothèses issues de sources différentes |

**Statut : toujours proposée, pas ajoutée au registre.** Aucune action
n'a été prise sur cette proposition sans validation explicite.

---

## E. Verdict factuel

**Corpus nécessite encore 2 corrections avant extraction — aucune lacune
de contenu de marché ne bloque, seulement des lacunes méthodologiques de
niveau A :**

1. **Valider (ou refuser) l'ajout de S027** — seule nouvelle source
   réellement indispensable identifiée par cet audit complet.
2. **Acter l'ordre de lecture priorisé** : S020 et S026 doivent être lus
   **en premier** dans le pipeline d'extraction (pas à leur tour normal
   de cluster), car ils couvrent des lacunes de niveau A (leakage,
   validation purgée, stationarité) qui doivent être comprises *avant*
   de formaliser des claims en hypothèses de type série temporelle —
   sinon le risque est de reproduire une version plus large de l'erreur
   H003 sans le garde-fou que ces deux sources fournissent.

Aucune autre correction n'est bloquante : le seul domaine `MISSING`
(construction de portefeuille, #27) est downstream et ne retarde pas le
début de l'extraction ; les 3 autres lacunes signalées au point 7
(regime detection, liquidity measurement, sentiment formalisé) sont de
niveau B/C, non bloquantes.

**Correction supplémentaire actée dans ce document** : S028 reclassé de
A à B dans `SOURCE_REGISTRY.md` (voir section Classification de ce
fichier, mise à jour en conséquence).

**Rien n'a été extrait, aucun claim créé, aucune hypothèse formalisée,
aucune source ajoutée au registre sans validation.** En attente de
validation explicite avant de passer à l'étape suivante.
