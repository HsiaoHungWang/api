from flask_restful import Resource
from flask import make_response, request
import time

class First(Resource):
    def get(self): 
        # time.sleep(5)
        response = make_response('Hello, Ajax!!')
        response.headers['Content-Type'] = 'text/plain'
        return response
    
    def post(self):      # POST /items
        pass

class Query(Resource):
    def get(self): 
        name = request.args.get('name')
        age = request.args.get('age')       
        response = make_response(f'Hello, {name}, You are {age} years old.')
        response.headers['Content-Type'] = 'text/plain'
        return response
       

   