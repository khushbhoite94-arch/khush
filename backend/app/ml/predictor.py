"""
AEGIS AI v2
ML Predictor
"""

from pathlib import Path
import joblib
import pandas as pd


class Predictor:

    def __init__(self, model_file):

        self.model = None

        if Path(model_file).exists():

            self.model = joblib.load(model_file)

    # -------------------------------------------------

    def predict(self, feature):

        if self.model is None:

            return {

                "prediction": None,

                "confidence": 0,

            }

        df = pd.DataFrame([feature])

        prediction = int(

            self.model.predict(df)[0]

        )

        probability = float(

            self.model.predict_proba(df)[0].max()

        )

        return {

            "prediction": prediction,

            "confidence": round(

                probability * 100,

                2,

            ),

        }