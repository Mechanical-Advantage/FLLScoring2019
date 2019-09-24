"""This module is the main Flask web application for the FLL Pit Display."""

from flask import Flask

# Initialize the Flask application
APP = Flask(__name__)
APP.config.from_object('config')

# Import necessary objects
from models import *
from api import *
from views import *

# Link the database to the Flask application
if APP.config['TEST_DB']:
    DB.init_app(APP)

if __name__ == '__main__':
    APP.run(host='0.0.0.0', debug=APP.config['DEBUG'])
