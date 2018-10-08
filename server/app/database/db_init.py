import psycopg2

#Connects to the DB
def base_creation(self,db_name):
    try:
        conn = psycopg2.connect("dbname={} user=postgres password=Power host=localhost".format(db_name))
        conn.autocommit=True #with this there's no need to call commit after execute
        cur = conn.cursor()
        return cur 
    except:
        return 'Could not connect to db'