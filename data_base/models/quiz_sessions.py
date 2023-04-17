from datetime import datetime

from sqlalchemy import Table, Column, ForeignKey, Integer, DateTime

from .metadata import metadata


quiz_sessions = Table(
    'quiz_sessions',
    metadata,
    Column('id', Integer(), primary_key=True),
    Column('user_id', ForeignKey('users.id')),
    Column('quiz_id', ForeignKey('quizzes.id')),
    Column('date', DateTime(), default=datetime.now)
)
