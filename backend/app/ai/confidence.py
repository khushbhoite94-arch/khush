"""
AEGIS AI v3
Institutional Confidence Engine

Aggregates signals from every engine and produces one
institutional-quality decision.

Features
--------
✓ Weighted voting
✓ Agreement calculation
✓ BUY / SELL dominance
✓ WAIT handling
✓ Confidence normalization
✓ Dashboard statistics
✓ Extensible
"""

from __future__ import annotations


class Confidence:

    def __init__(self):

        self.weights = {
            "smart_money": 35,
            "trend": 20,
            "momentum": 15,
            "volume": 10,
            "volatility": 5,
            "candlestick": 5,
            "ml": 10,
        }

        self.minimum_agreement = 60

    # =====================================================
    # WEIGHT
    # =====================================================

    def weight(self, engine):

        return self.weights.get(engine, 10)

    # =====================================================
    # CALCULATE
    # =====================================================

    def calculate(self, results):

        buy_score = 0.0
        sell_score = 0.0

        buy_votes = 0
        sell_votes = 0
        wait_votes = 0

        total_weight = 0

        for result in results:

            signal = result.get("signal", "WAIT").upper()

            confidence = float(
                result.get("confidence", 0)
            )

            engine = result.get(
                "engine",
                "unknown",
            )

            weight = self.weight(engine)

            total_weight += weight

            score = confidence * weight

            if signal == "BUY":

                buy_score += score
                buy_votes += 1

            elif signal == "SELL":

                sell_score += score
                sell_votes += 1

            else:

                wait_votes += 1

        if buy_score == 0 and sell_score == 0:

            return {
                "signal": "WAIT",
                "confidence": 0,
                "agreement": 0,
                "buy_votes": buy_votes,
                "sell_votes": sell_votes,
                "wait_votes": wait_votes,
            }

        total_score = buy_score + sell_score

        if buy_score > sell_score:

            signal = "BUY"
            confidence = buy_score / total_weight

            agreement = (
                buy_score / total_score
            ) * 100

        else:

            signal = "SELL"
            confidence = sell_score / total_weight

            agreement = (
                sell_score / total_score
            ) * 100

        if agreement < self.minimum_agreement:

            signal = "WAIT"

        return {

            "signal": signal,

            "confidence": round(
                confidence,
                2,
            ),

            "agreement": round(
                agreement,
                2,
            ),

            "buy_votes": buy_votes,

            "sell_votes": sell_votes,

            "wait_votes": wait_votes,

            "buy_score": round(
                buy_score,
                2,
            ),

            "sell_score": round(
                sell_score,
                2,
            ),
        }