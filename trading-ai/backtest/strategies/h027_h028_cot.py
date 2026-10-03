"""Test conjoint de H027 (extrêmes des commerciaux = retournement) et H028
(suivre les non-commerciaux), hypothèses contradictoires liées.

Protocole figé dans results/H027_H028_preregistration.md (commité avant le
chargement des prix). Données : rapports COT Legacy futures-only de la CFTC
(téléchargés et mis en cache localement, hors dépôt) et clôtures Yahoo `=F`.
"""
from __future__ import annotations

import io
import json
import math
import sys
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import yfinance as yf

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".cache" / "cot"
MARKETS = {  # code CFTC -> ticker Yahoo
    "002602": "ZC=F", "005602": "ZS=F", "001602": "ZW=F", "057642": "LE=F",
    "067651": "CL=F", "023651": "NG=F", "088691": "GC=F", "084691": "SI=F",
    "085692": "HG=F", "13874A": "ES=F", "043602": "ZN=F", "099741": "6E=F",
    "097741": "6J=F", "080732": "SB=F", "083731": "KC=F",
}
EXCLUDED = [("2013-09-24", "2013-11-05"), ("2018-12-18", "2019-03-05"), ("2025-09-23", "2026-01-31")]
START = pd.Timestamp("2000-01-01")
HALF_SPLIT = pd.Timestamp("2013-01-01")
HORIZONS = [4, 8, 13]
MAIN_H = 8
WINDOW = 52
INDEP = 8
N_PERM = 5000
SEED = 27
COST_SIDE = 0.0005
JUMP_MULT = 8
URLS = ["https://www.cftc.gov/files/dea/history/deacot1986_2016.zip"] + [
    f"https://www.cftc.gov/files/dea/history/deacot{y}.zip" for y in range(2017, 2027)]


def fetch(url: str) -> bytes:
    CACHE.mkdir(parents=True, exist_ok=True)
    p = CACHE / url.rsplit("/", 1)[1]
    if not p.exists():
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        p.write_bytes(urllib.request.urlopen(req, timeout=120).read())
    return p.read_bytes()


def load_cot() -> pd.DataFrame:
    frames = []
    for u in URLS:
        z = zipfile.ZipFile(io.BytesIO(fetch(u)))
        frames.append(pd.read_csv(z.open(z.namelist()[0]), low_memory=False))
    df = pd.concat(frames, ignore_index=True)
    df["code"] = df["CFTC Contract Market Code"].astype(str).str.strip()
    df = df[df["code"].isin(MARKETS)]
    out = pd.DataFrame({
        "code": df["code"],
        "asof": pd.to_datetime(df["As of Date in Form YYYY-MM-DD"]),
        "net_c": df["Commercial Positions-Long (All)"] - df["Commercial Positions-Short (All)"],
        "net_nc": df["Noncommercial Positions-Long (All)"] - df["Noncommercial Positions-Short (All)"],
    })
    return out.drop_duplicates(["code", "asof"], keep="last").sort_values(["code", "asof"])


def load_prices(ticker: str) -> pd.Series:
    df = yf.download(ticker, start="1999-01-01", interval="1d", auto_adjust=False, progress=False)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    s = df["Close"].dropna()
    s.index = pd.to_datetime(s.index).tz_localize(None)
    return s[s.index < pd.Timestamp.today().normalize()]


def log_index(px: pd.Series, zero_jumps: bool) -> tuple[pd.Series, int]:
    r = np.log(px / px.shift(1)).fillna(0.0)
    n_jumps = 0
    if zero_jumps:
        med = r.abs().rolling(60, min_periods=20).median().shift(1)
        jump = r.abs() > JUMP_MULT * med
        n_jumps = int(jump.sum())
        r = r.where(~jump, 0.0)
    return r.cumsum(), n_jumps


def excluded(d: pd.Timestamp) -> bool:
    return any(pd.Timestamp(a) <= d <= pd.Timestamp(b) for a, b in EXCLUDED)


def market_frame(cot: pd.DataFrame, px: pd.Series, zero_jumps: bool) -> tuple[pd.DataFrame, int]:
    li, nj = log_index(px, zero_jumps)
    dates = li.index
    c = cot.copy().reset_index(drop=True)
    c["min52"] = c["net_c"].shift(1).rolling(WINDOW - 1).min()
    c["max52"] = c["net_c"].shift(1).rolling(WINDOW - 1).max()
    c["is_min"] = c["net_c"] <= c["min52"]
    c["is_max"] = c["net_c"] >= c["max52"]

    def trade_idx(d: pd.Timestamp) -> int | None:
        i = dates.searchsorted(d)
        return int(i) if i < len(dates) else None

    entries = [trade_idx(a + pd.Timedelta(days=6)) for a in c["asof"]]
    c["entry_i"] = entries
    for h in HORIZONS:
        vals = []
        for i in entries:
            if i is None:
                vals.append(np.nan); continue
            j = trade_idx(dates[i] + pd.Timedelta(days=7 * h))
            vals.append(li.iloc[j] - li.iloc[i] if j is not None else np.nan)
        c[f"r{h}"] = vals
    # rendement d'une entrée à la suivante (test B)
    nxt = entries[1:] + [None]
    c["r_next"] = [li.iloc[j] - li.iloc[i] if (i is not None and j is not None) else np.nan
                   for i, j in zip(entries, nxt)]
    # momentum 52 semaines à l'entrée
    mom = []
    for i in entries:
        if i is None:
            mom.append(np.nan); continue
        k = dates.searchsorted(dates[i] - pd.Timedelta(days=364), side="right") - 1
        mom.append(np.sign(li.iloc[i] - li.iloc[k]) if k >= 0 else np.nan)
    c["mom"] = mom
    c["ok"] = (c["asof"] >= START) & ~c["asof"].apply(excluded) & c["entry_i"].notna()
    return c, nj


def mark_events(c: pd.DataFrame) -> pd.DataFrame:
    """Événement compté seulement si aucun événement compté du même côté
    dans les INDEP rapports précédents."""
    s = np.zeros(len(c))
    last_min = last_max = -10**9
    is_min, is_max = c["is_min"].to_numpy(), c["is_max"].to_numpy()
    for k in range(len(c)):
        if is_min[k] and k - last_min > INDEP:
            s[k] = -1
            last_min = k
        if is_max[k] and k - last_max > INDEP and s[k] == 0:
            s[k] = 1
            last_max = k
    c = c.copy()
    c["s"] = s
    return c


def nw_t(y: np.ndarray, X: np.ndarray, lags: int = 4):
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
    return beta, beta / np.sqrt(np.diag(V))


def p_two(t: float) -> float:
    return math.erfc(abs(t) / math.sqrt(2))


def test_a(frames: dict[str, pd.DataFrame], h: int) -> dict:
    rng = np.random.default_rng(SEED)
    obs, per_market, halves = [], {}, {"2000_2012": [], "2013_fin": []}
    pools = {}
    for code, c in frames.items():
        e = c[c["ok"] & c[f"r{h}"].notna()].copy()
        e["rd"] = e[f"r{h}"] - e[f"r{h}"].mean()
        ev = e[e["s"] != 0]
        vals = (ev["s"] * ev["rd"]).to_numpy()
        obs.extend(vals)
        for _, row in ev.iterrows():
            halves["2000_2012" if row["asof"] < HALF_SPLIT else "2013_fin"].append(row["s"] * row["rd"])
        per_market[MARKETS[code]] = {"n_min": int((ev["s"] == -1).sum()), "n_max": int((ev["s"] == 1).sum()),
                                     "moyenne_s_r": float(vals.mean()) if len(vals) else None}
        pools[code] = (e["rd"].to_numpy(), int((ev["s"] == -1).sum()), int((ev["s"] == 1).sum()))
    m0 = float(np.mean(obs))
    perm = np.empty(N_PERM)
    for b in range(N_PERM):
        tot = []
        for rd, nmin, nmax in pools.values():
            idx = rng.choice(len(rd), size=nmin + nmax, replace=False)
            sig = np.array([-1] * nmin + [1] * nmax)
            tot.append(sig * rd[idx])
        perm[b] = np.concatenate(tot).mean()
    return {"h_semaines": h, "n_evenements": len(obs), "moyenne_s_r": m0,
            "p_permutation_bilateral": float((np.abs(perm - perm.mean()) >= abs(m0 - perm.mean())).mean()),
            "moitie": {k: {"n": len(v), "moyenne": float(np.mean(v)) if v else None} for k, v in halves.items()},
            "par_marche": per_market}


def test_b(frames: dict[str, pd.DataFrame]) -> dict:
    rows = []
    for code, c in frames.items():
        e = c[c["ok"] & c["r_next"].notna() & c["mom"].notna()].copy()
        e["rd"] = e["r_next"] - e["r_next"].mean()
        e["pos"] = np.sign(e["net_nc"])
        e["flip"] = (e["pos"] != e["pos"].shift(1)).astype(float)
        e.loc[e.index[0], "flip"] = 0.0
        rows.append(pd.DataFrame({"asof": e["asof"], "P": e["pos"] * e["rd"], "M": e["mom"] * e["rd"],
                                  "cost": e["flip"] * 2 * COST_SIDE}))
    allr = pd.concat(rows).groupby("asof").mean().sort_index()
    allr["P_net"] = allr["P"] - allr["cost"]

    def stats(df: pd.DataFrame) -> dict:
        n = len(df)
        _, tP = nw_t(df["P_net"].to_numpy(), np.ones((n, 1)))
        beta, t = nw_t(df["P_net"].to_numpy(), np.column_stack([np.ones(n), df["M"].to_numpy()]))
        return {"n_semaines": n, "moyenne_brute": float(df["P"].mean()), "moyenne_nette": float(df["P_net"].mean()),
                "t_moyenne_nette": float(tP[0]), "alpha": float(beta[0]), "t_alpha": float(t[0]),
                "p_alpha": p_two(float(t[0])), "beta_momentum": float(beta[1]),
                "correlation_P_M": float(np.corrcoef(df["P"], df["M"])[0, 1])}

    return {"total": stats(allr), "2000_2012": stats(allr[allr.index < HALF_SPLIT]),
            "2013_fin": stats(allr[allr.index >= HALF_SPLIT])}


def run(zero_jumps: bool, cot: pd.DataFrame, prices: dict) -> dict:
    frames, jumps = {}, {}
    for code, tk in MARKETS.items():
        c, nj = market_frame(cot[cot["code"] == code], prices[tk], zero_jumps)
        frames[code] = mark_events(c)
        jumps[tk] = nj
    return {"sauts_neutralises": jumps if zero_jumps else None,
            "test_A": {f"h={h}": test_a(frames, h) for h in HORIZONS},
            "test_B": test_b(frames)}


def holm(pa: float, pb: float) -> tuple[float, float]:
    ps = sorted([("A", pa), ("B", pb)], key=lambda x: x[1])
    adj1 = min(1.0, 2 * ps[0][1])
    adj2 = max(adj1, ps[1][1])
    d = {ps[0][0]: adj1, ps[1][0]: adj2}
    return d["A"], d["B"]


def verdicts(main: dict) -> dict:
    A = main["test_A"][f"h={MAIN_H}"]
    B = main["test_B"]
    pa, pb = holm(A["p_permutation_bilateral"], B["total"]["p_alpha"])
    halves_pos = all((v["moyenne"] or 0) > 0 for v in A["moitie"].values())
    if A["moyenne_s_r"] > 0 and pa < 0.05 and halves_pos:
        v27 = "PROMISING"
    elif A["moyenne_s_r"] < 0 and pa < 0.05:
        v27 = "REJECTED"
    else:
        v27 = "INCONCLUSIVE"
    Bt = B["total"]
    alpha_halves = B["2000_2012"]["alpha"] > 0 and B["2013_fin"]["alpha"] > 0
    if Bt["moyenne_nette"] > 0 and Bt["t_moyenne_nette"] >= 1.96 and Bt["alpha"] > 0 and pb < 0.05 and alpha_halves:
        v28 = "PROMISING"
    elif (Bt["moyenne_nette"] < 0 and Bt["t_moyenne_nette"] <= -1.96) or (
            A["moyenne_s_r"] > 0 and pa < 0.05 and abs(Bt["t_moyenne_nette"]) < 1.96):
        v28 = "REJECTED"
    else:
        v28 = "INCONCLUSIVE"
    return {"p_A_holm": pa, "p_B_alpha_holm": pb, "H027": v27, "H028": v28}


def main() -> dict:
    cot = load_cot()
    prices = {tk: load_prices(tk) for tk in MARKETS.values()}
    principal = run(False, cot, prices)
    out = {"hypotheses": ["H027", "H028"], "preenregistrement": "results/H027_H028_preregistration.md",
           "donnees": {tk: f"{s.index.min().date()} / {s.index.max().date()}" for tk, s in prices.items()},
           "principal": principal,
           "sensibilite_sauts_neutralises": run(True, cot, prices)}
    out["verdicts_regle_preenregistree"] = verdicts(principal)
    return out


if __name__ == "__main__":
    res = main()
    path = ROOT / "results" / "H027_H028_results.json"
    runs = json.loads(path.read_text(encoding="utf-8")).get("runs", []) if path.exists() else []
    runs.append({"horodatage_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"), "resultat": res})
    path.write_text(json.dumps({"runs": runs}, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(res["verdicts_regle_preenregistree"], indent=1))
