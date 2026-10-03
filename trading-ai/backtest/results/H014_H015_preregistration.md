# H014 et H015 — Pré-enregistrement (rédigé et commité avant tout chargement de données)

Date : 2026-10-03. Données : bibliothèque publique de Kenneth French
(fichiers mensuels : 3 facteurs, momentum, 5 facteurs 2×3, reversal court
terme, reversal long terme). Avant ce document, seule la disponibilité HTTP
des fichiers a été vérifiée (aucun contenu lu).

## H014 — diversification value + momentum (S011, C-S011-01/02/11)

- Séries : `HML`, `Mom` (UMD), mensuelles, en %.
- Combinaison fixe `C = 0,6·HML + 0,4·UMD` rebalancée chaque mois (poids
  de la source, non optimisés).
- **Période de test : 2014-01 → dernier mois disponible** (hors échantillon
  de S011, qui s'arrête en décembre 2013). Contrôle de réplication :
  1927-01 → 2013-12 (attendu : drawdowns proches de −77 % UMD, −43 % HML,
  −30 % combinaison ; mise en œuvre seulement).
- Mesures : drawdown maximal (sur rendements cumulés composés), Sharpe
  annualisé (moyenne/écart-type × √12, facteurs déjà en excès).
- Inférence : bootstrap par blocs de 12 mois (5 000 tirages, graine 14)
  des différences de Sharpe `C − HML` et `C − UMD`, p unilatéral.
- Verdict :
  - `PROMISING` si `DD(C) ≤ 0,5 · DD(UMD)` **et** les deux différences de
    Sharpe > 0 avec p < 0,05 ;
  - `REJECTED` si `DD(C) > 0,8 · DD(UMD)` **ou** si Sharpe(C) < Sharpe d'un
    des deux facteurs avec p < 0,05 (bootstrap, sens inverse) ;
  - `INCONCLUSIVE` sinon.

## H015 — momentum temporel sur facteurs (S012, C-S012-02/05/08)

- Univers figé de 8 facteurs : `Mkt-RF`, `SMB`, `HML`, `RMW`, `CMA`
  (fichier 5 facteurs 2×3), `Mom`, `ST_Rev`, `LT_Rev`. **Déviation
  documentée** : S012 utilise 20 facteurs définis par déciles (top 3 −
  bottom 3) ; nous utilisons les définitions publiques standard.
- Règle : à la fin du mois t−1, pour chaque facteur, signal = signe de la
  somme des rendements des mois t−12 à t−1 ; position long/short sur le
  facteur pour le mois t ; portefeuille équipondéré des facteurs
  disponibles.
- **Période de test : 2016-01 → dernier mois** (hors échantillon de S012,
  qui s'arrête en décembre 2015). Contrôle : premier mois disponible →
  2015-12.
- Inférence : moyenne mensuelle, t Newey-West (lag 3) ; permutation par
  blocs de 12 mois des signaux (5 000 tirages, graine 15), p bilatéral ;
  comparaison avec le portefeuille équipondéré toujours long des mêmes
  facteurs (le momentum doit faire mieux que la simple détention).
- Partie conditionnelle au sentiment : **non testée** — l'indice
  Baker-Wurgler public s'arrête fin 2018 (fichier daté 2019-03-27), soit
  au plus 36 mois hors échantillon, insuffisant après partition en deux
  régimes. Statut de cette partie : non testable faute de données.
- Verdict (partie inconditionnelle) :
  - `PROMISING` si moyenne > 0, t NW ≥ 1,96, p permutation < 0,05, et
    moyenne > 0 sur 2016-2020 et 2021-fin ;
  - `REJECTED` si moyenne < 0 avec t NW ≤ −1,96 ;
  - `INCONCLUSIVE` sinon.

## Portée

Facteurs long-short **bruts, non investissables** (pas de coûts, pas de
contraintes de vente à découvert) : ces tests portent sur des **propriétés**
de séries publiques, pas sur des stratégies exploitables. `ROBUST`
inaccessible ; aucune conclusion de rentabilité.

## Journal des essais (R6)

Exécutions consignées dans `H014_H015_results.json` (champ `runs`).
