"""
AEGIS AI v3
Master Execution Engine
"""

from __future__ import annotations

from app.execution.paper_executor import PaperExecutor


class ExecutionEngine:

    def __init__(

        self,

        mode="PAPER",

        starting_balance=10000,

    ):

        self.mode = mode.upper()

        if self.mode == "PAPER":

            self.executor = PaperExecutor(

                starting_balance

            )

        else:

            raise NotImplementedError(

                "LIVE executor not implemented yet."

            )

    # =====================================================
    # BUY
    # =====================================================

    def buy(

        self,

        **kwargs,

    ):

        return self.executor.buy(

            **kwargs,

        )

    # =====================================================
    # SELL
    # =====================================================

    def sell(

        self,

        **kwargs,

    ):

        return self.executor.sell(

            **kwargs,

        )

    # =====================================================
    # UPDATE
    # =====================================================

    def update(

        self,

        price,

    ):

        return self.executor.update(

            price,

        )

    # =====================================================
    # CLOSE
    # =====================================================

    def close(

        self,

        trade_id,

        price,

    ):

        return self.executor.close_trade(

            trade_id,

            price,

        )

    # =====================================================
    # BALANCE
    # =====================================================

    @property

    def balance(self):

        return self.executor.get_balance()

    # =====================================================
    # EQUITY
    # =====================================================

    @property

    def equity(self):

        return self.executor.get_equity()

    # =====================================================
    # STATS
    # =====================================================

    def statistics(self):

        return self.executor.statistics()

    # =====================================================
    # RESET
    # =====================================================

    def reset(self):

        self.executor.reset()