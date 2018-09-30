import psycopg2
from db_secret import db_secrets

#Connects to the DB
def base_creation(self,db_name):
    try:
        conn = psycopg2.connect("dbname={} user={} password={} host=localhost".format(db_name,db_secrets['username'],db_secrets['password']))
        conn.autocommit=True #with this there's no need to call commit after execute
        cur = conn.cursor()
        return cur 
    except:
        return 'Could not connect to db' 