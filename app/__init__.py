from flask import Flask, jsonify

app = Flask(__name__)


# Configurations
app.config.from_object('config')


# Import modules using its blueprint handler variable
from app.views import *  # noqa

# Register blueprints
app.register_blueprint(home)
