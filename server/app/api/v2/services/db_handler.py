import datetime
import uuid
import random
from werkzeug.security import generate_password_hash, check_password_hash
from ....database.db_init import base_creation

class ServiceSpace():
    
    #Add user to db
    def Add_user_to_db(self,type,name,password,vendor_name,phone_no,email,about,location,image_url):
        
        cur = base_creation(self,'fast_food_db')

        if (type == 'ADMIN'):
            #Register to admin
            cur.execute("SELECT COUNT(id) FROM administrator_registrations")
            result = cur.fetchone()
            total_reg_count = result[0]
            total_reg_count = total_reg_count + 1
            reg_state = type
            reg_date = datetime.datetime.now()
            vendor_id = str(uuid.uuid1())                          
            adm_password = generate_password_hash(password, method='sha256')        
            query = "INSERT INTO administrator_registrations  values ( {}, '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(total_reg_count,name,vendor_name,about,location,image_url,phone_no,email,vendor_id,adm_password,reg_date,reg_state)
            print(query)
            cur.execute(query)

        elif (type == 'CUSTOMER'):
            #Register to customer
            cur.execute("SELECT COUNT(id) FROM customer_registration")
            result = cur.fetchone()
            total_reg_count = result[0]
            total_reg_count = total_reg_count + 1
            reg_date = datetime.datetime.now()
            reg_state = type
            customer_id = str(uuid.uuid1())                          
            cus_password = generate_password_hash(password, method='sha256')         
            query = "INSERT INTO customer_registration values ( {}, '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}','{}')".format(total_reg_count,name,about,location,image_url,phone_no,email,customer_id,cus_password,reg_date,reg_state)
            print(query)
            cur.execute(query)   
        
        else:
            return 'ONLY CUSTOMER OR ADMIN ARE ALLOWED'
          

    #Get logged in users details
    def retrieve_user(self,type,name,password):
        
        cur = base_creation(self,'fast_food_db')
        query = "SELECT customer_id FROM customer_registration WHERE customer_name = '{}'".format(name)
        cur.execute(query)
        result = cur.fetchone()
        return result[0]


    #Query all items from a customer
    def get_all_orders(self,customer_id):

        cur = base_creation(self,'fast_food_db')
        query = "SELECT * FROM orders_tbl WHERE order_from = '{}'".format(customer_id)
        cur.execute(query)
        result = cur.fetchall #Fetches data in a list
        return result 


    #Adds items to table
    def add_order_to_db(self,order_detail,order_amount,order_from,order_to,order_status):

        cur = base_creation(self,'fast_food_db')

        cur.execute("SELECT COUNT(id) FROM orders_tbl")
        result = cur.fetchone()
        total_reg_count = result[0]
        entry_count = total_reg_count + 1
        order_date = datetime.datetime.now()
        order_id = random.randint(100,1000000)
        query = "INSERT INTO orders_tbl values ({}, '{}',  '{}', '{}', '{}', '{}', '{}', '{}','Null')".format(entry_count,order_date,order_id,order_detail,order_amount,order_from,order_to,order_status)  
        cur.execute(query)
        result = cur.fetchall
        return result

    #Query all items from a customer
    def get_all_admin_orders(self,admin_id):

        cur = base_creation(self,'fast_food_db')
        query = "SELECT * FROM orders_tbl WHERE order_to = '{}'".format(admin_id)
        cur.execute(query)
        result = cur.fetchall #Fetches data in a list
        return result    

    def update_an_item(self,id,item_name,details,price,image_url,item_id):

        cur = base_creation(self,'fast_food_db')
        query = "UPDATE administrator_items set (id, item_name, details , price, image_url, item_id) values ( '{}', '{}', '{}', '{}', '{}', '{}','Null')".format(id,item_name,details,price,image_url,item_id)  
        cur.execute(query)
        result = cur.fetchall
        return result             

    def get_all_vendor_items(self,vendor_name):

        cur = base_creation(self,'fast_food_db')
        query = "SELECT * FROM administrator_items WHERE vendor_id = '{}'".format(vendor_name)
        cur.execute(query)
        result = cur.fetchall #Fetches data in a list
        return result         