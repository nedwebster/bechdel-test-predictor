from typing import Dict

import pandas as pd

from bechdel_test_predictor.model import Model
from bechdel_test_predictor.movie import Movie, MovieClient, MovieProcessor
from bechdel_test_predictor.prediction import Prediction


class BechdelAPI:
    def __init__(self):
        self.client = MovieClient()
        self.processor = MovieProcessor()
        self.model = Model()

    def get_movie(self, title: str) -> Movie:
        return self.client.get_movie(title)

    def process_movie(self, movie: Movie) -> pd.DataFrame:
        return self.processor.process_movie(movie)

    def get_prediction(self, processed_movie: pd.DataFrame) -> int:
        return self.model.predict(processed_movie)

    def format_prediction(self, title: str, prediction: int) -> dict:
        pred_object = Prediction(title=title, prediction=prediction)
        return pred_object.dict()

    def get_bechdel_prediction(self, title: str) -> Dict[str, str]:
        movie = self.get_movie(title)
        processed_movie = self.process_movie(movie)
        prediction = self.get_prediction(processed_movie)
        return self.format_prediction(title=movie.title, prediction=prediction)
