from typing import Dict

import numpy as np
import pandas as pd


class Model:
    """
    Dummy model class, used to build out infrastucture. This should be replaced by the real
    model when it is developed.

    """

    def __init__(self):
        pass

    def predict(self, data: pd.DataFrame) -> int:
        return np.random.randint(0, 4)


# TODO: Move this to a separate post-processing class
PREDICTION_MAP = {
    0: ("fail", "completely fail the test."),
    1: ("partial fail", "have at least two women in it."),
    2: ("partial fail", "have at least two women who talk to each other."),
    3: ("pass", "have at least two women who talk to each other about something besides a man!"),
}


# TODO: Move this to a separate post-processing class
def map_prediction(prediction: int) -> Dict[str, str]:
    """
    Maps the prediction to a human-readable format.

    Args:
        prediction (int): The prediction from the model.

    Returns:
        dict: A dictionary with the prediction and a summary.
    """
    formatted_pred = PREDICTION_MAP[prediction]
    return {
        "prediction": formatted_pred[0],
        "summary": f"We predict the movie will {formatted_pred[1]}",
    }
