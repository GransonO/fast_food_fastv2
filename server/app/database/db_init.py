import psycopg2

#Connects to the DB
def base_creation(self,db_name):
    Host = 'ec2-54-225-68-133.compute-1.amazonaws.com'
    Database = 'df4haveo5v04vq'
    User = 'xbrpdqtjsmtxfp'
    Port = '5432'
    Password = 'bdfdec3c6bfec300a06f78d99aa45fc7a3443425eb8a164013a6610a234cb92d'

    try:
        conn = psycopg2.connect("dbname={} user={} password={} host={} port={}".format(Database,User,Password,Host,Port))
        conn.autocommit=True #with this there's no need to call commit after execute
        cur = conn.cursor()
        return cur 
    except:
        return 'Could not connect to db' 