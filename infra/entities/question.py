from infra.configs.base import Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

import uuid

class Question(Base):
    __tablename__ = "question_table"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    text = Column(String, nullable=False)

    responses = relationship("Response", back_populates="question")

    def __repr__(self):
        return f"<Question (id={self.id} text={self.text})>"
