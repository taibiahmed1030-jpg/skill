"""Source de données unique et interchangeable pour le moteur de backtest.

Aujourd'hui : yfinance (gratuit, couvre forex/actions/indices/crypto, pas de
compte requis). Demain, si le marché cible devient Polymarket ou autre chose,
on ajoute un adaptateur ici (même interface : DataFrame avec colonne 'Close'
indexée par date) sans toucher au reste du pipeline.
"""
from __future__ import annotations

import pandas as pd
import yfinance as yf


def load_daily(ticker: str, start: str | None = None, end: str | None = None, period: str | None = None) -> pd.DataFrame:
    """Retourne un DataFrame OHLCV quotidien, colonnes aplaties (yfinance
    renvoie un MultiIndex par défaut dès qu'un seul ticker est demandé avec
    certaines versions -- on normalise ici pour que le reste du code n'ait
    jamais à s'en soucier)."""
    kwargs = {"progress": False, "auto_adjust": True}
    if period:
        df = yf.download(ticker, period=period, interval="1d", **kwargs)
    else:
        df = yf.download(ticker, start=start, end=end, interval="1d", **kwargs)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    df = df.dropna(how="all")
    return df
