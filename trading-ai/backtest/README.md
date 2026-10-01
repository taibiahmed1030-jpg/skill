# Moteur de backtest

Convertit une hypothèse du registre en test statistique sur données
historiques réelles. **Aucune décision "c'est rentable" ne sort de ce
dossier sans chiffres vérifiables à l'appui.**

## Structure

- `data_loader.py` — source de données interchangeable. Aujourd'hui :
  yfinance (gratuit, sans compte, couvre forex/actions/indices/crypto). Pour
  brancher une autre source (Polymarket, un broker, un fichier CSV), ajouter
  une fonction qui retourne un DataFrame avec une colonne `Close` indexée par
  date — rien d'autre à changer dans le reste du pipeline.
- `metrics.py` — calculs statistiques (Sharpe, max drawdown, test de
  permutation). Ne décide rien, calcule des nombres.
- `strategies/` — un script par hypothèse testée, nommé `<ID>_<nom>.py`.
  Chaque script est un event study ou un backtest de règles, autonome,
  reproductible.
- `results/` — sorties JSON brutes de chaque exécution, conservées pour
  audit (ne jamais écraser, horodater si re-test).

## Règles de rigueur (non négociables)

1. **Toujours comparer à une baseline.** Un rendement moyen positif ne veut
   rien dire seul — il doit battre la distribution de rendements "normaux"
   sur la même période, via un test de permutation ou équivalent.
2. **Vérifier l'indépendance des événements avant de compter N.** Voir
   l'exemple H003 dans `strategies/h003_vix_spike.py` : 21 jours de clôture
   VIX>45 ne sont que 7 crises réellement indépendantes. Compter les jours au
   lieu des épisodes gonfle artificiellement la significativité — piège
   classique à vérifier systématiquement.
3. **Tester la stabilité par sous-période.** Une hypothèse qui ne fonctionne
   que sur 2008-2009 n'est pas généralisable — refaire le test en excluant
   tour à tour chaque épisode dominant.
4. **Modéliser les coûts réels** (spread, slippage, commissions) avant toute
   promotion `validee` — un edge qui disparaît avec 0,1% de coûts par trade
   n'est pas un edge.
5. **Jamais de `validee` sans franchir le seuil du registre** (voir
   `hypotheses/schema.md`) : p < 0.05, ≥20 occurrences indépendantes,
   stabilité sur ≥2 sous-périodes distinctes.

## Après une hypothèse "validee" : paper trading obligatoire

Un backtest, même rigoureux, ne garantit pas la performance future (biais de
sélection, régime de marché qui change, stratégie qui se dégrade une fois
connue). Avant tout capital réel :

1. Coder la règle en mode simulation sur flux de données live (pas
   historique).
2. Faire tourner un minimum de semaines/mois selon la fréquence de la
   stratégie, sans aucune position réelle.
3. Comparer les résultats simulés aux résultats du backtest — un écart
   important est un signal d'alerte, pas un détail à ignorer.
4. Ne démarrer en capital réel qu'avec un risque minimal, en suivant les
   mêmes règles de gestion de drawdown que n'importe quel trader humain
   (voir section 9 de `TRADING_KNOWLEDGE_BASE.md`).

## Lancer un backtest

```bash
cd backtest/strategies
python3 h003_vix_spike.py
```

Le script met à jour `results/<ID>_<nom>.json`. La mise à jour du
`registry.json` (statut, métriques) reste une étape manuelle/review — jamais
automatique, pour forcer une relecture humaine ou LLM du résultat avant de
changer un statut.
