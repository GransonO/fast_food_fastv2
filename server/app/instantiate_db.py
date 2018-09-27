import psycopg2

class DatabaseBase():

    items_tables = "CREATE TABLE administrator.items ( id SERIAL PRIMARY KEY, item_name TEXT, details CHAR(100), price REAL, image_url CHAR(200), item_id CHAR(50))"
    vendors_table = "CREATE TABLE administrator.registrations ( id SERIAL PRIMARY KEY, vendor_name TEXT, details CHAR(255), location CHAR(100), image_url CHAR(155), phone_no CHAR(50), email CHAR(100), vendor_id CHAR(50), reg_date TIMESTAMP)"
    orders_table = "CREATE TABLE orders_tbl ( id SERIAL PRIMARY KEY, order_date TIMESTAMP,  order_id CHAR(50), order_detail CHAR(200), order_amount REAL, order_from CHAR(50), order_to CHAR(50), order_status CHAR(50),status_changed TIMESTAMP)"
    customer_tables = "CREATE TABLE customer.registration( id SERIAL PRIMARY KEY, customer_name TEXT, about CHAR(255), location CHAR(100), image_url CHAR(155), phone_no CHAR(50), email CHAR(100), vendor_id CHAR(50), reg_date TIMESTAMP)"

    database_tables = [items_tables,vendors_table,orders_table,customer_tables]

    #Connects to the DB
    def base_creation(self,db_name):
        try:
            conn = psycopg2.connect("dbname={} user=postgres password=Power host=localhost".format(db_name))
            conn.autocommit=True #with this there's no need to call commit after execute
            cur = conn.cursor()
            return cur 
        except:
            return 'Could not connect to db'   

    def create_db(self):
        '''Creates a db in start'''
        cur = DatabaseBase.base_creation(self,'postgres')
        cur.execute("CREATE DATABASE fast_food_db")
        cur.close()

    #Create table schema
    def create_schema(self):
        '''Creates a db'''
        cur = DatabaseBase.base_creation(self,'fast_food_db')
        cur.execute("CREATE SCHEMA administrator")
        cur.execute("CREATE SCHEMA customer")

        DatabaseBase.clean_up(self)

    #Create the necessary tables
    def create_tables(self):
        '''Creates all db tables'''
        cur = DatabaseBase.base_creation(self,'fast_food_db')
        for table in DatabaseBase.database_tables:
            cur.execute(table)

        DatabaseBase.clean_up(self) 
       
    #Cleans memory after use   
    def clean_up(self):
        '''Memory clean up'''
        cur = DatabaseBase.base_creation(self,'fast_food_db')
        cur.close()

    #Calls each build function in order
    def order_of_creation(self):
        DatabaseBase.create_db(self)
        DatabaseBase.create_schema(self)
        DatabaseBase.create_tables(self)      
       