from sqlalchemy import Table, Column, Integer, String
from . import metadata

users_table = Table('Users', metadata,
    Column('UserID', Integer, primary_key=True, autoincrement=True),
    Column('username', String, nullable=False),
    Column('userEmail', String, nullable=False, unique=True),
    Column('userAge', Integer)
)