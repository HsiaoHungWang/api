from sqlalchemy.sql import select, insert, update, delete
from flask import Flask, request
from flask_restful import Api, Resource
from db import engine, address_table

class DistinctCities(Resource):
    def get(self):
        stmt = select(address_table.c.city).distinct()
        with engine.connect() as conn:
            result = conn.execute(stmt)
            # return {'cities': [row.city for row in result]}, 200
            return [row.city for row in result], 200

class SiteIdsByCity(Resource):
    def get(self):
        city = request.args.get('city')        
        stmt = (
            select(address_table.c.site_id)
            .where(address_table.c.city == city)
            .distinct()
        )
        with engine.connect() as conn:
            result = conn.execute(stmt)
            # return {'site_ids': [row.site_id for row in result]}, 200
            return [row.site_id for row in result], 200
        
class RoadsBySiteId(Resource):
    def get(self):
        site_id = request.args.get('site_id')       
        stmt = (
            select(address_table.c.road)
            .where(address_table.c.site_id == site_id)
            .distinct()
        )
        with engine.connect() as conn:
            result = conn.execute(stmt)
            # return {'roads': [row.road for row in result]}, 200
            return [row.road for row in result], 200