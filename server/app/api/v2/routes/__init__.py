import os
from pathlib import Path
from flask import Flask, request, redirect, url_for, send_from_directory, jsonify
from flask_restplus import Resource,Api,fields
from werkzeug.utils import secure_filename #image name changer
import base64
import datetime
from functools import wraps
import jwt
from app import create_app
from ..services.db_handler import ServiceSpace
from app.secret import secrets 
from .validators import Validation

app_state = 'Testing'  #'Developing','Testing','Production'

path_to_folder = os.path.dirname(__file__)
UPLOAD_FOLDER = os.path.join(os.path.join(path_to_folder, 'static'), 'images') #Folder

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

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

api = Api(app, version='1.2', title='Fast Food Fast API', description='The Fast food fast APIs are for your daily food usage. Think Eatout, Revamped !!!',contact_email= 'oyombegranson@gmail.com',  default ='General', default_label='Non specific API operations', authorizations=authorize_properties )

#Namespaces
auth = api.namespace('Authentication', description='Login and Sign up processes',path='/')
profile = api.namespace('Profile', description='User & Administrator profiles',path='/')
test = api.namespace('tests', description='Application Testing endpoints',path='/')
menu = api.namespace('menu', description='Menu manipulation',path='/')
order = api.namespace('orders', description='Orders placement and processing',path='/')

#Models
auth_login_ = api.model('User Login',{'type': fields.String('The user can be either ADMIN or CUSTOMER'),'name': fields.String('The username registered'),'password': fields.String('The users password')})
auth_sign_up = api.model('User Sign Up',{'type': fields.String('The user can be either "ADMIN" or "CUSTOMER"'),'name': fields.String('The username registered'),'vendor_name': fields.String('The if user is Admin'),'password': fields.String('The users password'),'about': fields.String('Brief Users description'),'location': fields.String('The users location'),'image_url': fields.String('The users uploaded image'),'phone_no': fields.String('The users phone number'),'email': fields.String('The users email')})
order_request = api.model('User Order request', { 'order_to': fields.String('The vendor of the item'), 'order_amount': fields.Float('The total transaction amount') , 'order_quantity': fields.Integer('The number of items to order'), 'item_id': fields.String('The ordered item ID') })
put_item_status = api.model('Admin updating request', {'status': fields.String('Order status. Can be either NEW(CUSTOMER), PROCESSING(AUTO), COMPLETED(ADMIN), CANCELLED(ADMIN)') })
new_item_details = api.model('New Item Posting', { 'item_name': fields.String('Name of item'), 'details': fields.String('Brief description of item'),'price' : fields.Float('Price of the item'), 'image_url':fields.String('Url to hosted item\'s image'), 'category':fields.String('the items category(Lunch, Dinner, etc )')})
put_item_details = api.model('Updating an Item',{'item_name': fields.String('Name of item'), 'details': fields.String('Brief description of item'),'price' : fields.Float('Price of the item'), 'image_url':fields.String('Url to hosted item\'s image'), 'item_id':fields.Integer('Generated Item Id')})
put_user_details = api.model('Updating a users details', {'customer_name' : fields.String('Name of Customer'),'email':fields.String('Customer email address'),'phone':fields.String('Customer phone number'), 'location': fields.String('Customer Location'),'about' : fields.String('Customer brief introduction') })
customer_comments = api.model('Customers Comments',{'comment' : fields.String('Customers Comment'), 'comment_to' : fields.String('vendor_id')})
get_related_items = api.model('Related Items Fetching',{'item_id': fields.Integer('The respective item Id'), 'item_category': fields.String('The items category')})

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
                return {'response':'User Authorization error, Token passed is invalid','status':0,'data':'Token passed is invalid'},401
        else:
            return {'response':'User Authorization error, No logged in key passed','status':0,'data':'No logged in key passed'},401
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
            return {'response':'Authorization error, No Admin key passed','status':0,'data':'No Admin key passed'}
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
                item_id = sent_data['item_id']
                order_amount = sent_data['order_amount']
                order_quantity = sent_data['order_quantity']
                order_from = customer_id
                order_to = sent_data['order_to']
                result = ServiceSpace.add_order_to_db(self,item_id,order_amount,order_quantity,order_from,order_to,app_state)
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
        '''Get orders as specified ~NEW, PROCESSING, COMPLETED, CANCELLED~ '''
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

    @api.expect(put_item_status)    
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
                category  = sent_data['category']
                result = ServiceSpace.add_an_item_to_tbl(self,vendor_id,item_name,details,price,image_url,category,app_state)
                return {'response':'Posting Success','status':1,'data': result}, 200 

        except KeyError:
            return {'response':'Request Error','status':0,'data':'Please enter the data as specified'}, 400

    @api.expect(put_item_details)
    @api.doc(security='admin-key')
    @authorize_admin
    def put(self):
        '''Update a meal option in the menu (Admin)'''
        sent_data = api.payload
        try:
            if(sent_data == {}):
                return {'response':'Request Error','status':0,'data': 'You cant update an empty request'}, 204
            else:
                item_name = sent_data['item_name']
                details = sent_data['details']
                price = sent_data['price']
                image_url  = sent_data['image_url']
                item_id  = sent_data['item_id']
                result = ServiceSpace.update_an_item_in_tbl(self,item_name,details,price,image_url,app_state,item_id)
                return result, 200 

        except KeyError:
            return {'response':'Request Error','status':0,'data':'Please enter the data as specified'}, 400

class RequestSpecific(Resource):
    def get(self,item_id):
        '''Returns a specific Items details'''      
        result = ServiceSpace.get_specific_item(self,app_state,item_id)        
        return {'data' : result}

class AdminMenu(Resource):    
    @api.doc(security='admin-key')
    @authorize_admin
    def get(self):
        '''Get all the specific admins Item'''  
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

class AdminProfile(Resource):
    
    @api.doc(security='admin-key')
    @authorize_admin
    def get(self):
        '''Get all the admin details'''
        logged_in_token = request.headers['ADMIN-KEY']
        vendor_id = decode_token(logged_in_token)
        result = ServiceSpace.get_profile(self,app_state,vendor_id,'admin')
        return result

class UserProfile(Resource):
    
    @api.doc(security='logged_in_key')
    @authorize_user
    def get(self):
        '''Get all the users details'''        
        logged_in_token = request.headers['APP-LOGIN-KEY']
        user_id = decode_token(logged_in_token)
        result = ServiceSpace.get_profile(self,app_state,user_id,'customer')
        return result

    @api.doc(security='logged_in_key')
    @authorize_user
    @api.expect(put_user_details)
    def put(self):
        '''Updates the passed Customer details'''        
        logged_in_token = request.headers['APP-LOGIN-KEY']
        customer_id = decode_token(logged_in_token)
        sent_data = api.payload
        try:
            if(sent_data == {}):
                return {'response':'Request Error','status':0,'data': 'You cant update an empty request'}, 204
            else:
                customer_name = sent_data['customer_name']
                email = sent_data['email']
                phone = sent_data['phone']
                location  = sent_data['location']
                about  = sent_data['about']
                result = ServiceSpace.update_user_details(self,customer_name,email,phone,location,about,customer_id,app_state)
                return result, 200 

        except KeyError:
            return {'response':'Request Error','status':0,'data':'Please enter the data as specified'}, 400

class Comments(Resource):
    '''Processes comments placed by users'''

    @authorize_admin
    @api.doc(security='admin-key') #Login key for customers
    def get(self):
        '''Get all comments (Admins can only see their specific comments)'''
        pass

    @api.expect(customer_comments)
    @authorize_user
    @api.doc(security='logged_in_key') #Login key for customers
    def post(self):
        '''Add a new comment'''
        pass

class RelatedItems(Resource):
    @api.expect(get_related_items)
    def post(self):        
        ''' Get Items related to the selected Item '''
        sent_data = api.payload
        item_id = sent_data['item_id']
        category = sent_data['item_category']
        result = ServiceSpace.get_related_items(self,item_id,category,app_state) #Return max three items from query
        return result

class CategoryMenu(Resource):
    def get(self,category):
        '''Fetch all items as per category passed'''
        result = ServiceSpace.get_category_items(self,category,app_state)
        return result

class VendorMenu(Resource):
    def get(self,vendor_id):
        '''Gets all items from a specific vendor'''
        result = ServiceSpace.get_vendor_items(self,vendor_id,app_state)
        return result

class VendorsList(Resource):
    def get(self):
        '''Get all vendors data (Name and ID)'''
        result = ServiceSpace.get_vendors(self,app_state)
        return result

class Testing(Resource):
    def get(self):
        '''Test for get method'''
        return {'response':'This is a get test'}

    def post(self):
        '''Test post method'''
        return {'response':'This is a post test'}

    def put(self):
        '''Test for put method'''
        return {'response':'This is a put test'}

    def delete(self):
        '''Test delete method'''
        return {'response':'This is a delete test'}

class ImageRequest(Resource):
    def get(self,filename):
        '''Load an image from the static/images folder'''  
        try:
                
            with open(os.path.join(UPLOAD_FOLDER, filename), "rb") as image_file:
                image_read = image_file.read() 
                image_64_encode = base64.encodestring(image_read)
                output = image_64_encode.decode("utf-8")
                print(output)
                return {'image' : output, 'status' : 1}

        except FileNotFoundError:
            return {'image' : 'Could not be found','status': 0}

class ImageUpload(Resource):
    def post(self):
        '''Upload an image to the static/images folder'''
        if 'file' not in request.files:
            return {'response':'No file to upload'}
        file = request.files['file']
        if file.filename == '':
            return {'response':'No Selected file to upload'}
        if file and ImageUpload.allowed_file(self, file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            print(filename)
            return {'response':'Upload Success','data':filename}

    def allowed_file(self,filename):
        return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#Authenticate
auth.add_resource(Auth_Sign_Up,'/auth/signup')
auth.add_resource(Auth_Login,'/auth/login')

#Users actions
order.add_resource(UsersOrders,'/users/orders')
order.add_resource(UsersOrdersGet,'/users/orders/<string:status>')

#Administrators
order.add_resource(AdminAllOrders,'/orders/<string:status>')
order.add_resource(AdminSpecificOrders,'/orders/<int:order_id>')

#Menu 
menu.add_resource(RequestMenu,'/menu')
menu.add_resource(RequestSpecific,'/menu/<int:item_id>')
menu.add_resource(CategoryMenu,'/menu/<string:category>')
menu.add_resource(VendorMenu,'/vendor/<string:vendor_id>')
menu.add_resource(VendorsList,'/vendors')

#Admin Menu
menu.add_resource(AdminMenu,'/admin/menu')
menu.add_resource(SpecificAdminMenu,'/admin/menu/<int:item_id>')

#profile
profile.add_resource(AdminProfile,'/admin/profile')
profile.add_resource(UserProfile,'/user/profile')

#add a comment
api.add_resource(Comments, '/user/comment')

#related Items Fetching
menu.add_resource(RelatedItems, '/related')

#tests
test.add_resource(Testing, '/test')

#image_service
api.add_resource(ImageUpload,'/image')
api.add_resource(ImageRequest,'/image/<string:filename>')
