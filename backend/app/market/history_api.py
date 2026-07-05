"""
AEGIS AI
History API
"""

import yfinance as yf


class HistoryAPI:

    def load(

        self,

        symbol="AAPL",

        interval="1m",

        period="5d",

    ):

        df = yf.download(

            symbol,

            interval=interval,

            period=period,

            progress=False,

            auto_adjust=False,

            group_by="column",

            multi_level_index=False,

        )

        if df.empty:
            return []

        candles = []

        for _, row in df.iterrows():

            try:

                candles.append({

                    "open": float(row.Open),

                    "high": float(row.High),

                    "low": float(row.Low),

                    "close": float(row.Close),

                })

            except Exception:

                continue

        return candles