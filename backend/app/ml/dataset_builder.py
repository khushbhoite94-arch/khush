"""
AEGIS AI v2
Dataset Builder

Converts historical candles into ML datasets.
"""

from __future__ import annotations

import csv
from pathlib import Path

from app.ml.feature_engine import FeatureEngine


class DatasetBuilder:

    def __init__(self):

        self.features = FeatureEngine()

    # -----------------------------------------------------

    def create(self, candles):

        dataset = []

        for i in range(25, len(candles) - 1):

            history = candles[:i]

            current = candles[i]

            nxt = candles[i + 1]

            feature = self.features.build(history)

            if feature is None:

                continue

            feature = self.features.normalize(feature)

            label = 1 if nxt["close"] > current["close"] else 0

            feature["label"] = label

            dataset.append(feature)

        return dataset

    # -----------------------------------------------------

    def save_csv(

        self,

        dataset,

        filename,

    ):

        if not dataset:

            return

        path = Path(filename)

        path.parent.mkdir(

            parents=True,

            exist_ok=True,

        )

        columns = list(dataset[0].keys())

        with open(

            path,

            "w",

            newline="",

        ) as f:

            writer = csv.DictWriter(

                f,

                fieldnames=columns,

            )

            writer.writeheader()

            writer.writerows(dataset)

    # -----------------------------------------------------

    def load_csv(

        self,

        filename,

    ):

        path = Path(filename)

        if not path.exists():

            return []

        with open(path) as f:

            reader = csv.DictReader(f)

            data = []

            for row in reader:

                item = {}

                for k, v in row.items():

                    try:

                        item[k] = float(v)

                    except Exception:

                        item[k] = v

                data.append(item)

        return data

    # -----------------------------------------------------

    def summary(

        self,

        dataset,

    ):

        if not dataset:

            return {}

        buys = sum(

            1

            for x in dataset

            if x["label"] == 1

        )

        sells = len(dataset) - buys

        return {

            "rows": len(dataset),

            "buy_labels": buys,

            "sell_labels": sells,

        }