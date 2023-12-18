import os
from sqlalchemy import create_engine, String, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column 



Base = declarative_base()


class Account(Base):
    __tablename__ = 'account'

    id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    credentials = Column(String, unique=True, nullable=False)

    def __repr__(self):
        return f"{self.__class__.__name__}({', '.join([f'{k}={v}' for k, v in self.__dict__.items() if not k.startswith('_')])})"


class Log(Base):
    __tablename__ = 'log'

    id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String, nullable=False)
    log_string = Column(String, unique=True, nullable=False)
    log = Column(String, nullable=False)

    def __repr__(self):
        return f"{self.__class__.__name__}({', '.join([f'{k}={v}' for k, v in self.__dict__.items() if not k.startswith('_')])})"
