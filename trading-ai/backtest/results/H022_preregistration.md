# H022 — Pré-enregistrement (rédigé et commité avant tout chargement de données)

Date : 2026-10-03. Hypothèse : `hypotheses/registry.json` H022 (source V001,
C-V001-05 et C-V001-18 ; contexte V004). Énoncé testé : plus l'ouverture est
éloignée du centre du range de la veille, plus l'amplitude de la journée est
grande, **au-delà de ce qu'explique la volatilité récente**.

## Données

- `SPY` quotidien (Yahoo Finance), **prix non ajustés** (`auto_adjust=False`),
  1993-02 → dernier jour complet. Choix : l'ETF a une vraie ouverture de
  séance régulière (l'indice `^GSPC` a des ouvertures périmées sur une partie
  de l'historique — R1), et la séance régulière correspond au cadre de V001
  (ouverture « pit » vs range de la veille).
- Jours exclus : jours de détachement de dividende (l'ouverture brute baisse
  mécaniquement du dividende) ; toute année civile où plus de 2 % des jours
  ont `Open_t == Close_{t−1}` exactement (contrôle d'ouverture périmée),
  signalée dans les résultats.

## Variables

- `mid_{t−1} = (H_{t−1} + L_{t−1}) / 2`, `R_{t−1} = H_{t−1} − L_{t−1}`.
- `x_t = |O_t − mid_{t−1}| / R_{t−1}` (0 = ouverture au centre ; 0,5 = à un
  extrême ; > 0,5 = hors du range).
- `D_t = 1` si `O_t > H_{t−1}` ou `O_t < L_{t−1}` (ouverture hors équilibre).
- `y_t = ln(ln(H_t / L_t))` (log de l'amplitude log du jour).
- Contrôles de volatilité récente (connus avant l'ouverture) :
  `ln(moyenne_{20}(ln(H/L)))` sur t−20…t−1, `ln(ln(H_{t−1}/L_{t−1}))`,
  `|ln(C_{t−1}/C_{t−2})|`.

## Test principal (figé)

- `y_t = a + b·x_t + c'·contrôles + e`, MCO, erreurs HAC Newey-West (lag 10),
  échantillon complet.
- Prédiction : b > 0.
- Taille d'effet exigée (grand N → significativité triviale) : ouverture à un
  extrême vs au centre ⇒ amplitude prédite au moins 10 % plus grande, soit
  `exp(0,5·b) ≥ 1,10`.

## Contrôles (tous rapportés)

1. **Sous-périodes** : 1993-1999, 2000-2007, 2008-2016, 2017-fin (la
   période avant/après 2000 répond à C-V004-01/02 : changement de structure
   avec la cotation continue).
2. **Variante binaire** : `D_t` à la place de `x_t`.
3. **Contrôle strict (interprétation)** : ajout de `|ln(O_t / C_{t−1})|`
   normalisé par la moyenne des amplitudes sur 20 jours — distingue « la
   position de l'ouverture dans le range de la veille » d'un simple « effet
   de taille du gap ». N'entre pas dans la règle de verdict ; sert à
   l'interprétation.
4. **Perturbation** : fenêtre de volatilité 10, 20, 60 jours.
5. **Quintiles de x** : amplitude moyenne normalisée par quintile.
6. **Permutation par blocs (R10)** : blocs de 20 jours de `x_t` permutés
   (1 000 tirages, graine 22), p bilatéral pour b.

## Règles de verdict (figées)

- `PROMISING` si : b > 0, |t| ≥ 1,96, `exp(0,5·b) ≥ 1,10`, b > 0 dans les
  quatre sous-périodes, p de permutation < 0,05.
- `REJECTED` si b ≤ 0 avec t ≤ −1,96, **ou** si b > 0 significatif mais
  `exp(0,5·b) < 1,03` (effet statistiquement réel mais négligeable :
  l'affirmation de V001 sur les « plus grandes opportunités » ne tient pas
  en ordre de grandeur).
- `INCONCLUSIVE` sinon.
- Relation prédictive sur l'amplitude, **pas une stratégie** : `ROBUST`
  inaccessible, aucune conclusion de rentabilité.

## Journal des essais (R6)

Chaque exécution est consignée dans `H022_results.json` (champ `runs`).
