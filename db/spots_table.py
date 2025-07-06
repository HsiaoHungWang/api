from sqlalchemy import Table, Column, Integer, String, Text
from . import metadata

spots_table = Table('Spots', metadata,
    Column('SpotId', Integer, primary_key=True, autoincrement=True),
    Column('SpotTitle', String(100), nullable=False),
    Column('Address', String(200), nullable=False),
    Column('SpotDescription', Text, nullable=True),
    Column('CategoryId', Integer, nullable=True),
    Column('Longitude',Text),
    Column('Latitude',Text),
    Column('SpotImage', String(200), nullable=False)
)