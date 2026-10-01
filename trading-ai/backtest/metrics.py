"""Outils statistiques pour juger si un résultat de backtest est significatif
ou juste du bruit. Rien ici ne décide qu'une hypothèse est "bonne" -- ça
calcule des nombres, point. La décision de promotion suit les règles de
hypotheses/schema.md.
"""
from __future__ import annotations

import numpy as np


def sharpe_ratio(returns: np.ndarray, periods_per_year: int = 252) -> float:
    if len(returns) < 2 or returns.std(ddof=1) == 0:
        return float("nan")
    return float(np.mean(returns) / np.std(returns, ddof=1) * np.sqrt(periods_per_year))


def max_drawdown(equity_curve: np.ndarray) -> float:
    running_max = np.maximum.accumulate(equity_curve)
    drawdown = (equity_curve - running_max) / running_max
    return float(drawdown.min())


def permutation_test(
    event_returns: np.ndarray,
    all_returns: np.ndarray,
    n_perm: int = 10_000,
    seed: int = 42,
) -> float:
    """P-value: la probabilité d'observer un rendement moyen aussi extrême que
    celui des dates-événement, si on avait pioché le même nombre de dates au
    hasard dans la série complète. C'est le test qui distingue "l'édge est
    réel" de "j'ai eu de la chance sur 12 occurrences".
    """
    rng = np.random.default_rng(seed)
    observed = np.mean(event_returns)
    n = len(event_returns)
    if n == 0 or len(all_returns) < n:
        return float("nan")
    count = 0
    for _ in range(n_perm):
        sample = rng.choice(all_returns, size=n, replace=False)
        if abs(np.mean(sample)) >= abs(observed):
            count += 1
    return count / n_perm


def summary(event_returns: np.ndarray, all_returns: np.ndarray) -> dict:
    return {
        "nb_occurrences": int(len(event_returns)),
        "rendement_moyen_pct": round(float(np.mean(event_returns)) * 100, 3) if len(event_returns) else None,
        "rendement_median_pct": round(float(np.median(event_returns)) * 100, 3) if len(event_returns) else None,
        "pct_positif": round(float(np.mean(event_returns > 0)) * 100, 1) if len(event_returns) else None,
        "sharpe": round(sharpe_ratio(event_returns), 3) if len(event_returns) > 1 else None,
        "rendement_moyen_baseline_pct": round(float(np.mean(all_returns)) * 100, 3),
        "p_value_permutation": round(permutation_test(event_returns, all_returns), 4) if len(event_returns) else None,
    }
