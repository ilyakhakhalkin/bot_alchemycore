from sqlalchemy import Table, Column, Integer, String, Boolean

from .metadata import metadata


users = Table(
    'users',
    metadata,
    Column('id', Integer(), primary_key=True),
    Column('username', String(), unique=True),
    Column('first_name', String()),
    Column('last_name', String),
    Column('is_admin', Boolean(), default=False),
)
