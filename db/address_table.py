from sqlalchemy import Table, Column, Integer, String
from . import metadata

address_table = Table('Address', metadata,
    Column('id', Integer, primary_key=True),
    Column('city', String),
    Column('site_id', String),
    Column('road', String)
)
