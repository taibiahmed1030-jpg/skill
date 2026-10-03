# H012 — Pré-enregistrement (rédigé et commité avant tout chargement de données)

Date : 2026-10-03. Hypothèse : `hypotheses/registry.json` H012 (S015
C-S015-03/05/06/11 ; S016 ; critique C-S012-07). Aucun prix d'ETF n'a été
chargé avant ce document.

## Univers figé (12 ETF multi-classes, cotés avant 2008)

Actions : SPY, IWM, EFA, EEM, VNQ — Obligations : TLT, IEF, LQD, TIP —
Matières premières : GLD, DBC — Devise : UUP.
Prix ajustés des distributions (Yahoo, `auto_adjust=True`) ; taux sans
risque `^IRX`.

## Règle (paramètres de S015, figés)

- Fin de mois t : rendement excédentaire sur 12 mois (t−12 → t) ; signal =
  signe.
- Volatilité ex ante : écart-type EWMA des rendements quotidiens (centre de
  masse 60 jours, comme S015), annualisé (√261), connu à la date t.
- Poids de l'actif i pour le mois t+1 : `w_i = signal_i · 0,40 / σ_i`, puis
  portefeuille = moyenne des positions des actifs disponibles (≥ 13 mois
  d'historique). Pas de levier global supplémentaire.
- Rendement de l'actif = rendement total de l'ETF − taux sans risque du mois.
- Coûts (R12, pessimistes pour des ETF liquides) : 0,05 % × |Δw| à chaque
  rebalancement mensuel.

## Période

- **Test : 2010-01 → dernier mois complet** (S015 s'arrête en 2009).
  Les mois antérieurs (à partir du premier mois où ≥ 6 actifs sont
  disponibles) servent seulement de contrôle de mise en œuvre.

## Contrôles

1. **Exposition nette neutralisée (C-S012-07)** : chaque mois, on retire aux
   poids leur moyenne transversale (somme des poids nulle) ; rapporté.
2. Portefeuille passif à risque égal (toujours long, mêmes poids absolus) ;
   rapporté.
3. Moitiés : 2010-2017 et 2018-fin.
4. Permutation (R10) : signes des signaux permutés par blocs de 12 mois au
   sein de chaque actif (5 000 tirages, graine 12), p bilatéral sur le
   rendement net moyen.
5. Critères R14 rapportés à titre d'information (signe par année civile).

## Règles de verdict (figées)

- `PROMISING` si rendement net moyen > 0, t Newey-West (lag 3) ≥ 2,0,
  moyenne nette > 0 sur les deux moitiés, et p de permutation < 0,05.
- `REJECTED` si rendement net moyen < 0 avec t ≤ −2,0.
- `INCONCLUSIVE` sinon.
- Si `PROMISING` mais variante neutralisée non significative : la limite
  « dépend de l'exposition nette » est inscrite au registre.
- `ROBUST` inaccessible à ce stade (perturbation de paramètres et coûts réels
  par ETF non faits).

## Journal des essais (R6)

Exécutions consignées dans `H012_results.json` (champ `runs`).
