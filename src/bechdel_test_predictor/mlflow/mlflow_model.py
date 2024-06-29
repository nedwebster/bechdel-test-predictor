from mlflow.pyfunc import PythonModel

from bechdel_test_predictor.model.model import Model


class MlflowModel(PythonModel):
    """Model wrapper for a Mlflow compatible model."""

    name: str = "bechdel-test-predictor"

    def __init__(self, model: Model):
        self.model = model

    def predict(self, context, model_input):
        return self.model.predict(model_input)[0]
