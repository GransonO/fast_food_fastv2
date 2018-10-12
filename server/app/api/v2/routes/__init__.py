from flask import Flask, request
from flask_restplus import Resource,Api,fields
import datetime
from functools import wraps
import jwt
from app import create_app
from ..services.db_handler import ServiceSpace
from app.secret import secrets 
from .validators import Validation

app_state = 'Testing'  #'Developing','Testing','Production'
app = create_app(app_state)
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

api = Api(app, version='1.2', title='Fast Food Fast API', description='The Fast food fast APIs are for your daily food usage. Think Eatout, Revamped !!!',contact_email= 'oyombegranson@gmail.com',  default ='Fast Food Fast', default_label='All backend API operations', authorizations=authorize_properties )

auth_login_ = api.model('User Login',{'type': fields.String('The user can be either ADMIN or CUSTOMER'),'name': fields.String('The username registered'),'password': fields.String('The users password')})
auth_sign_up = api.model('User Sign Up',{'type': fields.String('The user can be either "ADMIN" or "CUSTOMER"'),'name': fields.String('The username registered'),'vendor_name': fields.String('The if user is Admin'),'password': fields.String('The users password'),'about': fields.String('Brief Users description'),'location': fields.String('The users location'),'image_url': fields.String('The users uploaded image'),'phone_no': fields.String('The users phone number'),'email': fields.String('The users email')})
order_request = api.model('User Order request', { 'order_to': fields.String('The vendor of the item'), 'order_amount': fields.Float('The total transaction amount') , 'order_detail': fields.String('Brief description of the order') })
put_item_details = api.model('Admin updating request', {'status': fields.String('Order status. Can be either NEW(CUSTOMER), PROCESSING(AUTO), COMPLETED(ADMIN), CANCELLED(ADMIN)') })
new_item_details = api.model('New Item Posting', { 'item_name': fields.String('Name of item'), 'details': fields.String('Brief description of item'),'price' : fields.Float('Price of the item'), 'image_url':fields.String('Url to hosted item\'s image')})

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
            return {'response':'Authorization error','status':0,'data':'No logged in key passed'},401
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
                return {'response':'Authorization error','status':0,'data':'Admin token passed is invalid'}
        else:
            return {'response':'Authorization error','status':0,'data':'No Admin key passed'}
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
        allowed = ['ADMIN','CUSTOMER']

        try:
            if(sent_data == {}):
                return {'response':'Entry error','data': 'You cant send an empty request'}, 403
            else:
                #Implement the JWT Authorization here
                type = sent_data['type']
                if type in allowed:

                    name = sent_data['name']
                    password = sent_data['password']

                    result = ServiceSpace.retrieve_user(self,type,name,password,app_state) 
                    
                    if result['password']:
                        encoded = jwt.encode({'token': result['user_id']}, app.config['SECRET_KEY'], algorithm='HS256')
                        print(encoded)
                        return {'response':'login success','login_token': encoded.decode('UTF-8'),'status':1}, 202             

                    else:
                        return {'response':'Your username or password may be wrong','status':0}, 401
                else:
                    return {'response':'The passed type is not allowed','status':0}, 405

        except KeyError:
            return {'response':'Please enter the data as specified','status':0}, 400

#Authentication sign up
class Auth_Sign_Up(Resource):

    @api.expect(auth_sign_up)
    def post(self):
        '''Users Authentication First time sign up'''
        sent_data = api.payload
        allowed = ['ADMIN','CUSTOMER']
        try:
            if(sent_data == {}):
                return {'response': 'You cant send an empty request','status':0}, 403
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

                
                mail_valid = Validation.email_Validation(self,email)
                pass_valid = Validation.password_Validation(self,password)
                if mail_valid == None:
                    return {'response': 'Email does not conform to standards( yyy@xxx.(com or co.ke))','status':0}, 400
                
                if pass_valid != 'Pass':
                    return {'response': pass_valid,'status':0}, 400

                if type not in allowed:
                    return {'response' : 'Sorry {}, the type value passed cannot be processed'.format(name),'status':0}, 400

                else:

                    result = ServiceSpace.Add_user_to_db(self,type,name,password,vendor_name,phone_no,email,about,location,image_url,app_state)
                    if (result['result'] == 'Success'):
                        response = 'Thanks {} for creating an {} account with us.'.format(name,type)
                        data = result['data']
                        return {'response': response,'data': data,'status':1}, 201 #Created 

                    else:
                        return {'response':'Sorry {} could not create an account for you. Try again or contact a human(0712 288 371) for assistance'.format(name),'status':0}, 204    

        except KeyError:
            return {'response':'Please enter the data as specified','status':0}, 400

#Users orders requests
class UsersOrders(Resource):
    
    @api.doc(security='logged_in_key') # Added to functions that require token access.
    @authorize_user
    def get(self):
        ''' Users get the order history for a particular user'''
        logged_in_token = request.headers['APP-LOGIN-KEY']
        customer_id = decode_token(logged_in_token)
        result = ServiceSpace.get_all_raw_orders(self,customer_id,app_state)
        return {'response':'Retrieving {} entries'.format(len(result)),'data':result,'status':1}, 200 #Return list with all customer items details

    @api.expect(order_request)    
    @api.doc(security='logged_in_key')
    @authorize_user
    def post(self):
        '''Users place an order for food'''
        sent_data = api.payload
        try:
            if(sent_data == {}):
                return {'response':'Order Error','status':0,'data': 'You can\'t send an empty request'}, 204
            else:
                logged_in_token = request.headers['APP-LOGIN-KEY']
                customer_id = decode_token(logged_in_token)
                order_detail = sent_data['order_detail']
                order_amount = sent_data['order_amount']
                order_from = customer_id
                order_to = sent_data['order_to']
                result = ServiceSpace.add_order_to_db(self,order_detail,order_amount,order_from,order_to,app_state)
                return {'response':'Order Created','status':1,'results': result}, 201    

        except KeyError:
            return {'response':'Order Error','status':0,'data':'Please enter the data as specified'}, 400


#Users orders requests
class UsersOrdersGet(Resource):
    
    @api.doc(security='logged_in_key') # Added to functions that require token access.
    @authorize_user
    def get(self,status):
        ''' Users get the order history for a particular user in particular state'''
        allowed = ['NEW','PROCESSING', 'COMPLETED', 'CANCELLED']
        status = status.upper()        
        if status not in allowed:
             return {'response':'Request Error','status':0,'data':'Only {} allowed'.format(allowed)}, 200

        logged_in_token = request.headers['APP-LOGIN-KEY']
        customer_id = decode_token(logged_in_token)
        result = ServiceSpace.get_all_orders(self,customer_id,app_state,status)
        return {'response':'Retrieving {} entries'.format(len(result)),'data':result,'status':1}, 200 #Return list with all customer items details


#Admin Actions
class AdminAllOrders(Resource):
    @api.doc(security='admin-key') # Added to functions that require token access.
    @authorize_admin
    def get(self,status):
        '''Get orders as specified ~NEW,PROCESSING, COMPLETED, CANCELLED~ '''
        allowed = ['NEW','PROCESSING', 'COMPLETED', 'CANCELLED']
        status = status.upper()        
        if status not in allowed:
             return {'response':'Request Error','status':0,'data':'Only {} allowed'.format(allowed)}, 200

        ''' Admin get all orders placed (Admin Only)'''
        logged_in_token = request.headers['ADMIN-KEY']
        admin_id = decode_token(logged_in_token)
        result = ServiceSpace.get_all_admin_orders(self,admin_id,app_state,status)
        if result == "There's nothing here, yet!":
            return {'response':'Request Success','status':0,'data':result}, 200    
        return {'response':'Request Success','status':1,'data':result}, 200

#Admin Specific Actions
class AdminSpecificOrders(Resource):
    
    @api.doc(security='admin-key') # Added to functions that require token access.
    @authorize_admin
    def get(self,order_id):
        '''Get a specific order ( By Admin Only)'''
        result = ServiceSpace.get_specific_order(self,order_id,app_state)
        return {'response':'Request Success','status':1,'data':result}, 200

    @api.expect(put_item_details)    
    @api.doc(security='admin-key')
    @authorize_admin
    def put(self,order_id):
        '''Update the status of an order (Admin Only)'''
        sent_data = api.payload
        allowed = ['NEW', 'PROCESSING', 'COMPLETED', 'CANCELLED']
        try:
            if(sent_data == {}):
                return {'response':'Request Error','status':0,'data': 'You cant send an empty request'}, 204
            else:
                status  = sent_data['status']
                if status in allowed:
                    result = ServiceSpace.update_an_item(self,status,order_id,app_state)
                    return result
                else:
                    return {'response':'Type Error','status':0,'data': 'The status type is not allowed'}, 400   

        except KeyError:
            return {'response':'Entry Error','status':0,'data':'Please enter the data as specified'}, 400

#Menu Requesting
class RequestMenu(Resource):
    def get(self):
        '''Preview items of a specific restaurant'''      
        result = ServiceSpace.get_all_vendor_items(self,app_state)
        return {'response':'Request Success','status':1,'data':result}

    @api.expect(new_item_details)
    @api.doc(security='admin-key')
    @authorize_admin
    def post(self):
        '''Add a meal option to the menu (Admin)'''
        sent_data = api.payload
        try:
            if(sent_data == {}):
                return {'response':'Request Error','status':0,'data': 'You cant post an empty request'}, 204
            else:
                logged_in_token = request.headers['ADMIN-KEY']
                vendor_id = decode_token(logged_in_token)
                item_name = sent_data['item_name']
                details = sent_data['details']
                price = sent_data['price']
                image_url  = sent_data['image_url']
                result = ServiceSpace.add_an_item_to_tbl(self,vendor_id,item_name,details,price,image_url,app_state)
                return {'response':'Posting Success','status':1,'data': result}, 200 

        except KeyError:
            return {'response':'Request Error','status':0,'data':'Please enter the data as specified'}, 400

class AdminMenu(Resource):    
    @api.doc(security='admin-key')
    @authorize_admin
    def get(self):
        '''Get all the specific admins Item'''
        '''Preview items of a specific restaurant'''    
        logged_in_token = request.headers['ADMIN-KEY']  
        vendor_id = decode_token(logged_in_token)
        result = ServiceSpace.get_specific_vendor_items(self,app_state,vendor_id)
        return {'response':'Request Success','status':1,'data':result}

class SpecificAdminMenu(Resource):
    
    @api.doc(security='admin-key')
    @authorize_admin
    def delete(self,item_id):
        '''Removes A Specific Admin Item'''
        ServiceSpace.delete_from_items(self,app_state,item_id)
        return {'response':'Request Success','status':1}


#Authentication
api.add_resource(Auth_Sign_Up,'/auth/signup')
api.add_resource(Auth_Login,'/auth/login')

#Users actions
api.add_resource(UsersOrders,'/users/orders')
api.add_resource(UsersOrdersGet,'/users/orders/<string:status>')

#Administrators
api.add_resource(AdminAllOrders,'/orders/<string:status>')
api.add_resource(AdminSpecificOrders,'/orders/<int:order_id>')

#Menu 
api.add_resource(RequestMenu,'/menu')

#Admin Menu
api.add_resource(AdminMenu,'/admin/menu')
api.add_resource(SpecificAdminMenu,'/admin/menu/<int:item_id>')
