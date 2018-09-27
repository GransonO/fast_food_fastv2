from flask import Flask
from flask_restplus import Resource,Api,fields
from app import create_app
from ..services.db_handler import DataSet 
from app.secret import all_secrets 

app = create_app('Developing')
#app.secret_key = all_secrets['jwt-key']
api = Api(app)

delete_prop = api.model('Deleting an item',{'uid': fields.String('The users id(Must be an admin )')})

#Authentication login and sign up
class Authentication(Resource):

    def post(self,action):
        '''Users Authentication'''
        if(action == 'signup'):
            return 'you have been signed up in'

        elif(action == 'login'):
            return 'You are logged in' 

        else:
            return {'data':'Human! There is no action to be preformed here'}

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
api.add_resource(Authentication,'/auth/<string:action>')

#Users actions
api.add_resource(UsersOrders,'/users/orders')

#Administrators
api.add_resource(AdminAllOrders,'/orders/ ')
api.add_resource(AdminSpecificOrders,'/orders/<int:num> ')

#Menu 
api.add_resource(RequestMenu,'/menu ')
