from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from data_base.dbcore import Base


class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    text = Column(String, index=True)
    quiz_id = Column(Integer, ForeignKey('quizzes.id'))

    quiz = relationship('Quiz', back_populates='questions')
    answers = relationship('Answer',
                           back_populates='question',
                           cascade='all, delete',
                           lazy='joined')

    responses = relationship('Response',
                             back_populates='question',
                             cascade='all, delete',
                             lazy='joined')

    def __str__(self) -> str:
        return f'QUESTION[ID:{self.id}, TEXT:{self.text}]'
