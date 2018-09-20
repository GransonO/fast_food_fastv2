from flask import Flask
from instance.config import App_Configurations

def create_app(Config_Status):
    app = Flask(__name__)
    app.config.from_object(App_Configurations[Config_Status])
    app.config.from_pyfile('../instance/config.py')

    return app