import backoff
import mlflow
from mlflow.pyfunc import PyFuncModel, PythonModel

from bechdel_test_predictor.training.mlflow.settings import MLFLOW_TRACKING_URI
from bechdel_test_predictor.logging.utils import db_logger


class BechdelTestPredictor(PythonModel):
    name: str = "bechdel-test-predictor"

    def __init__(self, model):
        self.model = model

    def predict(self, context, model_input):
        prediction = self.model.predict(model_input)[0]
        db_logger.info(f"Prediction: {prediction}")
        return prediction


def log_model(model):
    model = BechdelTestPredictor(model)
    mlflow.pyfunc.log_model(
        artifact_path="model",
        python_model=model,
        registered_model_name=model.name,
    )


@backoff.on_exception(
    backoff.constant,
    exception=mlflow.exceptions.RestException,
    max_time=100,  # Run for at most ... seconds
    interval=10,  # Poll every ... seconds
)
def load_latest_model(model_name: str) -> PyFuncModel:
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    client = mlflow.client.MlflowClient()

    registered_model = client.get_registered_model(model_name)
    model_version = registered_model.latest_versions[0].version  # type: ignore
    model = mlflow.pyfunc.load_model(model_uri=f"models:/{model_name}/{model_version}")
    return model
