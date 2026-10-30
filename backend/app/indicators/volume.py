"""
AEGIS AI v2
Volume Analyzer

Detects volume spikes and confirms
market participation.
"""

from __future__ import annotations


class Volume:

    def __init__(

        self,

        period=20,

    ):

        self.period = period

    # --------------------------------------------------

    def calculate(

        self,

        volumes,

    ):

        volumes = [

            float(v)

            for v in volumes

            if v is not None

        ]

        if len(volumes) < self.period:

            return {

                "current": None,

                "average": None,

                "ratio": None,

                "state": None,

            }

        current = volumes[-1]

        average = sum(

            volumes[-self.period:]

        ) / self.period

        ratio = current / average if average else 0

        if ratio >= 2:

            state = "VERY_HIGH"

        elif ratio >= 1.5:

            state = "HIGH"

        elif ratio >= 0.75:

            state = "NORMAL"

        else:

            state = "LOW"

        return {

            "current": round(current, 2),

            "average": round(average, 2),

            "ratio": round(ratio, 2),

            "state": state,

        }

    # --------------------------------------------------

    def spike(

        self,

        volumes,

    ):

        result = self.calculate(volumes)

        return result["state"] in (

            "HIGH",

            "VERY_HIGH",

        )

    # --------------------------------------------------

    def low(

        self,

        volumes,

    ):

        result = self.calculate(volumes)

        return result["state"] == "LOW"