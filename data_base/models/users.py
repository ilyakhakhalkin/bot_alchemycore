from sqlalchemy import Table, Column, String, Boolean, BigInteger

from .metadata import metadata


users = Table(
    'users',
    metadata,
    Column('id', BigInteger(), primary_key=True),
    Column('username', String(), unique=True, nullable=True),
    Column('first_name', String(), nullable=False),
    Column('last_name', String(), nullable=True),
    Column('full_name', String(), nullable=False),
    Column('is_admin', Boolean(), default=False),
    Column('blocked', Boolean(), default=False),
)
