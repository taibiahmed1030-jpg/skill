"""Test empirique de H003 : "Un spike du VIX > 45 est un bon point d'achat
sur le S&P500."

Méthode (event study) :
1. Télécharger VIX et S&P500 en historique quotidien max disponible.
2. Repérer chaque PREMIER jour d'une clôture VIX > 45 après une période où le
   VIX était resté sous 45 pendant au moins 10 jours (pour ne compter qu'un
   seul "événement" par épisode de panique, pas chaque jour d'un spike qui dure
   une semaine).
3. Pour chaque événement, mesurer le rendement du S&P500 à horizon 1, 3 et 6
   mois après.
4. Comparer ces rendements à la distribution de TOUS les rendements glissants
   de même horizon sur la période (le "baseline") via un test de permutation.

Ce script ne décide rien -- il produit des chiffres. La mise à jour du statut
dans le registre suit les règles de hypotheses/schema.md.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from data_loader import load_daily  # noqa: E402
from metrics import summary  # noqa: E402

VIX_THRESHOLD = 45.0
COOLDOWN_DAYS = 10
HORIZONS = {"1_mois": 21, "3_mois": 63, "6_mois": 126}


def find_spike_events(vix: pd.Series, threshold: float, cooldown: int) -> list[pd.Timestamp]:
    above = vix > threshold
    events = []
    last_event_idx = -cooldown - 1
    idx_list = list(vix.index)
    for i, is_above in enumerate(above):
        if is_above and (i - last_event_idx) > cooldown:
            events.append(idx_list[i])
            last_event_idx = i
    return events


def forward_return(prices: pd.Series, date: pd.Timestamp, horizon_days: int) -> float | None:
    if date not in prices.index:
        return None
    pos = prices.index.get_loc(date)
    if pos + horizon_days >= len(prices):
        return None
    p0 = prices.iloc[pos]
    p1 = prices.iloc[pos + horizon_days]
    return float(p1 / p0 - 1.0)


def all_rolling_returns(prices: pd.Series, horizon_days: int) -> np.ndarray:
    return (prices.shift(-horizon_days) / prices - 1.0).dropna().to_numpy()


def main() -> dict:
    print("Téléchargement VIX (^VIX) et S&P500 (^GSPC), historique max...")
    vix_df = load_daily("^VIX", period="max")
    spx_df = load_daily("^GSPC", period="max")

    vix = vix_df["Close"].dropna()
    spx = spx_df["Close"].dropna()
    common_start = max(vix.index.min(), spx.index.min())
    vix = vix[vix.index >= common_start]
    spx = spx[spx.index >= common_start]

    events = find_spike_events(vix, VIX_THRESHOLD, COOLDOWN_DAYS)
    print(f"Période couverte : {spx.index.min().date()} -> {spx.index.max().date()}")
    print(f"Événements détectés (VIX > {VIX_THRESHOLD}, cooldown {COOLDOWN_DAYS}j) : {len(events)}")
    for e in events:
        print(f"  - {e.date()}  (VIX = {vix.loc[e]:.1f})")

    results = {}
    for label, horizon in HORIZONS.items():
        event_rets = np.array([
            r for r in (forward_return(spx, e, horizon) for e in events) if r is not None
        ])
        baseline = all_rolling_returns(spx, horizon)
        results[label] = summary(event_rets, baseline)
        print(f"\n--- Horizon {label} ---")
        print(json.dumps(results[label], indent=2, ensure_ascii=False))

    return {
        "periode_testee": f"{spx.index.min().date()} / {spx.index.max().date()}",
        "nb_occurrences": len(events),
        "evenements": [str(e.date()) for e in events],
        "resultats_par_horizon": results,
    }


if __name__ == "__main__":
    out = main()
    out_path = Path(__file__).resolve().parents[1] / "results" / "H003_vix_spike.json"
    out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nRésultats sauvegardés dans {out_path}")
