from flask import Blueprint, jsonify, redirect, render_template, request

from ..models.user_model import User

main_blueprint = Blueprint("main_blueprint", __name__, static_folder="static", template_folder="templates")

# HOME
@main_blueprint.route("/", methods=["GET", "POST"])
def home():
    # if not current_user
    #   return redirect("login", 302)
    return render_template("home.html")    # todo change to home.html when login tested


# LOGIN
@main_blueprint.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    form_data = request.form
    username = form_data.get('user')
    password = form_data.get('pass')

    if not User.check_pass(username, password):
        # flash wrong user
        return redirect("login", 302)
    
    # flask-login stuff

    return render_template("home.html", username=username)  # TODO: replace with current user when implemented flask login


# Retrieve log(s)
@main_blueprint.route("/retrieve/", methods=["GET", "POST"])
def retrieve():
    get_entries = request.json

    entries = {}

    # mongo db query
    # build dictionary of returned results, display

    return render_template("read.html", entries=entries)


# add new entry
@main_blueprint.route("/write", methods=["GET", "POST"])
def write():
    if request.method == "GET":
        return render_template("write.html")
    
    new_entry = request.json

    # write to mongo db
    # confirm entry added
    # present success screen

    return render_template("write.html") # , new_post