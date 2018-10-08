import datetime
import uuid
import random
from werkzeug.security import generate_password_hash, check_password_hash
from ....database.db_init import base_creation

class ServiceSpace():
    
    #Get the app state
    def get_db_status(self,db_state):
        '''Assign name to database according to states'''
        if db_state == 'Production': #For production
            db_name = 'fast_food_db'
        else:
            db_name = 'test_fast_food_db' #For testing
        return db_name

    #Add user to db
    def Add_user_to_db(self,type,name,password,vendor_name,phone_no,email,about,location,image_url,app_state):
        db_name = ServiceSpace.get_db_status(self,app_state)
        cur = base_creation(self,db_name)
        print(type)
        if (type == 'ADMIN'):
            #Register to admin
            cur.execute("SELECT COUNT(id) FROM administrator_registrations")
            result = cur.fetchone()
            total_reg_count = result[0]
            total_reg_count = total_reg_count + 1
            reg_state = type
            reg_date = datetime.datetime.now()
            vendor_id = str(uuid.uuid1())    #public ID                       
            adm_password = generate_password_hash(password)   #Hash the password    
            query = "INSERT INTO administrator_registrations  values ( {}, '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')  RETURNING vendor_id".format(total_reg_count,name,vendor_name,about,location,image_url,phone_no,email,vendor_id,adm_password,reg_date,reg_state)
            print(query)
            cur.execute(query)
            result = cur.fetchone()[0]
            if result == vendor_id:
                item = {
                    'vendor_id' : vendor_id,
                    'name' : name,
                    'phone_no' : phone_no,
                    'email' : email,
                    'vendor_name': vendor_name,
                    'location' : location,
                    'reg_date' : str(reg_date),
                    'image_url' : image_url
                }
                return {'result':'Success','data': item}
            else:
                return {'result':'Failed'} 

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
            query = "INSERT INTO customer_registration values ( {}, '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}','{}')  RETURNING customer_id".format(total_reg_count,name,about,location,image_url,phone_no,email,customer_id,cus_password,reg_date,reg_state)
            print(query)
            cur.execute(query)  
            result = cur.fetchone()[0]
            if result == customer_id:
                item = {
                    'customer_id' : customer_id,
                    'name' : name,
                    'phone_no' : phone_no,
                    'email' : email,
                    'location' : location,
                    'reg_date' : str(reg_date),
                    'image_url' : image_url
                }
                return {'result':'Success','data': item}
            else:
                return {'result':'Failed'} 
        
        else:
            return 'ONLY CUSTOMER OR ADMIN ARE ALLOWED'
          
    #Get logged in users details
    def retrieve_user(self,type,name,password,app_state):

        db_name = ServiceSpace.get_db_status(self,app_state)
        if (type == 'CUSTOMER'):
            cur = base_creation(self,db_name)                  
            query = "SELECT cus_password,customer_id FROM customer_registration WHERE customer_name = '{}'".format(name)
            cur.execute(query)
            hash_pass = cur.fetchone()
            print('The Hash pass is {} in DB : {} For Table: customer_registration'.format(hash_pass,db_name))
            print('#')
            if hash_pass != None:
                result = check_password_hash(hash_pass[0], password) #TRUE OR FALSE
                print('The result is {}'.format(result))
                return {'password' : result, 'user_id' : hash_pass[1]}
            else:
                return {'password' : False, 'user_id' : 'Not Found'}

        elif  (type == 'ADMIN'):
            cur = base_creation(self,db_name)
            query = "SELECT adm_password,vendor_id FROM administrator_registrations WHERE username = '{}'".format(name)
            cur.execute(query)
            hash_pass = cur.fetchone()
            print('The Hash pass is {} in DB : {} For Table: administrator_registrations'.format(hash_pass,db_name))
            print(query)
            if hash_pass != None:
                result = check_password_hash(hash_pass[0], password) #TRUE OR FALSE
                return {'password' : result, 'user_id' : hash_pass[1]}
            else:
                return {'password' : False, 'user_id' : 'Not Found'}

        else:
            return {'response':'The user type is not allowed'}
      
    #Query all items with customers id from orders table
    def get_all_orders(self,customer_id,app_state):

        db_name = ServiceSpace.get_db_status(self,app_state)
        cur = base_creation(self,db_name)
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
    def add_order_to_db(self,order_detail,order_amount,order_from,order_to,app_state):

        db_name = ServiceSpace.get_db_status(self,app_state)
        cur = base_creation(self,db_name)

        cur.execute("SELECT COUNT(id) FROM orders_tbl")
        result = cur.fetchone()
        total_reg_count = result[0]
        entry_count = total_reg_count + 1
        order_date = datetime.datetime.now()
        order_id = random.randint(100,1000000)
        order_status = 'NEW' # PROCESSING(AUTO), COMPLETED(ADMIN), CANCELLED(ADMIN)
        status_changed = datetime.datetime.now()
        query = "INSERT INTO orders_tbl values ({}, '{}',  '{}', '{}', '{}', '{}', '{}', '{}','{}')  RETURNING order_id".format(entry_count,order_date,order_id,order_detail,order_amount,order_from,order_to,order_status,status_changed)  
        cur.execute(query)
        result = cur.fetchone()[0]
        print('Order id : {} Result : {}'.format(order_id,result))
        if result != None: #order_id:
            item = {
                'order_status' : order_status,
                'order_id' : order_id,
                'order_date' : str(order_date),
                'order_from' : order_from,
                'order_amount' : order_amount,
                'order_to' : order_to,
                'order_detail' : order_detail
            }
            return {'result':'Success','data': item}
        else:
            return {'result':'Failed'}

    #Query all orders from all customers
    def get_all_admin_orders(self,admin_id,app_state):

        db_name = ServiceSpace.get_db_status(self,app_state)
        cur = base_creation(self,db_name)
        query = "SELECT * FROM orders_tbl WHERE order_to = '{}'".format(admin_id)
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
                        'order_status' : result[7],
                        'status_changed' : str(result[8])
                    }
                orders_list.append(item)
            return {'adm_orders_list': orders_list} 

    #Query specific order from orders table
    def get_specific_order(self,order_id,app_state):

        db_name = ServiceSpace.get_db_status(self,app_state)
        cur = base_creation(self,db_name)
        query = "SELECT * FROM orders_tbl WHERE order_id = '{}'".format(order_id)
        cur.execute(query)
        result = cur.fetchone() #Fetches data in a list
        row_count = cur.rowcount
        #orders_list = []
        if row_count < 1:
            return 'Nothing here with that ID, Bro!'
        else:
            print(result)
            #for result in results:
            item = {
                    'order_date' : str(result[1]),
                    'order_id' : result[2],
                    'order_detail' : result[3],
                    'order_amount' : result[4],
                    'order_from' : result[5],
                    'order_status' : result[7],
                    'status_changed' : str(result[8])
                }
            #orders_list.append(item)
            return {'specific_order': item} 

    #Update the status of an order by its ID
    def update_an_item(self,status,order_id,app_state):
    
        db_name = ServiceSpace.get_db_status(self,app_state)
        cur = base_creation(self,db_name)
        status_changed = datetime.datetime.now()
        query = "UPDATE orders_tbl set order_status = '{}' ,status_changed = '{}' where order_id = '{}'".format(status,status_changed,order_id)  
         #retrieve updated order
        try:
            cur.execute(query)
            #retrieve updated order
            result = ServiceSpace.get_specific_order(self,order_id,app_state)
            return {'response':'Updated State','details': result}
        except:
            return {'response':'Whoops! Aye! Something terribly wrong happened!!!'}

    #Return all items in the items table( From all vendors)
    def get_all_vendor_items(self,app_state):
    
        db_name = ServiceSpace.get_db_status(self,app_state)
        cur = base_creation(self,db_name)
        query = "SELECT * FROM administrator_items"
        cur.execute(query)
        results = cur.fetchall() #Fetches data in a list
        row_count = cur.rowcount
        orders_list = []
        if row_count < 1:
            return 'Nothing here for you, Bro!'
        else:
            print(results)
            for result in results:
                item = {
                    'item_name': result[1],
                    'details': result[2],
                    'price' : result[3],
                    'image_url': result[4],
                    'item_id': result[5],
                    'vendor_id': result[6]
                    }
                orders_list.append(item)
            return {'items_list': orders_list}

    #Add items to table 
    def add_an_item_to_tbl(self,vendor_id,item_name,details,price,image_url,app_state):
        db_name = ServiceSpace.get_db_status(self,app_state)
        cur = base_creation(self,db_name)

        cur.execute("SELECT COUNT(id) FROM administrator_items")
        result = cur.fetchone()
        total_reg_count = result[0]
        entry_count = total_reg_count + 1
        item_id = random.randint(100,100000)
        added_date = datetime.datetime.now()
        query = "INSERT INTO administrator_items VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}')  RETURNING item_id ".format(entry_count, item_name, details, price, image_url, item_id, vendor_id)
        cur.execute(query)
        result = cur.fetchone()[0]
        print('result is {} Item is {}'.format(result,item_id))
        if int(result) == item_id:
            item = {
                'added_date' : str(added_date),
                'details' : details,
                'item_name' : item_name,
                'vendor_id' : vendor_id,
                'image_url' : image_url,
                'item_id' : item_id
            }
            return {'result':'Success','data': item}
        else:
            return {'result':'Failed'}
