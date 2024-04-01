import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

from bechdel_test_predictor.training.mlflow import train_mlflow_model  # noqa: E402


if __name__ == "__main__":
    if os.environ.get("TRAIN_MODEL"):
        train_mlflow_model()
    else:
        pass
