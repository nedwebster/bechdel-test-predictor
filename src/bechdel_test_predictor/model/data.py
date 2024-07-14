import json
import os
from contextlib import contextmanager
import tempfile
from pathlib import Path
from typing import Tuple

import numpy as np
import opendatasets as od
import pandas as pd
from sklearn.model_selection import train_test_split
from sqlalchemy import create_engine

from bechdel_test_predictor.model.settings import DATA_URL, QUERY, RANDOM_SEED, TARGET, TEST_SIZE


@contextmanager
def kaggle_json_manager():
    """Create a temporary kaggle.json file with kaggle credentials. This file is used for downloading data."""
    with open("kaggle.json", "w") as file:
        json.dump(
            {
                "username": os.environ["KAGGLE_USERNAME"],
                "key": os.environ["KAGGLE_KEY"],
            },
            file,
        )
    yield
    os.remove("kaggle.json")


def download_csv_data(data_url) -> pd.DataFrame:
    with kaggle_json_manager():
        with tempfile.TemporaryDirectory() as temp_dir:
            od.download(dataset_id_or_url=data_url, data_dir=temp_dir)
            data_path = Path(temp_dir) / "female-representation-in-cinema" / "movies.csv"
            df = pd.read_csv(data_path, index_col=0)
    return df


def load_sql_data(query) -> pd.DataFrame:
    engine = create_engine(os.environ["DB_CONNECTION_STRING"])
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
