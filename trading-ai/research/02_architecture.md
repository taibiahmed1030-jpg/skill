# Architecture multi-marchés — le marché comme paramètre, pas une dépendance

**But** : définir une architecture où changer de marché cible (ou en ajouter un deuxième) ne demande pas de réécrire le pipeline, seulement d'implémenter une interface. Suit le schéma fourni par l'utilisateur :

```
MARKET DATA → DATA VALIDATION → FEATURE ENGINEERING → KNOWLEDGE/RESEARCH ENGINE
→ HYPOTHESIS ENGINE → BACKTEST ENGINE → ROBUSTNESS/STATISTICAL VALIDATION
→ NO-TRADE ENGINE → RISK ENGINE → PAPER TRADING → EVENTUAL EXECUTION
```

## Principe directeur

Chaque étage communique avec le suivant via un **contrat de données stable** (un schéma, pas une classe concrète). Un étage ne doit jamais savoir si la donnée vient d'actions, de forex ou d'un marché prédictif — seulement qu'elle respecte le contrat. C'est ce qui permet d'ajouter un marché sans toucher aux étages situés après `MARKET DATA`.

## Détail par étage

### 1. MARKET DATA (déjà esquissé : `backtest/data_loader.py`)

**Rôle** : récupérer des données brutes depuis une source quelconque et les normaliser dans un format unique.

**Contrat de sortie** — un objet/DataFrame avec au minimum :
```
timestamp (UTC, tz-aware) | symbol | open | high | low | close | volume
```
Pour les marchés sans OHLCV classique (ex. marché prédictif binaire), le contrat se réduit à `timestamp | symbol | price (0-1) | volume` — même interface, champs optionnels selon la nature du marché déclarée par un adaptateur.

**Ce qui change selon le marché** : uniquement l'implémentation de l'adaptateur (`data_loader_equities.py`, `data_loader_forex.py`, `data_loader_prediction.py`, ...). Chacun sait parler à sa source (yfinance, Dukascopy, API Kalshi, etc.) et retourne le même contrat.

**Contrainte ressources** : chaque adaptateur doit écrire sur disque (cache) ce qu'il télécharge, avec une clé de cache incluant `(source, symbol, granularité, plage de dates)`. Ne jamais retélécharger une donnée déjà en cache — directement lié à la contrainte "pas de téléchargements inutiles" de l'utilisateur. `backtest/data_loader.py` actuel n'a PAS encore ce cache — à ajouter avant tout usage répété (voir `research/05_roadmap.md`).

### 2. DATA VALIDATION

**Rôle** : détecter les problèmes de données AVANT qu'ils ne contaminent une hypothèse ou un backtest. N'existe pas encore dans le projet — c'est un vrai manque identifié par cet audit.

**Vérifications minimales, indépendantes du marché** :
- Trous temporels inattendus (jours manquants hors jours de fermeture connus du marché concerné).
- Valeurs aberrantes (sauts de prix >X écarts-types sans explication, volumes négatifs, OHLC incohérent — ex. `low > high`).
- Doublons (même timestamp, même symbole, valeurs différentes).
- Cohérence temporelle (timestamps strictement croissants, pas de fuseau horaire ambigu).
- **Vérification de survivorship bias** : pour les marchés qui en souffrent (actions, crypto — voir `01_market_comparison.md`), vérifier explicitement qu'un univers "à une date passée" inclut les instruments qui ont disparu depuis, pas seulement l'univers actuel.

**Spécifique par marché** (plugin, pas dans le cœur) : ex. pour les marchés prédictifs, vérifier qu'un prix reste dans `[0, 1]` ; pour le forex, vérifier la cohérence bid/ask (ask ≥ bid toujours).

### 3. FEATURE ENGINEERING

**Rôle** : transformer les données validées en variables utilisables par les étages suivants (indicateurs techniques, données macro jointes, signaux de sentiment, etc.).

**Principe d'indépendance au marché** : une feature est une fonction `DataFrame → DataFrame` qui ajoute des colonnes. Les features génériques (moyennes mobiles, volatilité réalisée, rendements à horizon N) s'appliquent à n'importe quel marché respectant le contrat de l'étage 1. Les features spécifiques à un marché (yield spread pour le forex, funding rate pour les perpetuals crypto, probabilité implicite pour les marchés prédictifs) vivent dans des modules séparés et optionnels.

**Lien avec le contenu déjà ingéré** : toutes les features mentionnées dans `TRADING_KNOWLEDGE_BASE.md` (RSI, moyennes mobiles, Fibonacci, DXY, VIX, yield spread...) sont candidates pour cet étage — **mais rappel de la règle déjà posée** : une feature décrite dans une vidéo n'est qu'une idée de feature, pas une feature validée. Son utilité réelle se décide au `BACKTEST ENGINE`, jamais ici.

### 4. KNOWLEDGE / RESEARCH ENGINE

**Rôle** : c'est le `trading-ai/hypotheses/` + `trading-ai/ingestion/` déjà construits. Stocke ce qui a été appris (de vidéos, de papiers académiques, d'observations manuelles) sous forme d'hypothèses formalisées, avec leur statut de validation. **Déjà existant, pas à reconstruire.**

**Ce qui manque encore ici** : un lien explicite entre une hypothèse du registre et les features/marchés qu'elle requiert (actuellement `donnees_necessaires` est un texte libre, pas une référence structurée vers l'étage Feature Engineering) — à formaliser quand le registre grossira.

### 5. HYPOTHESIS ENGINE

**Rôle** : transformer une hypothèse en règle exécutable testable (ex: "si VIX > 45 alors acheter SPX" devient une fonction Python retournant un signal). C'est la couche de **traduction** entre une idée en langage naturel (sortie du Research Engine) et un objet que le Backtest Engine peut exécuter.

**Aujourd'hui** : fait manuellement, cas par cas (`backtest/strategies/h003_vix_spike.py` est un exemple de traduction manuelle réussie). **Pas encore généralisé** en un framework réutilisable (ex: un format de règle commun que n'importe quelle hypothèse peut remplir) — à faire une fois 3-4 hypothèses traduites à la main, pour généraliser depuis des cas réels plutôt que deviner une abstraction à l'avance.

### 6. BACKTEST ENGINE

**Rôle** : déjà esquissé (`backtest/metrics.py`, `backtest/data_loader.py`, un cas réel exécuté : H003). Exécute une règle du Hypothesis Engine sur des données historiques validées et produit des métriques brutes.

**Ce qui manque** : le module actuel est un *event study* (mesurer le rendement après un événement), pas encore un *vrai moteur de backtest à l'état* (ouverture/fermeture de positions avec taille, frais, marge, plusieurs positions simultanées). Les deux sont utiles à des moments différents :
- Event study → pour tester rapidement si une idée a un signal statistique, avant d'investir dans une simulation complète (c'est l'usage actuel, le bon choix pour le stade actuel du projet).
- Moteur de backtest à l'état → nécessaire dès qu'une hypothèse implique de la gestion de position (stop loss, sizing, plusieurs trades qui se chevauchent) — pas encore construit, à faire quand une hypothèse le demandera réellement (ex: H006 sur la gestion active du R:R).

### 7. ROBUSTNESS / STATISTICAL VALIDATION

**Rôle** : déjà en partie fait (test de permutation dans `metrics.py`, et surtout la correction manuelle du biais de clustering sur H003 — c'est exactement le travail de cet étage). À généraliser :
- Walk-forward / out-of-sample (tester sur une période, valider sur une autre, jamais la même).
- Test de stabilité par sous-période (déjà identifié comme manquant dans le verdict H003 — "pas de test de robustesse par sous-période effectué à ce stade").
- Correction pour tests multiples (si on teste 10 hypothèses, certaines auront un p<0.05 par pur hasard — un seuil de signification doit tenir compte du nombre d'hypothèses testées, ex. correction de Bonferroni ou false discovery rate).

### 8. NO-TRADE ENGINE

**Rôle** : décider explicitement QUAND NE PAS trader, même avec une hypothèse validée. Existe déjà comme **concept documenté** (`TRADING_KNOWLEDGE_BASE.md` section 8, et le principe répété "pas d'edge clair = pas de trade") mais pas encore comme **code**. À construire comme une couche de filtres qui peut bloquer un signal même validé : données suspectes à ce moment précis, événement macro imminent non modélisé, hypothèse hors de son régime de validité connu (ex: testée seulement en période de forte volatilité, on est en période calme).

### 9. RISK ENGINE

**Rôle** : dimensionnement de position, limites de drawdown, exposition corrélée — tout ce que `TRADING_KNOWLEDGE_BASE.md` section 9 documente déjà en théorie (facteur R, paliers de drawdown). Pas encore codé. Indépendant du marché par construction (le risque se raisonne en unités de compte, pas en unités de l'actif).

### 10. PAPER TRADING

**Rôle** : déjà défini en procédure dans `backtest/README.md` ("après une hypothèse validée : paper trading obligatoire"). **Explicitement mis en pause par consigne de l'utilisateur dans cette session** — rien à construire ici pour l'instant.

### 11. EVENTUAL EXECUTION

**Rôle** : connexion à un broker/une plateforme réelle. **Explicitement hors scope pour l'instant** (aucun compte réel, aucun ordre).

## Ce que ce document ne fait pas

Il ne choisit pas de marché, ne commence aucune implémentation au-delà de ce qui existe déjà, et ne construit pas encore les étages 2, 5 (généralisé), 7 (généralisé), 8, 9 — ils sont définis ici en interface/contrat pour que le futur travail s'y range, mais leur code reste à écrire (voir `research/05_roadmap.md` pour l'ordre).
