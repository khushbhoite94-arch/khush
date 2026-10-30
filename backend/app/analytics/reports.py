"""
AEGIS AI v3
Analytics Reports
"""

from __future__ import annotations

from datetime import datetime

from app.analytics.performance import Performance


class Reports:

    def __init__(self):

        self.performance = Performance()

    # =====================================================
    # BUILD
    # =====================================================

    def build(

        self,

        journal,

    ):

        self.performance.load(

            journal.export()

        )

        return {

            "generated_at": datetime.utcnow(),

            "performance":

                self.performance.report(),

            "journal":

                journal.summary(),

        }

    # =====================================================
    # DAILY
    # =====================================================

    def daily(

        self,

        journal,

    ):

        report = self.build(

            journal,

        )

        report["period"] = "DAILY"

        return report

    # =====================================================
    # WEEKLY
    # =====================================================

    def weekly(

        self,

        journal,

    ):

        report = self.build(

            journal,

        )

        report["period"] = "WEEKLY"

        return report

    # =====================================================
    # MONTHLY
    # =====================================================

    def monthly(

        self,

        journal,

    ):

        report = self.build(

            journal,

        )

        report["period"] = "MONTHLY"

        return report

    # =====================================================
    # SUMMARY
    # =====================================================

    def summary(

        self,

        journal,

    ):

        report = self.build(

            journal,

        )

        perf = report["performance"]

        jour = report["journal"]

        return {

            "generated_at":

                report["generated_at"],

            "total_trades":

                jour["total_trades"],

            "win_rate":

                perf["win_rate"],

            "net_profit":

                perf["net_profit"],

            "profit_factor":

                perf["profit_factor"],

            "expectancy":

                perf["expectancy"],

        }