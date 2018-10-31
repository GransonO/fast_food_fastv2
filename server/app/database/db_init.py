import psycopg2

#Connects to the DB
def base_creation(self,db_name):
    Host = 'ec2-54-75-239-237.eu-west-1.compute.amazonaws.com'
    db_name = 'd41f017o9eva2p'
    User = 'hqomzgqqgfgcnp'
    Port = '5432'
    Password = '760c64769ce69ec4829cafb57c00cd44acf12b7b6f4d729b9d51a2214a15f0fd'
    
    try:
        #conn = psycopg2.connect("dbname={} user={} password={} host={} port={}".format(db_name,User,Password,Host,Port))
        conn = psycopg2.connect("dbname={} user=postgres password=Power host=localhost".format(db_name))
        conn.autocommit=True #with this there's no need to call commit after execute
        cur = conn.cursor()
        return cur 
    except Exception as e:
        print('An error occurred.The error : {}'.format(e))
        #return 'Could not connect to db'
