from flask import Flask
from flask_restplus import Api

from app.api.v1 import routes

if __name__ == '__main__':
    routes.app.run()