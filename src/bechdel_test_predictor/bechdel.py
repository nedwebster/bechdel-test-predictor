import logging
import os
from typing import Dict

import pandas as pd
from mlflow.pyfunc import PyFuncModel

from bechdel_test_predictor.movie import Movie, MovieClient, MovieProcessor
from bechdel_test_predictor.prediction import Prediction


if os.environ.get("ENV", "local") == "docker":
    from bechdel_test_predictor.logging.utils import get_logger
    db_logger = get_logger()
else:
    db_logger = logging.getLogger()


class BechdelAPI:
    def __init__(self, model: PyFuncModel):
        self.client = MovieClient()
        self.processor = MovieProcessor()
        self.model = model

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

        log_output = {
            "input_title": title,
            "returned_title": movie.title,
            "prediction": prediction,
        }
        db_logger.info(log_output)

        return self.format_prediction(title=movie.title, prediction=prediction)
