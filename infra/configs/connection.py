from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from infra.configs.base import Base

from infra.entities import person, question, response

class DBConnectionHandler:
    CONNECTION_STRING = "sqlite:///data/data.db"

    def __init__(self):
        self.__engine = self.__create_database_engine()
        self.session = None

    def __create_database_engine(self):
        engine = create_engine(self.CONNECTION_STRING)
        return engine
    
    def create_tables(self):
        Base.metadata.create_all(self.__engine)

    def get_engine(self):
        return self.__engine

    def __enter__(self):
        session_make = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.session = session_make()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
