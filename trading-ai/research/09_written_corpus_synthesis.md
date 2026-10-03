# Synthèse du corpus écrit (2026-10-04)

Clôture de l'étape "collecte" pour les sources écrites. Détail par source :
`claims/S0XX.md` ; index, fusions, conflits et notes méthodologiques :
`CLAIMS_REGISTRY.md`. **Aucun backtest lancé, aucune hypothèse ajoutée à
`hypotheses/registry.json`** — conformément à l'ordre du pipeline
(collecter → dédupliquer → formaliser → vérifier la testabilité → filtrer
→ prioriser → tester), la formalisation n'interviendra qu'après la collecte
vidéo.

## 1. Bilan d'accès réel

| Niveau d'accès | Sources | Nombre |
|---|---|---|
| Texte intégral lu | S003, S004, S005, S007, S008, S009, S010, S011, S012, S015, S016, S021, S026, S027, S029, S030, S031 | 17 |
| Partiel légitime | S020 (table des matières + extrait éditeur ch. 5, 6, 7, 11, 12, 16) | 1 |
| Résumé seulement | S014, S017, S018, S022, S023 | 5 |
| Structure seulement | S001 (table des matières) | 1 |
| Aucun (livres sous droit d'auteur) | S002, S006, S013, S019, S024, S025 | 6 |

**Sources ajoutées pendant l'extraction** (toutes justifiées dans leur
fichier) : S029 (remplace S013), S030 (remplace S002), S031 (remplace
partiellement S006). **Sources écartées** : copies non autorisées (S001),
guide CBOT de diffusion non autorisée apparente (S006).

**Requalifications** : S004 = mémoire de Master ; S009 = résultats non
recevables ; S010, S011, S015, S016 = auteurs liés à des gérants
intéressés au résultat (signalé dans chaque fichier) ; S012 = working paper
non revu.

**Corrections du registre** : S007 (version 1999, pas 2006), S009
(deux auteurs), S018 (auteurs et revue).

## 2. Volume de claims

195 lignes de claims au total après ajout des lectures de synthèse (S026
lecture 14, S020 ch. 16), dont 1 fusion (C-S020-09/C-S027-09).

| Catégorie | Nombre (avant ajouts de synthèse) |
|---|---|
| EMPIRICAL FINDING | 65 |
| AUTHOR CLAIM | 61 |
| METHOD | 35 |
| FACT | 16 |
| HYPOTHESIS (candidats) | 9 |
| HEURISTIC | 3 |

Les deux tiers des claims sont des résultats empiriques ou des affirmations
d'auteurs — aucun n'est "validé pour notre marché" (règle transversale).

## 3. Couverture des 32 domaines après lecture réelle

Critères inchangés : `COVERED` = connaissances réellement extraites
permettant des claims testables ; `PARTIAL` = extraction superficielle,
au niveau résumé, ou partie du domaine absente ; `MISSING` = aucune source
lue. Seuls les domaines dont le statut change par rapport à
`08_final_coverage_audit.md` (partie A) sont commentés.

| # | Domaine | Avant | Après | Justification |
|---|---|---|---|---|
| 1 | Trading systématique | PARTIAL | **COVERED** | Protocoles de validation lus (S020, S027, S031) |
| 2 | Quantitative trading | PARTIAL | **COVERED** | Idem + S007, S008, S015 (stratégies documentées) |
| 3 | Microstructure | PARTIAL | **COVERED** | S003, S030 intégraux, S005 |
| 7 | Momentum | PARTIAL | **COVERED** | S011, S012, S015, S016 intégraux (S014 résumé) |
| 8 | Mean reversion | PARTIAL | **COVERED** | S007, S008, S009 — preuves surtout défavorables à la persistance |
| 10 | Volatilité | PARTIAL | PARTIAL | S029 couvre la volatilité comme signal ; mécanique des options absente (S013 inaccessible) |
| 11 | Volume | PARTIAL | PARTIAL | Uniquement des preuves négatives (S031, un marché, 5 min) |
| 12 | Order flow | PARTIAL | **COVERED** | S003 (déséquilibre), S030 (mémoire longue), S004 |
| 13 | Market profile | PARTIAL | **MISSING** | S006 inaccessible, alternative écartée — **rétrogradé** (la source candidate n'existait que sur le papier) |
| 14 | Liquidité | PARTIAL | **COVERED** | Mesure de Roll (S003), S030, S021 — la lacune "mesure de liquidité" est comblée par C-S003-05 |
| 15 | Régimes | PARTIAL | PARTIAL | Corrélation moyenne comme variable de régime (S016), sentiment (S012) ; pas de modèle formel de détection |
| 16 | Sentiment | PARTIAL | PARTIAL | Indice construit identifié (Baker-Wurgler, C-S012-05) mais non lu en source primaire |
| 17-18 | Positioning / COT | PARTIAL | PARTIAL | S015 intégral (positions spéculatives) ; S017, S018 au niveau résumé seulement |
| 19 | Options / IV | PARTIAL | PARTIAL | S029 (prime de variance) ; S013 inaccessible |
| 22-23 | Stat arb / pairs | PARTIAL | **COVERED** | S007, S008, S009, S026 (cointégration) |
| 24 | Factor investing | PARTIAL | **COVERED** | S010, S011, S012 |
| 26 | Séries temporelles | PARTIAL | **COVERED** | S026 (stationnarité, ARIMA, cointégration), S020 (différenciation fractionnaire), S029 (HAR) |
| 27 | Portfolio construction | MISSING | **PARTIAL** | Comblé sans nouvelle source : S026 lecture 14 et S020 ch. 16 (erreur d'estimation, HRP) |
| 28 | Risk management | COVERED | COVERED | Renforcé : CVaR cohérente (S026), L-VaR (S021), krachs du momentum (S011) |
| 29-31 | Exécution / coûts / impact | PARTIAL | **COVERED** | S021, S030, S003, S007, S011, S031 |
| 32 | Finance comportementale | PARTIAL | PARTIAL | S022, S023 au niveau résumé ; mécanismes cités dans S010, S011, S015 |

**Comptage** : 20 COVERED · 11 PARTIAL · 1 MISSING (Market Profile).

## 4. Concepts transversaux (rappel de `08_final_coverage_audit.md` partie B)

Toutes les lacunes de niveau A sont désormais couvertes par une lecture
réelle : leakage, purge/embargo (S020), stationnarité (S026), probabilité de
surajustement (S027). Les tests multiples sont corroborés par trois sources
indépendantes (S027, S008, S031). Walk-forward : défauts documentés (S020)
et protocole appliqué (S031). Seule la **détection de régime formelle**
reste partielle.

## 5. Candidats HYPOTHESIS (non formalisés — étape suivante du pipeline)

| Candidat | Idée | Données | Remarques de pré-dédoublonnage |
|---|---|---|---|
| C-S029-11 | Prime de variance (VIX² − variance réalisée) → rendement S&P 500 à 3 mois, hors échantillon post-2007 | Gratuites (yfinance) | **Concurrent de H003** — à tester sur les mêmes données |
| C-S015-11 | TSMOM multi-actifs figé a priori, net de coûts, post-2009 | ETF gratuits (approximation des futures) | Doit intégrer la critique C-S012-07 (exposition nette) |
| C-S016-13 | Corrélation moyenne entre marchés → performance TSMOM du mois suivant | Idem | Dépend de C-S015-11 |
| C-S011-11 | Diversification value + momentum (60/40) post-2013 | Gratuites (bibliothèque K. French) | Teste une propriété, pas une stratégie investissable |
| C-S012-08 | Momentum de facteurs post-2015, conditionné au sentiment | Gratuites (French, AQR, Stambaugh) | Testable avec C-S011-11 sur la même infrastructure |
| C-S010-13 | Portefeuille multi-facteurs net de coûts | Univers d'actions sans biais de survie | Données plus lourdes |
| C-S007-15 / C-S008-14 | Pairs trading distance vs cointégration, après 2009 | Univers sans biais de survie | **À fusionner** en une hypothèse comparative |
| C-S003-12 | Rebond partiel après un déséquilibre d'ordres journalier | Trades classés achat/vente (non gratuits) | Probablement `RETIRED` faute de données |

## 6. Conflits ouverts les plus structurants

1. **H003 (niveau du VIX) vs prime de variance (S029)** — à départager par test.
2. **Coûts du momentum** : données AQR (survit) vs littérature académique
   (ne survit pas) — à notre échelle, la version pessimiste est la plus
   pertinente.
3. **Pairs trading** : rentable dans la version 1999 de S007, largement non
   rentable après coûts jusqu'en 2009 (Do & Faff via S008), mais
   "persistant" selon Jacobs & Weber (via S008).
4. **TSMOM** : robuste sur un siècle (S015, S016, auteurs AQR) vs moins
   rentable qu'il n'y paraît une fois l'exposition nette neutralisée
   (critique citée par S012).

## 7. Lacunes restantes et implications pour la collecte vidéo

| Lacune | Statut | Pertinence d'une source vidéo |
|---|---|---|
| Market Profile (#13) | MISSING | **Élevée** — domaine de praticiens, peu de littérature académique ; les affirmations de praticiens sont exactement ce que notre pipeline sait falsifier |
| COT / positioning (#17-18) | PARTIAL, accès résumé | **Élevée** — usage pratique du rapport COT très présent chez les praticiens |
| Sentiment (#16) | PARTIAL | Moyenne |
| Régimes formels (#15) | PARTIAL | Moyenne — plutôt académique |
| Mécanique des options (#19) | PARTIAL | Faible tant qu'aucune stratégie options n'est envisagée |

Ces priorités guident le choix des vidéos (voir
`10_video_pipeline.md`, créé à l'étape suivante).
