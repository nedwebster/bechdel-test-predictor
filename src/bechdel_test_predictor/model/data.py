import os
import tempfile
from pathlib import Path
from typing import Tuple

import mlflow
import numpy as np
import opendatasets as od
import pandas as pd
from sklearn.model_selection import train_test_split
from sqlalchemy import create_engine

from bechdel_test_predictor.model.settings import DATA_URL, QUERY, RANDOM_SEED, TARGET, TEST_SIZE


def download_csv_data(data_url) -> pd.DataFrame:
    with tempfile.TemporaryDirectory() as temp_dir:
        od.download(dataset_id_or_url=data_url, data_dir=temp_dir)
        data_path = Path(temp_dir) / "female-representation-in-cinema" / "movies.csv"
        df = pd.read_csv(data_path, index_col=0)
        mlflow.log_param("data_shape_raw", df.shape)

        return df


def load_sql_data(query) -> pd.DataFrame:
    engine = create_engine(
        "postgresql://postgres:postgres123@postgres-db:5432/postgres"
    )  # TODO: remove hardcoded values
    with engine.connect() as connection:
        data = pd.read_sql(query, connection)
    return data


def get_data() -> pd.DataFrame:
    if os.environ.get("ENV", "LOCAL") == "DOCKER":
        return load_sql_data(QUERY)
    else:
        return download_csv_data(DATA_URL)


def preprocess_data(data: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    data = data.drop_duplicates()
    index_to_drop = data[(data["imdbid"] == 2180411) & (data["dubious"] == 0)].index
    data = data.drop(index_to_drop, axis=0)
    data[TARGET] = np.where(data["bt_score"].isin([2, 3]), 1, 0)
    train, test = train_test_split(data, test_size=TEST_SIZE, random_state=RANDOM_SEED)
    return train, test
