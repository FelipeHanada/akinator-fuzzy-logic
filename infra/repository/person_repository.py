from infra.configs.connection import DBConnectionHandler
from infra.entities.person import Person

class PersonRepository:
    def select_all(self):
        with DBConnectionHandler() as db:
            data = db.session.query(Person).all()

            return data
