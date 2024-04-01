import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

base = declarative_base()


class Log(base):
    __tablename__ = "model_logs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    time = Column(DateTime, nullable=False, default=datetime.datetime.now)
    level_name = Column(String(10), nullable=True)
    module = Column(String(200), nullable=True)
    thread_name = Column(String(200), nullable=True)
    file_name = Column(String(200), nullable=True)
    func_name = Column(String(200), nullable=True)
    line_no = Column(Integer, nullable=True)
    process_name = Column(String(200), nullable=True)
    message = Column(Text)
