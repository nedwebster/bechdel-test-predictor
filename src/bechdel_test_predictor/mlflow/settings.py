import os

import mlflow

ENV = os.environ.get("ENV", "LOCAL")
if ENV == "DOCKER":
    MLFLOW_TRACKING_URI = "http://mlflow-server:5001"
elif ENV == "LOCAL":
    MLFLOW_TRACKING_URI = mlflow.get_tracking_uri()
