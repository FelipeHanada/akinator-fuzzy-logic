from infra.configs.connection import DBConnectionHandler
from infra.entities.question import Question

class QuestionRepository:
    def select_all(self):
        with DBConnectionHandler() as db:
            data = db.session.query(Question).all()

            return data
