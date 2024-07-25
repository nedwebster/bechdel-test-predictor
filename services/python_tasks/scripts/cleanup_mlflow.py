import logging

from metaflow import FlowSpec, step, trigger_on_finish


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@trigger_on_finish("InitDataFlow")
class CleanupMlflowFlow(FlowSpec):
    @step
    def start(self):
        self.next(self.delete_model)

    @step
    def delete_model(self):
        from bechdel_test_predictor.mlflow.utils import delete_model

        delete_model("bechdel-test-predictor")
        self.next(self.delete_experiment)

    @step
    def delete_experiment(self):
        from bechdel_test_predictor.mlflow.utils import delete_experiment

        delete_experiment("bechdel_predictor_training")
        self.next(self.mlflow_gargbage_cleanup)

    @step
    def mlflow_gargbage_cleanup(self):
        import os
        import subprocess
        from bechdel_test_predictor.mlflow.settings import MLFLOW_TRACKING_URI

        os.environ["MLFLOW_TRACKING_URI"] = MLFLOW_TRACKING_URI
        subprocess.run(["mlflow", "gc", "--backend-store-uri", os.environ["DB_CONNECTION_STRING"]])
        self.next(self.end)

    @step
    def end(self):
        logger.info("Finished cleanup of mlflow models.")


if __name__ == "__main__":
    CleanupMlflowFlow()
