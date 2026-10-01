# Schéma du registre d'hypothèses

Chaque hypothèse dans `registry.json` est un objet avec les champs suivants :

| Champ | Type | Description |
|---|---|---|
| `id` | string | Identifiant unique (`H001`, `H002`, ...). Jamais réutilisé, même si une hypothèse est rejetée. |
| `idee` | string | Description courte et objective de l'hypothèse. |
| `source` | object | `{ "title": ..., "url": ..., "timestamp": ... }` — traçabilité vers le contenu d'origine. |
| `marche` | string | Marché concerné (`forex`, `actions`, `crypto`, `polymarket`, `general`). |
| `conditions` | string | Conditions précises de déclenchement, formulées de façon vérifiable. |
| `entree` / `sortie` / `no_trade` | string | Règles d'entrée, de sortie, de non-trade (si applicable — `null` sinon). |
| `timeframe` | string | Horizon temporel. |
| `donnees_necessaires` | array[string] | Données requises pour tester l'hypothèse. |
| `resultat_attendu` | string | Ce que l'hypothèse prédit. |
| `statut` | string | `non_testee` \| `en_test` \| `validee` \| `rejetee` \| `non_testable` (données indisponibles). |
| `backtest` | object \| null | Résultats du dernier backtest (voir ci-dessous), `null` si `statut = non_testee`. |
| `derniere_maj` | string | Date ISO de la dernière mise à jour du statut. |

## Objet `backtest`

```json
{
  "date_execution": "2026-10-01",
  "periode_testee": "2004-01-01 / 2026-09-30",
  "nb_occurrences": 12,
  "metriques": { "rendement_moyen_pct": 0.0, "sharpe": 0.0, "max_drawdown_pct": 0.0 },
  "p_value_permutation": 0.0,
  "verdict": "La description en une phrase du résultat, sans extrapolation.",
  "limites": "Biais connus, taille d'échantillon, periode couverte, etc."
}
```

## Règles de promotion de statut (jamais décidées par un LLM seul)

- `non_testee → en_test` : dès qu'un backtest est lancé.
- `en_test → validee` : **uniquement si** p-value de permutation < 0.05 ET nombre d'occurrences ≥ 20 ET le résultat est stable sur au moins 2 sous-périodes distinctes (pas un seul régime de marché). Même "validée", une hypothèse n'est pas une certitude — c'est un signal statistiquement significatif sur l'historique testé, rien de plus.
- `en_test → rejetee` : si le backtest contredit l'hypothèse ou n'atteint pas le seuil de significativité après un échantillon suffisant.
- Toute hypothèse `validee` doit encore passer par du paper trading (voir `backtest/README.md`) avant tout capital réel.
