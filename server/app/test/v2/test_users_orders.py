#Test the database interactions
from ...database.db_init import base_creation
from ...api.v2.services.db_handler import ServiceSpace

app_state = 'Testing' #Testing Configurations
test_order_from = '111111111' 
test_order_to = '222222222'

   
#Post an order
def test_user_get_orders(create_test_app): #Get No token
  '''Test for user get order'''
  response = create_test_app.get('/users/orders')
  assert response.status_code == 401
  assert b'No logged in key passed' in response.data
    
# #Post an order
# def test_pass_add_orders(create_test_app): # Get 
#   '''Test for user add order'''
#     customer_result = ServiceSpace()#Add test user
#     customer_result.Add_user_to_db('CUSTOMER','Test Add Customer','password','NON','0712288371','email@gmail.com','This is about me.','Limuru','The image','Testing')
#     result = customer_result.retrieve_user(self,'CUSTOMER','Test Add Customer','password','Testing')
    
#     user_order = ServiceSpace()#Add test items by user
#     user_order.add_order_to_db('Test Order Item 1','1000',TestDataBase.test_order_from,TestDataBase.test_order_to,TestDataBase.app_state)
#     user_order.add_order_to_db(self,'Test Order Item 2','2000',TestDataBase.test_order_from,TestDataBase.test_order_to,TestDataBase.app_state)
    
    
#     response_1 = create_test_app.get('/users/orders',headers= {
#     'Content-Type': 'application/json',
#     'accept': 'application/json', 
#     'APP-LOGIN-KEY': token
#     })

#     assert response_1.status_code == 401
#     assert b'No logged in key passed' in response.data
