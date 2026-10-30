"""
AEGIS AI v3
Universal AI Model Manager
"""

from __future__ import annotations

import os
import json
import joblib
from pathlib import Path
from datetime import datetime


class ModelManager:

    def __init__(

        self,

        model_dir="models/active",

    ):

        self.model_dir = Path(model_dir)

        self.model_dir.mkdir(

            parents=True,

            exist_ok=True,

        )

        self.model = None

        self.model_name = None

        self.metadata = {}

    # =====================================================
    # SAVE
    # =====================================================

    def save(

        self,

        model,

        name,

        metadata=None,

    ):

        model_path = self.model_dir / f"{name}.pkl"

        joblib.dump(

            model,

            model_path,

            compress=3,

        )

        info = {

            "name": name,

            "created": str(

                datetime.utcnow()

            ),

            "type": str(

                type(model)

            ),

        }

        if metadata:

            info.update(metadata)

        with open(

            self.model_dir / f"{name}.json",

            "w",

        ) as f:

            json.dump(

                info,

                f,

                indent=4,

            )

        self.model = model

        self.model_name = name

        self.metadata = info

        return model_path

    # =====================================================
    # LOAD
    # =====================================================

    def load(

        self,

        name,

    ):

        model_path = self.model_dir / f"{name}.pkl"

        if not model_path.exists():

            raise FileNotFoundError(

                f"Model '{name}' not found."

            )

        model = joblib.load(

            model_path,

        )

        meta = {}

        meta_path = self.model_dir / f"{name}.json"

        if meta_path.exists():

            with open(meta_path) as f:

                meta = json.load(f)

        self.model = model

        self.model_name = name

        self.metadata = meta

        return model

    # =====================================================
    # EXISTS
    # =====================================================

    def exists(

        self,

        name,

    ):

        return (

            self.model_dir /

            f"{name}.pkl"

        ).exists()

    # =====================================================
    # DELETE
    # =====================================================

    def delete(

        self,

        name,

    ):

        model = self.model_dir / f"{name}.pkl"

        meta = self.model_dir / f"{name}.json"

        if model.exists():

            os.remove(model)

        if meta.exists():

            os.remove(meta)

    # =====================================================
    # LIST
    # =====================================================

    def models(self):

        result = []

        for file in self.model_dir.glob("*.json"):

            with open(file) as f:

                result.append(

                    json.load(f)

                )

        return result

    # =====================================================
    # TRAIN
    # =====================================================

    def train(

        self,

        model,

        X,

        y,

    ):

        model.fit(

            X,

            y,

        )

        self.model = model

        return model

    # =====================================================
    # PREDICT
    # =====================================================

    def predict(

        self,

        X,

    ):

        if self.model is None:

            raise RuntimeError(

                "No model loaded."

            )

        prediction = self.model.predict(

    X,

)

        return prediction

    # =====================================================
    # PROBABILITY
    # =====================================================

    def probability(

        self,

        X,

    ):

        if self.model is None:

            raise RuntimeError(

                "No model loaded."

            )

        if hasattr(

            self.model,

            "predict_proba",

        ):

            return self.model.predict_proba(X)

        return None

    # =====================================================
    # SCORE
    # =====================================================

    def score(

        self,

        X,

        y,

    ):

        if self.model is None:

            return 0

        return self.model.score(

            X,

            y,

        )

    # =====================================================
    # FEATURE IMPORTANCE
    # =====================================================

    def feature_importance(self):

        if self.model is None:

            return None

        if hasattr(

            self.model,

            "feature_importances_",

        ):

            return list(

                self.model.feature_importances_

            )

        return None

    # =====================================================
    # EXPORT
    # =====================================================

    def export_metadata(self):

        return {

            "name": self.model_name,

            "metadata": self.metadata,

        }

    # =====================================================
    # RESET
    # =====================================================

    def unload(self):

        self.model = None

        self.model_name = None

        self.metadata = {}

    # =====================================================
    # READY
    # =====================================================

    def ready(self):

        return self.model is not None

# =====================================================
# CURRENT MODEL
# =====================================================

def current(self):

    return {

        "name": self.model_name,

        "loaded": self.ready(),

    }

    # =====================================================
    # SUMMARY
    # =====================================================

def summary(self):

    return {

        "loaded": self.ready(),

        "model": self.model_name,

        "metadata": self.metadata,

        "available_models": self.models(),

        "directory": str(

            self.model_dir,

        ),

    }