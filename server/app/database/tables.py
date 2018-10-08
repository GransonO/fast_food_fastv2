class SqlTables():
    '''Holds all database tables'''
    #Production tables
    items_tables = "CREATE TABLE administrator_items ( id SERIAL PRIMARY KEY, item_name TEXT, details TEXT, price REAL, image_url TEXT, item_id TEXT, vendor_id TEXT)"
    vendors_table = "CREATE TABLE administrator_registrations ( id SERIAL PRIMARY KEY, username TEXT, vendor_name TEXT, details TEXT, location TEXT, image_url TEXT, phone_no TEXT, email TEXT, vendor_id TEXT, adm_password TEXT, reg_date TIMESTAMP, reg_state TEXT)"
    orders_table = "CREATE TABLE orders_tbl ( id SERIAL PRIMARY KEY, order_date TIMESTAMP,  order_id TEXT, order_detail TEXT, order_amount REAL, order_from TEXT, order_to TEXT, order_status TEXT,status_changed TIMESTAMP)"
    customer_tables = "CREATE TABLE customer_registration( id SERIAL PRIMARY KEY, customer_name TEXT, about TEXT, location TEXT, image_url TEXT, phone_no TEXT, email TEXT, customer_id TEXT, cus_password TEXT, reg_date TIMESTAMP,reg_state TEXT)"

    production_database_tables = [items_tables,vendors_table,orders_table,customer_tables]

    #Tests tables
    test_items_tables = "CREATE TABLE administrator_items ( id SERIAL PRIMARY KEY, item_name TEXT, details TEXT, price REAL, image_url TEXT, item_id TEXT, vendor_id TEXT)"
    test_vendors_table = "CREATE TABLE administrator_registrations ( id SERIAL PRIMARY KEY, username TEXT, vendor_name TEXT, details TEXT, location TEXT, image_url TEXT, phone_no TEXT, email TEXT, vendor_id TEXT, adm_password TEXT, reg_date TIMESTAMP, reg_state TEXT)"
    test_orders_table = "CREATE TABLE orders_tbl ( id SERIAL PRIMARY KEY, order_date TIMESTAMP,  order_id TEXT, order_detail TEXT, order_amount REAL, order_from TEXT, order_to TEXT, order_status TEXT,status_changed TIMESTAMP)"
    test_customer_tables = "CREATE TABLE customer_registration( id SERIAL PRIMARY KEY, customer_name TEXT, about TEXT, location TEXT, image_url TEXT, phone_no TEXT, email TEXT, customer_id TEXT, cus_password TEXT, reg_date TIMESTAMP,reg_state TEXT)"

    test_database_tables = [test_items_tables,test_vendors_table,test_orders_table,test_customer_tables]