# H011 — Pré-enregistrement (rédigé et commité avant tout chargement de données)

Date : 2026-10-03. Hypothèse : `hypotheses/registry.json` H011 (source
S029, claims C-S029-01/03/04/06/08/11). Ce fichier fige le protocole ; toute
déviation ultérieure sera signalée comme telle dans le fichier de résultats.

## Données (gratuites, Yahoo Finance via `backtest/data_loader.py`)

- `^GSPC` clôture quotidienne (indice prix, **sans dividendes** — déviation
  vs S029, documentée) ; `^VIX` clôture quotidienne ; `^IRX` (bon du Trésor
  13 semaines, % annualisé) pour le taux sans risque.
- Échantillon : premier mois complet 1990-01 jusqu'au dernier mois dont le
  rendement à 3 mois est entièrement observé.

## Variables (fin de mois t, dernier jour de cotation)

- `RV_t = Σ_d (100 · ln(P_d / P_{d−1}))²` sur les jours de cotation du mois t
  (rendements quotidiens clôture-à-clôture ; S029 utilise du 5 minutes —
  **déviation connue** : C-S029-08 rapporte t = 2,34 pour cette variante
  VIX + RV quotidienne sur 1990-2007).
- `IV_t = VIX_t² / 12` (VIX de clôture du dernier jour du mois).
- `VRP_t = IV_t − RV_t` (unités : %² mensuels).
- `y_{t,k} = 100 · ln(P_{t+k} / P_t) − Σ_{j=0}^{k−1} IRX_{t+j} / 12`
  (rendement excédentaire log en %, k mois, IRX de fin de mois).

## Test principal (figé)

- Régression `y_{t,3} = a + b · VRP_t + e`, observations mensuelles
  chevauchantes, **période de test 2008-01 → fin** (hors de l'échantillon
  de S029).
- Inférence : t-statistique de **Hodrick (1992) 1B** (R9) ; Newey-West
  (lag 2) et régressions sur les trois sous-échantillons trimestriels **non
  chevauchants** rapportés à titre de contrôle.
- Prédiction : b > 0.

## Contrôles et robustesse (tous rapportés, quel que soit le résultat)

1. **Réplication** 1990-01 → 2007-12 (contrôle de mise en œuvre uniquement,
   pas une preuve ; attendu proche de C-S029-08).
2. **Comparaison H003 / C-S029-04** : même régression sur 2008+ avec `IV_t`
   seul, puis `RV_t` seul.
3. **Sous-périodes** : 2008-01 → 2016-12 et 2017-01 → fin.
4. **Exclusion des crises dominantes** : sans 2008-09 → 2009-06, puis sans
   2020-02 → 2020-06 (exclusion des observations dont la date t ou la
   fenêtre de rendement chevauche ces périodes).
5. **Perturbation d'horizon** : k = 1, 2, 3, 4, 6 mois (k = 3 reste le seul
   test principal).
6. **Hors-échantillon prédictif** : régression sur fenêtre croissante
   commençant en 1990, prévisions à partir de 2008 ; R² hors échantillon
   de Campbell-Thompson contre la moyenne historique croissante ; test de
   Clark-West.
7. **Permutation (R10)** : distribution de b sous l'hypothèse nulle par
   permutation par blocs de 12 mois de la série VRP (2 000 tirages, graine
   fixée à 11) sur la période de test.

## Règles de verdict (figées)

- `PROMISING` si : b > 0, |t Hodrick| ≥ 1,96 sur 2008+, **et** même signe de
  b sur les deux sous-périodes (contrôle 3), **et** p de permutation < 0,05.
- `REJECTED` si b < 0 avec t Hodrick ≤ −1,96 (contradiction franche).
- `INCONCLUSIVE` dans tous les autres cas.
- `ROBUST` est **inaccessible** pour ce test : H011 est une relation
  prédictive, pas une stratégie ; aucune conclusion de rentabilité, aucune
  règle de trading n'en est déduite. Les coûts (R11-R13) ne s'appliquent
  qu'à une éventuelle stratégie dérivée, qui serait une nouvelle hypothèse.
- Le statut de H003 n'est **pas** modifié par ce test ; la comparaison est
  rapportée comme information pour le conflit H003 / C-S029-04.

## Journal des essais (R6)

Toute exécution, y compris erronée ou relancée après correction de bug, est
consignée dans `H011_results.json` (champ `runs`).
