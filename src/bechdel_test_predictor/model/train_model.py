import logging
from typing import Tuple

import mlflow
import pandas as pd
from sklearn.metrics import average_precision_score, precision_score, recall_score, roc_auc_score

from bechdel_test_predictor.mlflow import log_model
from bechdel_test_predictor.mlflow.settings import MLFLOW_TRACKING_URI
from bechdel_test_predictor.model.data import get_data, preprocess_data
from bechdel_test_predictor.model.model import Model
from bechdel_test_predictor.model.pipeline import get_pipeline
from bechdel_test_predictor.model.settings import FEATURES, TARGET

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_data() -> Tuple[pd.DataFrame, pd.DataFrame]:
    data = get_data()
    train, test = preprocess_data(data)
    return train, test


def train_model(train: pd.DataFrame) -> Model:
    model = Model(pipeline=get_pipeline(), features=FEATURES, target=TARGET)
    model.fit(train)

    return model


def evaluate_model(test: pd.DataFrame, model: Model):
    test["label_prediction"] = model.predict(test)
    test["prediction"] = model.predict_proba(test)

    # Evaluate
    mlflow.log_metrics(
        {
            "Threshold": model.threshold,
            "AUC": float("{0:.3f}".format(roc_auc_score(test[TARGET], test["prediction"], average="weighted"))),
            "Average Precision": float("{0:.3f}".format(average_precision_score(test[TARGET], test["prediction"]))),
            "Precision": float(
                "{0:.3f}".format(precision_score(test[TARGET], test["label_prediction"], average="weighted"))
            ),
            "Recall": float("{0:.3f}".format(recall_score(test[TARGET], test["label_prediction"], average="weighted"))),
        }
    )


def train_mlflow_model():
    logger.info("Configuring MLflow")
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.autolog(disable=True)
    mlflow.set_experiment("bechdel_predictor_training")
    with mlflow.start_run() as run:
        logger.info(f"Mlflow run started: {run.info.run_id}")
        logger.info("Loading and prepping data")
        train, test = load_data()
        logger.info("Data successfully loaded and prepped")
        logger.info("Fitting model pipeline")
        pipeline = train_model(train)
        logger.info("Model pipeline successfully fitted")
        logger.info("Evaluating model on test set")
        evaluate_model(test, pipeline)
        logger.info("Logging model to mlflow model registry")
        log_model(pipeline)
        logger.info("Model successfully logged!")


if __name__ == "__main__":
    train_mlflow_model()
