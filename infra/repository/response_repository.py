from infra.configs.connection import DBConnectionHandler
from infra.entities.response import Response

class ResponseRepository:
    def select_all(self):
        with DBConnectionHandler() as db:
            data = db.session.query(Response).all()

            return data
    
    def select_by_id(self, id):
        with DBConnectionHandler() as db:
            data = db.session.query(Response).filter(Response.id == id).first()

            return data

    def select_by_data(self, person_id, question_id):
        with DBConnectionHandler() as db:
            data = db.session.query(Response).filter(Response.person_id == person_id, Response.question_id == question_id).first()

            return data

