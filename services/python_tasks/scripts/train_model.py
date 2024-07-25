import logging

from metaflow import FlowSpec, step, trigger_on_finish

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@trigger_on_finish("CleanupMlflowFlow")
class TrainingFlow(FlowSpec):
    @step
    def start(self):
        logger.info("Starting training flow")
        self.next(self.load_data)

    @step
    def load_data(self):
        from bechdel_test_predictor.model.data import get_data, preprocess_data

        logger.info("Loading data")
        data = get_data()
        train, test = preprocess_data(data)
        self.train = train
        self.test = test
        self.next(self.train_model)

    @step
    def train_model(self):
        logger.info("Training model")
        from bechdel_test_predictor.model.model import Model
        from bechdel_test_predictor.model.pipeline import get_pipeline
        from bechdel_test_predictor.model.settings import FEATURES, TARGET

        self.model = Model(pipeline=get_pipeline(), features=FEATURES, target=TARGET)
        self.model.fit(self.train)
        self.next(self.evaluate_model)

    @step
    def evaluate_model(self):
        from sklearn.metrics import average_precision_score, precision_score, recall_score, roc_auc_score

        from bechdel_test_predictor.model.settings import TARGET

        logger.info("Evaluating model")
        binary_predictions = self.model.predict(self.test)
        prob_predictions = self.model.predict_proba(self.test)
        self.auc = float("{0:.3f}".format(roc_auc_score(self.test[TARGET], prob_predictions, average="weighted")))
        self.average_precision = float("{0:.3f}".format(average_precision_score(self.test[TARGET], prob_predictions)))
        self.precision = float(
            "{0:.3f}".format(precision_score(self.test[TARGET], binary_predictions, average="weighted"))
        )
        self.recall = float("{0:.3f}".format(recall_score(self.test[TARGET], binary_predictions, average="weighted")))

        self.next(self.log_to_mlflow)

    @step
    def log_to_mlflow(self):
        import mlflow
        from bechdel_test_predictor.mlflow import log_model
        from bechdel_test_predictor.mlflow.settings import MLFLOW_TRACKING_URI

        mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
        mlflow.autolog(disable=True)
        mlflow.set_experiment("bechdel_predictor_training")
        with mlflow.start_run() as run:
            logger.info(f"Logging info to mlflow run_id: {run.info.run_id}")
            log_model(self.model)
            mlflow.log_metrics(
                {
                    "Threshold": self.model.threshold,
                    "AUC": self.auc,
                    "Average Precision": self.average_precision,
                    "Precision": self.precision,
                    "Recall": self.recall,
                }
            )
            mlflow.log_params(
                {
                    "features": self.model.features,
                    "target": self.model.target,
                    "train_data_shape": self.train.shape,
                    "test_data_shape": self.test.shape,
                }
            )
        self.next(self.end)

    @step
    def end(self):
        print("Training flow completed")


if __name__ == "__main__":
    TrainingFlow()
