from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger
from sqlalchemy.orm import relationship

from data_base.dbcore import Base
from models.answers import Answer


class Response(Base):
    __tablename__ = 'responses'

    id = Column(Integer, primary_key=True)
    quiz_session_id = Column(Integer, ForeignKey('quiz_sessions.id'))
    question_id = Column(Integer, ForeignKey('questions.id'))
    answer_id = Column(Integer, ForeignKey(Answer.id), nullable=True)
    poll_id = Column(BigInteger, nullable=True)
    options = Column(String, nullable=True)

    quiz_session = relationship('QuizSession',
                                back_populates='responses',
                                cascade='all, delete',
                                lazy='joined')
    question = relationship('Question',
                            back_populates='responses',
                            lazy='joined')
    answer = relationship('Answer',
                          back_populates='responses',
                          lazy='joined')

    def __init__(self, quiz_session_id, question_id) -> None:
        self.quiz_session_id = quiz_session_id
        self.question_id = question_id

    def __str__(self) -> str:
        return f'RESPONSE[ID:{self.id}, {self.question} - {self.answer}'
