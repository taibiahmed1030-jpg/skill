"""Test de H012 : momentum temporel (TSMOM, paramètres de S015) sur un univers
figé de 12 ETF multi-classes, hors échantillon après 2009, net de coûts.

Protocole figé dans results/H012_preregistration.md (commité avant le
chargement des données).
"""
from __future__ import annotations

import json
import math
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import yfinance as yf

ROOT = Path(__file__).resolve().parents[1]
TICKERS = ["SPY", "IWM", "EFA", "EEM", "VNQ", "TLT", "IEF", "LQD", "TIP", "GLD", "DBC", "UUP"]
TARGET_VOL = 0.40
COM = 60
COST = 0.0005
TEST_START = "2010-01"
HALF = "2018-01"
SEED = 12
N_PERM = 5000


def load() -> tuple[pd.DataFrame, pd.Series]:
    px = yf.download(TICKERS, start="1999-01-01", interval="1d", auto_adjust=True, progress=False)["Close"]
    px.index = pd.to_datetime(px.index).tz_localize(None)
    px = px[px.index < pd.Timestamp.today().normalize()]
    irx = yf.download("^IRX", start="1999-01-01", interval="1d", auto_adjust=True, progress=False)["Close"]
    if isinstance(irx, pd.DataFrame):
        irx = irx.iloc[:, 0]
    irx.index = pd.to_datetime(irx.index).tz_localize(None)
    return px, irx


def build(px: pd.DataFrame, irx: pd.Series):
    r_d = np.log(px / px.shift(1))
    vol = r_d.ewm(com=COM, min_periods=60).std() * math.sqrt(261)
    month = px.index.to_period("M")
    pm = px.groupby(month).last()
    volm = vol.groupby(month).last()
    rf_m = (irx.groupby(irx.index.to_period("M")).last() / 100 / 12).reindex(pm.index).ffill()
    ret_m = pm.pct_change().sub(rf_m, axis=0)            # rendement excédentaire du mois t
    ret12 = (pm / pm.shift(12) - 1).sub(rf_m.rolling(12).sum(), axis=0)
    sig = np.sign(ret12)
    w = sig * TARGET_VOL / volm                           # poids décidés en fin de mois t
    avail = w.notna().sum(axis=1)
    w = w.div(avail.where(avail > 0), axis=0)             # moyenne des positions disponibles
    w_next = w.shift(1)                                   # appliqués au mois t+1
    # dernier mois incomplet exclu
    last_day = px.index.max()
    if last_day < last_day + pd.offsets.BMonthEnd(0):
        ret_m, w_next, sig, volm = ret_m.iloc[:-1], w_next.iloc[:-1], sig.iloc[:-1], volm.iloc[:-1]
    return ret_m, w_next, sig, volm, avail.shift(1)


def portfolio(ret_m: pd.DataFrame, w: pd.DataFrame) -> pd.DataFrame:
    gross = (w * ret_m).sum(axis=1, min_count=1)
    turnover = w.fillna(0).diff().abs().sum(axis=1)
    net = gross - COST * turnover
    return pd.DataFrame({"brut": gross, "net": net, "rotation": turnover})


def nw_t(x: np.ndarray, lags: int = 3) -> float:
    e = x - x.mean()
    T = len(x)
    s = e @ e / T
    for L in range(1, lags + 1):
        s += 2 * (1 - L / (lags + 1)) * (e[L:] @ e[:-L]) / T
    return float(x.mean() / math.sqrt(s / T))


def stats(p: pd.DataFrame) -> dict:
    x = p["net"].dropna().to_numpy()
    return {"periode": f"{p.index.min()} / {p.index.max()}", "n_mois": int(len(x)),
            "moyenne_nette_mensuelle_pct": float(100 * x.mean()), "t_nw": nw_t(x),
            "sharpe_net_annualise": float(x.mean() / x.std(ddof=1) * math.sqrt(12)),
            "moyenne_brute_mensuelle_pct": float(100 * p["brut"].mean()),
            "rotation_mensuelle_moyenne": float(p["rotation"].mean())}


def main() -> dict:
    px, irx = load()
    ret_m, w, sig, volm, avail = build(px, irx)
    ok = avail >= 6
    w = w[ok]
    ret_m = ret_m.loc[w.index]
    main_p = portfolio(ret_m, w)
    w_neu = w.sub(w.mean(axis=1), axis=0).where(w.notna())
    neu_p = portfolio(ret_m, w_neu)
    pas_p = portfolio(ret_m, w.abs())
    test = main_p.loc[TEST_START:]
    # permutation par blocs de 12 mois des signes, actif par actif, sur la période de test
    rng = np.random.default_rng(SEED)
    wt = w.loc[TEST_START:].to_numpy()
    rt = ret_m.loc[TEST_START:].to_numpy()
    T = len(wt)
    blocks = [np.arange(i, min(i + 12, T)) for i in range(0, T, 12)]
    m0 = float(test["net"].mean())
    perm = np.empty(N_PERM)
    for b in range(N_PERM):
        wp = np.empty_like(wt)
        for j in range(wt.shape[1]):
            order = np.concatenate([blocks[k] for k in rng.permutation(len(blocks))])
            wp[:, j] = np.abs(wt[:, j]) * np.sign(wt[order, j])
        g = np.nansum(wp * rt, axis=1)
        to = np.abs(np.diff(np.nan_to_num(wp), axis=0, prepend=np.nan_to_num(wp[:1]))).sum(axis=1)
        perm[b] = (g - COST * to).mean()
    years = test["net"].groupby(test.index.year).sum()
    res = {"hypothese": "H012", "preenregistrement": "results/H012_preregistration.md",
           "donnees": {tk: str(px[tk].first_valid_index().date()) for tk in TICKERS},
           "controle_avant_2010": stats(main_p.loc[:"2009-12"]),
           "principal_2010_fin": stats(test),
           "moitie_2010_2017": stats(main_p.loc[TEST_START:"2017-12"]),
           "moitie_2018_fin": stats(main_p.loc[HALF:]),
           "exposition_nette_neutralisee_2010_fin": stats(neu_p.loc[TEST_START:]),
           "passif_risque_egal_2010_fin": stats(pas_p.loc[TEST_START:]),
           "permutation": {"moyenne_observee": m0, "p_bilateral": float((np.abs(perm - perm.mean()) >= abs(m0 - perm.mean())).mean())},
           "r14_signe_par_annee": {str(k): float(v) for k, v in years.items()}}
    p = res["principal_2010_fin"]
    halves = res["moitie_2010_2017"]["moyenne_nette_mensuelle_pct"] > 0 and res["moitie_2018_fin"]["moyenne_nette_mensuelle_pct"] > 0
    if p["moyenne_nette_mensuelle_pct"] > 0 and p["t_nw"] >= 2.0 and halves and res["permutation"]["p_bilateral"] < 0.05:
        v = "PROMISING"
    elif p["moyenne_nette_mensuelle_pct"] < 0 and p["t_nw"] <= -2.0:
        v = "REJECTED"
    else:
        v = "INCONCLUSIVE"
    res["verdict_regle_preenregistree"] = v
    return res


if __name__ == "__main__":
    res = main()
    path = ROOT / "results" / "H012_results.json"
    runs = json.loads(path.read_text(encoding="utf-8")).get("runs", []) if path.exists() else []
    runs.append({"horodatage_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"), "resultat": res})
    path.write_text(json.dumps({"runs": runs}, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(res, indent=1, ensure_ascii=False))
