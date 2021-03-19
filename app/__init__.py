"""
Service API initialize module
"""
import os
from flask import Flask, redirect
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from config.config import config_map

"""Create service API endpoint"""
# Get environment value
environment = os.getenv('Environment').capitalize()
environment = environment if environment in config_map.keys() else 'Staging'

# Create and configure main app
app = Flask(__name__, static_url_path='', static_folder='../app/web/static', template_folder='../app/web/templates')


@app.route('/')
def route():
    return redirect('/books')


# Configure app
app.config.from_object(config_map[environment])

# Initialize login extensions
login_manager = LoginManager(app)

# Create db object for app
db = SQLAlchemy(app)

from app.web import views
from app.authorization import auth
