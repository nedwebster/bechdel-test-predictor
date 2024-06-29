import logging
from typing import Any

import backoff
import mlflow
from mlflow.pyfunc import PyFuncModel

from bechdel_test_predictor.mlflow.mlflow_model import MlflowModel
from bechdel_test_predictor.mlflow.settings import MLFLOW_TRACKING_URI
from bechdel_test_predictor.model.model import Model

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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


def delete_model(model_name: str) -> None:
    """Recursively delete all model versions, and the model itself, from the mlflow registry."""
    mlflow_client = mlflow.client.MlflowClient(tracking_uri=MLFLOW_TRACKING_URI)
    try:
        versions = mlflow_client.get_latest_versions(name=model_name, stages=["staging", "production"])
    except mlflow.exceptions.RestException:
        logger.info(f"{model_name} model doesn't exist, skipping...")
        return None

    if len(versions) == 0:
        mlflow_client.delete_registered_model(model_name)
        logger.info(f"Deleted model: {model_name}")
    else:
        for version in versions:
            mlflow_client.transition_model_version_stage(
                name=model_name,
                version=version.version,
                stage="archived",
                archive_existing_versions=False,
            )
        delete_model(model_name)


def delete_experiment(experiment_name: str) -> None:
    mlflow_client = mlflow.client.MlflowClient(tracking_uri=MLFLOW_TRACKING_URI)
    experiment = mlflow_client.get_experiment_by_name(experiment_name)
    if experiment:
        if experiment.lifecycle_stage == "deleted":
            logger.info(f"Experiment {experiment_name} already deleted")
            return None
        else:
            mlflow_client.delete_experiment(experiment.experiment_id)
