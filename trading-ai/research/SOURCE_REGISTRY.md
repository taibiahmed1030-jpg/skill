# Registre des sources candidates — phase multi-sources

**Statut (2026-10-04) : 27 sources VALIDÉES par l'utilisateur (26 sources
initiales + S027). Aucune de ces sources n'a encore été lue/analysée en
profondeur, aucun claim n'a encore été extrait.** La validation porte sur
la *liste*, pas sur une lecture déjà faite — l'extraction complète reste
en attente d'un feu vert explicite séparé. S028 reste une source **B,
proposée/future, non ajoutée** — voir section dédiée plus bas.

**Méthode** : recherche ciblée par domaine sous-couvert (voir
`06_domain_coverage.md`), uniquement des sources réelles trouvées par
recherche web, aucune invention. Priorité donnée aux domaines ❌/🟡
(microstructure, mean reversion, volume/order flow, COT/positioning,
options/IV, stat arb/pairs trading, factor investing, ML/time-series,
exécution/coûts/impact, finance comportementale, intermarché) plutôt qu'à
une redite de price action/risk management déjà bien couverts par la
formation Elliot. 26 sources de contenu de marché + 1 source
méthodologique (S027) — qualité et diversité méthodologique privilégiées
sur le volume (préférence explicite de l'utilisateur : peu de sources très
pertinentes plutôt que beaucoup de répétitions).

## ⚠️ Ordre de lecture imposé — priorité méthodologique avant tout le reste

**Avant de lire la moindre source de contenu de marché (clusters
ci-dessous), lire dans cet ordre :**

1. **S020** — *Advances in Financial Machine Learning* (Lopez de Prado) — couvre le leakage et la validation croisée purgée/embargo (lacune transversale A).
2. **S026** — cours MIT 18.S096 — couvre la stationarité/non-stationarité des séries temporelles (lacune transversale A).
3. **S027** — *The Probability of Backtest Overfitting* — seule source couvrant le biais de sélection parmi de multiples hypothèses testées (lacune transversale A, aucune autre source du corpus ne la couvre).

Raison (voir `08_final_coverage_audit.md` parties B/C) : ces trois sources
ne portent pas sur un domaine de marché mais sur la discipline de
validation elle-même — les lire après, dans l'ordre normal par cluster,
risquerait de reproduire à plus grande échelle l'erreur déjà corrigée sur
H003 (biais de clustering) pendant l'extraction des 24 autres sources.

Légende Type : `papier` (article académique/working paper), `livre`,
`cours`, `recherche_institutionnelle` (banque/gérant/organisme).

---

## Market microstructure / liquidité / order flow

| SOURCE_ID | Titre | Auteur | Type | URL | Sujet | Pourquoi l'analyser | Qualité apparente | Redondance |
|---|---|---|---|---|---|---|---|---|
| S001 | Market Microstructure Theory | Maureen O'Hara (1995) | livre | https://openlibrary.org/books/OL1103097M/Market_microstructure_theory | Microstructure | Ouvrage fondateur du champ, définit le vocabulaire (formation du prix, spread, asymétrie d'info) qu'aucune autre source du projet ne couvre | Élevée — référence académique standard, citée par tout le champ | Nulle — domaine actuellement ❌ absent du projet |
| S002 | Trades, Quotes and Prices: Financial Markets Under the Microscope | Bouchaud, Bonart, Donier, Gould (2018) | livre | https://www.amazon.com/Trades-Quotes-Prices-Financial-Microscope/dp/110715605X *(corrigé le 2026-10-02 : l'URL Cambridge initiale était un lien mort/404 — voir note de vérification en fin de fichier)* | Microstructure, order flow | Synthèse moderne et empirique (pas seulement théorique) de la formation du prix ordre par ordre — complément direct à O'Hara | Élevée — Bouchaud est un chercheur reconnu (physique statistique appliquée aux marchés) | Nulle |
| S003 | Market microstructure (survey) | Hans R. Stoll | papier | https://www.acsu.buffalo.edu/~keechung/MGF743/Readings/Hans%20Stoll,%202003,%20Market%20microstructure.pdf | Microstructure, liquidité | Survey académique condensé, bon point d'entrée avant les ouvrages complets ci-dessus | Moyenne-élevée — papier de synthèse, pas une recherche originale récente | Nulle |
| S004 | Empirical Study of Market Impact Conditional on Order-Flow Imbalance | (arXiv 2004.08290) | papier | https://arxiv.org/pdf/2004.08290 | Order flow, market impact | Donnée empirique récente et quantifiée sur la relation déséquilibre de flux ↔ impact prix — directement formalisable en hypothèse testable | Moyenne — arXiv, non peer-reviewed confirmé, à vérifier avant usage | Nulle |
| S005 | Market Microstructure Knowledge Needed for Controlling an Intra-Day Trading Process | (arXiv 1302.4592) | papier | https://arxiv.org/pdf/1302.4592 | Microstructure appliquée à l'exécution intraday | Angle pratique (quelles infos de microstructure sont réellement actionnables intraday) plutôt que purement théorique | Moyenne | Nulle |

## Market profile / volume / auction market theory

| SOURCE_ID | Titre | Auteur | Type | URL | Sujet | Pourquoi l'analyser | Qualité apparente | Redondance |
|---|---|---|---|---|---|---|---|---|
| S006 | Mind Over Markets: Power Trading with Market-Generated Information | James F. Dalton, Eric T. Jones, Robert B. Dalton | livre | https://www.amazon.com/Mind-over-Markets-Generated-Information/dp/0934380538 | Market profile, volume profile, auction market theory | Référence historique qui a popularisé le Market Profile (Steidlmayer) — seule approche structurée du volume/profil de marché identifiée, domaine actuellement à 0% couvert | Élevée pour la discipline (texte de référence du domaine) — mais origine praticien, pas peer-reviewed : à traiter avec le même tagging [A]-[E] que la formation Elliot | Nulle — domaine ❌ absent |

## Mean reversion / pairs trading / arbitrage statistique

| SOURCE_ID | Titre | Auteur | Type | URL | Sujet | Pourquoi l'analyser | Qualité apparente | Redondance |
|---|---|---|---|---|---|---|---|---|
| S007 | Pairs Trading: Performance of a Relative-Value Arbitrage Rule | Gatev, Goetzmann, Rouwenhorst (NBER WP 7032, **1999** ; version publiée Review of Financial Studies 2006 distincte) | papier | https://www.nber.org/papers/w7032 | Pairs trading, mean reversion, stat arb | Papier fondateur du domaine, méthodologie "distance approach" précisément décrite et réplicable — **version lue : NBER 1999, données 1962-1997** (correction du 2026-10-04 : la description initiale mélangeait les versions 1999 et 2006) | Élevée — NBER, très cité, méthodologie transparente | Nulle |
| S008 | Statistical Arbitrage Pairs Trading Strategies: Review and Outlook | Krauss (2017), Journal of Economic Surveys | papier | https://onlinelibrary.wiley.com/doi/abs/10.1111/joes.12153 | Stat arb, pairs trading | Revue de littérature complète (toutes les variantes : distance, cointégration, copules, ML) — permet de couvrir le domaine en une seule lecture avant de choisir une variante à tester | Élevée — revue académique peer-reviewed | Faible (complète S007) |
| S009 | On the Profitability of Optimal Mean Reversion Trading Strategies | Peng Huang (arXiv 1602.05858) | papier | https://arxiv.org/pdf/1602.05858 | Mean reversion, modélisation stochastique (Ornstein-Uhlenbeck) | Approche mathématique différente (modèle stochastique plutôt que règle de distance) — utile pour tester si le mécanisme déclaré (retour à la moyenne) survit à une formalisation plus rigoureuse | Moyenne-élevée | Faible |

## Factor investing / portefeuille

| SOURCE_ID | Titre | Auteur | Type | URL | Sujet | Pourquoi l'analyser | Qualité apparente | Redondance |
|---|---|---|---|---|---|---|---|---|
| S010 | Foundations of Factor Investing | Jennifer Bender et al., MSCI Research Insight | recherche_institutionnelle | https://www.msci.com/documents/1296102/1336482/Foundations_of_Factor_Investing.pdf | Factor investing, portefeuille | Synthèse institutionnelle (pas un blog) de ce que sont réellement les facteurs (value, size, momentum, quality, low vol) et pourquoi ils seraient rémunérés — bonne base avant d'en tester un seul | Élevée — publication d'un fournisseur d'indices majeur, méthodologie documentée | Nulle — domaine ❌ absent |
| S011 | Fact, Fiction, and Momentum Investing | Asness, Frazzini, Israel, Moskowitz (AQR), Journal of Portfolio Management | recherche_institutionnelle | https://www.aqr.com/-/media/AQR/Documents/Journal-Articles/JPM-Fact-Fiction-and-Momentum-Investing.pdf | Momentum factor, biais de conception de backtest | **Particulièrement utile pour ce projet** : le papier liste explicitement les erreurs méthodologiques qui font croire à un edge momentum inexistant — directement transférable au protocole de validation (`04_protocols.md`) | Élevée — AQR, auteurs académiques reconnus (Asness, Moskowitz) | Nulle |
| S012 | Factor Momentum and the Momentum Factor | Ehsani, Linnainmaa, NBER WP 25551 | papier | https://www.nber.org/system/files/working_papers/w25551/w25551.pdf | Factor investing, momentum | Distingue le momentum "dans" chaque facteur du momentum "du" facteur lui-même — nuance utile pour éviter une hypothèse mal formulée | Élevée — NBER | Faible (lié à S011) |

## Volatilité / options

| SOURCE_ID | Titre | Auteur | Type | URL | Sujet | Pourquoi l'analyser | Qualité apparente | Redondance |
|---|---|---|---|---|---|---|---|---|
| S013 | Option Volatility and Pricing: Advanced Trading Strategies and Techniques | Sheldon Natenberg | livre | https://www.wiley.com/en-us/Option+Volatility+Trading+Strategies-p-9781592802920 | Options, volatilité implicite | Référence quasi-universelle sur la volatilité comme objet tradable (pas juste indicateur, à la différence du VIX dans la formation Elliot, section 2 de la KB) — ouvre un domaine entièrement absent | Élevée — référence standard de l'industrie des options depuis 1994 | Nulle — domaine ❌ absent |

## Momentum / trend following (séries temporelles)

| SOURCE_ID | Titre | Auteur | Type | URL | Sujet | Pourquoi l'analyser | Qualité apparente | Redondance |
|---|---|---|---|---|---|---|---|---|
| S014 | Returns to Buying Winners and Selling Losers: Implications for Stock Market Efficiency | Jegadeesh & Titman (1993), Journal of Finance | papier | https://econpapers.repec.org/RePEc:bla:jfinan:v:48:y:1993:i:1:p:65-91 (page Wiley officielle derrière paywall : DOI 10.1111/j.1540-6261.1993.tb04702.x) | Momentum (cross-sectional) | Papier fondateur de l'anomalie momentum, la plus répliquée en finance empirique — base de comparaison obligatoire pour toute hypothèse momentum | Élevée — un des papiers les plus cités en finance | Faible chevauchement avec section 3 KB (trendlines), mécanisme différent (cross-sectional vs technique) |
| S015 | Time Series Momentum | Moskowitz, Ooi, Pedersen (2012) | papier | https://w4.stern.nyu.edu/facdir/lpederse/papers/TimeSeriesMomentum.pdf | Momentum (séries temporelles, multi-actifs) | Contrairement à S014 (relatif entre actifs), teste le momentum absolu d'un seul actif sur 58 instruments — format event-study proche de ce que le projet sait déjà exécuter (cf. H003) | Élevée — très cité, méthodologie transparente et réplicable | Faible |
| S016 | A Century of Evidence on Trend-Following Investing | Hurst, Ooi, Pedersen (AQR) | recherche_institutionnelle | https://fairmodel.econ.yale.edu/ec439/hurst.pdf | Trend following, robustesse long terme | Teste la robustesse du trend-following sur ~100 ans et plusieurs crises — pertinent pour la discipline "stabilité par sous-période" déjà posée dans `04_protocols.md` | Élevée | Faible — complète les hypothèses de trend déjà présentes dans la KB (section 3) sans les dupliquer |

## Positioning / COT

| SOURCE_ID | Titre | Auteur | Type | URL | Sujet | Pourquoi l'analyser | Qualité apparente | Redondance |
|---|---|---|---|---|---|---|---|---|
| S017 | The Commitment of Traders (CoT) Report as a Trading Signal? Short-Term Price Reversals and Market Efficiency in the US-Futures Market | Dreesmann, Herberger, Charifzadeh (SSRN 4407250) | papier | https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4407250 | COT, positioning | Teste directement si le COT est exploitable en stratégie réelle (pas juste corrélé) — conclusion nuancée (sous-performe en portefeuille), utile comme garde-fou contre un excès d'optimisme | Moyenne-élevée — SSRN, méthodologie détaillée | Nulle — domaine ❌ absent |
| S018 | What do movements in financial traders' net long positions reveal about aggregate stock returns? | (ScienceDirect, Int'l Review of Financial Analysis) | papier | https://www.sciencedirect.com/science/article/abs/pii/S1062940818303474 | COT, positioning, actions agrégées | Angle complémentaire à S017 (prédiction de rendement agrégé plutôt que signal de trade individuel) — permet de voir si le mécanisme tient à un niveau macro | Moyenne-élevée | Faible (lié à S017) |

## Analyse intermarchés / régimes

| SOURCE_ID | Titre | Auteur | Type | URL | Sujet | Pourquoi l'analyser | Qualité apparente | Redondance |
|---|---|---|---|---|---|---|---|---|
| S019 | Intermarket Analysis: Profiting from Global Market Relationships | John J. Murphy | livre | https://www.amazon.com/Intermarket-Analysis-Profiting-Relationships-Trading/dp/0471023299 | Intermarché, régimes | La formation Elliot mentionne la chaîne dollar→pétrole→inflation→taux→actions en une ligne (section 2 KB) — Murphy est la référence qui développe ce mécanisme en profondeur, avec des exemples historiques vérifiables | Élevée — référence standard de l'analyse intermarché depuis 1991 | Faible — étend une ligne déjà présente plutôt que de la dupliquer |

## ML / séries temporelles appliqués aux marchés

| SOURCE_ID | Titre | Auteur | Type | URL | Sujet | Pourquoi l'analyser | Qualité apparente | Redondance |
|---|---|---|---|---|---|---|---|---|
| S020 | Advances in Financial Machine Learning | Marcos López de Prado | livre | https://www.wiley.com/en-us/Advances+in+Financial+Machine+Learning-p-9781119482086 | ML appliqué aux marchés, labeling, cross-validation, bet sizing | Référence la plus citée sur les pièges spécifiques du ML en finance (fuite d'information temporelle, cross-validation inadaptée) — directement utile pour éviter de refaire l'erreur de type "H003" à plus grande échelle si le projet passe un jour au ML classique (`03_model_approaches.md`, famille 3) | Élevée — auteur praticien ET académique (Cornell), ouvrage très cité | Nulle — complète `03_model_approaches.md` qui décrit la famille sans détail opérationnel |

## Exécution / coûts de transaction / market impact

| SOURCE_ID | Titre | Auteur | Type | URL | Sujet | Pourquoi l'analyser | Qualité apparente | Redondance |
|---|---|---|---|---|---|---|---|---|
| S021 | Optimal Execution of Portfolio Transactions | Almgren & Chriss (2000/2001) | papier | https://www.smallake.kr/wp-content/uploads/2016/03/optliq.pdf | Exécution, market impact, coûts de transaction | Modèle fondateur (impact permanent vs temporaire) cité dans presque toute la littérature d'exécution — permet de chiffrer un ordre de grandeur de coût réel, actuellement seulement qualitatif dans `04_protocols.md` étape C | Élevée — un des papiers fondateurs du domaine | Nulle — domaine 🟡 effleuré seulement qualitativement |

## Finance comportementale

| SOURCE_ID | Titre | Auteur | Type | URL | Sujet | Pourquoi l'analyser | Qualité apparente | Redondance |
|---|---|---|---|---|---|---|---|---|
| S022 | Prospect Theory: An Analysis of Decision under Risk | Kahneman & Tversky (1979), Econometrica | papier | https://www.econometricsociety.org/publications/econometrica/1979/03/01/prospect-theory-analysis-decision-under-risk | Finance comportementale, aversion à la perte | Base théorique de tous les biais déjà listés section 11 de la KB (erreurs à éviter) — permet de les relier à un cadre explicatif plutôt que de rester une simple liste empirique | Élevée — un des papiers fondateurs de l'économie comportementale (Nobel) | Faible — formalise un domaine déjà effleuré au niveau "erreurs du trader", pas au niveau "biais agrégé de marché" |
| S023 | The Disposition to Sell Winners Too Early and Ride Losers Too Long | Shefrin & Statman (1985), Journal of Finance | papier | https://ideas.repec.org/a/bla/jfinan/v40y1985i3p777-90.html (page Wiley officielle derrière paywall : DOI 10.1111/j.1540-6261.1985.tb05002.x) | Finance comportementale, disposition effect | Teste un biais précis et nommé, potentiellement formalisable en hypothèse testable sur données de prix (ex: autocorrélation négative après forte perte latente) | Élevée | Faible |

## Infrastructure / méthode générale (quantitative trading)

| SOURCE_ID | Titre | Auteur | Type | URL | Sujet | Pourquoi l'analyser | Qualité apparente | Redondance |
|---|---|---|---|---|---|---|---|---|
| S024 | Quantitative Trading: How to Build Your Own Algorithmic Trading Business (2nd ed.) | Ernest P. Chan | livre | https://www.wiley.com/en-us/Quantitative+Trading:+How+to+Build+Your+Own+Algorithmic+Trading+Business,+2nd+Edition-p-9781119800064 | Process de recherche quantitative, backtesting, gestion du risque | Couvre le "métier" de recherche quant lui-même (comment éviter l'overfitting, structurer un backtest) — complémentaire à `04_protocols.md`, écrit par un praticien avec expérience en banque et hedge funds | Élevée pour la discipline de recherche (moins pour des hypothèses de marché spécifiques) | Faible — renforce la méthode déjà en place plutôt que de la dupliquer |
| S025 | Algorithmic Trading: Winning Strategies and Their Rationale | Ernest P. Chan | livre | https://www.amazon.com/Algorithmic-Trading-Winning-Strategies-Rationale/dp/1118460146 | Stratégies quantitatives concrètes (mean reversion, momentum, saisonnalité) avec leur rationale économique | Chaque stratégie est présentée avec son "pourquoi" économique, pas juste la règle — cohérent avec l'exigence du projet de toujours identifier un mécanisme, pas seulement une corrélation | Élevée | Faible (lié à S024) |

## Cours

| SOURCE_ID | Titre | Auteur | Type | URL | Sujet | Pourquoi l'analyser | Qualité apparente | Redondance |
|---|---|---|---|---|---|---|---|---|
| S026 | 18.S096 Topics in Mathematics with Applications in Finance (Fall 2013) | MIT OpenCourseWare (Kempthorne, Lee, Strela, Xia) | cours | https://www.youtube.com/playlist?list=PLUl4u3cNGP63ctJIEC1UnZ0btsphnnoHR | Bases mathématiques (séries temporelles, VaR, volatilité, portefeuille, Black-Scholes) | Seule source du registre au format vidéo/cours structuré avec contenu méthodologique vérifiable (pas motivationnel) — couvre plusieurs domaines encore absents (séries temporelles, portefeuille) en une série cohérente plutôt que des vidéos isolées | Élevée — cours universitaire complet, gratuit, enseignants identifiés | Nulle |

---

## Validation statistique / overfitting (source validée le 2026-10-04)

S027 comble la seule lacune transversale de niveau A non déjà satisfaite
par une source existante du registre (voir `08_final_coverage_audit.md`
parties C/D). **Validée par l'utilisateur — fait maintenant partie du
registre, à lire en priorité (voir section "Ordre de lecture" ci-dessus),
pas encore lue/extraite.**

| SOURCE_ID | Titre | Auteur | Type | URL | Sujet | Pourquoi l'analyser | Qualité apparente | Redondance |
|---|---|---|---|---|---|---|---|---|
| S027 | The Probability of Backtest Overfitting | Bailey, Borwein, López de Prado, Zhu (2017), Journal of Computational Finance | papier | https://escholarship.org/uc/item/4w1110bb (miroir ouvert ; version citable aussi sur https://www.semanticscholar.org/paper/The-Probability-of-Backtest-Overfitting-Bailey-Borwein/b1233b4f5384f003e85c2e0eec1a2dfc08f624c5) | Overfitting, data snooping, validation statistique | **Directement lié à la leçon déjà apprise sur H003** (biais de clustering) — formalise un cadre général (PBO, cross-validation combinatoire) pour quantifier le risque d'avoir "trouvé" une stratégie par pur hasard de recherche multiple. Comble une lacune méthodologique critique non couverte par aucune des 26 autres sources | Élevée — Lopez de Prado déjà retenu (S020), méthode largement implémentée (packages R/Python) | Nulle — aucune autre source du registre ne traite spécifiquement l'overfitting de backtest |

## Sources ajoutées pendant l'extraction (décisions autonomes documentées)

| SOURCE_ID | Titre | Auteur | Type | URL | Sujet | Pourquoi ajoutée | Qualité apparente | Redondance |
|---|---|---|---|---|---|---|---|---|
| S029 | Expected Stock Returns and Variance Risk Premia | Bollerslev, Tauchen, Zhou (2009), Review of Financial Studies 22(11) | papier | https://public.econ.duke.edu/~boller/Published_Papers/rfs_09.pdf | Volatilité implicite, prime de variance, prédictibilité du marché actions | **Remplace S013 (Natenberg, inaccessible)** pour le domaine options/IV. Corpus vérifié d'abord : S026 ne couvre que la formule de Black-Scholes. Préférée à Carr & Wu (2009) car PDF légitime directement accessible (site de l'auteur) et lien direct avec H003 (VIX). Ajoutée le 2026-10-04 | Élevée — revue à comité de lecture de premier rang | Nulle |
| S030 | How Markets Slowly Digest Changes in Supply and Demand | Bouchaud, Farmer, Lillo (2008), arXiv 0809.0822 (chapitre du Handbook of Financial Markets) | papier (revue) | https://arxiv.org/abs/0809.0822 | Impact de marché, mémoire du flux d'ordres, liquidité | **Remplace S002 (livre de Bouchaud et al., inaccessible)** : même auteur principal, même programme de recherche, accès libre ; fournit en source primaire la loi d'impact concave citée de seconde main par S004. Ajoutée le 2026-10-04 | Élevée — auteurs de référence du domaine (affiliation CFM signalée) | Faible avec S003 (vision concurrente de l'origine de l'impact) |
| S031 | Structural Limits of OHLCV-Based Intraday Momentum Signals in MNQ Futures: A Systematic Falsification Study | Mathias Mesfin (2026), arXiv 2605.04004 | papier (préprint) | https://arxiv.org/abs/2605.04004 | Volume, signaux intrajournaliers de traders particuliers, protocole de falsification | **Remplace partiellement S006 (Dalton, inaccessible)** pour le domaine volume ; guide CBOT écarté (diffusion non autorisée apparente). Seule étude trouvée qui teste des signaux de volume populaires avec validation hors échantillon et coûts. Ajoutée le 2026-10-04 | **Modérée à faible** — chercheur indépendant, non revu par les pairs, mais protocole et limites transparents | Nulle |

## Source B proposée / future — non ajoutée (S028)

Ne pas ajouter maintenant, conformément à la consigne explicite du
2026-10-04. Reste une source de qualité pour combler un domaine à 0 %
(market making) mais non bloquante — voir `08_final_coverage_audit.md`
partie C pour la justification du reclassement A→B.

| SOURCE_ID | Titre | Auteur | Type | URL | Sujet | Pourquoi l'analyser (si activée plus tard) | Qualité apparente | Redondance |
|---|---|---|---|---|---|---|---|---|
| S028 (proposé, futur) | High-Frequency Trading in a Limit Order Book | Avellaneda & Stoikov (2008), Quantitative Finance | papier | https://doi.org/10.1080/14697680701381228 (page éditeur payante — résumé libre ; voir GitHub d'implémentation : https://github.com/Ahkylez/Avellaneda-Stoikov-Market-Making-Model) | Market making | Market making n'est couvert par aucune autre source ; ce papier est le modèle de référence (gestion d'inventaire, cotation bid/ask optimale). À activer seulement si un cas d'usage précis de market making/exécution apparaît | Élevée — un des papiers fondateurs du market making algorithmique, très cité | Nulle |

## Domaines encore sans source candidate identifiée (à rechercher dans un prochain tour si validé)

- **Sentiment de marché formalisé** (put/call ratio, AAII survey, indices de sentiment construits) — aucune source trouvée dans cette recherche qui soit à la fois rigoureuse et spécifique (différente du simple risk-on/risk-off déjà dans la KB).
- **Options/IV au-delà de Natenberg** (ex. recherche académique récente sur la prime de risque de variance) — S013 couvre la base, un deuxième angle plus quantitatif serait utile mais n'a pas été cherché pour ne pas surcharger ce premier tour.
- **Construction de portefeuille multi-actifs dédiée** (au-delà de ce que S020/S026 effleurent) — Markowitz/Black-Litterman non représentés ; S010/S011/S012/S026 n'effleurent le sujet qu'indirectement (facteurs, cours général). À chercher spécifiquement si un marché multi-actifs est retenu.
- **Liquidité comme mesure dédiée** (bid-ask spread decomposition, Amihud illiquidity ratio) — S001/S003 couvrent la microstructure générale mais aucune source ne porte spécifiquement sur la *mesure* de la liquidité.
- **Régime detection formalisé** (modèles de changement de régime de type Markov-switching, Hamilton 1989) — `03_model_approaches.md` section 4 nomme la famille, aucune source dédiée n'a encore été cherchée.

Ces manques sont documentés plutôt qu'ignorés, conformément à la logique
déjà appliquée dans `MISSING_CONTEXT.md`.

## Vérification technique des liens (2026-10-02)

Chaque URL du registre a été testée (code HTTP + confirmation du titre
quand la page le permettait). Résultats :

| Résultat | SOURCE_ID concernés | Détail |
|---|---|---|
| **200 OK, contenu confirmé** | S002(nouvelle URL), S004, S005, S006, S007, S009, S010, S011, S012, S013, S015, S016, S019, S020, S021, S024, S025, S026 | Accès direct réussi ; pour S004/S005/S009 le titre exact de la page a été extrait et correspond mot pour mot au titre annoncé |
| **200 OK, PDF non parsable automatiquement mais nom de fichier/contexte de recherche concordant** | S003 | Le PDF se charge (code 200) ; son contenu n'a pas pu être extrait automatiquement (flux binaire), mais le nom de fichier et le snippet de recherche correspondent précisément à "Hans Stoll, 2003, Market microstructure" — concordance forte mais pas une lecture ligne à ligne |
| **403 à la requête automatisée — probable protection anti-bot, pas nécessairement un lien mort** | S008 (Wiley), S017 (SSRN), S018 (ScienceDirect), S028 (DOI/Tandfonline) | Ces éditeurs bloquent systématiquement les requêtes non-navigateur ; les mêmes titres sont confirmés indexés par les moteurs de recherche avec métadonnées exactes. **Contenu intégral payant dans tous les cas** (abstract libre, texte complet sur abonnement institutionnel) — à signaler comme limite réelle si personne n'a d'accès institutionnel |
| **URL initiale morte (404), remplacée** | S001, S002, S014, S022, S023 | L'URL d'origine était soit absente (S001/S014/S022/S023 n'avaient qu'une référence bibliographique, pas de lien), soit un lien Cambridge cassé (S002). Remplacées ci-dessus par des liens fonctionnels vérifiés (OpenLibrary, Amazon, RePEc/EconPapers, Econometric Society) |

**Aucune source du registre ne s'est révélée inventée ou inexistante** —
le seul problème réel était des URL manquantes/mortes (5 sources), toutes
corrigées ci-dessus avec un lien fonctionnel. Les 4 sources en 403
(S008, S017, S018, S028) existent bien et sont indexées avec les bonnes
métadonnées, mais leur texte intégral n'est pas librement accessible —
différent d'un lien mort.

## Classification en trois catégories

**A — Prioritaires** (comblent un domaine actuellement à 0 % de couverture avec une source fondatrice et directement actionnable) :
S001 (microstructure, texte fondateur), S007 (pairs trading, méthodologie réplicable), S010 (factor investing, base conceptuelle), S013 (options/IV, seule source du domaine), S017 (COT, seul test direct en stratégie), S021 (exécution/impact, modèle fondateur quantifié), S027 (probability of backtest overfitting — **validée le 2026-10-04**, voir `08_final_coverage_audit.md` partie C : aucune autre source du corpus, y compris S020, ne couvre ce cadre spécifique — à lire en priorité, voir section "Ordre de lecture" en tête de fichier).

**A → B reclassé le 2026-10-03** : **S028** (market making, Avellaneda-Stoikov) a été réexaminé indépendamment de sa proposition initiale (`08_final_coverage_audit.md` partie C) et **n'est plus classé A**. Raison : c'est un domaine de marché spécifique, pas un concept transversal de validation statistique — pas "indispensable avant extraction" au même sens que S027 ; `03_model_approaches.md` a déjà conclu que le ML/RL n'est pas justifié tant qu'aucun cas d'usage étroit précis n'est sur la table. Reclassé ci-dessous.

**B — Importantes** (complètent un domaine prioritaire avec un angle méthodologique différent, ou structurent un domaine effleuré ; inclut S028 depuis le 2026-10-03) :
S002, S003, S004, S005 (microstructure/order flow, approfondissent S001), S006 (market profile, seule source mais praticien donc classé B plutôt que A), S008, S009 (stat arb/mean reversion, complètent S007), S011, S012 (factor/momentum, complètent S010), S015, S016 (momentum séries temporelles, directement testables avec l'outillage event-study existant), S018 (COT, complète S017), S020 (**à lire en priorité malgré son classement B** — couvre deux lacunes transversales de niveau A : leakage et validation purgée/embargo, voir `08_final_coverage_audit.md` partie C), S022, S023 (finance comportementale, fondateurs mais pas encore reliés à une hypothèse de prix formalisable), S028 (market making — domaine à 0 %, reclassé de A, reste de qualité mais non bloquant).

**C — Complémentaires** (utiles mais redondants avec une source déjà classée A/B du même cluster, ou de nature méthodologique générale plutôt que porteurs d'un domaine de marché nouveau) :
S014 (momentum cross-sectional — fondateur historiquement mais S015/S016 sont plus directement actionnables avec l'outillage déjà construit), S019 (intermarché — étend une ligne déjà présente dans la KB, praticien non académique), S024, S025 (Ernest Chan — renforcent une méthodologie déjà posée dans `04_protocols.md`, n'apportent pas de domaine de marché nouveau), S026 (MIT OCW — **à lire en priorité malgré son classement C** : couvre deux lacunes transversales de niveau A, stationarité et non-stationarité, voir `08_final_coverage_audit.md` partie C ; reste C pour l'apport de claims de marché spécifiques, pas pour la rigueur statistique).

## Prochaine étape (à valider, pas encore exécutée)

1. L'utilisateur choisit parmi ces 26 sources celles à analyser en
   profondeur (tout, un sous-ensemble, ou demande d'élargir certains
   clusters).
2. Seulement après validation : extraction de claims (`CLAIMS_REGISTRY.md`,
   squelette déjà créé) source par source, selon le tagging [A]-[E] déjà en
   place.
3. Formalisation en hypothèses avec dédoublonnage (`07_knowledge_pipeline.md`,
   sections 5-6) — toujours après, jamais avant.
