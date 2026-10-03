# Registre des claims — index

**Structure (décision du 2026-10-04)** : un fichier par source dans
`research/claims/S0XX.md` (claims détaillés + localisation + limites) ;
ce fichier-ci ne contient que l'index, la taxonomie, le journal des
fusions et celui des conflits inter-sources. Raison : ~28 sources à
traiter, un fichier unique devenait ingérable et chaque ajout risquait
d'abîmer les sections précédentes.

## Taxonomie (sources académiques/méthodologiques)

| Catégorie | Définition opérationnelle |
|---|---|
| `FACT` | Définition mathématique/structurelle vérifiable, indépendante du contexte. Pas "vrai/faux empiriquement" — une construction formelle. |
| `EMPIRICAL FINDING` | Résultat quantitatif observé sur un échantillon/période/marché précis. Ne généralise jamais au-delà sans test indépendant dans notre pipeline. |
| `METHOD` | Procédure/algorithme reproductible. N'est pas une affirmation sur les marchés. |
| `HEURISTIC` | Règle pratique sans garantie formelle complète, dépendante du contexte. |
| `AUTHOR CLAIM` | Affirmation argumentée de l'auteur, non redémontrée ici — jamais promue en fait sans vérification. |
| `HYPOTHESIS` | Proposition testable sur un marché, candidate à `hypotheses/registry.json` (après dédoublonnage, formalisation et priorisation — jamais directement). |

Correspondance avec le tagging [A]-[E] (sources narratives, `ingestion/SKILL.md`) : `EMPIRICAL FINDING`≈[E] · `METHOD`≈[B] · `HEURISTIC`≈[B] affaibli · `AUTHOR CLAIM`≈[A] · `HYPOTHESIS`≈[C] · `FACT` sans équivalent (plus strict).

**Règle transversale** : aucun claim n'est "validé pour notre marché" tant
qu'il n'a pas été testé dans notre pipeline. Un `EMPIRICAL FINDING` reste
attaché à son échantillon d'origine.

## Index des sources traitées

| Source | Fichier | Accès réel au texte | Claims | Dont HYPOTHESIS | Lot |
|---|---|---|---|---|---|
| S020 | `claims/S020.md` | Partiel légitime (TOC exacte + extrait éditeur ch.5/6/7/11/12) | 9 | 0 | 1 |
| S026 | `claims/S026.md` | Intégral (notes MIT OCW, lectures 8 et 12) | 5 | 0 | 1 |
| S027 | `claims/S027.md` | Intégral (miroir ouvert eScholarship) | 11 | 0 | 1 |
| S001 | `claims/S001.md` | **Limité** — table des matières seulement (copies non autorisées écartées) | 1 | 0 | 2 |
| S003 | `claims/S003.md` | Intégral (working paper 66 p.) | 14 | 1 candidat | 2 |
| S007 | `claims/S007.md` | Intégral — **version NBER 1999** (1962-1997), pas la version RFS 2006 | 15 | 1 candidat | 2 |
| S010 | `claims/S010.md` | Intégral (33 p.) — biais signalés : conflit d'intérêts commercial, historique probablement rétro-calculé | 13 | 1 candidat | 2 |
| S013 | `claims/S013.md` | **Aucun** — livre sous copyright, aucune version légitime | 0 | 0 | 2 |
| S029 | `claims/S029.md` | Intégral (30 p.) — **source ajoutée** pour remplacer S013 | 11 | 1 candidat | 2 |
| S017 | `claims/S017.md` | **Résumé seulement** (SSRN, éditeur et dépôt institutionnel bloqués/sans fichier) | 4 | 0 | 2 |
| S021 | `claims/S021.md` | Intégral (42 p., version déc. 2000) | 10 | 0 | 2 |
| S015 | `claims/S015.md` | Intégral (JFE 2012, 23 p.) | 11 | 1 candidat | 3 |
| S016 | `claims/S016.md` | Texte intégral ; **tableaux en image non extractibles** | 13 | 1 candidat | 3 |
| S011 | `claims/S011.md` | Intégral (texte) ; **texte de plaidoyer d'auteurs AQR** | 11 | 1 candidat | 3 |
| S012 | `claims/S012.md` | Intégral (NBER WP, non revu par les pairs) | 8 | 1 candidat | 3 |

## Journal des fusions (dédoublonnage)

| Claim retenu | Fusionné avec | Raison | Sources indépendantes |
|---|---|---|---|
| C-S027-09 | C-S020-09 | Même argument mathématique (le max de nombreux essais IID gonfle la performance apparente sans edge), même lignée d'auteurs, S020 ch.12 cite explicitement le papier | 1 (même auteur principal) |
| C-S003-07 | C-S007-05 (corroboration, pas fusion) | Même mécanisme (rebond bid-ask gonflant les profits des stratégies contrariantes) : déduit de la théorie chez Stoll, mesuré empiriquement (~200 bp/semestre) chez Gatev et al. | **2** (auteurs et méthodes différents) |
| C-S010-08 | C-S007-06 (corroboration) | Rendement théorique/académique ≠ rendement capturable après coûts : rotation, illiquidité et spreads réduisent fortement la prime affichée | **2** |
| C-S003-07 | C-S015-10 (corroboration) | Artefacts de microstructure (prix périmés, rebond) contaminant la prédictibilité à haute fréquence | **3** au total avec C-S007-05 (Stoll ; Gatev et al. ; Moskowitz et al.) |
| C-S015-07 | C-S016-07 (corroboration **non indépendante**) | Profil en "sourire" du trend-following face aux mouvements extrêmes du marché | **1** (équipe AQR commune, Ooi et Pedersen co-auteurs des deux) — la période 1880-1984 de S016 est en revanche un test hors échantillon *temporel* |

## Journal des conflits inter-sources

| Claim A | Claim B | Nature | Statut |
|---|---|---|---|
| H003 (registre, niveau du VIX > 45 → achat) | C-S029-04 (le niveau d'IV seul ne prédit pas ; seule la différence IV−RV prédit) | **Tension / spécification concurrente**, pas contradiction stricte : H003 porte sur des pics extrêmes (event study), S029 sur une régression linéaire continue. Les deux pointent dans le même sens (volatilité implicite élevée ↔ rendements futurs plus élevés) mais divergent sur la variable pertinente | **Ouvert** — à départager uniquement par test (H003 vs C-S029-11 sur mêmes données) |
| C-S007-10 (a) concurrence a érodé les profits | C-S007-10 (b) profits plus élevés quand le marché baisse | Explications concurrentes au sein d'une même source | **Ouvert** — conservées toutes deux |
| C-S010-06 (a) prime = risque systématique | C-S010-06 (b) prime = erreurs/contraintes | Explications concurrentes des primes factorielles | **Ouvert** — conservées toutes deux |
| C-S011-06 (FIM 2013, données AQR : le momentum survit facilement aux coûts) | C-S011-06 (Korajczyk & Sadka 2004 ; Lesmond et al. 2003 : coûts bien plus élevés, viabilité compromise) | **Contradiction réelle**, réconciliée par S011 via la taille de l'investisseur (coûts de l'investisseur moyen ≈ 10× ceux d'un grand institutionnel). **Pour ce projet, petite taille → la littérature pessimiste est la plus pertinente** | **Ouvert** — à départager par nos propres coûts réels mesurés, pas par l'une ou l'autre source |
| C-S011-05 (Novy-Marx 2012 : momentum US mieux mesuré sur t−12 à t−7) | C-S011-05 (Goyal & Wahal 2013 : 12 mois supérieur dans 35 pays sur 36) | Contradiction entre deux études citées de seconde main | **Ouvert** — à fixer *a priori* (12 mois, convention) plutôt qu'à choisir après test |
| C-S015-05/06 (TSMOM rentable sur 58 contrats) | C-S012-07 (Goyal & Jegadeesh 2017 ; Huang et al. 2018 : TSMOM moins rentable qu'il n'y paraît, exposition nette au marché non nulle) | **Contradiction citée de seconde main** contre S015 | **Ouvert** — tout test de C-S015-11 devra comparer le TSMOM à une exposition passive de même volatilité et neutraliser l'exposition nette |
| C-S011-03 (krachs du momentum = exposition conditionnelle au bêta, jambe short) | C-S012-04 (krachs = retournement simultané des autocorrélations des facteurs) | Explications concurrentes (non exclusives) | **Ouvert** |
| C-S015-08 (les spéculateurs **suivent** la tendance et profitent au détriment des hedgers, horizon 12 mois) | Lecture "contrarienne" du COT (C-S017-01 : stratégie de **renversement** court terme sur données COT, résumé seulement) | **Tension d'horizon**, pas contradiction démontrée : trend sur 12 mois vs renversement à court terme. Impossible à préciser sans le texte intégral de S017 | **Ouvert** — à départager par test (position spéculative nette comme signal de continuation vs de renversement, à plusieurs horizons) |

## Sources inaccessibles ou limitées

| Source | Limitation | Décision |
|---|---|---|
| S001 | Livre sous droit d'auteur ; seules des copies non autorisées existent en ligne | Copies écartées ; 1 claim structurel depuis la table des matières ; substance confiée à S003, remonté dans l'ordre de lecture |
| S013 | Livre sous droit d'auteur, aucune version légitime | Aucun claim ; remplacé par S029 (nouvelle source, justification dans `claims/S029.md`) |
| S017 | Texte intégral inaccessible (SSRN bloque, Inderscience bloque, dépôt Bamberg sans fichier) | 4 claims au niveau résumé uniquement, marqués comme tels ; aucun candidat HYPOTHESIS tant que le texte n'est pas lu |

## Notes méthodologiques transversales (à reporter dans `04_protocols.md` lors de la synthèse)

| Note | Origine | Contenu |
|---|---|---|
| N1 | C-S003-07 | Une autocorrélation négative à très court terme des prix de transaction peut être un artefact de rebond bid-ask : tester les hypothèses de retour à la moyenne court terme sur points milieux, pas sur derniers prix |
| N2 | C-S027-08 (7) | Ne jamais utiliser le PBO comme fonction objectif de recherche de stratégie |
| N3 | C-S027-08 (3) | Journaliser **tous** les essais (y compris les échecs) — condition nécessaire pour calculer un PBO honnête |
| N4 | C-S029-06 | Régressions à horizons chevauchants : erreurs standard de Hodrick (1992) ; ne jamais interpréter un R² qui croît avec l'horizon sur un prédicteur persistant comme une preuve |
| N5 | C-S007-12 | Benchmark placebo : comparer toute stratégie à la même règle appliquée à des sélections aléatoires (bootstrap) |
| N6 | C-S010-08, C-S007-06 | Toute prime "académique" doit être recalculée nette de coûts, rotation et contraintes d'investissabilité avant toute conclusion |
| N7 | C-S021-02/03/10 | Modèle de coûts minimal pour l'étape C : coût fixe ε = demi-spread + frais par transaction (dominant à petite taille) ; termes d'impact γ, η à ajouter seulement si la taille dépasse ~1 % du volume journalier |
