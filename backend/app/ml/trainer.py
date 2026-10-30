"""
AEGIS AI v2
Model Trainer

Simple Logistic Regression trainer using scikit-learn.
"""

from pathlib import Path
import joblib
import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


class Trainer:

    def __init__(self):

        self.model = LogisticRegression(max_iter=1000)

    # -------------------------------------------------

    def train(self, csv_file):

        df = pd.read_csv(csv_file)

        X = df.drop(columns=["label"])

        y = df["label"]

        X_train, X_test, y_train, y_test = train_test_split(

            X,

            y,

            test_size=0.2,

            shuffle=True,

            random_state=42,

        )

        self.model.fit(

            X_train,

            y_train,

        )

        prediction = self.model.predict(X_test)

        accuracy = accuracy_score(

            y_test,

            prediction,

        )

        return accuracy

    # -------------------------------------------------

    def save(self, filename):

        Path(filename).parent.mkdir(

            parents=True,

            exist_ok=True,

        )

        joblib.dump(

            self.model,

            filename,

        )

    # -------------------------------------------------

    def load(self, filename):

        self.model = joblib.load(filename)