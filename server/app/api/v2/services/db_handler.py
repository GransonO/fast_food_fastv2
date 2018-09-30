import datetime
import uuid
import random
from werkzeug.security import generate_password_hash, check_password_hash
from ....database.db_init import base_creation

class ServiceSpace():
    
    #Add user to db
    def Add_user_to_db(self,type,name,password,vendor_name,phone_no,email,about,location,image_url):
        
        cur = base_creation(self,'fast_food_db')
        print(type)
        if (type == 'ADMIN'):
            #Register to admin
            cur.execute("SELECT COUNT(id) FROM administrator_registrations")
            result = cur.fetchone()
            total_reg_count = result[0]
            total_reg_count = total_reg_count + 1
            reg_state = type
            reg_date = datetime.datetime.now()
            vendor_id = str(uuid.uuid1())     #public ID                       
            adm_password = generate_password_hash(password)   #Hash the password    
            query = "INSERT INTO administrator_registrations  values ( {}, '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')  RETURNING id".format(total_reg_count,name,vendor_name,about,location,image_url,phone_no,email,vendor_id,adm_password,reg_date,reg_state)
            print(query)
            cur.execute(query)
            return cur.fetchone()[0]

        elif (type == 'CUSTOMER'):
            #Register to customer
            cur.execute("SELECT COUNT(id) FROM customer_registration")
            result = cur.fetchone()
            total_reg_count = result[0]
            total_reg_count = total_reg_count + 1
            reg_date = datetime.datetime.now()
            reg_state = type
            customer_id = str(uuid.uuid1())   #public ID                       
            cus_password = generate_password_hash(password)  #Hash the password       
            query = "INSERT INTO customer_registration values ( {}, '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}','{}')  RETURNING id".format(total_reg_count,name,about,location,image_url,phone_no,email,customer_id,cus_password,reg_date,reg_state)
            print(query)
            cur.execute(query)  
            return cur.fetchone()[0] 
        
        else:
            return 'ONLY CUSTOMER OR ADMIN ARE ALLOWED'
          

    #Get logged in users details
    def retrieve_user(self,type,name,password):

        if (type == 'CUSTOMER'):
            cur = base_creation(self,'fast_food_db')
            query = "SELECT cus_password,customer_id FROM customer_registration WHERE customer_name = '{}'".format(name)
            cur.execute(query)
            hash_pass = cur.fetchone()
            print(hash_pass)
            result = check_password_hash(hash_pass[0], password) #TRUE OR FALSE
            return {'password' : result, 'user_id' : hash_pass[1]}

        elif  (type == 'ADMIN'):
            cur = base_creation(self,'fast_food_db')
            query = "SELECT adm_password,vendor_id FROM administrator_registrations WHERE username = '{}'".format(name)
            cur.execute(query)
            hash_pass = cur.fetchone()
            print(hash_pass)
            result = check_password_hash(hash_pass[0], password) #TRUE OR FALSE
            return {'password' : result, 'user_id' : hash_pass[1]}
      