"""Analyse de chevauchement H029/H031 vs H027/H028 — données COT uniquement.

Exécutée AVANT le pré-enregistrement de H029/H031 et sans aucun prix : elle
mesure à quel point les signaux de H029 (changement de signe des positions
nettes) et de H031 (filtre de variation hebdomadaire des non-commerciaux)
recouvrent ceux déjà testés (H027 extrêmes 52 semaines, H028 signe des
non-commerciaux). Elle ne dit rien des rendements.
"""
from __future__ import annotations

import importlib.util
import io
import json
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("cot", HERE / "h027_h028_cot.py")
cot = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cot)

PERSIST = 4      # le signe précédent doit avoir tenu >= 4 rapports
INDEP = 8        # pas d'événement compté dans les 8 rapports précédents
H = 8            # horizon principal (semaines)
DELTA = 3.0      # seuil H031 (%)


def load_full() -> pd.DataFrame:
    frames = []
    for u in cot.URLS:
        z = zipfile.ZipFile(io.BytesIO(cot.fetch(u)))
        frames.append(pd.read_csv(z.open(z.namelist()[0]), low_memory=False))
    df = pd.concat(frames, ignore_index=True)
    df["code"] = df["CFTC Contract Market Code"].astype(str).str.strip()
    df = df[df["code"].isin(cot.MARKETS)]
    out = pd.DataFrame({
        "code": df["code"], "asof": pd.to_datetime(df["As of Date in Form YYYY-MM-DD"]),
        "net_c": df["Commercial Positions-Long (All)"] - df["Commercial Positions-Short (All)"],
        "nc_long": df["Noncommercial Positions-Long (All)"], "nc_short": df["Noncommercial Positions-Short (All)"],
    })
    out["net_nc"] = out["nc_long"] - out["nc_short"]
    return out.drop_duplicates(["code", "asof"], keep="last").sort_values(["code", "asof"]).reset_index(drop=True)


def flips(net: np.ndarray) -> np.ndarray:
    """+1/-1 au rapport où le signe change (vers le nouveau signe), si le signe
    précédent a tenu PERSIST rapports et sans flip compté dans les INDEP précédents."""
    sg = np.sign(net)
    ev = np.zeros(len(net))
    last = -10**9
    for k in range(PERSIST, len(net)):
        if sg[k] != 0 and sg[k] != sg[k - 1] and np.all(sg[k - PERSIST:k] == sg[k - 1]) and k - last > INDEP:
            ev[k] = sg[k]
            last = k
    return ev


def extremes(net: pd.Series) -> np.ndarray:
    mn = net.shift(1).rolling(51).min()
    mx = net.shift(1).rolling(51).max()
    is_min, is_max = (net <= mn).to_numpy(), (net >= mx).to_numpy()
    s = np.zeros(len(net))
    lm = lx = -10**9
    for k in range(len(net)):
        if is_min[k] and k - lm > INDEP:
            s[k] = -1; lm = k
        if is_max[k] and k - lx > INDEP and s[k] == 0:
            s[k] = 1; lx = k
    return s


def near(ev_a: np.ndarray, ev_b: np.ndarray, w: int, same_sign: bool | None) -> tuple[int, int]:
    idx_a, idx_b = np.flatnonzero(ev_a), np.flatnonzero(ev_b)
    hit = 0
    for i in idx_a:
        j = idx_b[np.abs(idx_b - i) <= w]
        if same_sign is None:
            hit += int(len(j) > 0)
        elif same_sign:
            hit += int(np.any(ev_b[j] == ev_a[i]))
        else:
            hit += int(np.any(ev_b[j] == -ev_a[i]))
    return hit, len(idx_a)


def main() -> dict:
    df = load_full()
    agg = {k: [0, 0] for k in ["nc_flip_vs_h028_meme_position", "c_flip_vs_h028_meme_sens",
                               "c_flip_avec_nc_flip_oppose_2", "c_flip_avec_nc_flip_meme_sens_2",
                               "c_flip_pres_extreme_h027_4", "nc_flip_pres_extreme_h027_4",
                               "h031_signal_meme_sens_que_h028"]}
    per_market, n_weeks_total, cover = {}, 0, 0
    frac_h031_active = []
    for code, g in df.groupby("code"):
        g = g.reset_index(drop=True)
        ok = (g["asof"] >= cot.START) & ~g["asof"].apply(cot.excluded)
        f_nc, f_c = flips(g["net_nc"].to_numpy()), flips(g["net_c"].to_numpy())
        ext = extremes(g["net_c"])
        f_nc[~ok.to_numpy()] = 0; f_c[~ok.to_numpy()] = 0; ext[~ok.to_numpy()] = 0
        sg_nc = np.sign(g["net_nc"].to_numpy())
        # 1. H029-NC : sur les H semaines suivant un flip, la position H028 = nouveau signe ?
        for i in np.flatnonzero(f_nc):
            win = sg_nc[i:i + H]
            agg["nc_flip_vs_h028_meme_position"][0] += int((win == f_nc[i]).sum())
            agg["nc_flip_vs_h028_meme_position"][1] += len(win)
        # part de l'échantillon H028 couverte par les fenêtres H029-NC
        covered = np.zeros(len(g), dtype=bool)
        for i in np.flatnonzero(f_nc):
            covered[i:i + H] = True
        n_weeks_total += int(ok.sum()); cover += int((covered & ok.to_numpy()).sum())
        # 2. H029-C : le sens du flip des commerciaux coïncide-t-il avec la position H028 ?
        for i in np.flatnonzero(f_c):
            agg["c_flip_vs_h028_meme_sens"][0] += int(sg_nc[i] == f_c[i])
            agg["c_flip_vs_h028_meme_sens"][1] += 1
        for key, args in [("c_flip_avec_nc_flip_oppose_2", (f_c, f_nc, 2, False)),
                          ("c_flip_avec_nc_flip_meme_sens_2", (f_c, f_nc, 2, True)),
                          ("c_flip_pres_extreme_h027_4", (f_c, ext, 4, None)),
                          ("nc_flip_pres_extreme_h027_4", (f_nc, ext, 4, None))]:
            h, n = near(*args)
            agg[key][0] += h; agg[key][1] += n
        # 3. H031 : variation hebdomadaire en % du total non commercial
        tot = (g["nc_long"] + g["nc_short"]).replace(0, np.nan)
        d = (g["net_nc"].diff() / tot * 100).to_numpy()
        act = ok.to_numpy() & (np.abs(d) >= DELTA)
        frac_h031_active.append(float(act.sum() / max(ok.sum(), 1)))
        agg["h031_signal_meme_sens_que_h028"][0] += int((np.sign(d[act]) == sg_nc[act]).sum())
        agg["h031_signal_meme_sens_que_h028"][1] += int(act.sum())
        per_market[cot.MARKETS[code]] = {
            "flips_nc": int((f_nc != 0).sum()), "flips_c": int((f_c != 0).sum()),
            "extremes_h027": int((ext != 0).sum()), "semaines": int(ok.sum()),
            "part_semaines_h031_actif": round(frac_h031_active[-1], 3)}
    res = {"parametres": {"persistance": PERSIST, "independance": INDEP, "horizon": H, "seuil_h031_pct": DELTA},
           "indicateurs": {k: {"numerateur": v[0], "denominateur": v[1], "taux": round(v[0] / v[1], 3) if v[1] else None}
                           for k, v in agg.items()},
           "part_echantillon_h028_couverte_par_fenetres_h029_nc": round(cover / n_weeks_total, 3),
           "par_marche": per_market}
    return res


if __name__ == "__main__":
    r = main()
    (HERE.parent / "results" / "H029_H031_overlap.json").write_text(json.dumps(r, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(r, indent=1, ensure_ascii=False))
