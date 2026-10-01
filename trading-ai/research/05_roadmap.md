# Roadmap expérimentale

**Ce document ne choisit pas de marché.** Il définit l'ordre de travail une
fois qu'un ou plusieurs marchés auront été choisis, et identifie ce qui peut
être fait dès maintenant, indépendamment de ce choix.

## Ce qui peut être fait MAINTENANT, avant tout choix de marché

Ces tâches ne dépendent pas du marché retenu — elles renforcent le cœur du
pipeline (étages 1-2 de `02_architecture.md`) :

1. **Ajouter le cache au `data_loader.py`.** Aucune contrainte de ressources
   listée par l'utilisateur ("pas de téléchargements inutiles") n'est encore
   respectée mécaniquement — aujourd'hui, relancer `h003_vix_spike.py`
   retélécharge tout. Correction simple (cache disque par
   `source+symbole+granularité+plage`), à faire avant toute nouvelle
   expérience, quel que soit le marché visé ensuite.
2. **Construire l'étage DATA VALIDATION** (section 2 de `02_architecture.md`)
   comme module générique — trous temporels, valeurs aberrantes, doublons,
   cohérence OHLC. Aucune expérience sur un nouveau marché ne devrait
   démarrer sans passer par cette validation.
3. **Logger systématiquement chaque exécution de backtest** (déjà
   partiellement fait via `backtest/results/*.json`, à généraliser : date,
   durée d'exécution, version du code, paramètres exacts — pour
   reproductibilité totale, pas seulement le résultat final).
4. **Traduire 1-2 hypothèses supplémentaires** du registre en event studies,
   en choisissant celles dont les données sont les plus simples d'accès
   (ex: H010 sur la géopolitique nécessite une base d'événements classés —
   plus lourd à monter ; H005 sur Fibonacci/crowding nécessite des données
   de positionnement retail, pas gratuites et pas encore identifiées comme
   source — à documenter dans `MISSING_CONTEXT.md` si on s'y attaque).

## Ce qui dépend du choix de marché

Une fois une ou plusieurs catégories retenues (décision de l'utilisateur,
informée par `01_market_comparison.md`), dans cet ordre :

1. **Implémenter l'adaptateur `data_loader_<marché>.py`** correspondant,
   avec le cache déjà en place à l'étape précédente.
2. **Reconstituer un univers sans biais de survie** si le marché choisi y est
   exposé (actions, crypto — voir section 16 de `01_market_comparison.md`)
   avant tout backtest sur plusieurs titres/tokens.
3. **Choisir 2-3 hypothèses du registre déjà compatibles** avec ce marché
   (le champ `marche` de chaque hypothèse dans `registry.json` indique déjà
   la compatibilité a priori) et les tester en suivant le protocole complet
   de `04_protocols.md`.
4. **Construire le moteur de backtest à l'état** (section 6 de
   `02_architecture.md`) seulement si une hypothèse retenue l'exige
   réellement (gestion de position, pas juste un event study).
5. **Construire NO-TRADE ENGINE et RISK ENGINE** en code (aujourd'hui
   seulement documentés) une fois qu'au moins une hypothèse aura atteint
   `validee` ou s'en approchera, pour avoir un cas réel à encoder plutôt que
   de deviner les règles à l'avance.

## Ce qui reste explicitement EN PAUSE (consigne de l'utilisateur)

- Paper trading (protocole défini dans `04_protocols.md` étape E, non activé).
- Connexion à un compte réel, quelque soit le marché.
- Construction d'une stratégie spécifique à Polymarket ou tout autre marché.
- Tout placement d'ordre, simulé ou réel.

## Prochaine décision requise (pas avant, pas urgente)

Une fois ce rapport d'audit lu, la seule décision qui débloque la suite est
: **quelle(s) catégorie(s) de marché étudier en premier**, à partir de
`01_market_comparison.md`. Aucune autre décision n'est bloquante — tout le
reste (cache, validation, logs, protocoles) peut avancer en parallèle, quel
que soit ce choix.
