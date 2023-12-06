from flask import Blueprint, redirect, render_template, request
from flask_login import current_user, login_required, login_user, logout_user

from ..models.entry_model import Entry
from ..models.user_model import User

main_blueprint = Blueprint("main_blueprint", __name__, static_folder="static", template_folder="templates")

# HOME
@main_blueprint.route("/", methods=["GET"])
def home():
    if not current_user.is_authenticated:
      return redirect("/login", 302)
    
    entries = Entry.get_all()
    return render_template("home.html", entries=entries)


# LOGIN
@main_blueprint.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    form_data = request.form
    username = form_data.get('user')
    password = form_data.get('pass')

    user = User.get_by_username(username)

    if not user:
        print("ERRROR WRONG USER")
        # flash wrong user
        return redirect("login", 302)
 
    if not User.check_pass(username, password):
        # flash wrong pw
        print("ERRROR WRONG PW")
        return redirect("login", 302)
    
    login_user(User.to_object(user))

    # return render_template("home.html", current_user=current_user)
    return redirect("/", 302)


# LOGOUT
@main_blueprint.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    return redirect("/login", 302)


# Retrieve log(s)
@main_blueprint.route("/retrieve/", methods=["GET", "POST"])
def retrieve():
    if request.method == "GET":
        entries = Entry.get_all()

    criteria = request.form
    if criteria is not None:
        print(criteria)
        # entries = {}

    # mongo db query

    # build dictionary of returned results, display

    return render_template("home.html", entries=entries)


# add new entry
@main_blueprint.route("/write", methods=["GET", "POST"])
def write():
    if request.method == "GET":
        return redirect("/", 302)
    
    d = request.form
    new_entry = Entry(title=d["entry-title"], body=d["entry-body"], tags=d["entry-tags"])
    id = new_entry.save()

    if id is None:
        print("didnt save")
        # flash

    return redirect("/", 302)