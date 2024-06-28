import tempfile
from pathlib import Path

import opendatasets as od
import pandas as pd
from sqlalchemy import create_engine

from bechdel_test_predictor.model.settings import DATA_URL


def download_data() -> pd.DataFrame:
    with tempfile.TemporaryDirectory() as temp_dir:
        od.download(dataset_id_or_url=DATA_URL, data_dir=temp_dir)
        data_path = Path(temp_dir) / "female-representation-in-cinema" / "movies.csv"
        df = pd.read_csv(data_path, index_col=0)
        return df


def upload_to_psql(data: pd.DataFrame) -> None:
    engine = create_engine("postgresql://postgres:postgres123@postgres-db:5432/postgres")  # TODO: remove hardcoded values
    with engine.connect() as connection:
        data.to_sql("movies", connection, if_exists="replace", index=False)


if __name__ == "__main__":
    data = download_data()
    upload_to_psql(data)
