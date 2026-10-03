# H027 ↔ H028 — Pré-enregistrement (rédigé et commité avant tout chargement de prix)

Date : 2026-10-03. Hypothèses contradictoires liées (`hypotheses/registry.json`) :
- **H027** (V002, S017) : un extrême sur 52 semaines de la position nette des
  commerciaux annonce un retournement (commerciaux au plus court → baisse).
- **H028** (V003, S015, S018) : suivre la position nette des non-commerciaux.

**Déclaration** : avant ce document, seuls les fichiers COT de la CFTC ont été
ouverts, pour vérifier le schéma, les codes de contrats et la continuité des
dates (aucune statistique sur les positions ni aucun prix n'a été regardé).

## Données

- COT **Legacy, futures only**, CFTC (`deacot1986_2016.zip`, `deacotYYYY.zip`
  2017-2026). Champs : `Commercial Positions-Long/Short (All)`,
  `Noncommercial Positions-Long/Short (All)`, date d'observation (mardi).
- Univers **figé** (15 marchés, codes CFTC → tickers Yahoo `=F`) :
  maïs 002602 ZC, soja 005602 ZS, blé SRW 001602 ZW, bovins vivants 057642
  LE, pétrole WTI 067651 CL, gaz naturel 023651 NG, or 088691 GC, argent
  084691 SI, cuivre 085692 HG, E-mini S&P 500 13874A ES, T-Note 10 ans
  043602 ZN, euro 099741 6E, yen 097741 6J, sucre 080732 SB, café 083731 KC.
- Prix : clôtures quotidiennes Yahoo des séries continues `=F` (non
  ajustées, méthode de raccordement non documentée — réserve R3), à partir
  de 2000 ; l'historique COT antérieur sert seulement à initialiser les
  fenêtres de 52 semaines.

## Datation (R15)

- Entrée à la **clôture du premier jour de cotation ≥ date d'observation +
  6 jours calendaires** (lundi suivant la publication du vendredi).
- Exclusion des rapports dont la publication a été retardée par une
  fermeture de l'administration fédérale : dates d'observation du
  2013-09-24 au 2013-11-05, du 2018-12-18 au 2019-03-05, et du 2025-09-23
  au 2026-01-31 (fenêtre conservatrice, durée exacte du retard 2025 non
  vérifiée).

## Traitement des roulements (R3)

- Rendements log quotidiens ; **rendements démeanés par marché** (moyenne
  du marché sur tout l'échantillon, à l'horizon considéré) pour neutraliser
  la dérive systématique des sauts de raccordement.
- Sensibilité : jours où |r| > 8 × médiane des |r| des 60 jours précédents
  (sauts suspects) remplacés par 0, résultats recalculés et rapportés.

## Test A — extrêmes des commerciaux (arbitre H027 vs H028)

- `net_C = long − short` des commerciaux. Événement « min » si `net_C(t)`
  est ≤ au minimum des 51 rapports précédents ; « max » symétrique.
- Indépendance : un événement ne compte que s'il n'y a pas eu d'événement du
  même côté dans le même marché au cours des 8 rapports précédents.
- Signal H027 : s = −1 pour « min », +1 pour « max ».
- Statistique : moyenne sur tous les événements (2000-…) de s · r̃_h, où
  r̃_h est le rendement log démeané sur h semaines. **h = 8 semaines
  (principal)** ; 4 et 13 semaines rapportés.
- Inférence : permutation — dans chaque marché, mêmes nombres d'événements
  « min » et « max » tirés aléatoirement parmi les semaines éligibles,
  5 000 tirages, graine 27, p bilatéral.
- Rapportés : N par marché et par côté, moyenne par marché, moitiés
  2000-2012 et 2013-fin.

## Test B — suivre les non-commerciaux (H028 au sens général)

- Chaque semaine, position par marché = signe de `net_NC = long − short`
  des non-commerciaux ; détention d'une entrée à la suivante.
- Portefeuille équipondéré sur les marchés disponibles ; rendements
  hebdomadaires démeanés par marché (P_t).
- Contrôle « momentum déguisé » : même construction avec le signe du
  rendement de prix sur 52 semaines à la date d'entrée (M_t).
  Régression P_t = α + β·M_t, erreurs Newey-West (lag 4).
- Coûts (R12, pessimistes pour des futures liquides) : 0,05 % par côté à
  chaque changement de signe ; moyenne nette rapportée.

## Règles de verdict (figées)

Les deux p-values principales (test A, h = 8 ; test B, α) sont ajustées par
Holm (2 tests).

- **H027** : `PROMISING` si moyenne A > 0, p ajusté < 0,05 et moyenne > 0
  sur les deux moitiés ; `REJECTED` si moyenne A < 0 avec p ajusté < 0,05 ;
  sinon `INCONCLUSIVE`.
- **H028** : `PROMISING` si moyenne nette de P > 0 avec t NW ≥ 1,96,
  α > 0 avec p ajusté < 0,05, et α > 0 sur les deux moitiés ; `REJECTED`
  si moyenne de P < 0 avec t NW ≤ −1,96, ou si le test A est
  significativement positif (H027 confirmée au détriment de la lecture
  « suivre les spéculateurs aux extrêmes ») **et** P non significatif ;
  sinon `INCONCLUSIVE` (y compris P > 0 mais α non significatif = momentum
  déguisé, rapporté comme tel).
- `ROBUST` inaccessible à ce stade (étapes B-C de `04_protocols.md` non
  faites : perturbation complète des paramètres, coûts réels par marché).

## Journal des essais (R6)

Chaque exécution est consignée dans `H027_H028_results.json` (champ `runs`).
