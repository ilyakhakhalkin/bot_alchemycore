from sqlalchemy import Table, Column, ForeignKey, Integer, BigInteger, String

from .metadata import metadata


responses = Table(
    'responses',
    metadata,
    Column('id', Integer(), primary_key=True),
    Column('quiz_session_id', ForeignKey('quiz_sessions.id')),
    Column('question_id', ForeignKey('questions.id')),
    Column('user_id', ForeignKey('users.id')),
    Column('answer_id', ForeignKey('answers.id'), nullable=True),
    Column('poll_id', BigInteger(), nullable=True),
    Column('options', String(), nullable=True)
)
