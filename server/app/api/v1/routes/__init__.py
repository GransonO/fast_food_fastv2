from flask import Flask,Blueprint
from flask_restplus import Resource,Api,fields
from app import create_app      #Used . to import from a top level package
from ..services.data_handler import DataSet  #package for data manipulations

app = create_app('Developing')

api = Api(app)
post_order = api.model('Posting Order',{'name':fields.String('Name of the item'),'Description' : fields.String('Brief description of the item'),
'quantity' : fields.Integer('Total count of items'),'price': fields.Integer('Selling price'),'vendor':fields.String('Name of Vendor'),
'location':fields.String('Where located'),'image':fields.String('Your image url'),'identifier':fields.String('The items key')})

#For all Orders
class All(Resource):
    def get(self):
        '''Retrieves all items in the Dataset'''
        result = DataSet.get_all_orders(self)
        return {'data': result}, 200

    @api.expect(post_order)
    def post(self):
        '''Adds a new item to the items list'''
        sent_data = api.payload
        name = sent_data['name']
        description = sent_data['Description']
        quantity = sent_data['quantity']
        price = sent_data['price']
        vendor = sent_data['vendor']
        location = sent_data['location']
        image = sent_data['image']
        identifier = sent_data['identifier']

        result = DataSet.add_new_entry(self,name,description,quantity,price,vendor,location,image,identifier)
        return {'data': result}
        

#For Specific
class Specific(Resource):
    def get(self,num):
        '''Gets a specific order as requested'''
        result = DataSet.get_specific_entry(self, num)
        return {'data':result}

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
api.add_resource(User,'/v1/user/<int:info>')
