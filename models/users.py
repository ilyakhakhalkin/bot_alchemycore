from sqlalchemy import Column, String, Integer, BigInteger
from sqlalchemy.orm import relationship

from data_base.dbcore import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True)
    username = Column(String, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    is_admin = Column(Integer, index=True, default=False)
    
    quiz_sessions = relationship('QuizSession',
                                 order_by='desc(QuizSession.id)',
                                 back_populates='user',
                                 cascade='all, delete',
                                 lazy='joined')

    def __init__(self, id, username, first_name, last_name) -> None:
        self.id = id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name

    def __str__(self) -> str:
        return f"{getattr(self, 'username', '')} {getattr(self, 'first_name', '')} {getattr(self, 'last_name', '')} {getattr(self, 'id', '')}"
