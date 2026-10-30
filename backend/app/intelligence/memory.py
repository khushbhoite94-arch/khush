"""
AEGIS AI v2
AI Memory
"""

from __future__ import annotations

from collections import deque


class Memory:

    def __init__(

        self,

        size=500,

    ):

        self.memory = deque(

            maxlen=size,

        )

    # ----------------------------------------------------

    def remember(

        self,

        item,

    ):

        self.memory.append(item)

    # ----------------------------------------------------

    def last(self):

        if not self.memory:

            return None

        return self.memory[-1]

    # ----------------------------------------------------

    def last_n(

        self,

        n,

    ):

        return list(self.memory)[-n:]

    # ----------------------------------------------------

    def clear(self):

        self.memory.clear()

    # ----------------------------------------------------

    def __len__(self):

        return len(self.memory)

    # ----------------------------------------------------

    def wins(self):

        return [

            x

            for x in self.memory

            if x.get("pnl", 0) > 0

        ]

    # ----------------------------------------------------

    def losses(self):

        return [

            x

            for x in self.memory

            if x.get("pnl", 0) < 0

        ]

    # ----------------------------------------------------

    def winrate(self):

        total = len(self.memory)

        if total == 0:

            return 0

        wins = len(self.wins())

        return round(

            wins / total * 100,

            2,

        )

    # ----------------------------------------------------

    def statistics(self):

        return {

            "stored": len(self.memory),

            "wins": len(self.wins()),

            "losses": len(self.losses()),

            "winrate": self.winrate(),

        }