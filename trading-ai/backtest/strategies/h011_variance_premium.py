"""Test de H011 : la prime de variance (VIX²/12 − variance réalisée du mois)
prédit-elle le rendement excédentaire du S&P 500 à 3 mois après 2007 ?

Protocole figé dans results/H011_preregistration.md (commité avant le
chargement des données). Ce script ne décide rien : il calcule les
statistiques prévues et les écrit dans results/H011_results.json.
Dépendances : numpy, pandas, yfinance (via data_loader) — pas de statsmodels.
"""
from __future__ import annotations

import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from data_loader import load_daily  # noqa: E402

TEST_START = "2008-01"
CONTROL_END = "2007-12"
SUBPERIOD_SPLIT = "2016-12"
CRISES = {"2008-2009": ("2008-09", "2009-06"), "2020": ("2020-02", "2020-06")}
HORIZONS = [1, 2, 3, 4, 6]
MAIN_K = 3
N_PERM = 2000
SEED = 11


def norm_p_two_sided(t: float) -> float:
    return math.erfc(abs(t) / math.sqrt(2))


def build_monthly() -> pd.DataFrame:
    spx = load_daily("^GSPC", start="1989-12-01")["Close"]
    vix = load_daily("^VIX", start="1989-12-01")["Close"]
    irx = load_daily("^IRX", start="1989-12-01")["Close"]
    r = 100 * np.log(spx / spx.shift(1))
    month = spx.index.to_period("M")
    rv = (r ** 2).groupby(month).sum(min_count=1)
    n_days = r.groupby(month).count()
    px = spx.groupby(month).last()
    iv = (vix.groupby(vix.index.to_period("M")).last() ** 2) / 12
    rf = irx.groupby(irx.index.to_period("M")).last() / 12  # % par mois
    df = pd.DataFrame({"px": px, "rv": rv, "iv": iv, "rf": rf, "n_days": n_days})
    df = df.loc["1990-01":]
    # le dernier mois n'est retenu que s'il est complet (dernier jour ouvré atteint)
    last_day = spx.index.max()
    if last_day < (last_day + pd.offsets.BMonthEnd(0)):
        df = df.iloc[:-1]
    df["vrp"] = df["iv"] - df["rv"]
    df["r1"] = 100 * np.log(df["px"].shift(-1) / df["px"]) - df["rf"]  # rendement excédentaire t -> t+1
    return df


def forward_excess(df: pd.DataFrame, k: int) -> pd.Series:
    # y_{t,k} = somme des r1 de t à t+k-1 (r1_t couvre t -> t+1)
    return df["r1"].rolling(k).sum().shift(-(k - 1))


def ols(y: np.ndarray, X: np.ndarray):
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    return beta, resid


def newey_west_t(y: np.ndarray, X: np.ndarray, lags: int) -> tuple[np.ndarray, np.ndarray]:
    beta, e = ols(y, X)
    T = len(y)
    Z = X.T @ X / T
    u = X * e[:, None]
    S = u.T @ u / T
    for L in range(1, lags + 1):
        w = 1 - L / (lags + 1)
        G = u[L:].T @ u[:-L] / T
        S += w * (G + G.T)
    Zi = np.linalg.inv(Z)
    V = Zi @ S @ Zi / T
    return beta, beta / np.sqrt(np.diag(V))


def hodrick_1b_t(r1: np.ndarray, X: np.ndarray, sel: np.ndarray, k: int, beta: np.ndarray) -> np.ndarray:
    """Hodrick (1992) 1B. r1[t] = rendement t->t+1 (série contiguë complète),
    X[t] = [1, x_t] connu en t, sel = observations retenues. Variance de la
    pente chevauchante sous H0 : somme des k régresseurs passés multipliée
    par le rendement à un pas démeané."""
    T = len(r1)
    e1 = r1 - np.nanmean(r1[sel])
    idx = [t for t in range(k - 1, T) if sel[t - k + 1:t + 1].all() and not np.isnan(e1[t])]
    W = np.array([e1[t] * X[t - k + 1:t + 1].sum(axis=0) for t in idx])
    Z = X[sel].T @ X[sel] / sel.sum()
    S = W.T @ W / len(idx)
    Zi = np.linalg.inv(Z)
    V = Zi @ S @ Zi / len(idx)
    return beta / np.sqrt(np.diag(V))


def regress(full: pd.DataFrame, k: int, xcol: str = "vrp", start: str | None = None,
            end: str | None = None, exclude: tuple[str, str] | None = None) -> dict:
    """full = série mensuelle contiguë ; y est calculé AVANT toute sélection
    pour ne jamais sommer des mois non consécutifs."""
    d = full.copy()
    d["y"] = forward_excess(d, k)
    t_idx = d.index
    sel = np.ones(len(d), dtype=bool)
    if start:
        sel &= np.array(t_idx >= pd.Period(start, "M"))
    if end:
        sel &= np.array(t_idx <= pd.Period(end, "M"))
    if exclude:
        s_, e_ = pd.Period(exclude[0], "M"), pd.Period(exclude[1], "M")
        sel &= np.array([not (t <= e_ and t + k >= s_) for t in t_idx])
    sel &= d[[xcol, "r1"]].notna().all(axis=1).to_numpy()
    sel_y = sel & d["y"].notna().to_numpy()
    if sel_y.sum() < 24:
        return {"n_obs": int(sel_y.sum()), "note": "échantillon trop court"}
    y = d["y"].to_numpy()
    x = d[xcol].to_numpy()
    X = np.column_stack([np.ones(len(d)), x])
    beta, e = ols(y[sel_y], X[sel_y])
    yy = y[sel_y]
    r2 = 1 - (e @ e) / ((yy - yy.mean()) @ (yy - yy.mean()))
    _, t_nw = newey_west_t(yy, X[sel_y], lags=max(2, k - 1))
    t_h = hodrick_1b_t(d["r1"].to_numpy(), np.nan_to_num(X), sel, k, beta)
    ds = d[sel_y]
    nonover = []
    for off in range(k):
        s = ds.iloc[off::k]
        if len(s) >= 12:
            Xs = np.column_stack([np.ones(len(s)), s[xcol].to_numpy()])
            b_s, t_s = newey_west_t(s["y"].to_numpy(), Xs, lags=0)
            nonover.append({"decalage": off, "n": int(len(s)), "b": float(b_s[1]), "t_white": float(t_s[1])})
    return {
        "n_obs": int(sel_y.sum()),
        "periode": f"{ds.index.min()} / {ds.index.max()}",
        "b": float(beta[1]),
        "a": float(beta[0]),
        "r2": float(r2),
        "t_hodrick_1b": float(t_h[1]),
        "p_hodrick_bilateral": norm_p_two_sided(float(t_h[1])),
        "t_newey_west": float(t_nw[1]),
        "non_chevauchant": nonover,
    }


def block_permutation_p(df: pd.DataFrame, k: int, block: int = 12) -> dict:
    d = df.copy()
    d["y"] = forward_excess(d, k)
    d = d.loc[TEST_START:].dropna(subset=["y", "vrp"])
    y = d["y"].to_numpy()
    x = d["vrp"].to_numpy()
    X = np.column_stack([np.ones(len(d)), x])
    b0 = ols(y, X)[0][1]
    blocks = [x[i:i + block] for i in range(0, len(x), block)]
    rng = np.random.default_rng(SEED)
    bs = np.empty(N_PERM)
    for i in range(N_PERM):
        order = rng.permutation(len(blocks))
        xp = np.concatenate([blocks[j] for j in order])
        bs[i] = ols(y, np.column_stack([np.ones(len(xp)), xp]))[0][1]
    return {
        "b_observe": float(b0),
        "p_bilateral": float((np.abs(bs) >= abs(b0)).mean()),
        "p_unilateral_b_positif": float((bs >= b0).mean()),
        "n_permutations": N_PERM,
        "bloc_mois": block,
    }


def oos_forecast(df: pd.DataFrame, k: int, first_forecast: str = TEST_START) -> dict:
    d = df.copy()
    d["y"] = forward_excess(d, k)
    d = d.dropna(subset=["vrp"])
    pos = list(d.index)
    start_i = pos.index(pd.Period(first_forecast, "M"))
    yh, ym, yt = [], [], []
    for i in range(start_i, len(d)):
        if np.isnan(d["y"].iloc[i]):
            continue
        # estimation uniquement sur les observations dont le rendement est connu en t_i
        train = d.iloc[: max(0, i - k + 1)].dropna(subset=["y"])
        if len(train) < 60:
            continue
        X = np.column_stack([np.ones(len(train)), train["vrp"].to_numpy()])
        beta = ols(train["y"].to_numpy(), X)[0]
        ym.append(beta[0] + beta[1] * d["vrp"].iloc[i])
        yh.append(train["y"].mean())
        yt.append(d["y"].iloc[i])
    yt, ym, yh = map(np.array, (yt, ym, yh))
    r2_oos = 1 - ((yt - ym) ** 2).sum() / ((yt - yh) ** 2).sum()
    f = (yt - yh) ** 2 - ((yt - ym) ** 2 - (yh - ym) ** 2)
    _, t_cw = newey_west_t(f, np.ones((len(f), 1)), lags=max(2, k - 1))
    return {
        "n_previsions": int(len(yt)),
        "r2_oos_campbell_thompson": float(r2_oos),
        "clark_west_t": float(t_cw[0]),
        "clark_west_p_unilateral": float(0.5 * math.erfc(t_cw[0] / math.sqrt(2))),
    }


def main() -> dict:
    df = build_monthly()
    test = df.loc[TEST_START:]
    out = {
        "hypothese": "H011",
        "preenregistrement": "results/H011_preregistration.md",
        "donnees": {
            "premier_mois": str(df.index.min()),
            "dernier_mois": str(df.index.max()),
            "jours_par_mois_min": int(df["n_days"].min()),
            "vrp_moyenne_test": float(test["vrp"].mean()),
            "vrp_ar1_test": float(test["vrp"].autocorr(1)),
        },
        "principal": regress(df, MAIN_K, start=TEST_START),
        "replication_1990_2007": regress(df, MAIN_K, end=CONTROL_END),
        "comparaison_c_s029_04": {
            "iv_seul_2008plus": regress(df, MAIN_K, "iv", start=TEST_START),
            "rv_seul_2008plus": regress(df, MAIN_K, "rv", start=TEST_START),
        },
        "sous_periodes": {
            "2008_2016": regress(df, MAIN_K, start=TEST_START, end=SUBPERIOD_SPLIT),
            "2017_fin": regress(df, MAIN_K, start="2017-01"),
        },
        "exclusion_crises": {
            name: regress(df, MAIN_K, start=TEST_START, exclude=(s, e)) for name, (s, e) in CRISES.items()
        },
        "perturbation_horizon": {f"k={k}": regress(df, k, start=TEST_START) for k in HORIZONS},
        "hors_echantillon_predictif": oos_forecast(df, MAIN_K),
        "permutation_par_blocs": block_permutation_p(df, MAIN_K),
    }
    return out


def verdict(res: dict) -> str:
    p = res["principal"]
    sub = res["sous_periodes"]
    same_sign = all(sub[s].get("b", 0) > 0 for s in sub)
    perm_ok = res["permutation_par_blocs"]["p_bilateral"] < 0.05
    if p["b"] > 0 and abs(p["t_hodrick_1b"]) >= 1.96 and same_sign and perm_ok:
        return "PROMISING"
    if p["b"] < 0 and p["t_hodrick_1b"] <= -1.96:
        return "REJECTED"
    return "INCONCLUSIVE"


if __name__ == "__main__":
    res = main()
    res["verdict_regle_preenregistree"] = verdict(res)
    path = Path(__file__).resolve().parents[1] / "results" / "H011_results.json"
    runs = []
    if path.exists():
        runs = json.loads(path.read_text(encoding="utf-8")).get("runs", [])
    runs.append({"horodatage_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"), "resultat": res})
    path.write_text(json.dumps({"runs": runs}, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(res, indent=1, ensure_ascii=False))
