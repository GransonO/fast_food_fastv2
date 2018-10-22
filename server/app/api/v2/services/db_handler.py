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
    def get_all_orders(self,customer_id,app_state,status):

        db_name = ServiceSpace.get_db_status(self,app_state)
        cur = base_creation(self,db_name)
        query = "SELECT * FROM orders_tbl WHERE order_from = '{}' AND order_status='{}'".format(customer_id,status)
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
                        'order_detail' : ServiceSpace.getItemsDetails(self,app_state,result[3]),
                        'order_quantity' : result[4],
                        'order_amount' : result[5],
                        'order_from' : result[6],
                        'order_to' : ServiceSpace.getVendorDetails(self,app_state,result[7]),
                        'order_status' : result[8],
                        'status_changed' : str(result[9])
                    }
                orders_list.append(item)
            return {'orders_list': orders_list} 

    #Query all items with customers id from orders table
    def get_all_raw_orders(self,customer_id,app_state):

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
                        'order_detail' : ServiceSpace.getItemsDetails(self,app_state,result[3]),
                        'order_quantity' : result[4],
                        'order_amount' : result[5],
                        'order_from' : result[6],
                        'order_to' : ServiceSpace.getVendorDetails(self,app_state,result[7]),
                        'order_status' : result[8],
                        'status_changed' : str(result[9])
                    }
                orders_list.append(item)
            return {'orders_list': orders_list}

    #Adds ordered items to orders table
    def add_order_to_db(self,order_detail,order_amount,order_quantity,order_from,order_to,app_state):

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
        query = "INSERT INTO orders_tbl values ({}, '{}',  '{}', '{}', {}, '{}', '{}', '{}', '{}','{}')  RETURNING order_id".format(entry_count,order_date,order_id,order_detail,order_quantity,order_amount,order_from,order_to,order_status,status_changed)  
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
    def get_all_admin_orders(self,admin_id,app_state,status):

        db_name = ServiceSpace.get_db_status(self,app_state)
        cur = base_creation(self,db_name)
        query = "SELECT * FROM orders_tbl WHERE order_to = '{}' AND order_status = '{}'".format(admin_id,status)
        cur.execute(query)
        results = cur.fetchall() #Fetches data in a list
        row_count = cur.rowcount
        orders_list = []
        if row_count < 1:
            return 'There\'s nothing here, yet!'
        else:
            print(results)
            for result in results:
                item = {
                        'order_date' : str(result[1]),
                        'order_id' : result[2],
                        'item_details' : ServiceSpace.getItemsDetails(self,app_state,result[3]),
                        'order_quantity' : result[4],
                        'order_amount' : result[5],
                        'order_from' : ServiceSpace.getCustomerDetails(self,app_state,result[6]),
                        'order_status' : result[8],
                        'status_changed' : str(result[9])
                    }
                orders_list.append(item)
            return {'adm_orders_list': orders_list} 


    def getItemsDetails(self,app_state,item_id):
        '''Gets Items details from the orders list'''        
        db_name = ServiceSpace.get_db_status(self,app_state)
        cur = base_creation(self,db_name)
        query = "SELECT * FROM administrator_items WHERE item_id = '{}'".format(item_id)
        cur.execute(query)
        results = cur.fetchall() #Fetches data in a list
        row_count = cur.rowcount
        if row_count < 1:
            return {'response':'Nothing here for you, Human!','mess':0}
        else:
            print(results)
            for result in results:
                item = {
                    'item_name': result[1],
                    'details': result[2],
                    'price' : result[3],
                    'image_url': result[4],
                    'item_id': result[5],
                    'vendor_id': result[6],
                    'category' : result[7]
                    }
            return item

    def getCustomerDetails(self,app_state,customer_id):
        '''Get details of the customer'''
        db_name = ServiceSpace.get_db_status(self,app_state)
        cur = base_creation(self,db_name)
        query = "SELECT * FROM customer_registration WHERE customer_id = '{}'".format(customer_id)
        cur.execute(query)
        results = cur.fetchall() #Fetches data in a list
        row_count = cur.rowcount
        if row_count < 1:
            return {'response':'No user with that account, Human!','mess':0}
        else:
            print(results)
            for result in results:
                item = {
                    'customer_name': result[1],
                    'location': result[3],
                    'phone_number' : result[5]
                    }
            return item

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
            return {'response':'Nothing here with that ID, Bro!','status':0}
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
            return {'specific_order': item,'status':1} 

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
            return result
        except:
            return {'response':'Whoops! Aye! Something terribly wrong happened!!!','status':0}

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
            return {'response':'Nothing here for you, Human!','mess':0}
        else:
            print(results)
            for result in results:
                item = {
                    'item_name': result[1],
                    'details': result[2],
                    'price' : result[3],
                    'image_url': result[4],
                    'item_id': result[5],
                    'vendor_id': ServiceSpace.getVendorDetails(self,app_state,result[6]),
                    'category' : result[7]
                    }
                orders_list.append(item)
            return {'items_list': orders_list}

    def getVendorDetails(self,app_state,vendor_id):
        '''Get details of the customer'''
        db_name = ServiceSpace.get_db_status(self,app_state)
        cur = base_creation(self,db_name)
        query = "SELECT * FROM administrator_registrations WHERE vendor_id = '{}'".format(vendor_id)
        cur.execute(query)
        results = cur.fetchall() #Fetches data in a list
        row_count = cur.rowcount
        if row_count < 1:
            return {'response':'No vendor with that account, Human!','mess':0}
        else:
            print(results)
            for result in results:
                item = {
                    'vendor_name': result[2],
                    'location': result[4],
                    'phone_number' : result[6],
                    'email' : result[7],
                    'vendor_id' : result[8]
                    }
            return item

    #Add items to table 
    def add_an_item_to_tbl(self,vendor_id,item_name,details,price,image_url,category,app_state):
        db_name = ServiceSpace.get_db_status(self,app_state)
        cur = base_creation(self,db_name)

        cur.execute("SELECT COUNT(id) FROM administrator_items")
        result = cur.fetchone()
        total_reg_count = result[0]
        entry_count = total_reg_count + 1
        item_id = random.randint(100,100000)
        added_date = datetime.datetime.now()
        query = "INSERT INTO administrator_items VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')  RETURNING item_id ".format(entry_count, item_name, details, price, image_url, item_id, vendor_id, category)
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
                'item_id' : item_id,
                'category' : category
            }
            return {'result':'Success','data': item}
        else:
            return {'result':'Failed'}


    #Update items in table 
    def update_an_item_in_tbl(self,item_name,details,price,image_url,app_state,item_id):
        db_name = ServiceSpace.get_db_status(self,app_state)
        cur = base_creation(self,db_name)
        result = None
        try:
            query = "UPDATE administrator_items SET item_name = '{}',details = '{}',price = '{}',image_url = '{}' WHERE item_id = '{}'  RETURNING item_id ".format(item_name, details, price, image_url, item_id)
            cur.execute(query)
            result = cur.fetchone()[0]
            cur.close()
        except Exception as e:
            print('An error occurred.The error : {}'.format(e))

        print('result is {} Item is {}'.format(result,item_id))
        if int(result) == int(item_id):
            item = {
                'details' : details,
                'item_name' : item_name,
                'price' : price,
                'image_url' : image_url,
                'item_id' : item_id
            }
            return {'response':'Update Success','data': item, 'status' : 1}
        else:
            return {'response':'Update Failed', 'data': 'None', 'status' : 0}


    #Return all items in the items table( From all vendors)
    def get_specific_vendor_items(self,app_state,vendor_id):
    
        db_name = ServiceSpace.get_db_status(self,app_state)
        cur = base_creation(self,db_name)
        query = "SELECT * FROM administrator_items WHERE vendor_id = '{}'".format(vendor_id)
        cur.execute(query)
        results = cur.fetchall() #Fetches data in a list
        row_count = cur.rowcount
        orders_list = []
        if row_count < 1:
            return {'message':'Nothing here for you, Human!','mess':0}
        else:
            print(results)
            for result in results:
                item = {
                    'item_name': result[1],
                    'details': result[2],
                    'price' : result[3],
                    'image_url': result[4],
                    'item_id': result[5],
                    'vendor_id': result[6],
                    'category' : result[7]
                    }
                orders_list.append(item)
            return {'items_list': orders_list}

    def delete_from_items(self,app_state,item_id):
        '''Delete item from table'''
        db_name = ServiceSpace.get_db_status(self,app_state)
        cur = base_creation(self,db_name)
        sql = "DELETE FROM administrator_items WHERE item_id = '{}'".format(item_id)
        cur.execute(sql)

    def get_profile(self,app_state,id,type):
        db_name = ServiceSpace.get_db_status(self,app_state)
        cur = base_creation(self,db_name)
        if(type == 'admin'):
            query = "SELECT * FROM administrator_registrations WHERE vendor_id = '{}'".format(id)
            cur.execute(query)
            results = cur.fetchall()  
            if len(results) < 1:
                return {'response' : 'Admin Data Fetch Error', 'data' : 'That admin does not exist', 'status' : 0 }  

            for result in results:
                admin_details = {
                    'username' : result[1],
                    'vendor_name': result[2],
                    'details': result[3],
                    'location': result[4],
                    'image_url': result[5],
                    'phone_number' : result[6],
                    'email' : result[7]
                    }
            return {'response' : 'Admin Data Fetched Success', 'data' : admin_details, 'status' : 1 }

        elif (type == 'customer'):
            query = "SELECT * FROM customer_registration WHERE customer_id = '{}'".format(id)
            cur.execute(query)
            results = cur.fetchall()  
            if len(results) < 1:
                return {'response' : 'Customer Data Fetch Error', 'data' : 'That customer does not exist', 'status' : 0 }  

            for result in results:
                customer_details = {
                    'customer_name' : result[1],
                    'about' : result[2],
                    'location' : result[3],
                    'image_url' : result[4],
                    'phone_no' : result[5],
                    'email' : result[6],
                    'customer_id' : result[7],
                    'reg_date' : str(result[9])
                }
            return {'response' : 'Customer Data Fetched Success', 'data' : customer_details, 'status' : 1 }
        
    def update_user_details(self,customer_name,email,phone,location,about,customer_id,app_state):
        '''Update the customer's details'''
        db_name = ServiceSpace.get_db_status(self,app_state)
        cur = base_creation(self,db_name)
        result = None
        try:
            query = "UPDATE customer_registration SET customer_name = '{}',about = '{}',phone_no = '{}',email = '{}' WHERE customer_id = '{}'  RETURNING customer_id ".format(customer_name, about, phone, email, customer_id)
            cur.execute(query)
            result = cur.fetchone()[0]
            cur.close()
        except Exception as e:
            print('An error occurred.The error : {}'.format(e))

        print('result is {} Item is {}'.format(result,customer_id))
        if result == customer_id:
            customer_details = {
                'customer_name' : customer_name,
                'email'  : email,
                'phone' : phone,
                'location' : location,
                'about' : about
                }
            return {'response':'Update Success','data': customer_details, 'status' : 1}
        else:
            return {'response':'Update Failed', 'data': 'None', 'status' : 0}
        

    def get_related_items(self,item_id,category,app_state):
        '''Fetch all related Items'''
        db_name = ServiceSpace.get_db_status(self,app_state)
        cur = base_creation(self,db_name)
        query = "SELECT * FROM administrator_items WHERE category = '{}' AND item_id NOT IN ('{}') ORDER BY item_id LIMIT 3 ".format(category,item_id)
        cur.execute(query)
        results = cur.fetchall() #Fetches data in a list
        row_count = cur.rowcount
        orders_list = []
        if row_count < 1:
            return {'response':'No related Items','status':0}
        else:
            print(results)
            for result in results:
                item = {
                    'item_name': result[1],
                    'details': result[2],
                    'price' : result[3],
                    'image_url': result[4],
                    'item_id': result[5],
                    'vendor_id': ServiceSpace.getVendorDetails(self,app_state,result[6]),                    
                    'category' : result[7]
                    }
                orders_list.append(item)
            return {'related_list': orders_list}