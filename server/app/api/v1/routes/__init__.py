from flask import Flask,Blueprint
from flask_restplus import Resource,Api
from app import create_app      #Used . to import from a top level package

app = create_app('Developing')

api = Api(app)

#For all Orders
class All(Resource):
    def get(self):
        return '<h3>Get all entries</h3>'

    def post(self):
        return '<h3>Post an entry</h3>'

#For Specific
class Specific(Resource):
    def get(self,num):
        return '<h3>Get a specific entry number {} </h3>'.format(num)

    def put(self,num):
        return '<h3>Update specific entry number {} </h3>'.format(num) 

    def delete(self,num):
        return '<h3>Delete specific entry number {} </h3>'.format(num)

#For All Users
class AllUsers(Resource):
    def get(self):
        return 'all users'

#For a single user
class User(Resource):
    def get(self,info):
        return 'get specific customer'

    def post(self,info):
        return 'Register new customer' 

    def delete(self,info):
        return 'Deleted customer'


api.add_resource(All,'/v1/orders')
api.add_resource(Specific,'/v1/orders/<int:num>')
api.add_resource(AllUsers,'/v1/users')
api.add_resource(User,'/v1/user/<int:info')
