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
      
    #Query all items with customers id from orders table
    def get_all_orders(self,customer_id):

        cur = base_creation(self,'fast_food_db')
        query = "SELECT * FROM orders_tbl WHERE order_from = '{}'".format(customer_id)
        cur.execute(query)
        results = cur.fetchall() #Fetches data in a list
        row_count = cur.rowcount
        orders_list = []
        if row_count < 1:
            return 'You have not ordered anything yet! '
        else:
            print(results)
            for result in results:
                item = {
                        'order_date' : str(result[1]),
                        'order_id' : result[2],
                        'order_detail' : result[3],
                        'order_amount' : result[4],
                        'order_from' : result[5],
                        'order_to' : result[6],
                        'order_status' : result[7],
                        'status_changed' : str(result[8])
                    }
                orders_list.append(item)
            return {'orders_list': orders_list}

    #Adds ordered items to orders table
    def add_order_to_db(self,order_detail,order_amount,order_from,order_to):

        cur = base_creation(self,'fast_food_db')

        cur.execute("SELECT COUNT(id) FROM orders_tbl")
        result = cur.fetchone()
        total_reg_count = result[0]
        entry_count = total_reg_count + 1
        order_date = datetime.datetime.now()
        order_id = random.randint(100,1000000)
        order_status = 'PLACED' # PLACED, ACCEPTED(ADMIN),RUNNING(AUTO), COMPLETED(ADMIN), REJECTED(ADMIN)
        status_changed = datetime.datetime.now()
        query = "INSERT INTO orders_tbl values ({}, '{}',  '{}', '{}', '{}', '{}', '{}', '{}','{}')  RETURNING id".format(entry_count,order_date,order_id,order_detail,order_amount,order_from,order_to,order_status,status_changed)  
        cur.execute(query)
        result = cur.fetchone()[0]
        return result
