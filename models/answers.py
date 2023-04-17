from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from data_base.dbcore import Base


class Answer(Base):
    __tablename__ = 'answers'

    id = Column(Integer, primary_key=True)
    text = Column(String, index=True)
    is_correct = Column(Boolean)
    questions_id = Column(Integer, ForeignKey('questions.id'))

    question = relationship(
        'Question',
        back_populates='answers',
        lazy='joined'
    )

    responses = relationship(
        'Response',
        back_populates='answer',
        cascade='all, delete',
        lazy='joined'
    )

    def __str__(self) -> str:
        return f'ANSWER[ID:{self.id} TEXT:{self.text}]'
