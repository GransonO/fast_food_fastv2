#Test the database interactions
from ...database.db_init import base_creation
from ...api.v2.services.db_handler import ServiceSpace

class TestDataBase():
    '''Tests the database related actions'''
    
    app_state = 'Testing' #Testing Configurations
    test_order_from = '111111111' 
    test_order_to = '222222222' 

    #Get the app state
    def get_db_status(self,db_state):
        '''Assign name to database according to states'''
        if db_state == 'Production': #For production
            db_name = 'fast_food_db'
        else:
            db_name = 'test_fast_food_db' #For testing
        return db_name
        
    #Test is connection successful
    def test_cursor(self):
        cur = base_creation(self,'test_fast_food_db')
        assert cur != None 
    
    def test_add_new_user(self):
        #Admin entry
        adm_result = ServiceSpace.Add_user_to_db(self,'ADMIN','Granson Admin','password','Galitos','0712288371','email@gmail.com','This is about me.','Limuru','www.this_is_my_profile_image.com/img.png','Testing')
        
        assert "Granson Admin" in str(adm_result)
        assert "Galitos" in str(adm_result)
        assert "www.this_is_my_profile_image.com/img.png" in str(adm_result)
        #Customer Entry
        customer_result = ServiceSpace.Add_user_to_db(self,'CUSTOMER','Granson Customer','password','','0712288371','email@gmail.com','This is about me.','Limuru','The image','Testing')
                
        assert "Granson Customer" in str(customer_result)
        assert "Galitos" not in str(customer_result)
        assert "The image" in str(customer_result)
        #Error entry
        error_result = ServiceSpace.Add_user_to_db(self,'Something','Granson','password','Galitos','0712288371','email@gmail.com','This is about me.','Limuru','The image','Testing')
        assert error_result == 'ONLY CUSTOMER OR ADMIN ARE ALLOWED'

    def add_users_for_testing(self):
        #Add users first
        #Admin
        ServiceSpace.Add_user_to_db(self,'ADMIN','Granson','password','Galitos','0712288371','email@gmail.com','This is about me.','Limuru','The image','Testing')
        #Customer Entry
        ServiceSpace.Add_user_to_db(self,'CUSTOMER','Granson','password','Galitos','0712288371','email@gmail.com','This is about me.','Limuru','The image','Testing')
    
    #Test users in database
    def test_retrieve_user(self):
        TestDataBase.add_users_for_testing(self) #Adds users for testing
        #Retrieve users tests
        right_admin = ServiceSpace.retrieve_user(self,'ADMIN','Granson','password','Testing')
        assert right_admin['password'] == True
        wrong_admin = ServiceSpace.retrieve_user(self,'ADMIN','Granso','password','Testing')
        assert wrong_admin['password'] == False
        assert wrong_admin['user_id'] == 'Not Found'


        right_customer = ServiceSpace.retrieve_user(self,'CUSTOMER','Granson','password','Testing')
        assert right_customer['password'] == True
        wrong_customer  = ServiceSpace.retrieve_user(self,'ADMIN','Granso','password','Testing')
        assert wrong_customer['password'] == False
        assert wrong_customer['user_id'] == 'Not Found'

        not_accepted = ServiceSpace.retrieve_user(self,'USER','Granson','password','Testing')
        assert not_accepted['response'] == 'The user type is not allowed'

    def test_add_order_to_db(self):
        new_order = ServiceSpace.add_order_to_db(self,'Cake Meat Eggs','2000',TestDataBase.test_order_from,TestDataBase.test_order_to,TestDataBase.app_state)
        print(new_order)  
        assert new_order['data']['order_from'] == TestDataBase.test_order_from
        assert new_order['data']['order_amount'] == '2000' 
        assert new_order['data']['order_detail'] ==  'Cake Meat Eggs'
        assert new_order != None

    #def get_all_orders(self,customer_id,app_state):


    # def get_all_admin_orders(self,admin_id,app_state):

    # def get_specific_order(self,order_id,app_state):

    # def update_an_item(self,status,order_id,app_state):

    # def get_all_vendor_items(self,app_state):
    
    # def add_an_item_to_tbl(self,vendor_id,item_name,details,price,image_url,app_state):
    