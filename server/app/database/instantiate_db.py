#Create database and respective tables
from db_init import base_creation 

class DatabaseBase():

    items_tables = "CREATE TABLE administrator_items ( id SERIAL PRIMARY KEY, item_name TEXT, details TEXT, price REAL, image_url TEXT, item_id TEXT, vendor_id TEXT)"
    vendors_table = "CREATE TABLE administrator_registrations ( id SERIAL PRIMARY KEY, username TEXT, vendor_name TEXT, details TEXT, location TEXT, image_url TEXT, phone_no TEXT, email TEXT, vendor_id TEXT, adm_password TEXT, reg_date TIMESTAMP, reg_state TEXT)"
    orders_table = "CREATE TABLE orders_tbl ( id SERIAL PRIMARY KEY, order_date TIMESTAMP,  order_id TEXT, order_detail TEXT, order_amount REAL, order_from TEXT, order_to TEXT, order_status TEXT,status_changed TIMESTAMP)"
    customer_tables = "CREATE TABLE customer_registration( id SERIAL PRIMARY KEY, customer_name TEXT, about TEXT, location TEXT, image_url TEXT, phone_no TEXT, email TEXT, customer_id TEXT, cus_password TEXT, reg_date TIMESTAMP,reg_state TEXT)"

    database_tables = [items_tables,vendors_table,orders_table,customer_tables]
 
    def create_db(self):
        '''Creates a db in start'''
        cur = base_creation(self,'postgres')
        cur.execute("CREATE DATABASE fast_food_db")
        cur.close()

    #Create the necessary tables
    def create_tables(self):
        '''Creates all db tables'''
        cur = base_creation(self,'fast_food_db')
        for table in DatabaseBase.database_tables:
            cur.execute(table)

        DatabaseBase.clean_up(self) 
       
    #Cleans memory after use   
    def clean_up(self):
        '''Memory clean up'''
        cur = base_creation(self,'fast_food_db')
        cur.close()

    #Calls each build function in order
    def order_of_creation(self):
        try:
            DatabaseBase.create_db(self)
            DatabaseBase.create_tables(self)  
            return 'Creation Success'
        except:   
            return 'Error Occurred' 
