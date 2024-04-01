from logging import basicConfig, getLogger, INFO, Formatter

from bechdel_test_predictor.logging.handler import DBHandler


def get_logger():
    basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%d-%b-%y %H:%M:%S',
        level=INFO,
    )

    format = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    db_logger = getLogger("db_logger")
    db_handler = DBHandler(backup_logger_name='backup_logger')
    db_handler.setLevel(INFO)
    db_handler.setFormatter(format)
    db_logger.addHandler(db_handler)

    return db_logger


db_logger = get_logger()
