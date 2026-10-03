"""Tests de H014 (diversification HML/UMD 60/40) et H015 (momentum temporel
sur facteurs) sur la bibliothèque publique de Kenneth French.

Protocole figé dans results/H014_H015_preregistration.md (commité avant le
chargement des données). Facteurs bruts non investissables : propriétés de
séries, pas stratégies exploitables.
"""
from __future__ import annotations

import io
import json
import math
import re
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".cache" / "french"
BASE = "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/"
FILES = {"ff3": "F-F_Research_Data_Factors_CSV.zip", "mom": "F-F_Momentum_Factor_CSV.zip",
         "ff5": "F-F_Research_Data_5_Factors_2x3_CSV.zip", "st": "F-F_ST_Reversal_Factor_CSV.zip",
         "lt": "F-F_LT_Reversal_Factor_CSV.zip"}


def fetch(name: str) -> str:
    CACHE.mkdir(parents=True, exist_ok=True)
    p = CACHE / name
    if not p.exists():
        req = urllib.request.Request(BASE + name, headers={"User-Agent": "Mozilla/5.0"})
        p.write_bytes(urllib.request.urlopen(req, timeout=120).read())
    z = zipfile.ZipFile(io.BytesIO(p.read_bytes()))
    return z.read(z.namelist()[0]).decode("latin-1")


def parse_monthly(text: str) -> pd.DataFrame:
    """Premier bloc de lignes « YYYYMM, ... » (section mensuelle) avec son en-tête."""
    lines = text.splitlines()
    rows, header = [], None
    for i, ln in enumerate(lines):
        if re.match(r"^\s*\d{6}\s*,", ln):
            if header is None:
                header = [h.strip() for h in lines[i - 1].split(",")]
            rows.append([x.strip() for x in ln.split(",")])
        elif rows:
            break
    df = pd.DataFrame(rows, columns=["date"] + header[1:])
    df["date"] = pd.PeriodIndex(df["date"].str[:4] + "-" + df["date"].str[4:], freq="M")
    df = df.set_index("date").apply(pd.to_numeric, errors="coerce")
    return df.replace([-99.99, -999], np.nan)


def load() -> pd.DataFrame:
    ff3 = parse_monthly(fetch(FILES["ff3"]))
    mom = parse_monthly(fetch(FILES["mom"]))
    ff5 = parse_monthly(fetch(FILES["ff5"]))
    st = parse_monthly(fetch(FILES["st"]))
    lt = parse_monthly(fetch(FILES["lt"]))
    df = pd.DataFrame({"HML_3f": ff3["HML"], "Mom": mom.iloc[:, 0]})
    for c in ["Mkt-RF", "SMB", "HML", "RMW", "CMA"]:
        df[c] = ff5[c]
    df["ST_Rev"] = st.iloc[:, 0]
    df["LT_Rev"] = lt.iloc[:, 0]
    return df


def max_dd(r: pd.Series) -> float:
    eq = (1 + r / 100).cumprod()
    return float((eq / eq.cummax() - 1).min())


def sharpe(r: np.ndarray) -> float:
    return float(r.mean() / r.std(ddof=1) * math.sqrt(12))


def block_boot_sharpe_diff(a: np.ndarray, b: np.ndarray, seed: int, n: int = 5000, block: int = 12) -> dict:
    rng = np.random.default_rng(seed)
    T = len(a)
    d0 = sharpe(a) - sharpe(b)
    diffs = np.empty(n)
    nb = int(math.ceil(T / block))
    for i in range(n):
        starts = rng.integers(0, T - block + 1, nb)
        idx = np.concatenate([np.arange(s, s + block) for s in starts])[:T]
        diffs[i] = sharpe(a[idx]) - sharpe(b[idx])
    return {"diff_sharpe": d0, "p_unilateral_diff_positive": float((diffs <= 0).mean()),
            "p_unilateral_diff_negative": float((diffs >= 0).mean())}


def h014(df: pd.DataFrame) -> dict:
    d = df[["HML_3f", "Mom"]].dropna().rename(columns={"HML_3f": "HML", "Mom": "UMD"})
    d["C"] = 0.6 * d["HML"] + 0.4 * d["UMD"]

    def block(x: pd.DataFrame) -> dict:
        return {"periode": f"{x.index.min()} / {x.index.max()}", "n_mois": int(len(x)),
                **{f"dd_{k}": max_dd(x[k]) for k in ["HML", "UMD", "C"]},
                **{f"sharpe_{k}": sharpe(x[k].to_numpy()) for k in ["HML", "UMD", "C"]}}

    test = d.loc["2014-01":]
    res = {"replication_1927_2013": block(d.loc[:"2013-12"]), "test_2014_fin": block(test),
           "bootstrap_C_vs_HML": block_boot_sharpe_diff(test["C"].to_numpy(), test["HML"].to_numpy(), 14),
           "bootstrap_C_vs_UMD": block_boot_sharpe_diff(test["C"].to_numpy(), test["UMD"].to_numpy(), 141)}
    t = res["test_2014_fin"]
    dd_ratio = t["dd_C"] / t["dd_UMD"] if t["dd_UMD"] != 0 else float("nan")
    res["ratio_dd_C_sur_UMD"] = dd_ratio
    bh, bu = res["bootstrap_C_vs_HML"], res["bootstrap_C_vs_UMD"]
    if dd_ratio <= 0.5 and bh["diff_sharpe"] > 0 and bh["p_unilateral_diff_positive"] < 0.05 \
            and bu["diff_sharpe"] > 0 and bu["p_unilateral_diff_positive"] < 0.05:
        v = "PROMISING"
    elif dd_ratio > 0.8 or (bh["diff_sharpe"] < 0 and bh["p_unilateral_diff_negative"] < 0.05) \
            or (bu["diff_sharpe"] < 0 and bu["p_unilateral_diff_negative"] < 0.05):
        v = "REJECTED"
    else:
        v = "INCONCLUSIVE"
    res["verdict_regle_preenregistree"] = v
    return res


def nw_t_mean(x: np.ndarray, lags: int = 3) -> float:
    e = x - x.mean()
    T = len(x)
    s = e @ e / T
    for L in range(1, lags + 1):
        s += 2 * (1 - L / (lags + 1)) * (e[L:] @ e[:-L]) / T
    return float(x.mean() / math.sqrt(s / T))


def h015(df: pd.DataFrame) -> dict:
    facs = ["Mkt-RF", "SMB", "HML", "RMW", "CMA", "Mom", "ST_Rev", "LT_Rev"]
    F = df[facs]
    sig = np.sign(F.rolling(12, min_periods=12).sum().shift(1))
    strat = (sig * F).mean(axis=1, skipna=True).where(sig.notna().any(axis=1))
    passive = F.where(sig.notna()).mean(axis=1, skipna=True).where(sig.notna().any(axis=1))
    out = pd.DataFrame({"strat": strat, "passif": passive}).dropna()

    def stats(x: pd.DataFrame) -> dict:
        return {"periode": f"{x.index.min()} / {x.index.max()}", "n_mois": int(len(x)),
                "moyenne_mensuelle_pct": float(x["strat"].mean()), "t_nw": nw_t_mean(x["strat"].to_numpy()),
                "moyenne_passif_pct": float(x["passif"].mean()),
                "t_nw_strat_moins_passif": nw_t_mean((x["strat"] - x["passif"]).to_numpy())}

    test = out.loc["2016-01":]
    # permutation par blocs des signaux sur la période de test
    rng = np.random.default_rng(15)
    S = sig.loc[test.index].to_numpy()
    R = F.loc[test.index].to_numpy()
    m0 = float(np.nanmean(np.nanmean(S * R, axis=1)))
    blocks = [np.arange(i, min(i + 12, len(S))) for i in range(0, len(S), 12)]
    perm = np.empty(5000)
    for b in range(5000):
        order = np.concatenate([blocks[j] for j in rng.permutation(len(blocks))])
        perm[b] = np.nanmean(np.nanmean(S[order] * R, axis=1))
    res = {"controle_debut_2015": stats(out.loc[:"2015-12"]), "test_2016_fin": stats(test),
           "test_2016_2020": stats(out.loc["2016-01":"2020-12"]), "test_2021_fin": stats(out.loc["2021-01":]),
           "permutation": {"moyenne_observee": m0,
                           "p_bilateral": float((np.abs(perm - perm.mean()) >= abs(m0 - perm.mean())).mean())},
           "partie_sentiment": "non testée : indice Baker-Wurgler public arrêté fin 2018"}
    t = res["test_2016_fin"]
    halves = res["test_2016_2020"]["moyenne_mensuelle_pct"] > 0 and res["test_2021_fin"]["moyenne_mensuelle_pct"] > 0
    if t["moyenne_mensuelle_pct"] > 0 and t["t_nw"] >= 1.96 and res["permutation"]["p_bilateral"] < 0.05 and halves:
        v = "PROMISING"
    elif t["moyenne_mensuelle_pct"] < 0 and t["t_nw"] <= -1.96:
        v = "REJECTED"
    else:
        v = "INCONCLUSIVE"
    res["verdict_regle_preenregistree"] = v
    return res


if __name__ == "__main__":
    df = load()
    res = {"donnees": {"premier_mois": str(df.index.min()), "dernier_mois": str(df.dropna(how="all").index.max())},
           "H014": h014(df), "H015": h015(df)}
    path = ROOT / "results" / "H014_H015_results.json"
    runs = json.loads(path.read_text(encoding="utf-8")).get("runs", []) if path.exists() else []
    runs.append({"horodatage_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"), "resultat": res})
    path.write_text(json.dumps({"runs": runs}, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(res, indent=1, ensure_ascii=False))
