from flask import Flask
from flask_restplus import Resource,Api,fields
import datetime
from functools import wraps
import jwt
from app import create_app
from ..services.db_handler import ServiceSpace
from app.secret import secrets 

app = create_app('Developing')
app.config['SECRET_KEY'] = secrets['jwt-key']
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
                encoded = jwt.encode({'gen-token': result}, app.config['SECRET_KEY'], algorithm='HS256')

                return {'token':encoded, 'user-id': result}

        except KeyError:
            return {'data':'Please enter the data as specified'}


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
