import psycopg2

#Connects to the DB
def base_creation(self,db_name):
    Host = 'ec2-54-247-101-191.eu-west-1.compute.amazonaws.com'
    db_name = 'd9fpabqvje4pfk'
    User = 'awpvubyrjvurpb'
    Port = '5432'
    Password = 'bfad832890724724d4acf710faef3820fb5fa1423a60319438a33a1933a47554'
    
    try:
        conn = psycopg2.connect("dbname={} user={} password={} host={} port={}".format(db_name,User,Password,Host,Port))
        conn.autocommit=True #with this there's no need to call commit after execute
        cur = conn.cursor()
        return cur 
    except:
        return 'Could not connect to db'
