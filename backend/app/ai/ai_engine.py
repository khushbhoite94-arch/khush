"""
AEGIS AI v3
Main analysis and paper-trading orchestration.

The engine is deliberately fail-closed: invalid data, conflicting signals,
or analysis errors produce WAIT rather than an executable direction.
"""

from __future__ import annotations

from datetime import datetime
from math import isfinite
from numbers import Real

from app.analytics.smart_money_engine import SmartMoneyEngine
from app.analytics.statistics import Statistics
from app.ai.decision_engine import DecisionEngine
from app.ai.confidence import Confidence
from app.strategy.startegy_engine import StrategyEngine
from app.risk.risk_manager import RiskManager
from app.execution.paper_executor import PaperExecutor


class AIEngine:
    def __init__(self, starting_balance: float = 10000.0):
        self.smart_money = SmartMoneyEngine()
        self.statistics_engine = Statistics()
        self.decision_engine = DecisionEngine()
        self.confidence_engine = Confidence()
        self.strategy_engine = StrategyEngine()
        self.risk_manager = RiskManager()
        self.paper_executor = PaperExecutor(starting_balance=starting_balance)

        self.started = datetime.utcnow()
        self.version_number = "3.1"
        self.total_predictions = 0
        self.total_trades = 0
        self.last_report = None
        self.last_decision = None
        self.last_strategy = None
        self.last_candles = None
        self.last_error = None

    def reset(self):
        self.paper_executor.reset()
        self.risk_manager.reset_day()
        self.total_predictions = 0
        self.total_trades = 0
        self.last_report = None
        self.last_decision = None
        self.last_strategy = None
        self.last_candles = None
        self.last_error = None

    def health(self):
        return {
            "status": "RUNNING",
            "version": self.version_number,
            "started": self.started.isoformat(),
            "predictions": self.total_predictions,
            "trades": self.total_trades,
            "execution_mode": "PAPER_ONLY",
            "last_error": self.last_error,
        }

    @staticmethod
    def validate(candles):
        if not isinstance(candles, (list, tuple)) or len(candles) < 50:
            return False

        required = ("open", "high", "low", "close")
        for candle in candles:
            if not isinstance(candle, dict):
                return False
            values = [candle.get(key) for key in required]
            if any(not isinstance(value, Real) or not isfinite(float(value)) for value in values):
                return False
            open_price, high, low, close = map(float, values)
            if low <= 0 or high < low or high < max(open_price, close) or low > min(open_price, close):
                return False
        return True

    def process(self, candles):
        if not self.validate(candles):
            self.last_error = "Invalid candles: expected at least 50 valid OHLC records"
            decision = {"action": "WAIT", "reason": self.last_error}
            self.last_decision = decision
            return {"decision": decision, "action": "WAIT", "reason": self.last_error}

        try:
            closes = [float(candle["close"]) for candle in candles]
            report = self.smart_money.analyze(candles)
            strategy = self.strategy_engine.calculate(closes, candles)
            trend_decision = self.decision_engine.decide(candles)

            strategy_signal = strategy.get("signal", "WAIT")
            smart_money_signal = report.get("direction", "WAIT")
            decision_signal = trend_decision.get("action", "WAIT")

            # Require agreement across independently produced strategy and
            # smart-money directions, plus the decision engine's trade gate.
            signals = (strategy_signal, smart_money_signal, decision_signal)
            if not all(signal in ("BUY", "SELL") for signal in signals) or len(set(signals)) != 1:
                decision = {
                    "action": "WAIT",
                    "reason": "NO_AGREEMENT",
                    "strategy_signal": strategy_signal,
                    "smart_money_signal": smart_money_signal,
                    "analysis_signal": decision_signal,
                }
            else:
                decision = trend_decision

            # Confidence is calculated from the actual strategy and
            # smart-money outputs. Never feed the final decision back as a vote.
            confidence = self.confidence_engine.calculate([
                {
                    "engine": "smart_money",
                    "signal": smart_money_signal,
                    "confidence": report.get("confidence", 0),
                },
                {
                    "engine": "strategy",
                    "signal": strategy_signal,
                    "confidence": strategy.get("confidence", 0),
                },
            ])
            if decision.get("action") == "WAIT":
                confidence["signal"] = "WAIT"

            self.last_report = report
            self.last_strategy = strategy
            self.last_decision = decision
            self.last_candles = list(candles)
            self.last_error = None
            self.total_predictions += 1

            return {
                "time": datetime.utcnow().isoformat(),
                "action": decision.get("action", "WAIT"),
                "report": report,
                "strategy": strategy,
                "decision": decision,
                "confidence": confidence,
                "statistics": self.statistics_engine.analyze(candles),
            }
        except Exception as exc:
            self.last_error = f"{type(exc).__name__}: {exc}"
            decision = {"action": "WAIT", "reason": "ANALYSIS_ERROR"}
            self.last_decision = decision
            return {"action": "WAIT", "decision": decision, "reason": "ANALYSIS_ERROR"}

    def last_analysis(self):
        return self.last_report

    def last_trade(self):
        return self.last_decision

    def paper_trade(
        self,
        trade,
        current_positions=None,
        daily_loss=None,
        peak_balance=None,
    ):
        if not isinstance(trade, dict):
            return {"status": "REJECTED", "reason": "Trade must be a dictionary"}

        direction = trade.get("direction")
        if direction not in ("BUY", "SELL"):
            return {"status": "REJECTED", "reason": "Invalid direction"}

        try:
            balance = self.paper_executor.get_balance()
            open_count = len(self.paper_executor.get_open_positions())
            evaluation = self.risk_manager.evaluate(
                balance=balance,
                entry=float(trade["entry"]),
                stop_loss=float(trade["stop_loss"]),
                side=direction,
                open_positions=open_count,
            )
            if not evaluation.get("allowed") or evaluation.get("lot_size", 0) <= 0:
                return {"status": "REJECTED", "reason": evaluation.get("reason", "Risk check failed")}

            symbol = str(trade.get("symbol", "UNKNOWN"))
            target = float(trade.get("take_profit", evaluation["take_profit"]))
            args = (
                symbol,
                evaluation["lot_size"],
                float(trade["entry"]),
                float(trade["stop_loss"]),
                target,
            )
            opened = self.paper_executor.buy(*args) if direction == "BUY" else self.paper_executor.sell(*args)
            self.total_trades += 1
            return {"status": "OPENED", "trade": opened, "risk": evaluation}
        except (KeyError, TypeError, ValueError) as exc:
            return {"status": "REJECTED", "reason": str(exc)}

    def close_trade(self, trade, price):
        trade_id = trade.get("id") if isinstance(trade, dict) else trade
        try:
            return self.paper_executor.close_trade(trade_id, float(price))
        except (TypeError, ValueError):
            return None

    def update(self, price):
        try:
            return self.paper_executor.update(float(price))
        except (TypeError, ValueError):
            return []

    def statistics(self):
        return {
            "predictions": self.total_predictions,
            "trades_opened": self.total_trades,
            "paper_execution": self.paper_executor.statistics(),
        }

    def dashboard(self):
        return {
            "health": self.health(),
            "statistics": self.statistics(),
            "market_statistics": (
                self.statistics_engine.analyze(self.last_candles)
                if self.last_candles else None
            ),
            "last_report": self.last_report,
            "last_strategy": self.last_strategy,
            "last_decision": self.last_decision,
        }
