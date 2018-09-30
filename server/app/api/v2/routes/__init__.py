from flask import Flask, request
from flask_restplus import Resource,Api,fields
import datetime
from functools import wraps
import jwt
from app import create_app
from ..services.db_handler import ServiceSpace
from app.secret import secrets 

app = create_app('Developing')
app.config['SECRET_KEY'] = secrets['jwt-key']

authorize_properties = {
    'logged_in_key' : { #For logged in operations
        'type': 'apiKey',
        'in' : 'header',
        'name':'APP-LOGIN-KEY'
    }
    ,
    'admin-key' :{ # For admin operations
        'type': 'apiKey',
        'in' : 'header',
        'name':'ADMIN-KEY'        
    }
}

api = Api(app, authorizations=authorize_properties)

auth_login_ = api.model('User Login',{'type': fields.String('The user can be either ADMIN or CUSTOMER'),'name': fields.String('The username registered'),'password': fields.String('The users password')})
auth_sign_up = api.model('User Sign Up',{'type': fields.String('The user can be either "ADMIN" or "CUSTOMER"'),'name': fields.String('The username registered'),'vendor_name': fields.String('The if user is Admin'),'password': fields.String('The users password'),'about': fields.String('Brief Users description'),'location': fields.String('The users location'),'image_url': fields.String('The users uploaded image'),'phone_no': fields.String('The users phone number'),'email': fields.String('The users email')})
order_history = api.model('User Order history', { 'username': fields.String('The users name'), 'public-key': fields.String('The users public key, sent alongside the jtoken') })
order_request = api.model('User Order request', { 'order_to': fields.String('The vendor of the item'), 'order_from': fields.String('The users public key, sent alongside the jtoken'), 'order_amount': fields.String('The total transaction amount') , 'order_detail': fields.String('Brief description of the order') })

#item_details = api.model()
#put_item_details = api.model()
#Authentication login

def authorize_user(func):
    @wraps(func)
    def decorate_func(*args,**kwargs):
        if 'APP-LOGIN-KEY' in request.headers:
            logged_in_token = request.headers['APP-LOGIN-KEY']
            print('The token is {}'.format(logged_in_token))

            try: 
                user_id = jwt.decode(logged_in_token, app.config['SECRET_KEY'])
                #current_user = User.query.filter_by(public_id=data['public_id']).first()
                print('The user id is : {}'.format(user_id))
            except:
                return {'Token passed is invalid'}
        else:
            return 'No logged in key passed'
        return func(*args, **kwargs)    

    return decorate_func  

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
                print(result)
                if result['password']:
                    encoded = jwt.encode({'gen-token': result['user_id']}, app.config['SECRET_KEY'], algorithm='HS256')
                    print(encoded)
                    return {'login_token': encoded.decode('UTF-8')}              

                else:
                    return {'responce':'Could not find your account. Please try again'}, 301

        except KeyError:
            return {'data':'Please enter the data as specified'}


#Authentication sign up
class Auth_Sign_Up(Resource):

    @api.expect(auth_sign_up)
    @api.doc(security='logged_in_key') # Added to functions that require token access.
    @authorize_user
    def post(self):
        '''Users Authentication First time sign up'''
        sent_data = api.payload
        allowed = ['ADMIN','CUSTOMER','ADMINISTRATOR','USER']
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

                if type not in allowed:
                    return {'response' : 'The type passed cannot be processed'}

                else:

                    result = ServiceSpace.Add_user_to_db(self,type,name,password,vendor_name,phone_no,email,about,location,image_url)
                    if (result > 0):
                        response = 'Thanks {} for creating an account with us.'.format(name)
                        return {'data': response}, 201 #Created 

                    else:
                        return {'data':'Sorry {} could not create your account. Try again or contact a human(0712 288 371) for assistance'.format(name)}    

        except KeyError:
            return {'data':'Please enter the data as specified'}





#Authentication
api.add_resource(Auth_Sign_Up,'/auth/signup')
api.add_resource(Auth_Login,'/auth/login')
