from flask import Flask
from flask_restplus import Resource,Api,fields
import datetime
from functools import wraps

from app import create_app
from ..services.db_handler import ServiceSpace
from app.secret import all_secrets 

#import jwt 


app = create_app('Developing')
app.config['SECRET_KEY'] = all_secrets['jwt-key']
api = Api(app)

auth_login_ = api.model('User Login',{'type': fields.String('The user can be either ADMIN or CUSTOMER'),'name': fields.String('The username registered'),'password': fields.String('The users password')})
auth_sign_up = api.model('User Sign Up',{'type': fields.String('The user can be either "ADMIN" or "CUSTOMER"'),'name': fields.String('The username registered'),'vendor_name': fields.String('The if user is Admin'),'password': fields.String('The users password'),'about': fields.String('Brief Users description'),'location': fields.String('The users location'),'image_url': fields.String('The users uploaded image'),'phone_no': fields.String('The users phone number'),'email': fields.String('The users email')})
order_history = api.model('User Order history', { 'username': fields.String('The users name'), 'public-key': fields.String('The users public key, sent alongside the jtoken') })
order_request = api.model('User Order request', { 'order_to': fields.String('The vendor of the item'), 'order_from': fields.String('The users public key, sent alongside the jtoken'), 'order_amount': fields.String('The total transaction amount') , 'order_detail': fields.String('Brief description of the order') })

#item_details = api.model()
#put_item_details = api.model()
#Authentication login
class Auth_Login(Resource):

    @api.expect(auth_login_)
    def post(self):
        '''Users Authentication login'''
        sent_data = api.payload
        try:
            if(sent_data == {}):
                return {'data': 'You cant send an empty request'}
            else:
                #Implement the JWT Authorization here
                type = sent_data['type']
                name = sent_data['name']
                password = sent_data['password']

                result = ServiceSpace.retrieve_user(self,type,name,password)
                return {'token':'This will be the token', 'user-id': result}

        except KeyError:
            return {'data':'Please enter the data as specified'}

        except:
            return {'data':'Your data could not be posted, are you trying something clever?'}

#Authentication sign up
class Auth_Sign_Up(Resource):

    @api.expect(auth_sign_up)
    def post(self):
        '''Users Authentication First time sign up'''
        sent_data = api.payload
        try:
            if(sent_data == {}):
                return {'data': 'You cant send an empty request'}
            else:
                type = sent_data['type']
                name = sent_data['name']
                password = sent_data['password']
                vendor_name = sent_data['vendor_name']
                phone_no  = sent_data['phone_no']
                email = sent_data['email']
                about = sent_data['about']
                location = sent_data['location']
                image_url = sent_data['image_url']

                result = ServiceSpace.Add_user_to_db(self,type,name,password,vendor_name,phone_no,email,about,location,image_url)
                return {'data': result}    

        except KeyError:
            return {'data':'Please enter the data as specified'}


#Users data Interactions
class UsersOrders(Resource):
    
    @api.expect(order_history)
    def get(self):
        ''' Users get the order history for a particular user'''
        #Customer ID passed from the payload in headers after login
        sent_data = api.payload
        customer_id = sent_data['user_id']
        result = ServiceSpace.get_all_orders(self,customer_id)
        return {'data':result}

    @api.expect(order_request)
    def post(self):
        '''Users place an order for food'''
        sent_data = api.payload
        try:
            if(sent_data == {}):
                return {'data': 'You cant send an empty request'}
            else:
                order_detail = sent_data['order_detail']
                order_amount = sent_data['order_amount']
                order_from = sent_data['order_from']
                order_to = sent_data['order_to']
                order_status  = sent_data['order_status']
                result = ServiceSpace.add_order_to_db(self,order_detail,order_amount,order_from,order_to,order_status)
                return {'data': result}    

        except KeyError:
            return {'data':'Please enter the data as specified'}


#Admin Actions
class AdminAllOrders(Resource):
    ''' Admin get all orders placed (Admin Only)'''
    def get(self):
        sent_data = api.payload
        admin_id = sent_data['user_id']
        result = ServiceSpace.get_all_admin_orders(self,admin_id)
        return {'data':result}


#Admin Specific Actions
class AdminSpecificOrders(Resource):
    
    #@api.expect(item_details)
    def post(self,num):
        '''Add item to item table ( By Admin Only)'''
        sent_data = api.payload
        try:
            if(sent_data == {}):
                return {'data': 'You cant send an empty request'}
            else:
                order_detail = sent_data['order_detail']
                order_amount = sent_data['order_amount']
                order_from = sent_data['order_from']
                order_to = sent_data['order_to']
                order_status  = sent_data['order_status']
                result = ServiceSpace.add_order_to_db(self,order_detail,order_amount,order_from,order_to,order_status)
                return {'data': result}    

        except KeyError:
            return {'data':'Please enter the data as specified'}
        
    #@api.expect(put_item_details)
    def put(self,num):
        '''Update the status of an order (Admin Only)'''
        sent_data = api.payload
        try:
            if(sent_data == {}):
                return {'data': 'You cant post an empty request'}
            else:
                id = sent_data['id']
                item_name = sent_data['item_name']
                details = sent_data['details']
                price = sent_data['price']
                image_url  = sent_data['image_url']
                item_id  = sent_data['item_id']
                result = ServiceSpace.update_an_item(self,id,item_name,details,price,image_url,item_id)
                return {'data': result}    

        except KeyError:
            return {'data':'Please enter the data as specified'}

#Menu Requesting
class RequestMenu(Resource):
    def get(self):
        '''Preview items of a specific restaurant'''
        sent_data = api.payload
        user_id = sent_data['user_id']
        vendor_name = sent_data['vendor_name']        
        result = ServiceSpace.get_all_vendor_items(self,vendor_name)
        return {'data':result}
    
    def post(self):
        '''Add a meal option to the menu (Admin)'''
        sent_data = api.payload
        try:
            if(sent_data == {}):
                return {'data': 'You cant post an empty request'}
            else:
                id = sent_data['id']
                item_name = sent_data['item_name']
                details = sent_data['details']
                price = sent_data['price']
                image_url  = sent_data['image_url']
                item_id  = sent_data['item_id']
                result = ServiceSpace.update_an_item(self,id,item_name,details,price,image_url,item_id)
                return {'data': result}    

        except KeyError:
            return {'data':'Please enter the data as specified'}


#Authentication
api.add_resource(Auth_Sign_Up,'/auth/signup')
api.add_resource(Auth_Login,'/auth/login')

#Users actions
api.add_resource(UsersOrders,'/users/orders')

#Administrators
api.add_resource(AdminAllOrders,'/orders/ ')
api.add_resource(AdminSpecificOrders,'/orders/<int:num> ')

#Menu 
api.add_resource(RequestMenu,'/menu ')
