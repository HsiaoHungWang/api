from sqlalchemy import Table, Column, Integer, String
from . import metadata

members_table = Table("members", metadata,
    Column("MemberId", Integer, primary_key=True, autoincrement=True),
    Column("Name", String),
    Column("Email", String),
    Column("Age", Integer),
    Column("FileName", String),
    Column("Password", String)
)