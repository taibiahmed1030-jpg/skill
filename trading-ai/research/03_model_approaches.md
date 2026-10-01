# Familles d'approches pour le moteur de décision — survey documenté

**But** : ne pas présupposer que la couche de décision finale sera un LLM, ni un modèle ML quelconque. Documenter les familles disponibles, leurs cas d'usage réels en finance quantitative, leurs limites connues — pour qu'un choix expérimental (pas théorique) se fasse plus tard, étage `HYPOTHESIS ENGINE` / `BACKTEST ENGINE` de l'architecture.

**Principe déjà établi dans ce projet et qui s'applique à toutes les familles ci-dessous** : aucune famille ne "décide" qu'une stratégie est bonne — chacune ne fait que proposer une structure de règle candidate ; la validation reste toujours au Backtest Engine + Robustness Engine (section 7 de `02_architecture.md`).

## 1. Règles quantitatives explicites

**Principe** : des règles écrites à la main, avec des seuils explicites (ex: `h003_vix_spike.py` : "si VIX clôture > 45, acheter").

**Avantages** : totalement interprétables, faciles à auditer, aucun risque de boîte noire, peu coûteuses en calcul, pas de risque d'overfitting par "trop de paramètres" (il y en a peu).

**Limites** : capacité d'expression limitée (ne capture pas d'interactions complexes entre variables), les seuils sont souvent choisis arbitrairement (risque de biais de confirmation si choisis en regardant les données).

**Usage actuel dans ce projet** : c'est la famille utilisée pour toutes les hypothèses du registre jusqu'ici. Reste le point de départ naturel — rien ne justifie de passer à une famille plus complexe avant d'avoir épuisé ce qu'une règle simple peut montrer.

## 2. Statistiques classiques

**Principe** : régression linéaire/logistique, tests d'hypothèse, analyse de corrélation/cointégration, modèles ARIMA/GARCH pour la volatilité.

**Avantages** : cadre théorique mature (intervalles de confiance, tests de significativité directement interprétables), peu de données nécessaires comparé au ML, standard de facto en recherche académique en finance (donc comparable à la littérature existante).

**Limites** : hypothèses fortes (linéarité, stationnarité) souvent violées par les marchés réels ; les régimes de marché changent (un modèle GARCH calibré sur une période calme se comporte mal en crise).

**Usage pertinent** : l'étage Robustness/Statistical Validation du pipeline (section 7 de `02_architecture.md`) EST déjà cette famille (tests de permutation, etc.) — pas seulement un candidat pour la couche de décision, c'est aussi l'outil de validation lui-même.

## 3. Machine learning "classique" (hors deep learning)

**Principe** : arbres de décision, forêts aléatoires, gradient boosting (XGBoost/LightGBM), SVM — pour prédire un label (direction du prix, probabilité de succès d'un setup) à partir de features.

**Avantages** : capture des interactions non-linéaires entre features sans nécessiter autant de données qu'un réseau de neurones profond ; gradient boosting est l'outil le plus utilisé en pratique dans les compétitions de prédiction financière (ex. Kaggle) pour sa robustesse et son rapport performance/coût de calcul.

**Limites** : risque d'overfitting élevé si le nombre de features dépasse largement le nombre d'observations indépendantes (problème déjà identifié concrètement dans ce projet avec H003 : 21 "observations" qui n'étaient que 7 épisodes indépendants — un ML entraîné naïvement sur un tel échantillon serait très fragile) ; interprétabilité moindre qu'une règle explicite (atténuable avec des outils d'explicabilité comme SHAP).

## 4. Modèles de séries temporelles (time series dédiés)

**Principe** : au-delà d'ARIMA/GARCH classiques, inclut les modèles d'état (Kalman filters, modèles à changement de régime/Markov switching) et les approches plus récentes (Prophet, modèles de séries temporelles à base de transformers comme Temporal Fusion Transformer).

**Avantages** : conçus spécifiquement pour la dépendance temporelle et l'autocorrélation — pertinent vu que l'audit de H003 a montré que l'autocorrélation/le clustering temporel est précisément le piège à éviter dans ce projet.

**Limites** : les modèles à changement de régime sont utiles pour détecter qu'on est "en crise" vs "en marché calme" (directement utile à l'étage No-Trade Engine) mais ne prédisent pas directement un prix futur de façon fiable.

## 5. Classification

**Principe** : reformuler le problème non pas comme "prédire le prix" mais comme "ce setup va-t-il réussir, oui/non" ou "dans quel régime sommes-nous" — un problème de classification, souvent plus robuste qu'une régression de prix.

**Avantages** : aligné avec la façon dont ce projet formule déjà ses hypothèses (conditions → résultat attendu, binaire ou catégoriel) ; plus facile à valider statistiquement (taux de succès, matrice de confusion) qu'une prédiction de valeur continue.

**Limites** : perd l'information de magnitude (un setup qui "réussit de 0,1%" et un qui "réussit de 10%" sont comptés pareil) sauf si combiné à une estimation de taille de gain séparée.

## 6. Modèles probabilistes / bayésiens

**Principe** : au lieu d'une prédiction ponctuelle, produire une distribution de probabilité sur le résultat, mise à jour au fur et à mesure que de nouvelles données arrivent (inférence bayésienne).

**Avantages** : correspond presque exactement au raisonnement déjà documenté dans `TRADING_KNOWLEDGE_BASE.md` ("une seule donnée ne crée jamais une thèse seule — c'est une succession de données qui met à jour les probabilités d'une thèse déjà posée", section 1) — c'est littéralement une mise à jour bayésienne informelle. Formaliser ce raisonnement en un cadre bayésien explicite est une piste naturelle et cohérente avec le matériau déjà ingéré. Permet aussi de quantifier l'incertitude (utile pour le Risk Engine : une probabilité à 55% ± 20% ne doit pas être traitée comme une probabilité à 55% ± 2%).

**Limites** : nécessite de définir des distributions a priori (subjectif si mal justifié), plus coûteux à calculer que des règles simples pour des mises à jour fréquentes.

## 7. Ensembles de modèles

**Principe** : combiner plusieurs modèles/règles (vote, moyenne pondérée, stacking) plutôt que se fier à un seul.

**Avantages** : réduit la variance par rapport à un seul modèle fragile ; cohérent avec le principe déjà établi "chaque pièce du puzzle" (macro + technique + positionnement + risk management, jamais une seule source de vérité) — un ensemble est la formalisation naturelle de ce principe.

**Limites** : complexifie l'audit (pourquoi le système a-t-il pris cette décision ?) ; peut masquer qu'aucun modèle individuel n'est réellement bon si l'ensemble "moyenne" plusieurs signaux faibles sans base statistique solide.

## 8. Reinforcement Learning (RL)

**Principe** : un agent apprend une politique de décision (quand acheter/vendre/ne rien faire) en maximisant une récompense cumulée via interaction simulée avec le marché.

**État de la recherche (2025-2026, sources ci-dessous)** : le RL a des résultats de production réels et audités dans des domaines **étroits et spécifiques** — le market making, l'exécution d'ordres (minimiser l'impact de marché sur un gros ordre) et le hedging dynamique sont cités comme ayant produit des résultats de qualité production. En dehors de ces usages étroits, le RL en trading général souffre d'un **mode d'échec récurrent documenté** : le "simulator/backtest overfitting", où la politique apprend à exploiter des artefacts du simulateur plutôt qu'un vrai edge de marché, et s'effondre en conditions réelles. Un système RL mal conçu peut aussi "ajuster son comportement à des patterns historiques qui ne se reproduiront probablement pas" [[arxiv 2512.10913]](https://arxiv.org/html/2512.10913v1).

**Conclusion pour ce projet** : le RL n'est **pas justifié à ce stade**. Il devient potentiellement pertinent plus tard et uniquement si un besoin précis apparaît (ex: optimiser l'exécution d'un ordre de grande taille sur un marché illiquide) — jamais comme solution par défaut pour "trouver des stratégies". La demande explicite de l'utilisateur ("reinforcement learning si réellement justifié") trouve ici sa réponse : pas justifié pour l'instant, à réévaluer si un cas d'usage précis et étroit se présente.

## 9. LLM pour recherche/analyse

**Principe** : **déjà le rôle assigné dans ce projet** — lire du contenu, formaliser des hypothèses, écrire du code de traduction hypothèse→règle, interpréter des résultats de backtest en langage clair. **Jamais** pour décider seul qu'une stratégie est bonne (règle déjà posée et non négociable, cf. consigne de l'utilisateur dans cette même conversation).

**Développement récent pertinent** : la recherche 2025-2026 identifie une tendance "agents augmentés par LLM" où un LLM propose des facteurs/features ou sert de module de mémoire à côté d'un moteur RL/ML classique, mais note explicitement que "la conception de la récompense, la modélisation des coûts de transaction et la robustesse hors-échantillon comptent plus que la capacité du modèle" — autrement dit, un LLM plus gros ne compense pas un protocole de validation faible [[arxiv 2512.10913]](https://arxiv.org/html/2512.10913v1). Confirme directement la priorité déjà fixée dans ce projet : le protocole de validation passe avant le choix du modèle.

## 10. Systèmes hybrides

**Principe** : combiner plusieurs familles ci-dessus à différents étages du pipeline plutôt que choisir une seule famille pour tout.

**C'est en réalité déjà l'architecture retenue dans ce projet**, pas une 10e option parmi d'autres :
- LLM → Research/Knowledge Engine (lecture, formalisation).
- Règles explicites / statistiques classiques → Hypothesis Engine et Robustness Engine (déjà en place).
- ML classique ou probabiliste → candidat naturel pour une version future du Hypothesis Engine quand les règles simples auront montré leurs limites sur des hypothèses plus complexes (plusieurs features combinées).
- RL → non retenu pour l'instant (voir section 8).

## Comment trancher expérimentalement (pas en théorie)

Conformément à la demande de l'utilisateur ("déterminer expérimentalement quelle architecture est adaptée"), la démarche concrète sera, dans l'ordre :
1. Continuer avec des règles explicites tant qu'elles suffisent à représenter une hypothèse (cas de toutes les hypothèses H001-H010 actuelles).
2. Ne passer à du ML classique que le jour où une hypothèse nécessite réellement de combiner plusieurs features de façon non-linéaire pour être testée correctement — et dans ce cas, toujours comparer la performance ML à la règle simple équivalente (si le ML ne bat pas significativement une règle simple après correction de l'overfitting, garder la règle simple — principe de parcimonie).
3. Ne jamais ajouter de complexité (ensemble, RL, deep learning) sans un besoin désigné par un échec documenté d'une approche plus simple sur une hypothèse précise.

## Sources

- [Reinforcement Learning in Financial Decision Making: A Systematic Review (arXiv 2512.10913)](https://arxiv.org/html/2512.10913v1)
- [Agentic Trading: When LLM Agents Meet Financial Markets (arXiv 2605.19337)](https://arxiv.org/pdf/2605.19337)
- [Comparative Analysis of Deep RL Models for Trading (NHSJS)](https://nhsjs.com/2025/comparative-analysis-of-the-effectiveness-of-deep-reinforcement-learning-models-for-trading-in-the-stock-market/)
- [Deep learning for algorithmic trading: systematic review (ScienceDirect)](https://www.sciencedirect.com/science/article/pii/S2590005625000177)
