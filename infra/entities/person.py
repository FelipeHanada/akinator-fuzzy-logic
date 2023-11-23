from infra.configs.base import Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

import uuid

class Person(Base):
    __tablename__ = "person_table"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    name = Column(String, nullable=False)

    responses = relationship("Response", back_populates="person")

    def __repr__(self):
        return f"<Person (id={self.id} name={self.name})>"
