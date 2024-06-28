from typing import List

import numpy as np
import pandas as pd
from sklearn.metrics import precision_recall_curve
from sklearn.pipeline import Pipeline


class Model:
    name: str = "bechdel-test-predictor"
    """Class to represent the machine learning model."""

    def __init__(self, pipeline: Pipeline, features: List[str], target: str):
        self.pipeline = pipeline
        self.features = features
        self.target = target
        self._threshold = 0.5

    @property
    def threshold(self) -> float:
        return self._threshold

    @threshold.setter
    def threshold(self, value: float) -> None:
        self._threshold = value

    def fit(self, data: pd.DataFrame) -> None:
        self.pipeline.fit(data[self.features].copy(), data[self.target])
        self._optimise_threshold(data)

    def _optimise_threshold(self, data: pd.DataFrame) -> None:
        preds_bin = self.predict_proba(data)
        precision, recall, thresholds = precision_recall_curve(data[self.target], preds_bin)
        fscore = (2 * precision * recall) / (precision + recall)
        ix = np.argmax(fscore)
        self.threshold = thresholds[ix]

    def predict_proba(self, data: pd.DataFrame) -> np.ndarray:
        return self.pipeline.predict_proba(data[self.features].copy())[:, 1]

    def predict(self, data: pd.DataFrame) -> np.ndarray:
        return (self.predict_proba(data) > self.threshold).astype(int)
