from infra.configs.base import Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

import uuid

class Response(Base):
    __tablename__ = "response_table"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    response = Column(Integer, nullable=False)
    # this is an integer from 0 to 1 (no/yes)

    person_id = Column(String, ForeignKey("person_table.id"))
    person = relationship("Person", back_populates="responses")

    question_id = Column(String, ForeignKey("question_table.id"))
    question = relationship("Question", back_populates="responses")

    def __repr__(self):
        return f"<Response (id={self.id} response={self.response})>"
