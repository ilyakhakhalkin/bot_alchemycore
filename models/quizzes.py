from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from data_base.dbcore import Base


class Quiz(Base):
    __tablename__ = 'quizzes'

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)

    questions = relationship(
        'Question',
        back_populates='quiz',
        cascade='all, delete',
        lazy='joined'
    )

    def __str__(self) -> str:
        return self.name
