from sqlalchemy import Table, Column, Integer, String

from .metadata import metadata


quizzes = Table(
    'quizzes',
    metadata,
    Column('id', Integer(), primary_key=True),
    Column('name', String(20), unique=True),
)
