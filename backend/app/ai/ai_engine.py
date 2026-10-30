"""
AEGIS AI v3
Institutional AI Engine
"""

from __future__ import annotations
from datetime import datetime
from app.analytics.smart_money_engine import SmartMoneyEngine
from app.analytics.statistics import Statistics
from app.ai.decision_engine import DecisionEngine
from app.ai.confidence import Confidence
from app.strategy.startegy_engine import StrategyEngine
from app.risk.risk_manager import RiskManager
from app.execution.trade_manager import TradeManager


class AIEngine:

    # =====================================================
    # INIT
    # =====================================================

    def __init__(self):

        self.smart_money = SmartMoneyEngine()

        self.statistics = Statistics()

        self.decision_engine = DecisionEngine()

        self.confidence = Confidence()

        self.startegy_engine = StrategyEngine()

        self.risk_manager = RiskManager()

        self.trade_manager = TradeManager()

        self.started = datetime.utcnow()

        self.total_predictions = 0

        self.total_trades = 0

        self.version_number = "3.0"

        self.last_report = None

        self.last_decision = None
            # =====================================================
    # RESET
    # =====================================================

    def reset(self):

        self.trade_manager.reset()

        self.total_predictions = 0

        self.total_trades = 0

        self.last_report = None

        self.last_decision = None

    # =====================================================
    # HEALTH
    # =====================================================

    def health(self):

        return {

            "status": "RUNNING",

            "version": self.version_number,

            "started": self.started.isoformat(),

            "predictions": self.total_predictions,

            "trades": self.total_trades,

        }

    # =====================================================
    # VALIDATE
    # =====================================================

    def validate(

        self,

        candles,

    ):

        if candles is None:

            return False

        if len(candles) < 30:

            return False

        return True
             # =====================================================
    # PROCESS
    # =====================================================

    def process(

        self,

        candles,

    ):

        if not self.validate(

            candles,

        ):

            return {

                "action": "WAIT",

                "reason": "Not enough candles",

            }

        # ----------------------------------------------

        report = self.smart_money.analyze(

            candles,

        )

        self.last_report = report

        # ----------------------------------------------

        strategy = self.strategy_engine.analyze(

            report,

        )

        # ----------------------------------------------

        decision = self.decision_engine.decide(

            report,

            strategy,

        )

        self.last_decision = decision

        self.total_predictions += 1

        # ----------------------------------------------

        confidence = self.confidence.calculate(

            [

                {

                    "signal": decision["action"],

                    "confidence": report["confidence"],

                }

            ]

        )

        # ----------------------------------------------

        result = {

            "time": datetime.utcnow().isoformat(),

            "report": report,

            "strategy": strategy,

            "decision": decision,

            "confidence": confidence,

            "statistics": self.statistics.summary(),

        }

        return result
        # =====================================================
    # LAST REPORT
    # =====================================================

    def last_analysis(

        self,

    ):

        return self.last_report

    # =====================================================
    # LAST DECISION
    # =====================================================

    def last_trade(

        self,

    ):

        return self.last_decision
        # =====================================================
    # PAPER TRADE
    # =====================================================

    def paper_trade(

        self,

        trade,

        current_positions=0,

        daily_loss=0,

        peak_balance=10000,

    ):

        approved = self.risk_manager.safe_trade(

            trade,

            current_positions,

            daily_loss,

            peak_balance,

        )

        if not approved:

            return {

                "status": "REJECTED",

                "trade": trade,

            }

        opened = self.trade_manager.open_trade(

            trade,

        )

        self.total_trades += 1

        return {

            "status": "OPENED",

            "trade": opened,

        }

    # =====================================================
    # CLOSE TRADE
    # =====================================================

    def close_trade(

        self,

        trade,

        price,

    ):

        closed = self.trade_manager.close_trade(

            trade,

            price,

        )

        return closed

    # =====================================================
    # UPDATE LIVE PRICE
    # =====================================================

    def update(

        self,

        price,

    ):

        return self.trade_manager.update(

            price,

        )
        # =====================================================
    # STATISTICS
    # =====================================================

    def statistics(

        self,

    ):

        return {

            "predictions": self.total_predictions,

            "trades": self.total_trades,

            "performance": self.trade_manager.statistics(),

        }

    # =====================================================
    # DASHBOARD
    # =====================================================

    def dashboard(

        self,

    ):

        return {

            "health": self.health(),

            "statistics": self.statistics.analyze(
            candles,
    ),

            "last_report": self.last_report,

            "last_decision": self.last_decision,

        }