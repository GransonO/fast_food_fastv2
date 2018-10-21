class SqlTables():
    '''Holds all database tables'''
    #Production tables
    items_tables = "CREATE TABLE administrator_items ( id REAL, item_name TEXT, details TEXT, price REAL, image_url TEXT, item_id TEXT  PRIMARY KEY, vendor_id TEXT)"
    vendors_table = "CREATE TABLE administrator_registrations ( id REAL, username TEXT, vendor_name TEXT, details TEXT, location TEXT, image_url TEXT, phone_no TEXT, email TEXT, vendor_id TEXT PRIMARY KEY, adm_password TEXT, reg_date TIMESTAMP, reg_state TEXT)"
    orders_table = "CREATE TABLE orders_tbl ( id REAL, order_date TIMESTAMP,  order_id TEXT PRIMARY KEY, order_detail TEXT, order_quantity REAL, order_amount REAL, order_from TEXT, order_to TEXT, order_status TEXT,status_changed TIMESTAMP)"
    customer_tables = "CREATE TABLE customer_registration( id REAL, customer_name TEXT, about TEXT, location TEXT, image_url TEXT, phone_no TEXT, email TEXT, customer_id TEXT PRIMARY KEY, cus_password TEXT, reg_date TIMESTAMP,reg_state TEXT)"

    production_database_tables = [items_tables,vendors_table,orders_table,customer_tables]

    #Tests tables
    test_items_tables = "CREATE TABLE administrator_items ( id REAL, item_name TEXT, details TEXT, price REAL, image_url TEXT, item_id TEXT, vendor_id TEXT)"
    test_vendors_table = "CREATE TABLE administrator_registrations ( id REAL, username TEXT, vendor_name TEXT, details TEXT, location TEXT, image_url TEXT, phone_no TEXT, email TEXT, vendor_id TEXT PRIMARY KEY, adm_password TEXT, reg_date TIMESTAMP, reg_state TEXT)"
    test_orders_table = "CREATE TABLE orders_tbl ( id REAL, order_date TIMESTAMP,  order_id TEXT PRIMARY KEY, order_detail TEXT, order_quantity REAL, order_amount REAL, order_from TEXT, order_to TEXT, order_status TEXT,status_changed TIMESTAMP)"
    test_customer_tables = "CREATE TABLE customer_registration( id REAL, customer_name TEXT, about TEXT, location TEXT, image_url TEXT, phone_no TEXT, email TEXT, customer_id TEXT PRIMARY KEY, cus_password TEXT, reg_date TIMESTAMP,reg_state TEXT)"

    test_database_tables = [test_items_tables,test_vendors_table,test_orders_table,test_customer_tables]
    database_tables_names = ['administrator_items','administrator_registrations','orders_tbl','customer_registration']