from dataclasses import dataclass

PREDICTION_MAP = {
    0: ("fail", "fail the test."),
    1: ("pass", "pass the test, having at least two women who talk to each other!"),
}

PRE_SUMMARY = "We predict the movie will "


@dataclass
class Prediction:
    title: str
    prediction: int

    def __post_init__(self):
        self.classified_prediction = PREDICTION_MAP[self.prediction][0]
        self.summary = f"{PRE_SUMMARY}{PREDICTION_MAP[self.prediction][1]}"

    def dict(self):
        return self.__dict__
