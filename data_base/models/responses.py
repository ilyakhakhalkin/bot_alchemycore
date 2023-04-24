from sqlalchemy import Table, Column, ForeignKey, Integer, BigInteger, String

from .metadata import metadata


responses = Table(
    'responses',
    metadata,
    Column('id', Integer(), primary_key=True),
    Column('quiz_session_id',
           ForeignKey(
               'quiz_sessions.id',
               ondelete='CASCADE',
               onupdate='CASCADE'
               )
           ),
    Column('question_id',
           ForeignKey(
               'questions.id',
               ondelete='CASCADE',
               onupdate='CASCADE'
               )
           ),
    Column('user_id',
           ForeignKey(
               'users.id',
               ondelete='CASCADE',
               onupdate='CASCADE'
               )
           ),
    Column('answer_id',
           ForeignKey(
               'answers.id',
               ondelete='CASCADE',
               onupdate='CASCADE'
               ),
           nullable=True
           ),
    Column('poll_id', BigInteger(), nullable=True),
    Column('options', String(), nullable=True)
)
