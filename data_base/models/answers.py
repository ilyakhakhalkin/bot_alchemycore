from sqlalchemy import Table, Column, ForeignKey, Integer, String, Boolean

from .metadata import metadata


answers = Table(
    'answers',
    metadata,
    Column('id', Integer(), primary_key=True),
    Column('question_id',
           ForeignKey(
               'questions.id',
               ondelete='CASCADE',
               onupdate='CASCADE'
            )
           ),
    Column('text', String(), nullable=False),
    Column('is_correct', Boolean(), default=False)
)
