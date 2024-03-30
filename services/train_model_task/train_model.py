import os

from bechdel_test_predictor.training.mlflow import train_mlflow_model


if __name__ == "__main__":
    if os.environ.get("TRAIN_MODEL"):
        train_mlflow_model()
    else:
        pass
