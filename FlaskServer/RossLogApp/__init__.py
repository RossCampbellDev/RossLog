import os

from dotenv import load_dotenv
from flask import Blueprint, Flask

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

# Blueprint
from RossLogApp.main_blueprint.main_blueprint import main_blueprint

app.register_blueprint(main_blueprint, url_prefix="/")

def create_app():
    return app