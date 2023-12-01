from flask import Blueprint, redirect, render_template, request

main_blueprint = Blueprint("main_blueprint", __name__, static_folder="static", template_folder="templates")

# HOME
@main_blueprint.route("/", methods=["GET"])
def home():
    return render_template("home.html")