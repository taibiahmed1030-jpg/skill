# Registre des claims

**Premier remplissage : 2026-10-04, lot S020 → S026 → S027 (sources
méthodologiques prioritaires, lues en premier conformément à la consigne
explicite).** Aucune autre source n'a encore été traitée. Aucune hypothèse
de trading n'a été générée à partir de ce lot — ces trois sources sont
méthodologiques (validation statistique), pas du contenu de marché ; c'est
un résultat attendu, pas une lacune.

## Taxonomie de catégorisation (nouvelle, remplace le tagging [A]-[E] pour
les sources académiques/méthodologiques — voir note de compatibilité en
fin de fichier)

| Catégorie | Définition opérationnelle |
|---|---|
| `FACT` | Définition mathématique/structurelle vérifiable, indépendante du contexte (ex. définition de la stationnarité). N'est pas "vrai ou faux empiriquement" — c'est une construction formelle. |
| `EMPIRICAL FINDING` | Résultat quantitatif observé par la source sur un échantillon/période/marché précis. Ne généralise jamais au-delà de cet échantillon sans test indépendant. |
| `METHOD` | Procédure/algorithme reproductible décrit par la source (ex. CSCV, PurgedKFold). N'est pas en soi une affirmation sur les marchés. |
| `HEURISTIC` | Règle pratique/recommandation sans garantie formelle complète, dépendante du contexte d'application. |
| `AUTHOR CLAIM` | Affirmation de l'auteur présentée comme vraie, argumentée/sourcée mais non redémontrée indépendamment ici — jamais transformée en fait sans vérification. |
| `HYPOTHESIS` | Proposition testable sur un marché, formalisable dans `hypotheses/registry.json`. **Aucune occurrence dans ce lot** — attendu, ce sont des sources de méthode, pas de marché. |

## S027 — The Probability of Backtest Overfitting (Bailey, Borwein, López de Prado, Zhu, 2017)

**Accès réel** : texte intégral du papier (35 pages) téléchargé depuis le
miroir ouvert eScholarship et extrait avec `pypdf`. Toutes les
localisations ci-dessous pointent vers des pages/sections réellement
lues, pas reconstruites de mémoire.

| CLAIM_ID | Catégorie | Claim | Localisation | Conditions / limites |
|---|---|---|---|---|
| C-S027-01 | METHOD | Procédure CSCV (Combinatorially Symmetric Cross-Validation) : partitionner la matrice de performance M (T×N) en S sous-matrices égales ; former toutes les combinaisons C(S,S/2) ; pour chacune, calculer le rang IS et OOS de chaque configuration, en déduire un logit λc de la performance OOS de la configuration optimale IS ; la distribution des λc sur toutes les combinaisons donne f(λ). | §2.2, Algorithm 2.3, pp. 10-13 | Exige une "vraie matrice" (mêmes lignes pour toutes les colonnes, observations synchrones) et une métrique de performance estimable sur sous-échantillons |
| C-S027-02 | FACT | Définition de la Probability of Backtest Overfitting (PBO) : probabilité bayésienne que la configuration optimale IS se classe sous la médiane OOS parmi les N configurations testées. | §2.1, Définitions 2.1-2.2, pp. 9-10 | Construction mathématique définitionnelle, pas un résultat empirique |
| C-S027-03 | AUTHOR CLAIM | La méthode "hold-out" est peu fiable pour évaluer l'overfitting d'un backtest : contamination possible si les données sont publiques, inadéquate sous 1000 observations (citant Weiss & Kulikowski), forte variance de l'estimation (citant Van Belle & Kerr), et surtout **ignore le nombre d'essais tentés avant de choisir une configuration**. | Introduction, pp. 6-8 | Argumentation appuyée sur des citations tierces non revérifiées indépendamment ici (White 2000, Romano & Wolf 2005, etc.) |
| C-S027-04 | EMPIRICAL FINDING | Exemple synthétique 1 (marche aléatoire pure, T=1000 jours ≈4 ans, N=8800 combinaisons de paramètres d'une règle saisonnière mensuelle) : la configuration optimale IS affiche un Sharpe annualisé de 1,27 (PSR-stat 2,83) mais un **PBO de 55 %**, avec ~53 % des Sharpe OOS négatifs malgré des Sharpe IS tous positifs (1 à 2,2). | §6, Figures 6-9, pp. 25-26 | **Données purement synthétiques (marche aléatoire), zéro signal réel par construction** — démontre un faux positif, n'est pas un résultat de marché |
| C-S027-05 | EMPIRICAL FINDING | Exemple synthétique 2 (même protocole, mais effet saisonnier réellement injecté dans les données) : PBO tombe à 13 %, seulement 13 % des Sharpe OOS négatifs, Sharpe annualisé 1,54 validé comme non substantiellement surajusté. | §6, Figures 10-13, pp. 26-27 | Toujours données synthétiques — démontre que CSCV distingue correctement signal réel vs bruit dans ce cas contrôlé |
| C-S027-06 | HEURISTIC | S=16 sous-matrices est "une valeur raisonnable dans la plupart des cas" : donne 12 780 combinaisons (σ[f(λ)]<0,0045 à 95 %) tout en préservant une structure trimestrielle si M couvre ~4 ans de données quotidiennes. | §4, pp. 21-22 | Dépend explicitement de l'horizon des données (S=24 recommandé si >6 ans) — pas une constante universelle |
| C-S027-07 | HEURISTIC | Le nombre de configurations testées N doit satisfaire N≫10 si l'on veut distinguer des valeurs de PBO inférieures à 1/10 — sinon la distribution des rangs relatifs est trop discrète. | §4, p. 22 | Dépend du seuil de PBO que l'investisseur juge significatif |
| C-S027-08 | METHOD (limites) | Limites explicites de CSCV listées par les auteurs : (1) la symétrie ne convient pas à toute performance fortement autocorrélée si S est grand ; (2) poids égal à tous les échantillons, sous-optimal si une info a priori existe ; (3) **problème du tiroir à dossiers** — cacher des essais sous-estime l'overfitting, en ajouter de voués à l'échec le biaise ; (4) n'évalue pas la *correction* du backtest (coûts erronés, lookahead) ; (5) ne capture pas une rupture structurelle hors de la période T disponible ; (6) un PBO élevé n'exclut pas l'existence de stratégies réellement habiles parmi les N (overfitting "entre stratégies habiles similaires") ; (7) **ne jamais utiliser CSCV/PBO comme fonction objectif pour guider la recherche d'une stratégie** — ce serait un détournement de mesure en cible. | §5, pp. 24-26 | — |
| C-S027-09 | AUTHOR CLAIM | Tester des millions/milliards de combinaisons de paramètres sur les mêmes données rend l'apparition de faux positifs "presque certaine", même si chaque test individuel est nominalement significatif à 95 % — car ce seuil de 5 % ne vaut que pour un test appliqué une seule fois, pas répété des milliards de fois sur les mêmes données. | Introduction, pp. 4-5 | **Fusionné avec C-S020-09 (même argument, même lignée d'auteurs) — voir note de fusion ci-dessous** |
| C-S027-10 | AUTHOR CLAIM | Un Sharpe ratio IS élevé "ne nous dit rien sur la représentativité de ce résultat" quand le nombre d'essais n'est pas contrôlé — la performance apparente IS seule n'est jamais une preuve de généralisation OOS ; seule l'analyse de dégradation IS/OOS (pente de régression, typiquement négative si overfit) renseigne sur la généralisabilité réelle. | §3.2, pp. 14-15 | Distinction centrale demandée par la consigne : performance apparente ≠ performance généralisable |
| C-S027-11 | METHOD | Trois diagnostics complémentaires au PBO, dérivables du même cadre CSCV : (a) dégradation de performance (pente IS→OOS), (b) probabilité de perte OOS, (c) dominance stochastique (l'absence de dominance de la distribution OOS des configurations optimales IS sur la distribution OOS globale est "un signe clair d'overfitting"). | §3, pp. 13-19 | — |

## S020 — Advances in Financial Machine Learning (López de Prado, 2018)

**Accès réel** : le livre est sous droit d'auteur (Wiley), aucun achat
effectué. Deux documents légitimement publics ont été utilisés : (a) la
table des matières complète et exacte (bibliothèque ETH Zurich, usage
catalogue standard) pour la structure chapitre/section/page ; (b) un
extrait "bonus" fourni par l'éditeur (218 pages, figures/équations/
extraits de code — pas la prose intégrale) contenant du texte réel des
chapitres 5, 6, 7, 11 et 12. **Les claims ci-dessous notées "prose non
confirmée" s'appuient sur le titre de section (confirmé réel) et une
description largement corroborée par des sources secondaires
indépendantes et cohérentes entre elles — pas sur la lecture directe du
paragraphe original. À revérifier sur le texte primaire si une citation
exacte est nécessaire plus tard.**

| CLAIM_ID | Catégorie | Claim | Localisation | Conditions / limites |
|---|---|---|---|---|
| C-S020-01 | METHOD | *Purging* : retirer de l'ensemble d'entraînement toute observation dont l'intervalle de détermination du label chevauche dans le temps un intervalle de label de l'ensemble de test. | Ch.7 §7.4.1 "Purging the Training Set", code réel confirmé (Snippet 7.1, fonction `getTrainTimes`) | — |
| C-S020-02 | METHOD | *Embargo* : après purge, retirer en plus une fenêtre d'observations d'entraînement immédiatement après chaque ensemble de test (taille = `pctEmbargo` × nb total d'observations), car l'information peut encore fuir par autocorrélation même après la purge. | Ch.7 §7.4.2 "Embargo", code réel confirmé (Snippet 7.2, fonction `getEmbargoTimes`) | — |
| C-S020-03 | METHOD | Classe `PurgedKFold` : K-Fold modifié pour la finance — pas de mélange aléatoire (test contigu dans le temps), purge des chevauchements, embargo appliqué après le test. | Ch.7 §7.4.3 "The Purged K-Fold Class", code réel confirmé (Snippet 7.3) | — |
| C-S020-04 | AUTHOR CLAIM | Le K-Fold CV standard "échoue en finance" parce que les observations financières ne sont pas IID (labels qui chevauchent plusieurs jours) — un mélange aléatoire laisse fuir de l'information entre train et test, gonflant artificiellement la performance mesurée. | Ch.7 §7.3 "Why K-Fold CV Fails in Finance" | **Titre de section confirmé réel ; argumentaire reconstruit de sources secondaires concordantes (Wikipedia "Purged cross-validation", plusieurs analyses indépendantes), prose originale non directement lue** |
| C-S020-05 | EMPIRICAL FINDING | Étude de cas (séries de prix log de futures nommés — ex. obligations/devises/matières premières) : toutes les séries atteignent la stationnarité (test ADF, seuil critique -2,8623 à 95 %) à un ordre de différenciation fractionnaire d<0,6, la majorité déjà à d<0,3 — moins qu'une différenciation entière (d=1). | Ch.5, tableau de l'étude de cas (tickers JO1 Comdty, JY1 Curncy, KC1 Comdty, L1 Comdty confirmés dans l'extrait réel) | **Échantillon précis = futures nommés non identifiés avec certitude (pas actions, pas notre univers) — à revérifier avant tout usage** |
| C-S020-06 | AUTHOR CLAIM | "Dilemme stationnarité vs. mémoire" : la différenciation entière standard (d=1) pour rendre une série stationnaire détruit une grande partie de sa mémoire/information prédictive ; la différenciation fractionnaire (d non entier) peut atteindre la stationnarité en préservant davantage de mémoire. | Ch.5 §5.2 "The Stationarity vs. Memory Dilemma" | **Titre de section confirmé réel ; argumentaire complet reconstruit de sources secondaires, prose originale non directement lue au-delà du tableau de résultats (C-S020-05)** |
| C-S020-07 | METHOD | Combinatorial Purged Cross-Validation (CPCV) pour le backtest : partitionne T observations en N groupes ; pour un ensemble de test de taille k groupes, génère C(N,k) découpages train/test distincts ("chemins"), chacun purgé+embargoté ; produit une **distribution** de chemins de backtest plutôt qu'un seul chemin walk-forward. | Ch.12 §12.4 "The Combinatorial Purged Cross-Validation Method", §12.4.1, §12.5 ; équations et figures réelles confirmées dans l'extrait (pp. 95-97) | Partage directement le même cadre mathématique que S027 (CSCV/PBO), mêmes auteurs |
| C-S020-08 | AUTHOR CLAIM | Le walk-forward (WF) standard a pour défaut que ses décisions les plus précoces reposent sur une fraction bien plus petite de l'échantillon total que ses décisions tardives, même avec période de chauffe. | Ch.12, calcul réel confirmé dans l'extrait (équation ¼T+¾t0, p. 95) | — |
| C-S020-09 | FACT | L'espérance du maximum de I résultats IID suivant une loi normale standard croît avec I (≈√(2 log I)) — formalise que tester davantage de configurations (I) sur un instrument sans edge réel (martingale) produit mécaniquement un meilleur Sharpe IS apparent, sans aucun signal réel. | Ch.12 §12.5, p. 97, équation réelle confirmée dans l'extrait, citant explicitement Bailey et al. [2014] | **Fusionné avec C-S027-09 : même argument mathématique, même lignée d'auteurs — comptée comme UNE hypothèse/fait avec deux sources, pas deux occurrences indépendantes (règle de dédoublonnage, `07_knowledge_pipeline.md` §5)** |

## S026 — MIT 18.S096, Lectures 8 ("Time Series Analysis") et 12 ("Time Series Analysis III")

**Accès réel** : notes de cours PDF téléchargées directement depuis
`ocw.mit.edu` (matériel pédagogique librement publié par le MIT), texte
intégral extrait et lu.

| CLAIM_ID | Catégorie | Claim | Localisation | Conditions / limites |
|---|---|---|---|---|
| C-S026-01 | FACT | Définitions formelles de stationnarité stricte (invariance de toutes les distributions fini-dimensionnelles sous translation temporelle) et de stationnarité au sens large/covariance (moyenne, variance et autocovariance constantes, autocovariance ne dépendant que du décalage τ). | Lecture 8, diapositives 3-4 | — |
| C-S026-02 | FACT | Théorème de représentation de Wold : toute série stationnaire à moyenne nulle se décompose en Xt = Vt + St, où Vt est linéairement déterministe (combinaison de son propre passé) et St une moyenne mobile infinie d'innovations de bruit blanc non corrélées. | Lecture 8, diapositive 5 | — |
| C-S026-03 | METHOD | Test de Dickey-Fuller (DF) : pour un AR(1) Xt=φXt-1+ηt, teste H0: φ=1 (racine unitaire/non-stationnarité) contre H1: |φ|<1 (stationnarité), via la statistique (φ̂-1)/se(φ̂) dont la distribution sous H0 n'est PAS la loi de Student standard mais la distribution DF propre. | Lecture 8, diapositive 31 | Erreur classique à éviter : lire ce t-statistique comme un t de Student ordinaire |
| C-S026-04 | FACT | Famille de tests apparentés : ADF (Said & Dickey 1984) et Phillips-Perron (1988) testent tous deux H0 = non-stationarité ; **KPSS teste l'hypothèse inverse, H0 = stationnarité** — asymétrie méthodologique importante pour interpréter un test qui "ne rejette pas" dans l'un ou l'autre sens. | Lecture 8, diapositive 32 | — |
| C-S026-05 | METHOD | Cointégration : un processus {Xt} est intégré d'ordre d (I(d)) s'il faut le différencier d fois pour le rendre stationnaire ; si plusieurs séries non-stationnaires partagent une tendance stochastique commune telle qu'une combinaison linéaire d'entre elles est stationnaire (ordre inférieur), elles sont dites cointégrées (formalisé via VAR(p)/VECM). | Lecture 12, diapositives 3+ | **Lien direct avec S007/S008 déjà au registre** : fonde formellement l'approche "distance"/cointégration des papiers de pairs trading déjà retenus — ajouté ici car directement utile, pas une extension non sollicitée du périmètre |

## Note de fusion explicite (dédoublonnage appliqué)

**C-S027-09 et C-S020-09 sont le même argument mathématique** (le
maximum d'un grand nombre d'essais IID gonfle mécaniquement la
performance apparente, sans edge réel), démontré par la même équipe
d'auteurs dans deux publications différentes (le papier S027 et le livre
S020, chapitre 12, qui cite explicitement le papier). Conformément à la
règle de dédoublonnage (`07_knowledge_pipeline.md` §5), **ceci compte comme
une seule entrée à deux sources, pas deux faits indépendants** — et ces
deux sources ne comptent que pour **une seule source "indépendante"**
(même auteur principal), pas deux, si cet argument est un jour formalisé
en règle de validation dans `hypotheses/schema.md`.

## Conflits détectés

**Aucun.** Les trois sources de ce lot sont mutuellement cohérentes et
largement complémentaires (S020 ch.11-12 et S027 partagent littéralement
le même cadre CSCV/PBO ; S026 fournit les définitions formelles —
stationnarité, test DF/ADF, cointégration — que S020 utilise sans les
redériver). Aucune contradiction à signaler pour ce lot.

## Compatibilité avec le tagging [A]-[E] existant

Le tagging [A]-[E] (`ingestion/SKILL.md`) reste la référence pour les
sources de type formation/vidéo (contenu narratif d'un formateur). Pour
les sources académiques/méthodologiques comme celles de ce lot, la
taxonomie à 6 catégories ci-dessus est plus précise et la remplace —
correspondance approximative si besoin de rétro-compatibilité : `FACT`≈
aucun équivalent direct (plus strict que [A]) · `EMPIRICAL FINDING`≈[E]
(nécessite validation indépendante avant tout usage) · `METHOD`≈[B]
(règle explicite) · `HEURISTIC`≈[B] affaibli · `AUTHOR CLAIM`≈[A] ·
`HYPOTHESIS`≈[C].
