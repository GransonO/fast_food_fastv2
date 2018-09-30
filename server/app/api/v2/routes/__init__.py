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
order_request = api.model('User Order request', { 'order_to': fields.String('The vendor of the item'), 'order_amount': fields.String('The total transaction amount') , 'order_detail': fields.String('Brief description of the order') })
put_item_details = api.model('Admin updating request', {'status': fields.String('Order status. Can be either NEW(CUSTOMER), PROCESSING(AUTO), COMPLETED(ADMIN), CANCELLED(ADMIN)') })
new_item_details = api.model('New Item Posting', { 'item_name': fields.String('Name of item'), 'details': fields.String('Brief description of item'),'price' : fields.String('Price of the item'), 'image_url':fields.String('Url to hosted item\'s image')})

#Authentication for all users decorator
def authorize_user(func):
    @wraps(func)
    def decorate_func(*args,**kwargs):
        if 'APP-LOGIN-KEY' in request.headers:
            logged_in_token = request.headers['APP-LOGIN-KEY']
            print('The token is {}'.format(logged_in_token))

            try: 
                decode_token(logged_in_token)

            except:
                return {'Token passed is invalid'}
        else:
            return 'No logged in key passed'
        return func(*args, **kwargs)    

    return decorate_func 

#Authentication for Admin decorator
def authorize_admin(adm):
    @wraps(adm)
    def decorate_adm(*args,**kwargs):
        if 'ADMIN-KEY' in request.headers:
            logged_in_token = request.headers['ADMIN-KEY']
            print('The admin token is {}'.format(logged_in_token))

            try: 
                decode_token(logged_in_token)

            except:
                return {'Admin token passed is invalid'}
        else:
            return 'No Admin key passed'
        return adm(*args, **kwargs)    

    return decorate_adm 

def decode_token(token):
    '''Decode token for other functions'''
    user_details = jwt.decode(token, app.config['SECRET_KEY'])
    user_id = user_details['token'] #User token to be used in subsequent requests
    return user_id

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
                print(result)
                if result['password']:
                    encoded = jwt.encode({'token': result['user_id']}, app.config['SECRET_KEY'], algorithm='HS256')
                    print(encoded)
                    return {'response':'login success','login_token': encoded.decode('UTF-8')}              

                else:
                    return {'responce':'Could not find your account. Please try again'}

        except KeyError:
            return {'data':'Please enter the data as specified'}

#Authentication sign up
class Auth_Sign_Up(Resource):

    @api.expect(auth_sign_up)
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
                    return {'response' : 'Sorry {}, the type value passed cannot be processed'.format(name)}

                else:

                    result = ServiceSpace.Add_user_to_db(self,type,name,password,vendor_name,phone_no,email,about,location,image_url)
                    if (result > 0):
                        response = 'Thanks {} for creating an account with us.'.format(name)
                        return {'data': response}, 201 #Created 

                    else:
                        return {'data':'Sorry {} could not create an account for you. Try again or contact a human(0712 288 371) for assistance'.format(name)}    

        except KeyError:
            return {'data':'Please enter the data as specified'}

#Users orders requests
class UsersOrders(Resource):
    
    @api.doc(security='logged_in_key') # Added to functions that require token access.
    @authorize_user
    def get(self):
        ''' Users get the order history for a particular user'''
        logged_in_token = request.headers['APP-LOGIN-KEY']
        customer_id = decode_token(logged_in_token)
        result = ServiceSpace.get_all_orders(self,customer_id)
        return {'data':result}, 200 #Return list with all customer items details

    @api.expect(order_request)    
    @api.doc(security='logged_in_key')
    @authorize_user
    def post(self):
        '''Users place an order for food'''
        sent_data = api.payload
        try:
            if(sent_data == {}):
                return {'data': 'You cant send an empty request'}
            else:
                logged_in_token = request.headers['APP-LOGIN-KEY']
                customer_id = decode_token(logged_in_token)
                order_detail = sent_data['order_detail']
                order_amount = sent_data['order_amount']
                order_from = customer_id
                order_to = sent_data['order_to']
                result = ServiceSpace.add_order_to_db(self,order_detail,order_amount,order_from,order_to)
                return {'data': result}    

        except KeyError:
            return {'data':'Please enter the data as specified'}

#Admin Actions
class AdminAllOrders(Resource):
    @api.doc(security='admin-key') # Added to functions that require token access.
    @authorize_admin
    def get(self):
        ''' Admin get all orders placed (Admin Only)'''
        logged_in_token = request.headers['ADMIN-KEY']
        admin_id = decode_token(logged_in_token)
        result = ServiceSpace.get_all_admin_orders(self,admin_id)
        return {'data':result}


#Admin Specific Actions
class AdminSpecificOrders(Resource):
    
    @api.doc(security='admin-key') # Added to functions that require token access.
    @authorize_admin
    def get(self,order_id):
        '''Get a specific order ( By Admin Only)'''
        result = ServiceSpace.get_specific_order(self,order_id)
        return {'data':result}

    @api.expect(put_item_details)    
    @api.doc(security='admin-key')
    @authorize_admin
    def put(self,order_id):
        '''Update the status of an order (Admin Only)'''
        sent_data = api.payload
        try:
            if(sent_data == {}):
                return {'data': 'You cant send an empty request'}
            else:
                status  = sent_data['status']
                result = ServiceSpace.update_an_item(self,status,order_id)
                return {'data': result}    

        except KeyError:
            return {'data':'Please enter the data as specified'}

#Menu Requesting
class RequestMenu(Resource):
    def get(self):
        '''Preview items of a specific restaurant'''      
        result = ServiceSpace.get_all_vendor_items(self)
        return {'data':result}

    @api.expect(new_item_details)
    @api.doc(security='admin-key')
    @authorize_admin
    def post(self):
        '''Add a meal option to the menu (Admin)'''
        sent_data = api.payload
        try:
            if(sent_data == {}):
                return {'data': 'You cant post an empty request'}
            else:
                logged_in_token = request.headers['ADMIN-KEY']
                vendor_id = decode_token(logged_in_token)
                item_name = sent_data['item_name']
                details = sent_data['details']
                price = sent_data['price']
                image_url  = sent_data['image_url']
                result = ServiceSpace.add_an_item_to_tbl(self,vendor_id,item_name,details,price,image_url)
                return {'data': result} 

        except KeyError:
            return {'data':'Please enter the data as specified'}


#Authentication
api.add_resource(Auth_Sign_Up,'/auth/signup')
api.add_resource(Auth_Login,'/auth/login')

#Users actions
api.add_resource(UsersOrders,'/users/orders')

#Administrators
api.add_resource(AdminAllOrders,'/orders/')
api.add_resource(AdminSpecificOrders,'/orders/<int:order_id>')

#Menu 
api.add_resource(RequestMenu,'/menu')