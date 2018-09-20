from flask import Flask
from flask_restplus import Resource,Api
from app import create_app

flask_app = create_app('Developing')

#from app.api.v1 import routes

if __name__ == '__main__':
    flask_app.run()