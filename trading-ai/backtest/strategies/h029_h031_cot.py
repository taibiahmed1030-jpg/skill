"""Tests de H029 (flip des positions nettes, scindée en H029-NC / H029-C) et
H031 (filtre COT d'une stratégie de tendance), selon
results/H029_H031_preregistration.md (commité avant tout calcul de rendement).

Réutilise le chargement et la datation R15 de h027_h028_cot.py.
"""
from __future__ import annotations

import importlib.util
import json
import math
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def _load(name: str, file: str):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


cot = _load("cot", "h027_h028_cot.py")
ovl = _load("ovl", "h029_h031_overlap.py")

HALF = pd.Timestamp("2013-01-01")
DELTA = 3.0
SMA_MAIN, SMA_ALT = 50, (20, 100)
COST = 0.0005
N_PLACEBO = 1000
PLACEBO_BLOCK = 13
CORN = "002602"


# ---------------------------------------------------------------- H029
def h029(cotdf: pd.DataFrame, prices: dict, zero_jumps: bool) -> dict:
    cot.SEED = 29
    out = {}
    for cat, col in [("H029-NC", "net_nc"), ("H029-C", "net_c")]:
        frames = {}
        for code, tk in cot.MARKETS.items():
            g = cotdf[cotdf["code"] == code][["code", "asof", "net_c", "net_nc"]]
            c, _ = cot.market_frame(g, prices[tk], zero_jumps)
            c["s"] = ovl.flips(c[col].to_numpy())
            frames[code] = c
        out[cat] = {f"h={h}": cot.test_a(frames, h) for h in cot.HORIZONS}
    return out


def holm2(pa: float, pb: float) -> tuple[float, float]:
    lo, hi = sorted([pa, pb])
    a1 = min(1.0, 2 * lo)
    a2 = max(a1, hi)
    return (a1, a2) if pa <= pb else (a2, a1)


def verdict_h029(r: dict) -> dict:
    nc, c = r["H029-NC"]["h=8"], r["H029-C"]["h=8"]
    p_nc, p_c = holm2(nc["p_permutation_bilateral"], c["p_permutation_bilateral"])

    def ok(x, p):
        return x["moyenne_s_r"] > 0 and p < 0.05 and all((v["moyenne"] or 0) > 0 for v in x["moitie"].values())

    sig_pos = {"NC": nc["moyenne_s_r"] > 0 and p_nc < 0.05, "C": c["moyenne_s_r"] > 0 and p_c < 0.05}
    if (ok(nc, p_nc) and not sig_pos["C"]) or (ok(c, p_c) and not sig_pos["NC"]):
        v = "PROMISING"
    elif nc["moyenne_s_r"] <= 0 and c["moyenne_s_r"] <= 0 and min(p_nc, p_c) < 0.05:
        v = "REJECTED"
    else:
        v = "INCONCLUSIVE"
    return {"p_holm_NC": p_nc, "p_holm_C": p_c, "H029": v}


# ---------------------------------------------------------------- H031
def delta_weekly(g: pd.DataFrame) -> pd.DataFrame:
    g = g.sort_values("asof").reset_index(drop=True)
    tot = (g["nc_long"] + g["nc_short"]).replace(0, np.nan)
    g["delta"] = g["net_nc"].diff() / tot * 100
    g = g[~g["asof"].apply(cot.excluded)]
    return g[["asof", "delta"]].dropna()


def daily_delta(dw: pd.DataFrame, dates: pd.DatetimeIndex, lag_days: int) -> pd.Series:
    eff = dw["asof"] + pd.Timedelta(days=lag_days)
    idx = dates.searchsorted(eff)
    s = pd.Series(np.nan, index=dates)
    for i, v in zip(idx, dw["delta"].to_numpy()):
        if i < len(dates):
            s.iloc[i] = v
    return s.ffill()


def strategies(px: pd.Series, dlt: pd.Series, n_sma: int) -> tuple[pd.Series, pd.Series]:
    sma = px.rolling(n_sma).mean()
    above, below = px > sma, px < sma
    pos_a = pd.Series(np.where(above, 1.0, np.where(below, -1.0, 0.0)), index=px.index).where(sma.notna(), 0.0)
    sig = pd.Series(np.nan, index=px.index)
    sig[above & (dlt >= DELTA)] = 1.0
    sig[below & (dlt <= -DELTA)] = -1.0
    pos_b = sig.ffill().fillna(0.0)
    return pos_a, pos_b


def pnl(pos: pd.Series, r: pd.Series) -> pd.Series:
    return pos.shift(1) * r - COST * pos.diff().abs().fillna(0.0)


def nw_t(x: np.ndarray, lags: int = 10) -> float:
    e = x - x.mean()
    T = len(x)
    s = e @ e / T
    for L in range(1, lags + 1):
        s += 2 * (1 - L / (lags + 1)) * (e[L:] @ e[:-L]) / T
    return float(x.mean() / math.sqrt(s / T))


def sharpe(x: pd.Series) -> float:
    x = x.dropna()
    return float(x.mean() / x.std(ddof=1) * math.sqrt(252)) if x.std(ddof=1) > 0 else float("nan")


def market_returns(px: pd.Series, zero_jumps: bool) -> pd.Series:
    li, _ = cot.log_index(px, zero_jumps)
    r = li.diff()
    r = r[r.index >= cot.START]
    return r - r.mean()


def h031(cotfull: pd.DataFrame, prices: dict, zero_jumps: bool) -> dict:
    dws = {code: delta_weekly(cotfull[cotfull["code"] == code]) for code in cot.MARKETS}
    rets = {code: market_returns(prices[tk], zero_jumps) for code, tk in cot.MARKETS.items()}

    def portfolio(n_sma: int, dmap: dict) -> pd.DataFrame:
        a_list, b_list = [], []
        for code, tk in cot.MARKETS.items():
            px = prices[tk]
            dl = dmap[code].reindex(px.index)
            pa, pb = strategies(px, dl, n_sma)
            r = rets[code].reindex(px.index)
            a_list.append(pnl(pa, r).rename(code))
            b_list.append(pnl(pb, r).rename(code))
        A = pd.concat(a_list, axis=1).loc[cot.START:].mean(axis=1)
        B = pd.concat(b_list, axis=1).loc[cot.START:].mean(axis=1)
        return pd.DataFrame({"A": A, "B": B}).dropna()

    dmap = {code: daily_delta(dws[code], prices[tk].index, 6) for code, tk in cot.MARKETS.items()}

    def summarize(P: pd.DataFrame) -> dict:
        d = (P["B"] - P["A"]).to_numpy()
        return {"periode": f"{P.index.min().date()} / {P.index.max().date()}", "n_jours": int(len(P)),
                "diff_moyenne_annualisee_pct": float(d.mean() * 252 * 100), "t_nw_diff": nw_t(d),
                "sharpe_net_A": sharpe(P["A"]), "sharpe_net_B": sharpe(P["B"]),
                "rendement_annualise_A_pct": float(P["A"].mean() * 252 * 100),
                "rendement_annualise_B_pct": float(P["B"].mean() * 252 * 100)}

    main = portfolio(SMA_MAIN, dmap)
    res = {"principal_sma50": summarize(main),
           "moitie_2000_2012": summarize(main[main.index < HALF]),
           "moitie_2013_fin": summarize(main[main.index >= HALF]),
           **{f"sma{n}": summarize(portfolio(n, dmap)) for n in SMA_ALT}}
    if not zero_jumps:
        rng = np.random.default_rng(31)
        m0 = float((main["B"] - main["A"]).mean())
        perm = np.empty(N_PLACEBO)
        for b in range(N_PLACEBO):
            pm = {}
            for code, tk in cot.MARKETS.items():
                dw = dws[code].copy()
                v = dw["delta"].to_numpy()
                blocks = [v[i:i + PLACEBO_BLOCK] for i in range(0, len(v), PLACEBO_BLOCK)]
                dw["delta"] = np.concatenate([blocks[j] for j in rng.permutation(len(blocks))])
                pm[code] = daily_delta(dw, prices[tk].index, 6)
            P = portfolio(SMA_MAIN, pm)
            perm[b] = float((P["B"] - P["A"]).mean())
        res["placebo"] = {"diff_observee_quotidienne": m0, "moyenne_placebo": float(perm.mean()),
                          "p_bilateral": float((np.abs(perm - perm.mean()) >= abs(m0 - perm.mean())).mean()),
                          "n_tirages": N_PLACEBO}
        # diagnostic look-ahead : maïs 2015-03 -> 2025-03, donnée datée mercredi vs publication
        px = prices[cot.MARKETS[CORN]]
        r = rets[CORN].reindex(px.index)
        diag = {}
        for label, lag in [("date_publication_R15", 6), ("antidate_mercredi_comme_V003", 1)]:
            dl = daily_delta(dws[CORN], px.index, lag).reindex(px.index)
            pa, pb = strategies(px, dl, SMA_MAIN)
            ra, rb = pnl(pa, r).loc["2015-03-01":"2025-03-31"], pnl(pb, r).loc["2015-03-01":"2025-03-31"]
            diag[label] = {"rendement_annualise_B_pct": float(rb.mean() * 252 * 100), "sharpe_B": sharpe(rb),
                           "rendement_annualise_A_pct": float(ra.mean() * 252 * 100), "sharpe_A": sharpe(ra),
                           "nb_changements_position_B": int((pb.loc["2015-03-01":"2025-03-31"].diff().abs() > 0).sum())}
        res["diagnostic_lookahead_mais"] = diag
    return res


def verdict_h031(r: dict) -> str:
    p = r["principal_sma50"]
    cond = (p["diff_moyenne_annualisee_pct"] > 0 and p["t_nw_diff"] >= 2.0
            and r["moitie_2000_2012"]["diff_moyenne_annualisee_pct"] > 0
            and r["moitie_2013_fin"]["diff_moyenne_annualisee_pct"] > 0
            and all(r[f"sma{n}"]["diff_moyenne_annualisee_pct"] > 0 for n in SMA_ALT)
            and r["placebo"]["p_bilateral"] < 0.05 and p["sharpe_net_B"] > p["sharpe_net_A"])
    if cond:
        return "PROMISING"
    if p["diff_moyenne_annualisee_pct"] < 0 and p["t_nw_diff"] <= -2.0:
        return "REJECTED"
    return "INCONCLUSIVE"


def main() -> dict:
    cotfull = ovl.load_full()
    prices = {tk: cot.load_prices(tk) for tk in cot.MARKETS.values()}
    r029 = h029(cotfull, prices, False)
    r031 = h031(cotfull, prices, False)
    res = {"preenregistrement": "results/H029_H031_preregistration.md",
           "H029": r029, "H031": r031,
           "sensibilite_sauts_neutralises": {"H029": h029(cotfull, prices, True), "H031": h031(cotfull, prices, True)},
           "verdicts_regle_preenregistree": {**verdict_h029(r029), "H031": verdict_h031(r031)}}
    return res


if __name__ == "__main__":
    res = main()
    path = ROOT / "results" / "H029_H031_results.json"
    runs = json.loads(path.read_text(encoding="utf-8")).get("runs", []) if path.exists() else []
    runs.append({"horodatage_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"), "resultat": res})
    path.write_text(json.dumps({"runs": runs}, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(res["verdicts_regle_preenregistree"], indent=1))
