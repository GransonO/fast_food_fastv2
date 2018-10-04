import psycopg2
#Connects to the DB
def base_creation(self,db_name):
    Host = 'ec2-75-101-153-56.compute-1.amazonaws.com'
    User = 'zmpgcuupebdapt'
    Port = '5432'
    db_name = 'd8cv78aggrjnp3'
    Password = '2281a9c0b937637b819852eb171db14e790e4c74a544a101f12a604535697aea'

    try:
        conn = psycopg2.connect("dbname={} user={} password={} host={} port={}".format(db_name,User,Password,Host,Port))
        conn.autocommit=True #with this there's no need to call commit after execute
        cur = conn.cursor()
        return cur 
    except:
        return 'Could not connect to db' 