# H029 et H031 — Pré-enregistrement (rédigé et commité avant tout chargement de prix)

Date : 2026-10-03. Seules les données COT (signal) ont été lues, pour
l'analyse de chevauchement `H029_H031_overlap.json` (script
`strategies/h029_h031_overlap.py`), qui ne contient aucun prix ni rendement.
Les prix Yahoo ont été chargés lors du test H027/H028, mais **aucune
statistique de rendement conditionnelle aux signaux H029/H031 n'a été
calculée**.

## Analyse de chevauchement (avant test)

| Mesure (2000-2026, 15 marchés) | Valeur |
|---|---|
| Fenêtres de 8 semaines après un flip des non-commerciaux : part des semaines où la position H028 = nouveau signe | 70,7 % (2 587 / 3 657) |
| Part de l'échantillon H028 couverte par ces fenêtres | 17,8 % |
| Flips des commerciaux accompagnés d'un flip **opposé** des non-commerciaux à ± 2 rapports | 49,6 % (231 / 466) — de même sens : 0,9 % |
| Flips des commerciaux dont le nouveau signe = position H028 | 33,3 % |
| Flips (commerciaux / non-commerciaux) à ± 4 rapports d'un extrême H027 | 47,0 % / 44,1 % |
| Semaines où le filtre H031 est actif (|Δ| ≥ 3 %) dont le sens = position H028 | 54,3 % |

**Conclusions avant test** :
- H029 n'est pas redondante avec H028 : c'est un sous-ensemble conditionnel
  (« flip récent », 18 % de l'échantillon), à 71 % de même position — a
  priori faible puisque H028 est nulle, mais question distincte.
- **H029 telle que rédigée est contradictoire en interne** : dans la moitié
  des cas, commerciaux et non-commerciaux basculent ensemble en sens opposé,
  et « suivre la nouvelle position d'une grande catégorie » prédit alors
  deux directions opposées. H029 est donc scindée en **H029-NC** (suivre le
  flip des non-commerciaux) et **H029-C** (suivre le flip des commerciaux),
  testées séparément, ajustement de Holm sur 2.
- H031 n'est pas redondante (signal quasi indépendant de H028).

## Données et datation (identiques à H027/H028)

COT Legacy futures-only, 15 marchés figés, prix Yahoo `=F` ; donnée COT
utilisable à partir de la clôture du premier jour de cotation ≥ date
d'observation + 6 jours (lundi suivant la publication, R15) ; exclusions des
fenêtres de fermeture administrative ; échantillon 2000-01 → fin ;
rendements démeanés par marché ; sensibilité aux sauts de raccordement
(|r| > 8 × médiane 60 j mis à 0).

## H029-NC et H029-C

- Événement : changement de signe de la position nette de la catégorie, si
  le signe précédent a tenu ≥ 4 rapports et sans événement compté dans les
  8 rapports précédents (même marché, même catégorie).
- Signal s = nouveau signe. Statistique : moyenne de s · r̃_h, h = 8 semaines
  (principal), 4 et 13 rapportés.
- Inférence : permutation (dates aléatoires dans chaque marché, mêmes
  effectifs de +1 et −1), 5 000 tirages, graine 29, p bilatéral ; Holm sur
  les 2 catégories.
- Verdict H029 :
  - `PROMISING` si une catégorie a moyenne > 0, p ajusté < 0,05, moyenne
    > 0 sur 2000-2012 et 2013-fin, **et** que l'autre catégorie n'est pas
    significativement positive (sinon contradiction interne non résolue →
    `INCONCLUSIVE`) ;
  - `REJECTED` si les deux catégories ont une moyenne ≤ 0, dont au moins
    une avec p ajusté < 0,05 ;
  - `INCONCLUSIVE` sinon.

## H031 — filtre COT sur une stratégie de tendance (V003)

- Données quotidiennes. Δ_t = (net_NC_t − net_NC_{t−1}) / (long_NC_t +
  short_NC_t) × 100, valeur connue à partir de la date R15 et maintenue
  jusqu'au rapport suivant.
- Stratégie A (non filtrée) : position +1 si clôture > SMA50, sinon −1.
- Stratégie B (filtrée, logique de V003) : passe long si clôture > SMA50 et
  Δ ≥ +3 ; passe court si clôture < SMA50 et Δ ≤ −3 ; sinon conserve la
  position précédente (plate au départ).
- Positions décidées à la clôture t, appliquées au rendement t+1. Coûts
  0,05 % par côté et par changement de position.
- Portefeuille équipondéré des 15 marchés ; série quotidienne de la
  différence nette (B − A).
- Contrôles : SMA 20 et 100 ; placebo (R8) — Δ remplacé par la série Δ
  du même marché permutée par blocs de 13 rapports, 1 000 tirages,
  graine 31, p bilatéral sur la moyenne de B − A ; moitiés 2000-2012 /
  2013-fin.
- **Diagnostic de look-ahead (sans poids dans le verdict)** : maïs
  2015-03 → 2025-03 (la démonstration de V003), stratégie B recalculée avec
  la donnée datée au **mercredi** comme dans la vidéo, comparée à la version
  datée à la publication.
- Verdict H031 :
  - `PROMISING` si moyenne nette (B − A) > 0, t Newey-West (lag 10) ≥ 2,0,
    > 0 sur les deux moitiés, > 0 pour SMA 20 et 100, p placebo < 0,05,
    **et** Sharpe net de B > Sharpe net de A ;
  - `REJECTED` si moyenne nette (B − A) < 0 avec t ≤ −2,0 ;
  - `INCONCLUSIVE` sinon.

## Séparation des niveaux de preuve (rapportés séparément)

Réplication de la source (impossible ici : V002/V003 ne fournissent aucune
statistique, sauf le backtest non recevable de V003 → diagnostic) ;
hors échantillon ; significativité ; ordre de grandeur économique
(rendement annualisé de la différence, Sharpe) ; coûts. `ROBUST`
inaccessible à ce stade.

## Journal des essais (R6)

Exécutions consignées dans `H029_H031_results.json` (champ `runs`).
