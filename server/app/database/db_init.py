import psycopg2

#Connects to the DB
def base_creation(self,db_name):
    Host = 'ec2-79-125-14-195.eu-west-1.compute.amazonaws.com'
    db_name = 'dedk65lu11g1fu'
    User = 'klwlbptnwhgrfu'
    Port = '5432'
    Password = '047e97a8129573fee0f42072fc7220b544d1068f4cf56ffd37df008db6c05ad2'
    
    try:
        conn = psycopg2.connect("dbname={} user={} password={} host={} port={}".format(db_name,User,Password,Host,Port))
        #conn = psycopg2.connect("dbname={} user=postgres password=Power host=localhost".format(db_name))
        conn.autocommit=True #with this there's no need to call commit after execute
        cur = conn.cursor()
        return cur 
    except Exception as e:
        print('An error occurred.The error : {}'.format(e))
        return 'Could not connect to db'
