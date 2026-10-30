"""
AEGIS AI v3
Analytics Exporter
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from datetime import datetime


class Exporter:

    def __init__(self, export_dir="exports"):

        self.export_dir = Path(export_dir)

        self.export_dir.mkdir(

            parents=True,

            exist_ok=True,

        )

    # =====================================================
    # JSON
    # =====================================================

    def json(

        self,

        data,

        filename=None,

    ):

        if filename is None:

            filename = (

                datetime.utcnow()

                .strftime("%Y%m%d_%H%M%S")

                + ".json"

            )

        path = self.export_dir / filename

        with open(

            path,

            "w",

            encoding="utf-8",

        ) as f:

            json.dump(

                data,

                f,

                indent=4,

                default=str,

            )

        return path

    # =====================================================
    # CSV
    # =====================================================

    def csv(

        self,

        rows,

        filename=None,

    ):

        rows = list(rows)

        if not rows:

            return None

        if filename is None:

            filename = (

                datetime.utcnow()

                .strftime("%Y%m%d_%H%M%S")

                + ".csv"

            )

        path = self.export_dir / filename

        with open(

            path,

            "w",

            newline="",

            encoding="utf-8",

        ) as f:

            writer = csv.DictWriter(

                f,

                fieldnames=rows[0].keys(),

            )

            writer.writeheader()

            writer.writerows(rows)

        return path

    # =====================================================
    # JOURNAL
    # =====================================================

    def journal(

        self,

        journal,

        filename="journal.csv",

    ):

        return self.csv(

            journal.export(),

            filename,

        )

    # =====================================================
    # REPORT
    # =====================================================

    def report(

        self,

        report,

        filename="report.json",

    ):

        return self.json(

            report,

            filename,

        )

    # =====================================================
    # GENERIC
    # =====================================================

    def export(

        self,

        data,

        filename,

    ):

        suffix = Path(filename).suffix.lower()

        if suffix == ".json":

            return self.json(

                data,

                filename,

            )

        if suffix == ".csv":

            return self.csv(

                data,

                filename,

            )

        raise ValueError(

            "Unsupported export format."

        )