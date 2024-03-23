import backoff
import mlflow
from mlflow.pyfunc import PyFuncModel


@backoff.on_exception(
    backoff.constant,
    exception=mlflow.exceptions.RestException,
    max_time=100,  # Run for at most ... seconds
    interval=10,  # Poll every ... seconds
)
def load_latest_model(model_name: str) -> PyFuncModel:
    client = mlflow.client.MlflowClient()

    registered_model = client.get_registered_model(model_name)
    model_version = registered_model.latest_versions[0].version  # type: ignore
    model = mlflow.pyfunc.load_model(model_uri=f"models:/{model_name}/{model_version}")
    return model
