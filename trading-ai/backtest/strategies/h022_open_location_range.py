"""Test de H022 : la position de l'ouverture par rapport au range de la veille
prédit-elle l'amplitude de la journée, au-delà de la volatilité récente ?

Protocole figé dans results/H022_preregistration.md (commité avant le
chargement des données). Ce script calcule et consigne ; il ne décide rien
d'autre que l'application mécanique de la règle pré-enregistrée.
"""
from __future__ import annotations

import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import yfinance as yf

TICKER = "SPY"
SUBPERIODS = {"1993_1999": ("1993", "1999"), "2000_2007": ("2000", "2007"),
              "2008_2016": ("2008", "2016"), "2017_fin": ("2017", "2100")}
NW_LAGS = 10
N_PERM = 1000
SEED = 22


def load() -> tuple[pd.DataFrame, list]:
    t = yf.Ticker(TICKER)
    df = t.history(period="max", interval="1d", auto_adjust=False, actions=True)
    df.index = df.index.tz_localize(None).normalize()
    df = df[["Open", "High", "Low", "Close", "Dividends"]].dropna(subset=["Open", "High", "Low", "Close"])
    df = df[df.index < pd.Timestamp.today().normalize()]  # dernier jour complet uniquement
    exdiv = list(df.index[df["Dividends"] > 0])
    return df, exdiv


def build(df: pd.DataFrame, exdiv: list, win: int = 20) -> tuple[pd.DataFrame, dict]:
    d = pd.DataFrame(index=df.index)
    H, L, O, C = df["High"], df["Low"], df["Open"], df["Close"]
    rng = np.log(H / L)
    mid1 = ((H + L) / 2).shift(1)
    R1 = (H - L).shift(1)
    d["x"] = (O - mid1).abs() / R1
    d["D"] = ((O > H.shift(1)) | (O < L.shift(1))).astype(float)
    d["y"] = np.log(rng)
    d["c_avg"] = np.log(rng.shift(1).rolling(win).mean())
    d["c_prev"] = np.log(rng.shift(1))
    d["c_ret"] = np.log(C.shift(1) / C.shift(2)).abs()
    d["gap_norm"] = np.log(O / C.shift(1)).abs() / rng.shift(1).rolling(win).mean()
    stale = (O == C.shift(1))
    stale_by_year = stale.groupby(d.index.year).mean()
    bad_years = [int(y) for y, v in stale_by_year.items() if v > 0.02]
    keep = ~d.index.isin(exdiv) & ~d.index.year.isin(bad_years) & (R1 > 0)
    d = d[keep].replace([np.inf, -np.inf], np.nan).dropna()
    info = {"jours_exclus_dividende": len(exdiv), "annees_exclues_ouverture_perimee": bad_years,
            "taux_ouverture_perimee_max_annuel": float(stale_by_year.max())}
    return d, info


def ols_hac(y: np.ndarray, X: np.ndarray, lags: int = NW_LAGS):
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    e = y - X @ beta
    T = len(y)
    u = X * e[:, None]
    S = u.T @ u / T
    for L in range(1, lags + 1):
        G = u[L:].T @ u[:-L] / T
        S += (1 - L / (lags + 1)) * (G + G.T)
    Zi = np.linalg.inv(X.T @ X / T)
    V = Zi @ S @ Zi / T
    r2 = 1 - (e @ e) / ((y - y.mean()) @ (y - y.mean()))
    return beta, beta / np.sqrt(np.diag(V)), r2


def fit(d: pd.DataFrame, var: str = "x", extra: list[str] | None = None) -> dict:
    cols = [var, "c_avg", "c_prev", "c_ret"] + (extra or [])
    X = np.column_stack([np.ones(len(d))] + [d[c].to_numpy() for c in cols])
    beta, t, r2 = ols_hac(d["y"].to_numpy(), X)
    b = float(beta[1])
    out = {"n": int(len(d)), "periode": f"{d.index.min().date()} / {d.index.max().date()}",
           "b": b, "t_hac": float(t[1]), "r2": float(r2)}
    if var == "x":
        out["ratio_amplitude_extreme_vs_centre"] = math.exp(0.5 * b)
    else:
        out["ratio_amplitude_hors_range"] = math.exp(b)
    return out


def permutation(d: pd.DataFrame, block: int = 20) -> dict:
    cols = ["c_avg", "c_prev", "c_ret"]
    Xc = np.column_stack([np.ones(len(d))] + [d[c].to_numpy() for c in cols])
    y = d["y"].to_numpy()
    x = d["x"].to_numpy()
    b0 = np.linalg.lstsq(np.column_stack([x, Xc]), y, rcond=None)[0][0]
    blocks = [x[i:i + block] for i in range(0, len(x), block)]
    rng = np.random.default_rng(SEED)
    bs = np.empty(N_PERM)
    for i in range(N_PERM):
        xp = np.concatenate([blocks[j] for j in rng.permutation(len(blocks))])
        bs[i] = np.linalg.lstsq(np.column_stack([xp, Xc]), y, rcond=None)[0][0]
    return {"b_observe": float(b0), "p_bilateral": float((np.abs(bs) >= abs(b0)).mean()), "n_permutations": N_PERM}


def quintiles(d: pd.DataFrame) -> list[dict]:
    q = pd.qcut(d["x"], 5, labels=False)
    norm = np.exp(d["y"]) / np.exp(d["c_avg"])  # amplitude / amplitude moyenne 20 j
    return [{"quintile": int(k), "x_median": float(d["x"][q == k].median()),
             "amplitude_normalisee_moyenne": float(norm[q == k].mean()), "n": int((q == k).sum())}
            for k in range(5)]


def main() -> dict:
    raw, exdiv = load()
    d, info = build(raw, exdiv)
    res = {"hypothese": "H022", "preenregistrement": "results/H022_preregistration.md",
           "donnees": {"ticker": TICKER, **info, "n_jours": int(len(d))},
           "principal": fit(d),
           "sous_periodes": {k: fit(d.loc[a:b]) for k, (a, b) in SUBPERIODS.items()},
           "variante_binaire_D": fit(d, "D"),
           "controle_strict_gap": fit(d, "x", ["gap_norm"]),
           "perturbation_fenetre": {f"win={w}": fit(build(raw, exdiv, w)[0]) for w in (10, 20, 60)},
           "quintiles_x": quintiles(d),
           "permutation_par_blocs": permutation(d)}
    return res


def verdict(r: dict) -> str:
    p = r["principal"]
    ratio = p["ratio_amplitude_extreme_vs_centre"]
    subs_pos = all(v["b"] > 0 for v in r["sous_periodes"].values())
    if p["b"] > 0 and abs(p["t_hac"]) >= 1.96 and ratio < 1.03:
        return "REJECTED"
    if p["b"] <= 0 and p["t_hac"] <= -1.96:
        return "REJECTED"
    if p["b"] > 0 and abs(p["t_hac"]) >= 1.96 and ratio >= 1.10 and subs_pos and r["permutation_par_blocs"]["p_bilateral"] < 0.05:
        return "PROMISING"
    return "INCONCLUSIVE"


if __name__ == "__main__":
    res = main()
    res["verdict_regle_preenregistree"] = verdict(res)
    path = Path(__file__).resolve().parents[1] / "results" / "H022_results.json"
    runs = json.loads(path.read_text(encoding="utf-8")).get("runs", []) if path.exists() else []
    runs.append({"horodatage_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"), "resultat": res})
    path.write_text(json.dumps({"runs": runs}, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(res, indent=1, ensure_ascii=False))
