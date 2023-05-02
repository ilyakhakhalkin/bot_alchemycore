from datetime import datetime

from sqlalchemy import (Table,
                        Column,
                        ForeignKey,
                        Integer,
                        DateTime,
                        Boolean,
                        String,
                        )

from .metadata import metadata


quiz_sessions = Table(
    'quiz_sessions',
    metadata,
    Column('id', Integer(), primary_key=True),
    Column('user_id',
           ForeignKey(
               'users.id',
               ondelete='CASCADE',
               onupdate='CASCADE',
               )
           ),
    Column('quiz_id',
           ForeignKey(
               'quizzes.id',
               ondelete='CASCADE',
               onupdate='CASCADE'
               )
           ),
    Column('date', DateTime(), default=datetime.now),
    Column('requested', Boolean(), default=False),
    Column('filepath', String(), default=None, nullable=True),
    Column('completed', Boolean(), default=False),
    Column('score', Integer(), default=0)
)
