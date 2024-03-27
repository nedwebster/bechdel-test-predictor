import mlflow
import numpy as np
from mlflow.pyfunc import PythonModel


class DummyModel(PythonModel):
    def __init__(self):
        pass

    def predict(self, context, model_input):
        return np.random.randint(0, 4)


def main():
    mlflow.set_tracking_uri("http://mlflow-server:5001")
    mlflow.set_experiment("train_model")
    model = DummyModel()
    model_info = mlflow.pyfunc.log_model(
        artifact_path="model_file",
        python_model=model,
        registered_model_name="bechdel-test-model",
        pip_requirements="requirements.txt",
    )
    print(model_info.model_uri)


if __name__ == "__main__":
    main()
