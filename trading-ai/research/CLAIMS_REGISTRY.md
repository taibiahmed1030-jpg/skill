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
| S004 | `claims/S004.md` | Intégral — **requalifié : mémoire de Master**, k-fold non temporel | 6 | 0 | 3 |
| S005 | `claims/S005.md` | Intégral — **pertinence faible** à notre échelle, extraction limitée | 5 | 0 | 3 |
| S009 | `claims/S009.md` | Intégral — **résultats non recevables** (sélection sur la période de test) | 4 | 0 | 3 |
| S008 | `claims/S008.md` | Intégral (discussion paper FAU 2015, version libre de l'article JES 2017) | 14 | 1 candidat | 3 |
| S018 | `claims/S018.md` | **Résumé seulement** (ScienceDirect payant) ; références corrigées | 2 | 0 | 3 |
| S022 | `claims/S022.md` | **Résumé officiel seulement** (JSTOR) | 3 | 0 | 3 |
| S023 | `claims/S023.md` | **Très limité** — résumé indexé par moteur de recherche uniquement | 2 | 0 | 3 |
| S002 | `claims/S002.md` | **Aucun** — livre sous copyright | 0 | 0 | 3 |
| S030 | `claims/S030.md` | Intégral (111 p.) — **source ajoutée** pour remplacer S002 | 8 | 0 | 3 |
| S006 | `claims/S006.md` | **Aucun** — livre sous copyright ; guide CBOT écarté (diffusion non autorisée apparente) | 0 | 0 | 3 |
| S031 | `claims/S031.md` | Intégral (17 p.) — **source ajoutée**, préprint indépendant de qualité modérée | 7 | 0 | 3 |

## Journal des fusions (dédoublonnage)

| Claim retenu | Fusionné avec | Raison | Sources indépendantes |
|---|---|---|---|
| C-S027-09 | C-S020-09 | Même argument mathématique (le max de nombreux essais IID gonfle la performance apparente sans edge), même lignée d'auteurs, S020 ch.12 cite explicitement le papier | 1 (même auteur principal) |
| C-S003-07 | C-S007-05 (corroboration, pas fusion) | Même mécanisme (rebond bid-ask gonflant les profits des stratégies contrariantes) : déduit de la théorie chez Stoll, mesuré empiriquement (~200 bp/semestre) chez Gatev et al. | **2** (auteurs et méthodes différents) |
| C-S010-08 | C-S007-06 (corroboration) | Rendement théorique/académique ≠ rendement capturable après coûts : rotation, illiquidité et spreads réduisent fortement la prime affichée | **2** |
| C-S003-07 | C-S015-10 (corroboration) | Artefacts de microstructure (prix périmés, rebond) contaminant la prédictibilité à haute fréquence | **3** au total avec C-S007-05 (Stoll ; Gatev et al. ; Moskowitz et al.) |
| C-S027-09 (tests multiples → faux positifs) | C-S008-12 (cointégration testée paire par paire sans contrôle du taux d'erreur familial) | Corroboration **indépendante** du problème des comparaisons multiples dans la littérature pairs trading | **2** (Krauss sans lien avec Bailey/López de Prado) |
| C-S007-09 (déclin de rentabilité jusqu'en 1997) | C-S008-04, C-S008-10 (déclin confirmé jusqu'en 2009 ; effet REIT disparu après 2000) | Corroboration et prolongation du déclin | **2** (Do & Faff indépendants de GGR) |
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
| C-S007-06 (version 1999 : profits nets positifs et significatifs après coûts) | C-S008-04 (Do & Faff, données jusqu'en 2009 : méthode GGR de base **largement non rentable** après coûts) | **Contradiction temporelle** : la conclusion de S007 ne tient pas sur la période ultérieure | **Ouvert** — favorise une formulation de C-S007-15 qui teste explicitement la persistance après 2009 |
| C-S008-04 (déclin, non rentable après coûts) | C-S008-09 (Jacobs & Weber : phénomène persistant sur 34 marchés ; Jacobs 2015 : top 5 des anomalies) | Contradiction entre études citées par la même revue — dépend des variantes, marchés et traitement des coûts | **Ouvert** |
| C-S007-01/02 (période de formation de 12 mois) | C-S008-07 (Huck 2013 : 12 mois = creux de performance, 6/18/24 mois forts) | **Fragilité paramétrique** de la règle d'origine | **Ouvert** — à intégrer comme test de perturbation de paramètre, sans optimiser la durée |
| C-S021-02/04 (impact modélisé **linéaire** dans le rythme de trading, Almgren-Chriss) | C-S004-01 / C-S030-02 (impact **concave**, loi de la racine carrée σ·√(Q/V), désormais en source primaire via S030) | **Contradiction de modèle partiellement réconciliée par C-S030-03** : impact concave au niveau de la transaction / du méta-ordre, approximativement linéaire avec composante permanente au niveau agrégé | **Partiellement résolu** (dépendance d'échelle) ; faible enjeu à notre échelle — seul le coût fixe ε compte (N7) |
| C-S003-03 (spread d'information : les traders informés imposent un coût d'antisélection, Glosten-Milgrom) | C-S030-04 (sur marché anonyme, pas de distinction informé/non informé ; impact d'origine mécanique) | **Visions concurrentes de l'origine de l'impact et du spread** ; S030 reconnaît aller "à l'encontre de la vision dominante" | **Ouvert** — sans conséquence directe sur nos tests quotidiens |
| C-S011-03 (krachs du momentum = exposition conditionnelle au bêta, jambe short) | C-S012-04 (krachs = retournement simultané des autocorrélations des facteurs) | Explications concurrentes (non exclusives) | **Ouvert** |
| C-S015-08 (les spéculateurs **suivent** la tendance et profitent au détriment des hedgers, horizon 12 mois) | Lecture "contrarienne" du COT (C-S017-01 : stratégie de **renversement** court terme sur données COT, résumé seulement) | **Tension d'horizon**, pas contradiction démontrée : trend sur 12 mois vs renversement à court terme. Impossible à préciser sans le texte intégral de S017 | **Ouvert** — à départager par test (position spéculative nette comme signal de continuation vs de renversement, à plusieurs horizons) |

## Sources inaccessibles ou limitées

| Source | Limitation | Décision |
|---|---|---|
| S001 | Livre sous droit d'auteur ; seules des copies non autorisées existent en ligne | Copies écartées ; 1 claim structurel depuis la table des matières ; substance confiée à S003, remonté dans l'ordre de lecture |
| S013 | Livre sous droit d'auteur, aucune version légitime | Aucun claim ; remplacé par S029 (nouvelle source, justification dans `claims/S029.md`) |
| S017 | Texte intégral inaccessible (SSRN bloque, Inderscience bloque, dépôt Bamberg sans fichier) | 4 claims au niveau résumé uniquement, marqués comme tels ; aucun candidat HYPOTHESIS tant que le texte n'est pas lu |
| S018 | Texte intégral payant ; dépôt institutionnel sans fichier | 2 claims au niveau résumé ; domaine COT désormais signalé comme faiblement couvert en accès réel |
| S022 | Texte sur JSTOR (accès membre) | 3 claims depuis le résumé officiel ; copies de sites de cours non utilisées |
| S023 | Texte payant, pas de résumé sur RePEc, éditeur bloque | 2 claims depuis un résumé indexé, signalés comme tels ; candidat initial du registre abandonné faute de lecture |
| S002 | Livre sous copyright | Remplacé par S030 (même auteur principal, accès libre) |
| S006 | Livre sous copyright ; guide CBOT de diffusion non autorisée apparente | Guide écarté et supprimé du scratchpad ; volume couvert par S031 ; **Market Profile sans source** |

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
| N8 | C-S009-04 | La période de test ne doit intervenir dans **aucune** décision de sélection (paires, paramètres, sous-univers) — sinon elle cesse d'être hors échantillon |
| N9 | C-S004-06, C-S020-04 | Pas de k-fold standard sur séries temporelles : validation chronologique, avec purge/embargo dès que les labels chevauchent |
| N10 | C-S005-05 | Mouvements intrajournaliers extrêmes sans information (type flash crash) : à signaler dans l'étage DATA VALIDATION plutôt qu'à interpréter comme signaux |
| N11 | C-S030-06 | Rendements quotidiens à queues épaisses : préférer les tests de permutation/bootstrap aux tests supposant la normalité |
| N12 | C-S031-01 | Gabarit de validation à adopter : t ≥ 2 sur rendements **nets** hors échantillon, effectif minimal par pli, net positif après friction, **même signe chaque année de test**, permutation p < 0,05 |
| N13 | C-S031-04, C-S021-10 | Vérifier d'abord que le **rendement brut par trade** dépasse le coût aller-retour avant toute analyse statistique — la plupart des signaux intrajournaliers échouent dès ce filtre |
| N14 | C-S031-07 | Tout contrat continu doit documenter sa méthode de raccordement aux dates de roulement |
