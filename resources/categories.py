from sqlalchemy.sql import select, insert, update, delete
from flask import Flask, request
from flask_restful import Api, Resource
from db import engine, categories_table

class Categories(Resource):
    def get(self):
        stmt = select(categories_table)
        with engine.connect() as conn:
            result = conn.execute(stmt)
            
            return [dict(row._mapping) for row in result], 200

        
