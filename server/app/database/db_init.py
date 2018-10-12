import psycopg2

#Connects to the DB
def base_creation(self,db_name):
    Host = 'ec2-46-51-184-229.eu-west-1.compute.amazonaws.com'
    db_name = 'd2atgsnecjnp3c'
    User = 'wywkzbvvmrhxiw'
    Port = '5432'
    Password = 'dd1e98da7141ef01dbf9ebf05ce1225d91b96c12542a57a5bbb251dc324250ff'
    
    try:
        conn = psycopg2.connect("dbname={} user={} password={} host={} port={}".format(db_name,User,Password,Host,Port))
        conn.autocommit=True #with this there's no need to call commit after execute
        cur = conn.cursor()
        return cur 
    except:
        return 'Could not connect to db'
