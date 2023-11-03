import os
from pathlib import Path

import opendatasets as od


DATA_URL = "https://www.kaggle.com/datasets/vinifm/female-representation-in-cinema/"


def download_data() -> None:
    download_path = os.getcwd() + "/data"
    Path(download_path).mkdir(parents=True, exist_ok=True)
    od.download(dataset_id_or_url=DATA_URL, data_dir=download_path)


if __name__ == "__main__":
    download_data()
