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
