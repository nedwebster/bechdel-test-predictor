import logging

from metaflow.decorators import step
from metaflow.flowspec import FlowSpec


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InitData(FlowSpec):
    @step
    def start(self):
        logger.info("Starting init data flow")
        self.next(self.download_data)

    @step
    def download_data(self):
        logger.info("Downloading data")
        from bechdel_test_predictor.model.data import download_csv_data
        from bechdel_test_predictor.model.settings import DATA_URL

        self.data = download_csv_data(DATA_URL)
        self.next(self.ingest_data)

    @step
    def ingest_data(self):
        logger.info("Ingesting data to PSQL")
        import os

        from sqlalchemy import create_engine

        engine = create_engine(os.environ["DB_CONNECTION_STRING"])
        with engine.connect() as connection:
            self.data.to_sql("movies", connection, if_exists="replace", index=False)
        self.next(self.end)

    @step
    def end(self):
        logger.info("Data initialisation completed")


if __name__ == "__main__":
    InitData()
