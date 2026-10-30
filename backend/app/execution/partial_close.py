"""
AEGIS AI v3
Partial Close Manager
"""

from __future__ import annotations


class PartialClose:

    def __init__(

        self,

        default_percentage=0.50,

    ):

        self.default_percentage = default_percentage

    # =====================================================
    # CAN CLOSE
    # =====================================================

    def can_close(

        self,

        trade,

    ):

        return (

            not trade.get(

                "partial_closed",

                False,

            )

            and

            trade.get(

                "lot_size",

                0,

            ) > 0

        )

    # =====================================================
    # APPLY
    # =====================================================

    def apply(

        self,

        trade,

        percentage=None,

    ):

        if not self.can_close(

            trade,

        ):

            return trade

        if percentage is None:

            percentage = self.default_percentage

        percentage = max(

            0.0,

            min(

                percentage,

                1.0,

            ),

        )

        original = trade.get(

            "lot_size",

            0,

        )

        closed = original * percentage

        remaining = original - closed

        trade["closed_size"] = round(

            closed,

            4,

        )

        trade["lot_size"] = round(

            remaining,

            4,

        )

        trade["partial_closed"] = True

        return trade

    # =====================================================
    # RESET
    # =====================================================

    def reset(

        self,

    ):

        return True