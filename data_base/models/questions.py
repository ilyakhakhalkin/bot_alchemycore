from sqlalchemy import Table, Column, ForeignKey, Integer, String

from .metadata import metadata


questions = Table(
    'questions',
    metadata,
    Column('id', Integer(), primary_key=True),
    Column('text', String(), nullable=False),
    Column('quiz_id',
           ForeignKey('quizzes.id',
                      ondelete='CASCADE',
                      onupdate='CASCADE'
                      )
           ),
)
