# Comparaison des catégories de marché — rapport documenté

**But** : donner les caractéristiques factuelles de chaque catégorie sur les 20 critères demandés, pour permettre une décision rationnelle. **Ce document ne classe rien et ne recommande rien** — il documente.

**Méthode** : recherche web ciblée (2026, sources datées) pour les faits qui changent vite (prix, offres API, régulation) + connaissances établies en finance quantitative pour les faits structurels stables (longueur d'historique, nature de la liquidité). Chaque affirmation datée/chiffrée est sourcée. Les sources tierces non officielles (blogs, comparateurs) sont signalées comme telles — à revérifier avant toute décision budgétaire.

**Catégories couvertes** : Actions · ETF · Futures · Forex · Crypto · Marchés prédictifs. Une 7e catégorie ("Options") est ajoutée en fin de document car plusieurs critères (liquidité, structure des données) en font une famille à part entière que l'utilisateur n'avait pas listée mais qui mérite d'être connue.

---

## 1. Actions (equities)

| # | Critère | Constat |
|---|---|---|
| 1 | Qualité/profondeur données historiques | Très bonne pour les grandes capitalisations US. Risque connu et documenté : la plupart des jeux de données gratuits/bon marché n'incluent **que les tickers actuellement cotés** → biais de survie si on backteste sur l'univers d'aujourd'hui en remontant dans le temps. |
| 2 | Longueur d'historique | Décennies à plus d'un siècle pour les plus grandes valeurs US (NYSE/Nasdaq) ; variable ailleurs. |
| 3 | Granularité | Quotidien très répandu ; 1-minute disponible gratuitement jusqu'à 10 ans via Alpaca (compte gratuit, pas besoin de financer le compte) [[Alpaca]](https://alpaca.markets/learn/fetch-historical-data) ; tick-level disponible via Alpaca (trades individuels) et Polygon.io (payant au-delà d'un niveau gratuit limité). |
| 4 | Coûts d'accès aux données | **Gratuit** : Alpaca (jusqu'à 10 ans de 1-min, données IEX temps réel) [[Alpaca support]](https://alpaca.markets/support/data-provider-alpaca). **Payant** : Polygon.io gratuit = 5 requêtes/min + 2 ans de daily ; palier "Stocks Developer" $79/mois pour 10 ans d'historique [[Polygon.io]](https://polygon.io/). Fondamentaux point-in-time sans biais de survie (ex. Sharadar) = payant, catalogue dédié [[Sharadar]](https://sharadar.com/). |
| 5 | Coûts de transaction | Commissions à $0 chez la plupart des brokers retail US (Alpaca, etc.) ; coût réel = spread bid-ask + impact de marché, faible sur les grandes capitalisations liquides. |
| 6 | Liquidité | Très élevée sur les indices majeurs (S&P500, Nasdaq100) ; chute fortement sur les petites capitalisations — à vérifier titre par titre. |
| 7 | Spreads | Serrés sur les grandes capitalisations (souvent 1 cent) ; peuvent s'élargir fortement sur les small caps ou en préouverture/après clôture. |
| 8 | Slippage | Faible sur grandes capitalisations en heures normales ; significatif sur ordres de taille importante ou titres peu liquides. |
| 9 | Disponibilité intraday | Oui, large (voir granularité) — IEX (Alpaca, gratuit) couvre ~2,5% du volume total US, donc représentatif mais pas exhaustif [[Alpaca]](https://alpaca.markets/support/data-provider-alpaca). |
| 10 | Order book | Disponible via IEX (profondeur limitée, gratuit) ; carnet complet (Level 2/3, tous exchanges) = payant, fournisseurs type Polygon/Databento. |
| 11 | Données fondamentales/macro/sentiment | Très riche et mature : fondamentaux (bilans, résultats), consensus analystes, sentiment (news, réseaux sociaux) — écosystème le plus développé de toutes les catégories. |
| 12 | Paper trading | Natif et gratuit chez plusieurs brokers (ex. Alpaca paper trading API). |
| 13 | Exécution automatisée future | Mature : APIs de brokers (Alpaca, Interactive Brokers, etc.) conçues pour l'algo trading retail. |
| 14 | Contraintes techniques | Faibles à modérées — écosystème Python très développé (yfinance, Alpaca SDK, etc.). |
| 15 | Contraintes réglementaires | Historiquement la règle "Pattern Day Trader" (PDT, minimum $25k pour >3 day-trades/5 jours) limitait le trading actif à petit capital. **Changement majeur** : la SEC a approuvé l'élimination complète de la règle PDT par la FINRA le 14 avril 2026, effective au 4 juin 2026 — remplacée par une exigence de marge basée sur le risque réel, sans minimum fixe [[AngelInvestorsNetwork]](https://angelinvestorsnetwork.com/regulatory-compliance/pattern-day-trader-rule-eliminated-sec-2026-implications) [[StockTitan]](https://www.stocktitan.net/articles/pattern-day-trader-rule-eliminated-2026). À reconfirmer au moment de l'implémentation réelle (règle très récente). |
| 16 | Risque de survivorship bias | **Élevé par défaut** si on utilise un univers de tickers actuels. Corrigeable avec des jeux de données point-in-time dédiés (Sharadar, Norgate, QuantRocket, EODHD) — tous payants [[Concretum Group]](https://concretumgroup.substack.com/p/constructing-a-survivorship-bias) [[QuantRocket]](https://www.quantrocket.com/blog/survivorship-bias/). |
| 17 | Risque de lookahead/data leakage | Classique sur les données fondamentales (résultats trimestriels souvent disponibles avec une date de publication différente de la date de "période couverte" — piège fréquent si mal géré) ; moins présent sur le pur OHLCV. |
| 18 | Reproductibilité des tests | Bonne — formats de données standards, outils open-source matures (backtrader, vectorbt, zipline-reloaded). |
| 19 | Diversité des régimes historiques | Très large : bulles (dot-com 2000), crises (2008, 2020), marchés haussiers prolongés, hausses de taux agressives (2022) — spectre complet sur 50+ ans pour les US. |
| 20 | Potentiel de recherche d'inefficiences | Marché le plus étudié académiquement et le plus arbitré par des acteurs institutionnels sophistiqués (HFT, quant funds) — les inefficiences "faciles" sont généralement déjà exploitées ; l'edge retail, s'il existe, est plus probablement sur des niches (small caps, événements spécifiques) que sur les grandes capitalisations liquides. |

---

## 2. ETF

Sous-catégorie des actions au sens de la structure de marché et des données (mêmes brokers, mêmes APIs, mêmes exchanges), avec des différences notables :

| # | Critère | Constat spécifique ETF (vs actions) |
|---|---|---|
| 1-4, 9-10 | Données | Identique aux actions (mêmes fournisseurs, mêmes coûts, mêmes APIs). |
| 5-8 | Coûts/liquidité/spread/slippage | Très variable selon l'ETF : les ETF phares (SPY, QQQ) ont une liquidité et des spreads excellents, souvent meilleurs que les actions individuelles ; les ETF de niche (sectoriels, thématiques, à effet de levier) peuvent avoir une liquidité faible et un spread large malgré un "prix" qui semble normal. |
| 11 | Fondamentaux | Différent : un ETF n'a pas de "résultats trimestriels" — ses fondamentaux pertinents sont la composition du panier sous-jacent, le tracking error vs l'indice, les frais de gestion (expense ratio), et pour les ETF à effet de levier/inverse, la dérive de rebalancement quotidien (un facteur de risque spécifique et bien documenté qui dégrade la performance sur le long terme indépendamment de la direction du marché). |
| 16 | Survivorship bias | Existe aussi : des ETF ferment/fusionnent régulièrement (faible actif sous gestion) — même précaution que pour les actions. |
| 19-20 | Régimes / inefficiences | Potentiellement intéressant sur les ETF à effet de levier (mécanique de rebalancement connue et modélisable) et sur les primes/décotes temporaires vs valeur liquidative (NAV) — niche moins encombrée que le trading direct d'actions. |

---

## 3. Futures

| # | Critère | Constat |
|---|---|---|
| 1 | Qualité/profondeur | Données institutionnelles de haute qualité disponibles (CME Globex MDP 3.0 via Databento) mais payantes — pas d'équivalent gratuit de qualité comparable aux actions. |
| 2 | Longueur historique | Variable par contrat — certains contrats (indices, matières premières majeures) ont des décennies d'historique ; attention à la continuité des contrats (roll-over) qui complique la construction de séries longues cohérentes. |
| 3 | Granularité | Tick-level disponible (payant) jusqu'au quotidien. |
| 4 | Coûts d'accès données | Databento a ouvert un accès public à prix transparent et usage-based en avril 2023, avec $125 de crédits gratuits à l'inscription ; exemple cité : données fin de journée Eurodollar = $3,29 pour 5 ans, données tick = $95,61 pour 5 ans [[Databento]](https://nexusfi.com/a/data/databento-futures-market-data). NinjaTrader offre des données CME top-of-book gratuites avec un compte financé [[NinjaTrader forum]](https://discourse.ninjatrader.com/t/can-anyone-recommend-a-cost-effective-futures-data-feed-for-ninjatrader-cme/4045). Pas d'intégration directe Databento↔NinjaTrader 8 (export CSV manuel nécessaire). |
| 5 | Coûts de transaction | Commissions par contrat (variable selon broker), généralement faibles en absolu mais à rapporter à la taille du contrat. |
| 6 | Liquidité | Très élevée sur les contrats phares (E-mini S&P500, pétrole WTI, or) ; chute vite sur les contrats de mois lointains ou les marchés de niche. |
| 7-8 | Spreads/slippage | Serrés sur les contrats liquides en heures actives ; la continuité entre contrats (roll) introduit un coût/risque spécifique à cette classe d'actifs. |
| 9-10 | Intraday / order book | Disponibles via Databento (payant) ; profondeur de marché complète accessible, contrairement à la plupart des fournisseurs actions gratuits. |
| 11 | Fondamentaux/macro | Directement liés aux données macro (stocks de pétrole, rapports USDA pour l'agricole, etc.) — l'actif lui-même est souvent un proxy macro, cohérent avec le contenu déjà ingéré dans ce projet (pétrole comme leading indicator). |
| 12 | Paper trading | Disponible chez plusieurs brokers futures (NinjaTrader, Interactive Brokers). |
| 13 | Exécution automatisée | Mature côté institutionnel et semi-pro ; API disponibles mais écosystème globalement moins "plug-and-play" pour un développeur solo que les actions. |
| 14 | Contraintes techniques | Plus élevées que les actions : gestion des contrats/roll, marge, spécifications de contrat variables par produit. |
| 15 | Contraintes réglementaires | Jamais concerné par la règle PDT (qui ne s'applique qu'aux actions/options US) [[FuturesHive]](https://www.futureshive.com/blog/day-trading-rules-complete-guide) — marge et levier réglementés différemment (CFTC). |
| 16 | Survivorship bias | Moins pertinent que pour les actions (les contrats ne "disparaissent" pas de la même façon), mais la gestion du roll-over introduit ses propres biais si mal faite. |
| 17 | Lookahead/leakage | Risque spécifique autour des dates de rapports (USDA, EIA stocks pétrole) publiés à heure fixe — bien documentées, donc gérable. |
| 18 | Reproductibilité | Bonne une fois la méthodologie de roll fixée et documentée (point de friction fréquent si non standardisé). |
| 19 | Diversité des régimes | Large sur les contrats historiques majeurs (chocs pétroliers, crises financières, contango/backwardation extrêmes en 2020 sur le pétrole). |
| 20 | Potentiel d'inefficiences | Marché dominé par des acteurs institutionnels et des commodity trading advisors sophistiqués sur les contrats liquides ; des niches (contrats moins suivis, relations intermarchés) peuvent être moins arbitrées. |

---

## 4. Forex

| # | Critère | Constat |
|---|---|---|
| 1 | Qualité/profondeur | Dukascopy (banque et broker suisse) publie son flux tick complet gratuitement en HTTP, sans clé API ni compte, considéré comme l'une des meilleures sources gratuites du marché [[Medium]](https://medium.com/@saleem.latif.ee/downloading-20-years-of-backtest-grade-forex-data-from-dukascopy-4335633def96). |
| 2 | Longueur historique | 15+ ans de données tick chez Dukascopy [[GitHub duka-data]](https://github.com/dela-99/duka-data). |
| 3 | Granularité | Tick-by-tick jusqu'au mensuel, avec bid/ask (spread inclus) — rare d'avoir le spread historique gratuitement sur d'autres classes d'actifs. |
| 4 | Coûts d'accès données | **Gratuit** chez Dukascopy (outil web + export CSV + plusieurs wrappers Python/Node open-source) [[Dukascopy]](https://www.dukascopy.com/swiss/english/marketwatch/historical/). |
| 5 | Coûts de transaction | Pas de commission chez la plupart des brokers retail (rémunération via le spread) ; swap/rollover quotidien selon différentiel de taux (voir `TRADING_KNOWLEDGE_BASE.md` section carry trade). |
| 6 | Liquidité | Marché le plus liquide au monde en volume agrégé sur les paires majeures (EUR/USD, USD/JPY) ; marché décentralisé (pas de bourse centrale), donc la liquidité "vue" dépend du broker/liquidity provider utilisé. |
| 7 | Spreads | Très serrés sur les paires majeures chez les brokers ECN ; plus larges sur les paires exotiques. |
| 8 | Slippage | Généralement faible sur majeures en conditions normales ; important lors d'annonces macro à fort impact ou de gaps de weekend (déjà documenté dans `TRADING_KNOWLEDGE_BASE.md`). |
| 9 | Intraday | Oui, natif chez Dukascopy et la plupart des brokers. |
| 10 | Order book | **Marché décentralisé (OTC)** : pas de carnet d'ordres central unique comme pour les actions/futures — chaque broker/ECN a son propre livre, aucune vision "complète" du marché n'existe pour un acteur retail. Limite structurelle propre au forex. |
| 11 | Fondamentaux/macro | Très riche niveau macro (taux d'intérêt, inflation, banques centrales — cœur de la formation déjà ingérée) ; pas de "fondamentaux" au sens actions (pas de bilan d'une devise). |
| 12 | Paper trading | Disponible chez la quasi-totalité des brokers retail (comptes démo). |
| 13 | Exécution automatisée | Mature — la majorité des brokers forex retail offrent une API ou un support MetaTrader/cTrader scriptable. |
| 14 | Contraintes techniques | Faibles — écosystème très démocratisé (MetaTrader 4/5 domine, scripts MQL ou API REST selon broker). |
| 15 | Contraintes réglementaires | Jamais concerné par la PDT (US) ; réglementation du levier variable selon juridiction (ex. limites ESMA en UE, NFA aux US) — à vérifier selon le pays de résidence/broker choisi. |
| 16 | Survivorship bias | Non pertinent de la même façon que les actions — les paires de devises majeures ne "disparaissent" pas. |
| 17 | Lookahead/leakage | Risque autour du calendrier économique (déjà couvert en détail dans `TRADING_KNOWLEDGE_BASE.md` — distinction attendu/range d'attentes) ; data-vendors variables en qualité d'horodatage. |
| 18 | Reproductibilité | Bonne grâce à Dukascopy (source stable, gratuite, largement utilisée dans la littérature retail) — mais c'est **un seul fournisseur** (prix d'un seul broker, pas un consensus de marché), à garder en tête. |
| 19 | Diversité des régimes | Large (décennies de cycles de taux, crises de change, interventions de banques centrales). |
| 20 | Potentiel d'inefficiences | Marché dominé par les flux institutionnels et les banques ; micro-structure OTC complexifie la recherche d'edge pur "prix" — l'edge retail documenté dans la formation ingérée est plutôt macro/positionnement que haute fréquence. |

---

## 5. Crypto

| # | Critère | Constat |
|---|---|---|
| 1 | Qualité/profondeur | CryptoDataDownload fournit des CSV OHLCV gratuits (Binance, Bitstamp, Gemini, Bitfinex, etc.) en daily/horaire/1-minute, **sans login, sans limite de taux, sans paywall** pour le téléchargement direct [[CryptoDataDownload]](https://www.cryptodatadownload.com/data/). |
| 2 | Longueur historique | Depuis 2017 pour beaucoup de paires sur CryptoDataDownload ; plus courte que forex/actions par nature (marché jeune). |
| 3 | Granularité | Daily/horaire/1-minute en gratuit ; tick-level et carnet d'ordres disponibles via API payante (ex. CryptoDataDownload API, Amberdata) [[CryptoDataDownload API]](https://www.cryptodatadownload.com/api/) [[Amberdata]](https://www.amberdata.io/binance-market-data). |
| 4 | Coûts d'accès données | Gratuit pour OHLCV standard ; payant pour tick/carnet d'ordres/flux temps réel à grande échelle. API gratuite avec limites de taux documentées (120 req/h anonyme, jusqu'à 10 000 req/jour avec token) — largement suffisant pour de la recherche, pas pour du trading haute fréquence. |
| 5 | Coûts de transaction | Variable selon exchange (souvent 0,1% par trade sur les CEX majeures), peut être négligeable sur certains DEX selon la structure de frais ; à vérifier par plateforme. |
| 6 | Liquidité | Très élevée sur BTC/ETH sur les CEX majeures ; chute très vite sur les altcoins — spectre de liquidité le plus large de toutes les catégories (du quasi-aussi-liquide-que-le-forex au quasi-illiquide en quelques clics). |
| 7-8 | Spreads/slippage | Serrés sur BTC/ETH/paires majeures ; potentiellement très élevés sur altcoins ou en période de forte volatilité (le marché crypto est réputé pour des mouvements de prix et une volatilité bien supérieurs aux marchés traditionnels). |
| 9 | Intraday | Oui, natif et généralement gratuit (contrairement aux actions/futures où l'intraday fin est plus souvent payant). |
| 10 | Order book | Disponible — marché 24/7, carnet d'ordres public sur la plupart des CEX, snapshots historiques via fournisseurs spécialisés (payant pour l'historique profond). |
| 11 | Fondamentaux/macro/sentiment | Écosystème spécifique en développement (on-chain data, dominance BTC, funding rates des perpetual futures, sentiment réseaux sociaux) — différent des fondamentaux actions, mais riche et de plus en plus structuré. |
| 12 | Paper trading | Disponible chez la plupart des grands exchanges (testnet/sandbox). |
| 13 | Exécution automatisée | Très mature — APIs REST/WebSocket natives chez toutes les grandes plateformes, écosystème de bots déjà très développé. |
| 14 | Contraintes techniques | Modérées — multiplicité des exchanges (fragmentation de la liquidité), nécessité de gérer les spécificités de chaque API. |
| 15 | Contraintes réglementaires | Nouvelles règles de déclaration fiscale IRS pour les transactions crypto entrant en vigueur au 1er janvier 2026 (US) [[source citée par la recherche]]. Globalement moins encadré que les marchés actions pour le trading retail (pas de PDT), mais cadre réglementaire en évolution rapide selon juridiction. |
| 16 | Survivorship bias | Présent et potentiellement important : de nombreux tokens/exchanges ont disparu (faillites, hacks, rug pulls) — construire un univers "des cryptos qui existent aujourd'hui" biaise fortement un backtest historique. |
| 17 | Lookahead/leakage | Risque spécifique : annonces de listing/delisting, forks, airdrops mal horodatés dans certains jeux de données gratuits. |
| 18 | Reproductibilité | Bonne pour OHLCV standard (CryptoDataDownload largement utilisé et documenté) ; plus complexe dès qu'on inclut plusieurs exchanges (prix légèrement différents d'une plateforme à l'autre). |
| 19 | Diversité des régimes | Historique court (depuis ~2017 pour la plupart des données exploitables) mais déjà passé par plusieurs cycles extrêmes (euphorie 2017, crash 2018, bull run 2020-21, crash 2022, cycles 2024-26) — forte volatilité condensée sur peu d'années. |
| 20 | Potentiel d'inefficiences | Marché plus jeune, plus fragmenté entre exchanges, participation retail encore importante — souvent cité comme offrant plus d'inefficiences qu'un marché actions mature, mais aussi plus de bruit et un risque de régime qui change vite (maturation rapide du marché). |

---

## 6. Marchés prédictifs (Polymarket, Kalshi, etc.)

| # | Critère | Constat |
|---|---|---|
| 1 | Qualité/profondeur | Données accessibles via les APIs officielles (Kalshi `docs.kalshi.com`, Polymarket via des fournisseurs tiers type PolyOrderbooks) et plusieurs fournisseurs tiers spécialisés [[Kalshi docs]](https://docs.kalshi.com/getting_started/historical_data) [[PolyOrderbooks]](https://docs.polyorderbooks.com/). |
| 2 | Longueur historique | **Courte par nature** : Probalytics indique un historique de carnet complet depuis novembre 2025 pour Polymarket et mai 2026 pour Kalshi [[Probalytics]](https://www.probalytics.io/) — c'est la classe d'actifs avec le moins d'historique de marché de toutes celles étudiées ici (le marché lui-même est jeune en tant que produit financier structuré). |
| 3 | Granularité | Snapshots de carnet d'ordres complet (L2) horodatés à la milliseconde chez certains fournisseurs tiers — granularité fine disponible malgré l'historique court. |
| 4 | Coûts d'accès données | APIs officielles existent (gratuites pour les données de marché courantes) ; données historiques profondes/carnet complet passent par des fournisseurs tiers payants (DepthFeed, Probalytics, EntityML) [[DepthFeed]](https://depthfeed.com/historical-data). |
| 5 | Coûts de transaction | Frais de marché spécifiques à chaque plateforme (structure différente d'un broker traditionnel — à documenter précisément par plateforme avant toute utilisation). |
| 6 | Liquidité | Très variable et potentiellement **faible par marché individuel** — contrairement à une paire forex ou une action liquide, chaque "marché" Polymarket/Kalshi est un contrat unique sur un événement spécifique, avec sa propre liquidité, souvent concentrée autour des événements les plus suivis (élections, grands événements sportifs) et beaucoup plus mince ailleurs. |
| 7-8 | Spreads/slippage | Peuvent être significatifs sur les marchés de niche à faible volume ; meilleurs sur les marchés phares. |
| 9 | Intraday | Oui, disponible (marché continu jusqu'à résolution). |
| 10 | Order book | Disponible, y compris L2 historique chez des fournisseurs spécialisés — point positif par rapport aux actions/forex gratuits. |
| 11 | Fondamentaux/macro/sentiment | Nature différente : la "donnée fondamentale" ici est l'information publique sur l'événement sous-jacent (sondages électoraux, données macro officielles pour les marchés sur CPI/Fed, etc.) — pas de bilan d'entreprise, pas de taux d'intérêt classique. Le formateur de la vidéo déjà ingérée utilise explicitement Polymarket comme *source* de probabilités implicites pour lire des événements macro (voir `TRADING_KNOWLEDGE_BASE.md` section 13). |
| 12 | Paper trading | Pas d'équivalent standard "compte démo" documenté comme pour le forex/actions — à vérifier par plateforme ; la nature résolution-unique de chaque marché rend le concept différent (on ne peut pas "rejouer" un marché déjà résolu de la même façon qu'un prix continu). |
| 13 | Exécution automatisée future | APIs de trading existent (CLOB API Polymarket, API Kalshi) — techniquement faisable, mais écosystème d'outils tiers bien moins mature que pour forex/actions/crypto. |
| 14 | Contraintes techniques | Modérées à élevées : peu d'outils open-source matures pour le backtesting spécifique à ce type de marché (contrats à résolution binaire/catégorielle, pas de série de prix continue classique) — probablement à construire soi-même. |
| 15 | Contraintes réglementaires | **Le point le plus mouvant de toute cette comparaison.** Polymarket opère légalement aux US depuis novembre 2025 comme Designated Contract Market régulé par la CFTC (entité séparée "Polymarket US" / QCX LLC) [[startpolymarket.com]](https://startpolymarket.com/countries/united-states/) [[polymarket101.com]](https://www.polymarket101.com/en/docs/countries/is-polymarket-legal-in-united-states/). Mais le cadre reste contesté : la Cour d'appel du 3e circuit a jugé le 7 avril 2026 que les contrats sur événements sportifs sont des "swaps" relevant de la loi fédérale (favorable à Kalshi/Polymarket), tandis que la Cour d'appel du 9e circuit a refusé le 21 mai 2026 de suspendre des actions d'application dans le Nevada et l'État de Washington — un désaccord actif entre circuits judiciaires. La CFTC a engagé des actions contre 9 États (Arizona, Connecticut, Illinois, New York, Nouveau-Mexique, Minnesota, Rhode Island, Wisconsin, Kentucky), et l'État de New York poursuit Kalshi pour 36 milliards de dollars (31 juillet 2026) pour opération de jeu d'argent non autorisée [[sources ci-dessus]]. **Ce point doit être revérifié à la date d'implémentation réelle** — c'est un cadre juridique encore en formation, pas stabilisé. |
| 16 | Survivorship bias | Peu pertinent au sens classique (chaque marché est un événement unique qui se résout, pas un "titre" qui peut être retiré de la cote) — mais un biais analogue existe si on n'étudie que les marchés encore actifs/populaires en ignorant ceux qui ont eu très peu de volume ou ont été annulés/contestés. |
| 17 | Lookahead/leakage | Risque **structurellement différent et important** : la résolution d'un marché dépend d'un événement réel dont la date/l'issue peut être ambiguë ou contestée (litiges de résolution documentés dans l'écosystème des marchés prédictifs) — un biais de data leakage spécifique à surveiller (ex: utiliser une information de résolution qui n'était pas encore publique au moment du trade). |
| 18 | Reproductibilité | Limitée aujourd'hui par le jeune âge du marché et la fragmentation des fournisseurs de données historiques (plusieurs fournisseurs tiers concurrents avec des couvertures différentes, pas encore de standard établi comparable à un flux OHLCV boursier). |
| 19 | Diversité des régimes | **Très faible** — l'historique de marché structuré ne couvre qu'une fenêtre très récente (2025-2026 pour les carnets complets), donc aucun cycle économique complet, aucune vraie crise de marché n'a encore été traversée par ce type de plateforme sous sa forme actuelle. |
| 20 | Potentiel de recherche d'inefficiences | Marché jeune, participation encore largement retail, structure d'information asymétrique propre à chaque événement — potentiel réel d'inefficiences documenté par la littérature sur les marchés de prédiction en général, mais la jeunesse du marché signifie aussi moins de recul pour valider statistiquement quoi que ce soit sur plusieurs années (contrainte directe avec l'objectif du projet : "stratégies rentables sur des années"). |

---

## 7. Option (catégorie non listée par l'utilisateur, ajoutée pour complétude)

Mentionnée ici brièvement car elle partage l'infrastructure de données des actions mais a une structure de risque et de données fondamentalement différente (prix dérivé de plusieurs variables : sous-jacent, volatilité implicite, temps jusqu'à expiration, taux sans risque). Carnet d'ordres et chaînes d'options disponibles via les mêmes fournisseurs que les actions (Polygon, etc.), généralement payant au-delà d'un niveau basique. Risque de lookahead spécifique autour de la volatilité implicite (donnée dérivée, pas directement observable sans modèle). Non détaillée selon les 20 critères ici faute de l'avoir listée dans la demande initiale — à creuser si cette catégorie intéresse.

---

## Synthèse factuelle transversale (pas un classement)

- **Coût d'accès aux données gratuites de qualité raisonnable** existe dans les 5 catégories principales (Alpaca pour actions/ETF, Databento avec crédit gratuit pour futures, Dukascopy pour forex, CryptoDataDownload pour crypto, APIs officielles pour marchés prédictifs) — aucune catégorie n'est bloquée faute de données, mais la profondeur gratuite varie fortement.
- **La longueur d'historique disponible** suit cet ordre décroissant assez net : Actions/Forex (décennies) > Futures (variable, décennies sur les contrats majeurs) > Crypto (depuis ~2017) > Marchés prédictifs (depuis 2025-2026 pour les données structurées) — ce critère est particulièrement important si l'objectif explicite du projet est de valider des stratégies "sur des années" et sur plusieurs régimes de marché.
- **Le carnet d'ordres central n'existe pas** structurellement pour le forex (marché OTC décentralisé) — c'est une limite propre à cette classe, pas un manque de données.
- **La réglementation est stable** pour actions/forex/futures/crypto dans leurs grandes lignes (même si la règle PDT vient de changer) ; elle est **activement contestée et non stabilisée** pour les marchés prédictifs aux US — point de vigilance spécifique si cette catégorie est retenue.
- **Le biais de survie** est un risque réel et documenté pour actions et crypto, moins pour forex/futures (nature de l'instrument), et peu pertinent (mais avec un analogue différent) pour les marchés prédictifs.
- **La diversité des régimes de marché historiques** est maximale pour actions/forex/futures (multiples crises, cycles de taux, chocs géopolitiques couverts par la formation déjà ingérée), nettement plus réduite pour crypto, et quasi inexistante à ce stade pour les marchés prédictifs faute d'historique.

## Sources

- [Alpaca — Fetch Historical Market Data](https://alpaca.markets/learn/fetch-historical-data)
- [Alpaca Support — data provider](https://alpaca.markets/support/data-provider-alpaca)
- [Polygon.io](https://polygon.io/)
- [Sharadar — US stock fundamentals](https://sharadar.com/)
- [Databento futures market data](https://databento.com/futures) / [NexusFi Academy sur Databento](https://nexusfi.com/a/data/databento-futures-market-data)
- [NinjaTrader forum — CME data feed](https://discourse.ninjatrader.com/t/can-anyone-recommend-a-cost-effective-futures-data-feed-for-ninjatrader-cme/4045)
- [Dukascopy — Historical Data Export](https://www.dukascopy.com/swiss/english/marketwatch/historical/)
- [duka-data (GitHub)](https://github.com/dela-99/duka-data)
- [CryptoDataDownload](https://www.cryptodatadownload.com/data/) / [API](https://www.cryptodatadownload.com/api/)
- [Amberdata — Binance market data](https://www.amberdata.io/binance-market-data)
- [Kalshi API docs — historical data](https://docs.kalshi.com/getting_started/historical_data)
- [PolyOrderbooks docs](https://docs.polyorderbooks.com/)
- [DepthFeed — historical data](https://depthfeed.com/historical-data)
- [Probalytics](https://www.probalytics.io/)
- [AngelInvestorsNetwork — PDT rule eliminated](https://angelinvestorsnetwork.com/regulatory-compliance/pattern-day-trader-rule-eliminated-sec-2026-implications)
- [StockTitan — PDT rule eliminated 2026](https://www.stocktitan.net/articles/pattern-day-trader-rule-eliminated-2026)
- [FuturesHive — day trading rules](https://www.futureshive.com/blog/day-trading-rules-complete-guide)
- [startpolymarket.com — US legal status](https://startpolymarket.com/countries/united-states/)
- [polymarket101.com — CFTC regulated status](https://www.polymarket101.com/en/docs/countries/is-polymarket-legal-in-united-states/)
- [Concretum Group — survivorship-bias-free database](https://concretumgroup.substack.com/p/constructing-a-survivorship-bias)
- [QuantRocket — primer on survivorship bias](https://www.quantrocket.com/blog/survivorship-bias/)

**Note de fiabilité** : plusieurs sources ci-dessus sont des blogs/comparateurs tiers, pas des sources primaires officielles. Les faits chiffrés (prix exacts, dates réglementaires) doivent être reconfirmés sur les sites officiels (CFTC, SEC/FINRA, documentation API de chaque fournisseur) au moment où une décision budgétaire ou d'implémentation est prise — ce rapport date du 2 octobre 2026 et certains faits (en particulier la situation réglementaire des marchés prédictifs, en évolution active) peuvent avoir changé.
