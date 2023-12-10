from typing import Dict

from bechdel_test_predictor.model import Model
from bechdel_test_predictor.movie import MovieClient, MovieProcessor


class BechdelTestClient:
    def __init__(self):
        self.client = MovieClient()
        self.processor = MovieProcessor()
        self.model = Model()
        self.prediction_map = {
            0: ("fail", "completely fail the test."),
            1: ("partial fail", "have at least two women in it."),
            2: ("partial fail", "have at least two women who talk to each other."),
            3: ("pass", "have at least two women who talk to each other about something besides a man!"),
        }
        self.summary_prefix = "We predict the movie will "

    def _format_output(self, prediction: int) -> Dict[str, str]:
        formatted_pred = self.prediction_map[prediction]
        return {
            "prediction": formatted_pred[0],
            "summary": self.summary_prefix + formatted_pred[1],
        }

    def get_bechdel_prediction(self, title: str) -> str:
        movie = self.client.get_movie(title)
        processed_movie = self.processor.process_movie(movie)
        prediction = self.model.predict(processed_movie)

        return self._format_output(prediction)
