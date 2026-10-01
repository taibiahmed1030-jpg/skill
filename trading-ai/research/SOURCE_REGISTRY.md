# Registre des sources candidates — phase multi-sources

**Statut : liste candidate à valider par l'utilisateur. Aucune de ces
sources n'a encore été lue/analysée en profondeur, aucun claim n'a encore
été extrait.** Conformément à la consigne explicite, la collecte massive
(lecture complète, extraction de claims) n'a pas commencé — ceci est
l'étape "construire une liste de sources candidates" demandée avant toute
analyse.

**Méthode** : recherche ciblée par domaine sous-couvert (voir
`06_domain_coverage.md`), uniquement des sources réelles trouvées par
recherche web, aucune invention. Priorité donnée aux domaines ❌/🟡
(microstructure, mean reversion, volume/order flow, COT/positioning,
options/IV, stat arb/pairs trading, factor investing, ML/time-series,
exécution/coûts/impact, finance comportementale, intermarché) plutôt qu'à
une redite de price action/risk management déjà bien couverts par la
formation Elliot. 26 sources retenues — qualité et diversité
méthodologique privilégiées sur le volume (préférence explicite de
l'utilisateur : peu de sources très pertinentes plutôt que beaucoup de
répétitions).

Légende Type : `papier` (article académique/working paper), `livre`,
`cours`, `recherche_institutionnelle` (banque/gérant/organisme).

---

## Market microstructure / liquidité / order flow

| SOURCE_ID | Titre | Auteur | Type | URL | Sujet | Pourquoi l'analyser | Qualité apparente | Redondance |
|---|---|---|---|---|---|---|---|---|
| S001 | Market Microstructure Theory | Maureen O'Hara (1995) | livre | (référence académique standard, pas de lien unique officiel) | Microstructure | Ouvrage fondateur du champ, définit le vocabulaire (formation du prix, spread, asymétrie d'info) qu'aucune autre source du projet ne couvre | Élevée — référence académique standard, citée par tout le champ | Nulle — domaine actuellement ❌ absent du projet |
| S002 | Trades, Quotes and Prices: Financial Markets Under the Microscope | Bouchaud, Bonart, Donier, Gould (2018) | livre | https://www.cambridge.org/core/books/trades-quotes-and-prices/ | Microstructure, order flow | Synthèse moderne et empirique (pas seulement théorique) de la formation du prix ordre par ordre — complément direct à O'Hara | Élevée — Bouchaud est un chercheur reconnu (physique statistique appliquée aux marchés) | Nulle |
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
| S007 | Pairs Trading: Performance of a Relative-Value Arbitrage Rule | Gatev, Goetzmann, Rouwenhorst (NBER WP 7032, 2006) | papier | https://www.nber.org/papers/w7032 | Pairs trading, mean reversion, stat arb | Papier fondateur du domaine, méthodologie "distance approach" précisément décrite et réplicable (1962-2002, résultats chiffrés) — bon candidat pour une hypothèse directement formalisable | Élevée — NBER, très cité, méthodologie transparente | Nulle |
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
| S014 | Returns to Buying Winners and Selling Losers: Implications for Stock Market Efficiency | Jegadeesh & Titman (1993), Journal of Finance | papier | (référence académique standard JF 1993, vol. 48) | Momentum (cross-sectional) | Papier fondateur de l'anomalie momentum, la plus répliquée en finance empirique — base de comparaison obligatoire pour toute hypothèse momentum | Élevée — un des papiers les plus cités en finance | Faible chevauchement avec section 3 KB (trendlines), mécanisme différent (cross-sectional vs technique) |
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
| S022 | Prospect Theory: An Analysis of Decision under Risk | Kahneman & Tversky (1979), Econometrica | papier | (référence académique standard, Econometrica vol. 47) | Finance comportementale, aversion à la perte | Base théorique de tous les biais déjà listés section 11 de la KB (erreurs à éviter) — permet de les relier à un cadre explicatif plutôt que de rester une simple liste empirique | Élevée — un des papiers fondateurs de l'économie comportementale (Nobel) | Faible — formalise un domaine déjà effleuré au niveau "erreurs du trader", pas au niveau "biais agrégé de marché" |
| S023 | The Disposition to Sell Winners Too Early and Ride Losers Too Long | Shefrin & Statman (1985), Journal of Finance | papier | (référence académique standard JF 1985, vol. 40) | Finance comportementale, disposition effect | Teste un biais précis et nommé, potentiellement formalisable en hypothèse testable sur données de prix (ex: autocorrélation négative après forte perte latente) | Élevée | Faible |

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

## Domaines encore sans source candidate identifiée (à rechercher dans un prochain tour si validé)

- **Sentiment de marché formalisé** (put/call ratio, AAII survey, indices de sentiment construits) — aucune source trouvée dans cette recherche qui soit à la fois rigoureuse et spécifique (différente du simple risk-on/risk-off déjà dans la KB).
- **Options/IV au-delà de Natenberg** (ex. recherche académique récente sur la prime de risque de variance) — S013 couvre la base, un deuxième angle plus quantitatif serait utile mais n'a pas été cherché pour ne pas surcharger ce premier tour.
- **Construction de portefeuille multi-actifs dédiée** (au-delà de ce que S020/S026 effleurent) — à chercher spécifiquement si un marché multi-actifs est un jour retenu.

Ces manques sont documentés plutôt qu'ignorés, conformément à la logique
déjà appliquée dans `MISSING_CONTEXT.md`.

## Prochaine étape (à valider, pas encore exécutée)

1. L'utilisateur choisit parmi ces 26 sources celles à analyser en
   profondeur (tout, un sous-ensemble, ou demande d'élargir certains
   clusters).
2. Seulement après validation : extraction de claims (`CLAIMS_REGISTRY.md`,
   squelette déjà créé) source par source, selon le tagging [A]-[E] déjà en
   place.
3. Formalisation en hypothèses avec dédoublonnage (`07_knowledge_pipeline.md`,
   sections 5-6) — toujours après, jamais avant.
