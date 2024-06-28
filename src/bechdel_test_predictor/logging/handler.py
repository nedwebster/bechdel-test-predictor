# handler.py
import os
from logging import Handler, getLogger
from traceback import print_exc

from bechdel_test_predictor.logging.crud import Crud
from bechdel_test_predictor.logging.models import Log

my_crud = Crud(
    connection_string=os.environ["DB_CONNECTION_STRING"],
    encoding="utf-8",
    pool_size=10,
    max_overflow=20,
    pool_recycle=3600,
)

my_crud.initiate()


class DBHandler(Handler):
    backup_logger = None

    def __init__(self, level=0, backup_logger_name=None):
        super().__init__(level)
        if backup_logger_name:
            self.backup_logger = getLogger(backup_logger_name)

    def emit(self, record):
        try:
            message = self.format(record)

            try:
                new_log = Log(
                    module=record.module,
                    thread_name=record.threadName,
                    file_name=record.filename,
                    func_name=record.funcName,
                    level_name=record.levelname,
                    line_no=record.lineno,
                    process_name=record.processName,
                    message=message,
                )
                # raise

                my_crud.insert(instances=new_log)
            except Exception:
                if self.backup_logger:
                    try:
                        getattr(self.backup_logger, record.levelname.lower())(record.message)
                    except Exception:
                        print_exc()
                else:
                    print_exc()

        except Exception:
            print_exc()
