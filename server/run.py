from flask import Flask
from flask_restplus import Api

from app.api.v2 import routes

if __name__ == '__main__':
    import os  
    port = int(os.environ.get('PORT', 5000)) 
    routes.app.run(host='127.0.0.1', port=port) #Change host to 127.0.0.1 to test locally 
