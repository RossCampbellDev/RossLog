import os

from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager

from .models.user_model import User

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')
login_manager = LoginManager()
login_manager.login_view = "/login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id: int) -> User:
    return User.to_object(User.get_by_id(user_id))


# Blueprint
from RossLogApp.main_blueprint.main_blueprint import main_blueprint

app.register_blueprint(main_blueprint, url_prefix="/")

def create_app():
    return app