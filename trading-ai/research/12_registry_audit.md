# Audit du registre H011-H031 (2026-10-03)

Fait après le cycle de tests H011, H012, H014, H015, H022, H027-H029, H031.
Aucun résultat nouveau n'est introduit ici : chiffres tirés des fichiers
`backtest/results/*_results.json` ; les puissances statistiques du §6 sont
des calculs a posteriori sur les tailles d'effet **publiées** par les sources.

## 0. État du registre

| Statut | Hypothèses |
|---|---|
| REJECTED | H014 |
| INCONCLUSIVE (testées) | H011, H012, H015, H022, H027, H028, H029, H031 |
| UNTESTED, testable gratuitement | H013 (dépend de H012), **H030 variante hebdomadaire** (voir §1) |
| UNTESTED, bloquée par les données | H016, H017, H019, H020, H021, H023, H024, H025, H026 |
| RETIRED | H018 |
| PROMISING / ROBUST | aucune |

11 tests principaux ont été réalisés au total. Les plus petites p-values :
H029-NC 0,057 et H029-C 0,054 (miroirs l'une de l'autre), H031 t = 2,24
(non attribuable au signal, placebo p = 0,65). Avec 11 tests, environ 0,5
faux positif est attendu au seuil de 5 % : **l'ensemble est compatible avec
l'absence d'effet hors échantillon**.

## 1. Hypothèses encore testables gratuitement

| Hypothèse | Données | Intérêt / remarque |
|---|---|---|
| **H030** OI × tendance, **variante hebdomadaire** | `Open Interest (All)` du rapport COT (gratuit, déjà en cache) + prix Yahoo | Seule hypothèse de la famille « volume / open interest » testable sans achat ; l'OI quotidien reste non disponible gratuitement |
| **H008** (hors plage H011-H031, enrichie par C-V002-14) | « Non reportables » du COT Legacy, proxy des petits traders | Opérationnalisation gratuite du positionnement retail contrarien ; chevauchement à mesurer d'abord avec H028 (les non reportables sont la contrepartie des deux autres catégories) |
| H013 | Comme H012 | Valeur faible : conditionne une stratégie (H012) qui n'est pas significative |
| H011 version 5 minutes | Variance réalisée intraday du S&P 500 | **Non gratuite** : la bibliothèque Oxford-Man (gratuite) est arrêtée depuis 2022 ; la version quotidienne déjà testée est celle que C-S029-08 dit plus faible |
| H015 partie sentiment | Indice Baker-Wurgler | Fichier public arrêté fin 2018 ; une mise à jour publique est à vérifier avant tout test |

## 2. Hypothèses bloquées uniquement par les données

| Hypothèse | Donnée manquante |
|---|---|
| H016, H017 | Univers d'actions US **sans biais de survie** (CRSP ou équivalent, payant) ; les listes de composants actuels introduiraient un biais de survie inacceptable |
| H019-H021, H023-H026 | Futures intraday (voir §8) |
| H018 (RETIRED) | Transactions classées achat/vente |

## 3. Hypothèses redondantes

| Paire | Chevauchement mesuré | Conséquence |
|---|---|---|
| H029-NC ⊂ H028 | 71 % de positions identiques dans les fenêtres H029, 18 % de l'échantillon H028 | Sous-ensemble conditionnel ; tous deux non concluants |
| H029-C ↔ H029-NC | 49,6 % des flips en sens opposé simultané | Résultats miroirs (−1,0 % / +0,9 %) : un seul test informatif en réalité |
| H029-C ↔ H027 | 47 % des flips à ± 4 rapports d'un extrême | Recouvrement partiel |
| H031 ↔ H028 | 54 % d'accord de sens (≈ indépendant) | Non redondantes |
| H013 → H012 | Dépendance logique | H013 reportée |
| H008 ↔ H028 | Non mesuré | À mesurer avant de tester H008 |
| H020 (3 niveaux) | Fusion pré-déclarée, correction pour 3 tests | — |

## 4. Contradictions non résolues

| Conflit | État |
|---|---|
| V002 vs V003 (lecture des commerciaux), C-S015-08 vs lecture contrarienne | **Dissous, pas tranché** : aucune des deux lectures n'a de pouvoir prédictif (H027, H028, H029) |
| H003 (niveau du VIX) vs C-S029-04 (seule la différence IV−RV prédit) | Non tranché : H011 n'est pas concluante après 2008 ; H003 reste `en_test` sur 7 épisodes |
| TSMOM (S015) vs critique de l'exposition nette (C-S012-07) | **Partiellement éclairé** : H012 n'est pas significative et la variante neutralisée l'est encore moins (t = 0,42), ce qui va dans le sens de la critique |
| V001 vs V004 (non-stationnarité du Market Profile) | Non testable (données intraday) ; la profondeur nécessaire est au §8 |
| C-S007-06 vs C-S008-04 (rentabilité du pairs trading), C-S007 vs C-S008-07 (fenêtre de formation) | Bloqués (univers sans biais de survie) |
| C-S011-05 (Novy-Marx vs Goyal-Wahal) | Non testable avec les facteurs publics (il faudrait les rendements individuels des actions) |
| C-S011-06 (coûts du momentum) | Non testé ; exigerait des données de coûts par titre |
| Impact linéaire vs concave (S021 / S030) | Hors de portée de nos données |

## 5. Claims vidéo sans hypothèse testable

| Claim | Raison | Pourrait devenir testable si… |
|---|---|---|
| C-V001-06, -12, -19, -23 ; C-V002-07 (mécanismes), -13 ; C-V004-11, -13 | Non testables par nature (opinions, attribution comportementale, invitation à la sélection a posteriori) | — |
| C-V001-07 (sortir vite d'un trade contre la valeur), -13 (cassure tardive, version prix), -14 (« sauf cassure rapide »), -15 ; C-V004-04, -05, -09 | Pas de seuil chiffré ou données intraday nécessaires | Données intraday + seuil fixé par nous (risque de caricature à signaler) |
| C-V001-21 (plus haut historique nocturne) | Trop rare (< 20 épisodes) | — |
| C-V001-24, -25 ; C-V003-03/-04/-08 ; C-V002-01/-02/-03 | Règles de processus ou faits de structure | Déjà intégrés aux protocoles (R3, R15) |
| C-V002-12 (hausse sur OI en baisse = faiblesse) | Couverte par **H030** | Test hebdomadaire possible (§1) |
| C-V002-15 (spreads par échéance) | Hors périmètre ; le COT ne donne pas l'OI par échéance | OI par contrat |

## 6. Biais potentiels dans les tests réalisés

1. **Puissance statistique non calculée ex ante.** Calcul a posteriori avec les
   tailles d'effet publiées (t attendu ≈ t source × √(durée test / durée
   source)) :

   | Test | t attendu si l'effet publié persistait | Puissance approx. (α = 5 %) | t observé | Lecture |
   |---|---|---|---|---|
   | H011 | 2,34 × √(222/216) ≈ 2,4 | ≈ 65 % | 0,94 | Puissance modérée : l'absence de signal est informative mais pas décisive |
   | H015 | 7,04 × √(10,7/52,5) ≈ 3,2 | ≈ 89 % | 1,1 | Bonne puissance : déclin probable, ou effet de notre univers de facteurs différent |
   | H012 | Sharpe > 1 × √16,75 ≈ 4 (futures ; moins pour 12 ETF) | élevée | 1,51 | Déclin probable, avec la réserve ETF ≠ futures |
   | H027-H031 | Aucune taille d'effet publiée (praticiens) | non calculable | — | — |

   → Règle **R16** ajoutée (calcul de puissance obligatoire dans le
   pré-enregistrement).
2. **Asymétrie des verdicts.** REJECTED exige un effet significatif de signe
   opposé : avec une puissance faible, presque tout finit INCONCLUSIVE et le
   registre ne se « nettoie » jamais. → **R17** : critère de futilité /
   équivalence pré-déclaré (borne d'effet économiquement minimal).
3. **Démeanage sur l'échantillon complet** (H027-H031) : la moyenne de chaque
   marché utilise toute la période, donc une information future (légère,
   non conditionnelle au signal). → **R18** : démeanage en fenêtre
   croissante pour les tests futurs.
4. **Reproductibilité des prix Yahoo** : seules les données COT et French sont
   en cache ; les séries Yahoo peuvent être révisées. → **R19** : empreinte
   (hash, dates, nombre de lignes) des données téléchargées consignée dans
   chaque `*_results.json`.
5. **Choix de formalisation pour les claims de praticiens** (seuils,
   horizons, SMA 50) : un rejet réfute la version formalisée, pas
   nécessairement la pratique (déjà signalé dans chaque fiche).
6. **Connaissance générale du chercheur** : les univers (15 futures, 12 ETF)
   ont été figés avant les tests, mais avec la connaissance de l'histoire des
   marchés (2008, 2020). Biais inévitable, limité par le figement a priori.
7. **Biais de survie léger dans l'univers ETF de H012** : ETF choisis parmi
   ceux qui existent encore aujourd'hui.
8. **Qualité des données** : séries `=F` non ajustées (R3) ; prix négatif du
   WTI en avril 2020 (jours mis à 0) ; filtre « ouverture périmée » de H022
   trop strict (8 années exclues) ; `^GSPC` sans dividendes (H011).
9. **Multiplicité au niveau du cycle** : 11 tests principaux sans correction
   globale. Sans conséquence ici (aucun PROMISING), mais à tenir dans un
   journal cumulé (R19 inclut un compteur de tests).
10. **Contrôles qui ont fonctionné** : le placebo de H031 a évité de promouvoir
    une amélioration statistiquement significative mais non attribuable ; le
    contrôle « taille du gap » de H022 et le contrôle momentum de H028 ont
    joué le même rôle. À généraliser (R8 déjà en place).

## 7. Effets dont la période source est trop courte (ou mal adaptée) pour une vraie validation hors échantillon

| Source / hypothèse | Problème |
|---|---|
| S011 → H014 | La propriété (protection contre les krachs du momentum) dépend d'événements rares ; 2014-2026 n'en contient aucun de l'ampleur de 2009. Le REJECTED est correct **tel que formalisé**, mais la propriété sous-jacente n'a pas été réellement mise à l'épreuve |
| S029 → H011 | 18,75 ans hors échantillon, mais seulement ≈ 74 trimestres indépendants : puissance ≈ 65 % |
| S012 → H015 | 10,7 ans hors échantillon : puissance correcte pour l'effet publié, mais la moitié 2016-2020 seule ne fait que 60 mois |
| S031 (préprint 2026) | Aucune période hors échantillon disponible |
| V001-V004, V002/V003 | Aucune période source déclarée : « hors échantillon » non défini ; seul l'exemple de V003 (maïs 2015-2025) est daté |
| S017, S018 | Lus au niveau du résumé seulement : périodes non vérifiées |
| Market Profile (V004) | La non-stationnarité annoncée (cotation 24 h) impose des données **antérieures** à la bascule électronique pour être testée (§8) |

## 8. Données nécessaires pour les hypothèses Market Profile (rien n'a été acheté)

| Élément | Exigence | Pourquoi |
|---|---|---|
| Instrument | E-mini S&P 500 (ES), contrats individuels + dates de roulement ; en option DX, Russell, Brent (V004) | Marché des exemples de V001 |
| Granularité | Barres **1 minute** OHLCV (permet de reconstruire les TPO 30 min, les toucher de niveau au tick près, le volume par barre) | H019-H021, H023-H026 ; 30 minutes suffiraient sauf pour H020 (± 1 tick) |
| Sessions | Horodatage complet nuit + séance régulière (RTH 8:30-15:15 CT) | Inventaire de nuit (H021), plus haut/bas de nuit (H020) |
| Règlement officiel quotidien CME | Indispensable (« unchanged ») | H020, H021 ; la clôture 1 minute n'est qu'une approximation à ± 1 tick, précisément l'ordre de grandeur testé par H020 |
| Profondeur | **Idéalement depuis 1998-2000** (création de l'ES en 1997, ère du parquet) ; **minimum 2008+** | Avant/après la généralisation de la cotation électronique continue, pour tester C-V004-01/02 ; 2008+ ne couvre qu'un seul régime |

**Hypothèses débloquées** : H019 (POC), H020 (extrêmes à un niveau
mécanique), H021 (inventaire de nuit, « 65 % »), H023 (value area), H024
(one-time framing), H025 (profil à temps variable), H026 (volume extrême sans
mouvement), plus la version 5 minutes de H011 si le fournisseur propose aussi
l'indice.

**Coûts identifiés (pages publiques consultées le 2026-10-03, aucun achat) :**
- FirstRate Data, ES : barres 1/5/30 min et 1 h, séries continues
  (non ajustée, ajustement absolu, ajustement proportionnel) **depuis le
  2008-01-02** ; contrats individuels depuis ESZ08 ; mises à jour à 99,95 $
  par an après le premier mois. **Prix d'achat initial non affiché** dans la
  page récupérée (contenu dynamique) : non identifié. Limite : ne remonte pas
  avant 2008, donc pas de test de la bascule électronique.
- Databento, Portara (CQG), Kibot, CME DataMine : tarifs non lisibles sans
  navigation interactive ou compte (page 403 pour CME) — **coût non
  identifié**.
- Gratuit mais insuffisant : Yahoo `ES=F` en 60 minutes (≈ 730 jours) ou
  30 minutes (≈ 60 jours) — profondeur trop faible et granularité qui
  déforme la définition des TPO ; utilisable au mieux comme pilote
  descriptif, jamais comme validation.
- Exclu : jeux de données redistribués sans licence claire (ex. dépôts
  communautaires), conformément à la règle sur les copies non autorisées.

**Décision requise de l'utilisateur** avant tout achat ou création de compte
chez un fournisseur (même avec crédit gratuit, la création de compte engage
l'identité de l'utilisateur).

## 9. Règles ajoutées aux protocoles (tests futurs uniquement, non rétroactives)

R16 (puissance), R17 (futilité / équivalence), R18 (démeanage en fenêtre
croissante), R19 (empreinte des données et compteur cumulé de tests) —
détail dans `04_protocols.md`. Les verdicts déjà rendus ne sont **pas**
recalculés avec ces règles.
