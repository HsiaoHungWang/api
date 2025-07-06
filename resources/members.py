# # resources/members.py
# from flask_restful import Resource, reqparse
# from flask import request
from werkzeug.utils import secure_filename
# from sqlalchemy import insert, select, update, delete
# from db.engine import engine
# from db.tables.members_table import members_table
from flask_bcrypt import Bcrypt
from sqlalchemy.sql import select, insert, update, delete
from flask import Flask, request
from flask_restful import Api, Resource
from db import engine, members_table

import os

bcrypt = Bcrypt()

# UPLOAD_FOLDER = 'avatars'  # 確保這個資料夾存在
UPLOAD_FOLDER = os.path.join('static', 'avatars')
class Members(Resource):
    def get(self):
        stmt = select(members_table)
        with engine.connect() as conn:
            result = conn.execute(stmt)
            data = [dict(row._mapping) for row in result]
        
        return data, 200
        # return {"members": data}, 200

    def post(self):
        name = request.form.get("Name")
        email = request.form.get("Email")
        age = request.form.get("Age")
        password = request.form.get("Password")

        # 檔案欄位
        file = request.files.get("File")
        filename = None
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))

        hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")

        stmt = insert(members_table).values(
            Name=name,
            Email=email,
            Age=age,
            FileName=filename,
            Password=hashed_pw
        )

        with engine.connect() as conn:
            conn.execute(stmt)
            conn.commit()

        return {"message": "Member created"}, 201

class Member(Resource):
    def get(self, id):
        stmt = select(members_table).where(members_table.c.MemberId == id)
        with engine.connect() as conn:
            result = conn.execute(stmt).fetchone()
            if result:
                return dict(result._mapping), 200
            return {'message': '找不到使用者'}, 404
        
    def put(self, id):
        mid = request.form.get("MemberId")
        name = request.form.get("Name")
        email = request.form.get("Email")
        age = request.form.get("Age")  

        update_data = { 
            "Name": name,
            "Email": email,
            "Age": age
        }
       
        stmt = update(members_table).where(members_table.c.MemberId == mid).values(**update_data)

        with engine.connect() as conn:
            conn.execute(stmt)
            conn.commit()

        return {"message": "Member updated"}, 200

    def delete(self, id):    
        stmt = delete(members_table).where(members_table.c.MemberId == id)

        with engine.connect() as conn:
            conn.execute(stmt)
            conn.commit()

        return {"message": "Member deleted"}, 200