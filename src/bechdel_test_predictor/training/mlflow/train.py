import logging
import tempfile
from pathlib import Path
from typing import Tuple

import mlflow
import numpy as np
import opendatasets as od
import pandas as pd
from sklearn.metrics import average_precision_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from bechdel_test_predictor.training.mlflow import log_model
from bechdel_test_predictor.training.mlflow.settings import MLFLOW_TRACKING_URI
from bechdel_test_predictor.training.pipeline import get_pipeline
from bechdel_test_predictor.training.settings import DATA_URL, RANDOM_SEED, TARGET

logger = logging.getLogger(__name__)


def download_data() -> pd.DataFrame:
    with tempfile.TemporaryDirectory() as temp_dir:
        od.download(dataset_id_or_url=DATA_URL, data_dir=temp_dir)
        data_path = Path(temp_dir) / "female-representation-in-cinema" / "movies.csv"
        df = pd.read_csv(data_path, index_col=0)
        mlflow.log_param("data_shape_raw", df.shape)

        return df


def preprocess_data(df) -> Tuple[pd.DataFrame, pd.DataFrame]:
    n = df.shape[0]
    df = df.drop_duplicates()
    index_to_drop = df[(df["imdbid"] == 2180411) & (df["dubious"] == 0)].index
    df = df.drop(index_to_drop, axis=0)
    mlflow.log_param("data_duplicates_dropped", n - df.shape[0])

    df[TARGET] = np.where(df["bt_score"].isin([2, 3]), 1, 0)

    # Split intro train and test
    train, test = train_test_split(df, test_size=0.3, random_state=RANDOM_SEED)
    mlflow.log_param("data_shape_train", train.shape)
    mlflow.log_param("data_shape_test", test.shape)

    return train, test


def fit_pipeline(train: pd.DataFrame) -> Pipeline:
    pipeline = get_pipeline()
    pipeline.fit(train.copy(), train[TARGET])

    return pipeline


def evaluate_model(test: pd.DataFrame, pipeline: Pipeline):
    preds = pipeline.predict_proba(test.copy())[:, 1]
    test["label_prediction"] = pipeline.predict(test.copy())
    test["prediction"] = preds

    # Evaluate
    mlflow.log_metrics(
        {
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
        logger.info("Downloading data")
        df = download_data()
        logger.info("Data successfully downloaded")
        logger.info("Processing data")
        train, test = preprocess_data(df)
        logger.info("Data successfully processed")
        logger.info("Fitting model pipeline")
        pipeline = fit_pipeline(train)
        logger.info("Model pipeline successfully fitted")
        logger.info("Evaluating model on test set")
        evaluate_model(test, pipeline)
        logger.info("Logging model to mlflow model registry")
        log_model(pipeline)
        logger.info("Model successfully logged!")
