from sqlalchemy import Column, Integer, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship

from data_base.dbcore import Base


class QuizSession(Base):
    __tablename__ = 'quiz_sessions'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    score = Column(Integer, default=0)
    requested = Column(Integer, default=0)
    keep = Column(Integer, default=0)

    user_id = Column(Integer, ForeignKey('users.id'))
    quiz_id = Column(Integer, ForeignKey('quizzes.id'))
    
    user = relationship('User', back_populates='quiz_sessions', lazy='joined')
    quiz = relationship('Quiz', lazy='joined')
    responses = relationship('Response',
                             back_populates='quiz_session',
                             cascade='all, delete',
                             lazy='joined')

    def __init__(self, user_id, quiz_id) -> None:
        self.user_id = user_id
        self.quiz_id = quiz_id

    def __str__(self) -> str:
        return f'QUIZ_SESSION[ID:{self.id}, USER_ID:{self.user_id}]'
