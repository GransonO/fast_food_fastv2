from flask import Flask
from flask_restplus import Resource,Api,fields
from app import create_app
from ..services.db_handler import ServiceSpace 
from app.secret import all_secrets 

app = create_app('Developing')
#app.secret_key = all_secrets['jwt-key']
api = Api(app)

delete_prop = api.model('Deleting an item',{'uid': fields.String('The users id(Must be an admin )')})
auth_login_ = api.model('User Login',{'type': fields.String('The user can be either ADMIN or CUSTOMER'),'name': fields.String('The username registered'),'password': fields.String('The users password')})
auth_sign_up = api.model('User Sign Up',{'type': fields.String('The user can be either ADMIN or CUSTOMER'),'name': fields.String('The username registered'),'vendor_name': fields.String('The if user is Admin'),'password': fields.String('The users password'),'about': fields.String('Brief Users description'),'location': fields.String('The users location'),'image_url': fields.String('The users uploaded image'),'phone_no': fields.String('The users phone number'),'email': fields.String('The users email')})

#Authentication login
class Auth_Login(Resource):

    @api.expect(auth_login_)
    def post(self,action):
        '''Users Authentication'''
        if(action == 'login'):
            sent_data = api.payload
            Auth_Login.auth_verify(self,sent_data)

        else:
            return {'data':'Human! There is no action to be preformed here'}

    def auth_verify(self,sent_data):
        try:
            if(sent_data == {}):
                return {'data': 'You cant send an empty request'}
            else:
                type = sent_data['type']
                name = sent_data['name']
                password = sent_data['password']

                result = ServiceSpace.retrieve_user(self,type,name,password)
                return {'data': result}    

        except KeyError:
            return {'data':'Please enter the data as specified'}

        except:
            return {'data':'Your data could not be posted, are you trying something clever?'}

#Authentication sign up
class Auth_Sign_Up(Resource):

    @api.expect(auth_sign_up)
    def post(self,action):
        '''Users Authentication'''
        if(action == 'signup'):
            sent_data = api.payload
            Auth_Sign_Up.auth_verify(self,sent_data)

        else:
            return {'data':'Human! There is no action to be preformed here'}

    def auth_verify(self,sent_data):
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

        except:
            return {'data':'Your data could not be posted, are you trying something clever?'}

#Users data Interactions
class UsersOrders(Resource):
    ''' Users get the order history for a particular user'''
    def get(self):
        return 'Get the order history for a particular user' 

    def post(self):
        '''Users place an order for food'''
        return 'Place an order for food'        

#Admin Actions
class AdminAllOrders(Resource):
    ''' Admin get all orders placed (Admin Only)'''
    def get(self):
        pass

#Admin Specific Actions
class AdminSpecificOrders(Resource):
    '''Add a specific order (Admin Only)'''
    def get(self,num):
        pass

    def put(self,num):
        '''Update the status of an order (Admin Only)'''
        pass

#Menu Requesting
class RequestMenu(Resource):
    def get(self):
        '''Get available menu (All)'''
        pass 
    
    def post(self):
        '''Add a meal option to the menu (Admin)'''
        pass


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
