from flask import Flask
from flask_restful import Api, Resource
from flask_cors import CORS

from resources.hello import HelloWorld
from resources.first import First, Query
from resources.items import Item, Items
from resources.users import User, Users
from resources.address import DistinctCities, SiteIdsByCity, RoadsBySiteId
from resources.spots import Spots,SpotCategoryStats,SpotsByDistrict
from resources.categories import Categories
from resources.members import Members, Member
from resources.image import Image, Base64Image


app = Flask(__name__)
CORS(app)
api = Api(app)

# @app.route('/')
# def index():
#     return "Hello, Flask!!"

# class HelloWorld(Resource):
#     def get(self):
#         return {'message':'Hello, API!!'}
    
api.add_resource(HelloWorld, '/')
api.add_resource(First, '/api')
api.add_resource(Query, '/api/query')
api.add_resource(Items, '/api/items')
api.add_resource(Item, '/api/items/<int:id>')
api.add_resource(Users, '/api/users')
api.add_resource(User, '/api/users/<int:id>')
api.add_resource(DistinctCities, '/api/cities')
api.add_resource(SiteIdsByCity, '/api/sites')
api.add_resource(RoadsBySiteId, '/api/roads')
api.add_resource(Spots,'/api/spots' )
api.add_resource(SpotCategoryStats,'/api/spot-category-stats' )
api.add_resource(SpotsByDistrict, '/api/spot-district')
api.add_resource(Categories, '/api/categories')
api.add_resource(Members, '/api/members')
api.add_resource(Member, '/api/members/<int:id>')
api.add_resource(Image, '/api/image')
api.add_resource(Base64Image, '/api/image/base64')

if __name__=='__main__':
    app.run()