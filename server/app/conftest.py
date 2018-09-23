from flask import Flask
from flask_restplus import Api, Resource
import pytest
from .data_handler_test import DataSet

#Initialize the application
app = Flask(__name__)
app.config['TESTING'] = True
app.config['DEBUG'] = True

api = Api(app)

#For all Orders
class test_All(Resource):
    def get(self):
        '''Retrieves all items in the Dataset'''
        result = DataSet.get_all_orders(self)
        return {'data': result}, 200

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
        
#For populated entries
class test_populated(Resource):
    def get(self):
        '''Retrieves all items in the Dataset'''
        result = DataSet.get_present_orders(self)
        return {'data': result}, 200

#For Specific
class test_Specific(Resource):
    def get(self,num):
        '''Gets a specific order as requested'''
        result = DataSet.get_specific_entry(self, num)
        return {'data':result}

    def put(self,num):
        '''Use the unique id to edit an items details'''
        update_data = api.payload

        item_id = num
        name = update_data['name']
        description = update_data['Description']
        quantity = update_data['quantity']
        price = update_data['price']
        vendor = update_data['vendor']
        location = update_data['location']
        image = update_data['image']
        identifier = update_data['identifier']

        result = DataSet.update_entry(self,item_id,name,description,quantity,price,vendor,location,image,identifier)
        return {'data':result} 

    def delete(self,num):
        '''Delete an item passed by Admin of account'''
        delete_data = api.payload
        user_id = delete_data['uid']

        result = DataSet.delete_item(self,user_id,num)
        return {'data':{
            'delete_state': 'Successful',
            'available_data': result
        }}


api.add_resource(test_All, '/v1/orders') #Test for empty Orders
api.add_resource(test_populated, '/v1/orders/present') #Test for present Orders
api.add_resource(test_Specific, '/v1/orders/<int:num>')

@pytest.fixture
def create_test_app():
    '''Create a test app client'''
    test_app = app.test_client()

    yield test_app