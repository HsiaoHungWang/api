# from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.sql import select, insert, update, delete
from flask import Flask, request
from flask_restful import Api, Resource
from db import engine, users_table



# # 建立 SQLite 連線與資料表描述
# engine = create_engine('sqlite:///mydb.db', echo=True)
# metadata = MetaData()

# users_table = Table('Users', metadata,
#     Column('UserID', Integer, primary_key=True, autoincrement=True),
#     Column('username', String, nullable=False),
#     Column('userEmail', String, nullable=False, unique=True),
#     Column('userAge', Integer)
# )

# metadata.create_all(engine)  # 建立表格


class Users(Resource):
    def get(self):
        with engine.connect() as conn:
            query = select(users_table)
            result = conn.execute(query)
            users = [dict(row._mapping) for row in result]
            return users, 200

    def post(self):
        data = request.get_json()
        stmt = insert(users_table).values(
            username=data['username'],
            userEmail=data['userEmail'],
            userAge=data.get('userAge')
        )
        with engine.connect() as conn:
            result = conn.execute(stmt)
            conn.commit()
        return {'message': '使用者已新增'}, 201

class User(Resource):
    def get(self, id):
        stmt = select(users_table).where(users_table.c.UserID == id)
        with engine.connect() as conn:
            result = conn.execute(stmt).fetchone()
            if result:
                return dict(result._mapping), 200
            return {'message': '找不到使用者'}, 404

    def put(self, id):
        data = request.get_json()
        stmt = (
            update(users_table)
            .where(users_table.c.UserID == id)
            .values(username=data['username'],
                    userEmail=data['userEmail'],
                    userAge=data.get('userAge'))
        )
        with engine.connect() as conn:
            conn.execute(stmt)
            conn.commit()
        return {'message': '使用者已更新'}, 200

    def delete(self, id):
        stmt = delete(users_table).where(users_table.c.UserID == id)
        with engine.connect() as conn:
            conn.execute(stmt)
            conn.commit()
        return {'message': '使用者已刪除'}, 204
