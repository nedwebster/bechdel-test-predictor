import logging
from typing import Any

import backoff
import mlflow
from mlflow.pyfunc import PyFuncModel, PythonModel

from bechdel_test_predictor.mlflow.settings import MLFLOW_TRACKING_URI
from bechdel_test_predictor.model.model import Model

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MlflowModel(PythonModel):
    """Model wrapper for a Mlflow compatible model."""

    name: str = "bechdel-test-predictor"

    def __init__(self, model: Model):
        self.model = model

    def predict(self, context, model_input):
        return self.model.predict(model_input)[0]


def log_model(model: Model):
    """Log MlflowModel to mlflow model registry."""
    mlflow_model = MlflowModel(model)
    mlflow.pyfunc.log_model(
        artifact_path="model",
        python_model=mlflow_model,
        registered_model_name=model.name,
    )


def backoff_message(x: Any) -> None:
    logger.info("No model found, retrying in 10 seconds...")


@backoff.on_exception(
    backoff.constant,
    exception=mlflow.exceptions.RestException,
    interval=10,  # Poll every ... seconds
    on_backoff=backoff_message,
)
def load_latest_model(model_name: str) -> PyFuncModel:
    """Load the latest model from the model registry, based on model version."""
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    client = mlflow.client.MlflowClient()

    registered_model = client.get_registered_model(model_name)
    model_version = registered_model.latest_versions[0].version  # type: ignore
    model = mlflow.pyfunc.load_model(model_uri=f"models:/{model_name}/{model_version}")
    return model
