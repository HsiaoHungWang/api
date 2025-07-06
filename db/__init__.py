from sqlalchemy import create_engine, MetaData

engine = create_engine('sqlite:///mydb.db', echo=True)
metadata = MetaData()

# 在這裡統一匯入其他表格，確保它們被註冊到 metadata
from .users_table import users_table
from .address_table import address_table
from .spots_table import spots_table
from .categories_table import categories_table
from .members_table import members_table

metadata.create_all(engine)