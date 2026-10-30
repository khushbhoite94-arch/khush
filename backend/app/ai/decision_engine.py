"""
AEGIS AI v3
Institutional Decision Engine
"""

from __future__ import annotations

from app.analytics.smart_money_engine import SmartMoneyEngine


class DecisionEngine:

    def __init__(

        self,

        minimum_confidence=70,

    ):

        self.smart_money = SmartMoneyEngine()

        self.minimum_confidence = minimum_confidence

    # =====================================================
    # TREND FILTER
    # =====================================================

    def trend_filter(

        self,

        report,

    ):

        trend = report["market"]["trend"]

        if trend == "UPTREND":

            return "BUY"

        if trend == "DOWNTREND":

            return "SELL"

        return "WAIT"

    # =====================================================
    # CONFIDENCE FILTER
    # =====================================================

    def confidence_filter(

        self,

        report,

    ):

        return (

            report["confidence"]

            >= self.minimum_confidence

        )

    # =====================================================
    # RISK REWARD
    # =====================================================

    def risk_reward(

        self,

        entry,

        stop,

        target,

    ):

        risk = abs(

            entry - stop

        )

        reward = abs(

            target - entry

        )

        if risk <= 0:

            return 0

        return reward / risk

    # =====================================================
    # STOP LOSS
    # =====================================================

    def stop_loss(

        self,

        candles,

        direction,

    ):

        current = candles[-1]

        atr = current.get(

            "atr",

            None,

        )

        if atr is None:

            atr = (

                current["high"]

                - current["low"]

            )

        if direction == "BUY":

            return current["close"] - atr

        return current["close"] + atr

    # =====================================================
    # TAKE PROFIT
    # =====================================================

    def take_profit(

        self,

        candles,

        direction,

    ):

        current = candles[-1]

        atr = current.get(

            "atr",

            None,

        )

        if atr is None:

            atr = (

                current["high"]

                - current["low"]

            )

        if direction == "BUY":

            return current["close"] + atr * 2

        return current["close"] - atr * 2

    # =====================================================
    # EXECUTION PRICE
    # =====================================================

    def entry(

    self,

    candles,

):

     current = candles[-1]

     return round(

        float(

            current["close"]

        ),

        5,

    )
    # =====================================================
    # BUILD TRADE
    # =====================================================

    def build_trade(

        self,

        candles,

        direction,

    ):

        entry = self.entry(candles)

        stop = self.stop_loss(

            candles,

            direction,

        )

        target = self.take_profit(

            candles,

            direction,

        )

        rr = self.risk_reward(

            entry,

            stop,

            target,

        )

        return {

          "direction": direction,

           "entry": round(entry, 5),

           "stop_loss": round(stop, 5),
   
           "take_profit": round(target, 5),

           "risk_reward": round(rr, 2),

            "created_by": "DecisionEngine",

  }
    # =====================================================
    # FINAL DECISION
    # =====================================================

    def decide(

        self,

        candles,

    ):

        report = self.smart_money.analyze(

            candles

        )

        if not self.confidence_filter(report):

            return {

                "action": "WAIT",

                "reason": "LOW_CONFIDENCE",

                "report": report,

            }

        direction = self.trend_filter(

            report

        )

        if direction == "WAIT":

            return {

                "action": "WAIT",

                "reason": "NO_CLEAR_TREND",

                "report": report,

            }

        trade = self.build_trade(

            candles,

            direction,

        )

        return {

            "action": direction,

            "confidence": report["confidence"],

            "trade": trade,

            "report": report,

        }

    # =====================================================
    # READY
    # =====================================================

    def ready(

        self,

        candles,

    ):

        decision = self.decide(

            candles

        )

        return decision.get(

            "action",

            "WAIT",

    ) != "WAIT"

    # =====================================================
    # SUMMARY
    # =====================================================

    def summary(

        self,

        candles,

    ):

        decision = self.decide(

            candles

        )

        return {

            "action": decision["action"],

            "confidence": decision.get(

                "confidence",

                0,

            ),

            "trade": decision.get(

                "trade",

                None,

            ),

        }