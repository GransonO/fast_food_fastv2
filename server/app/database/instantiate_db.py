#Create database and respective tables
from .db_init import base_creation 
from .tables import SqlTables
class DatabaseBase():
    '''Creates Production database'''

    def get_db_status(self,db_state):
        '''Assign name to database according to states'''
        if db_state == 'Production': #For production
            db_name = 'fast_food_db'
        else:
            db_name = 'test_fast_food_db' #For testing
        return db_name
    
    def checkDbState(self,databasename):
        print(' => Passed db : {}'.format(databasename))
        cur = base_creation(self,databasename)
        return cur

    def create_db(self,db_state):
        '''Creates a db in start'''
        cur = base_creation(self,'postgres')
        db_name = DatabaseBase.get_db_status(self,db_state)
        print('Creating {}'.format(db_name))
        cur.execute("CREATE DATABASE {}".format(db_name))
        cur.close()

    #Create the necessary tables
    def create_tables(self,db_state):
        '''Creates all db tables'''
        db_name = DatabaseBase.get_db_status(self,db_state)
        print('Creating tables for {}'.format(db_name))

        tables = None
        if db_name == 'fast_food_db': #Production db
            tables = SqlTables.production_database_tables
        else:
            tables = SqlTables.test_database_tables

        cur = base_creation(self,db_name)
        for table in tables:
            print('DB Action => {} '.format(table))
            try:
                cur.execute(table)
            except Exception as e:
                print('Create Table error : {}'.format(e))
        cur.close()

    #Drop db
    def drop_db(self,db_state):
        print('Droping {} database ...'.format(db_state))
        db_name = DatabaseBase.get_db_status(self,db_state)
        if db_state == 'Testing':
            cur = base_creation(self,'postgres') #Use admin privilege to drop db
            cur.execute('DROP DATABASE IF EXISTS  {}'.format(db_name))
            cur.close()

    #Drop tables
    def drop_tb(self,db_state):
        print('Droping Tables for {} database ...'.format(db_state))
        db_name = DatabaseBase.get_db_status(self,db_state)
        
        tables = None
        if db_name == 'fast_food_db': #Production db
            tables = SqlTables.database_tables_names
        else:
            tables = SqlTables.database_tables_names
        
        cur = base_creation(self,db_name)
        for table_name in tables:
            print('Dropping {} '.format(table_name))
            cur.execute('DROP TABLE IF EXISTS {}'.format(table_name))
        cur.close()


    #Calls each build function in order
    def order_of_creation(self,db_state):
        #DatabaseBase.drop_db(self,db_state) #Drop DB if exists
        #DatabaseBase.create_db(self,db_state) #Create DB
        DatabaseBase.drop_tb(self,db_state)
        DatabaseBase.create_tables(self,db_state) #Create tables
        return 'Creation Success for state {}.'.format(db_state)
