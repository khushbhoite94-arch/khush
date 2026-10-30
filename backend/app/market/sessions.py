"""
AEGIS AI
Market Sessions
"""

from datetime import datetime, timezone


class MarketSessions:

    @staticmethod
    def utc_hour():

        return datetime.now(timezone.utc).hour

    @classmethod
    def asian(cls):

        h = cls.utc_hour()
        return 0 <= h < 8

    @classmethod
    def london(cls):

        h = cls.utc_hour()
        return 8 <= h < 16

    @classmethod
    def new_york(cls):

        h = cls.utc_hour()
        return 13 <= h < 21

    @classmethod
    def overlap(cls):

        h = cls.utc_hour()
        return 13 <= h < 16

    @classmethod
    def current(cls):

        if cls.overlap():
            return "LONDON_NEWYORK"

        if cls.london():
            return "LONDON"

        if cls.new_york():
            return "NEW_YORK"

        if cls.asian():
            return "ASIAN"

        return "CLOSED"