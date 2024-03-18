from typing import Dict

from bechdel_test_predictor.model import Model, map_prediction
from bechdel_test_predictor.movie import MovieClient, MovieProcessor


class BechdelAPI:
    def __init__(self):
        self.client = MovieClient()
        self.processor = MovieProcessor()
        self.model = Model()

    def get_bechdel_prediction(self, title: str) -> Dict[str, str]:
        movie = self.client.get_movie(title)
        processed_movie = self.processor.process_movie(movie)
        prediction = self.model.predict(processed_movie)

        return map_prediction(prediction)
