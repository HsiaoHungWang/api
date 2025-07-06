from sqlalchemy import Table, Column, Integer, String
from . import metadata

categories_table = Table('SpotsCategories', metadata,
    Column('CategoryId', Integer, primary_key=True),
    Column('CategoryName', String)
)
