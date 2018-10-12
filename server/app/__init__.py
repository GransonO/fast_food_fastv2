from flask import Flask
from flask_cors import CORS
from instance.config import App_Configurations
from .database.instantiate_db import DatabaseBase
from .database.db_init import base_creation

def create_app(Config_Status):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(App_Configurations[Config_Status]) #'Developing','Testing','Production'
    database = DatabaseBase()

    databasename = database.get_db_status(Config_Status)
    #Create specific database
    if Config_Status != 'Production':
        print('Checking if {} Database Exists ....'.format(Config_Status))
        cur = database.checkDbState(databasename) #Check if connection to passed db
        print('Cursor says : {}!'.format(cur))
        #print(database.order_of_creation(Config_Status))
        print('Required database set for action')    

    return app
