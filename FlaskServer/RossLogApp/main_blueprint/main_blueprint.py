from flask import Blueprint, redirect, render_template, request
from flask_login import current_user, login_required, login_user, logout_user

from ..models.entry_model import Entry
from ..models.user_model import User

main_blueprint = Blueprint("main_blueprint", __name__, static_folder="static", template_folder="templates")

# HOME
@main_blueprint.route("/", methods=["GET"])
@main_blueprint.route("/<entry_id>", methods=["GET"])
def home(entry_id=None):
	if not current_user.is_authenticated:
		return redirect("/login", 302)
	
	read_entry = Entry.get_by_id(entry_id) if entry_id is not None else None
	entries = Entry.get_all()
	return render_template("home.html", entries=entries, read_entry=read_entry)


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
@main_blueprint.route("/search/", methods=["GET", "POST"])
def search():
	if request.method == "GET":
		entries = Entry.get_all()
	else:
		form_data = request.form
		if form_data is not None:
			criteria = {}
			start_date = form_data.get("start-date")
			end_date = form_data.get("end-date")
			title = form_data.get("search-title")
			body = form_data.get("search-body")
			tags = form_data.get("search-tags")

			if start_date and end_date:
				criteria["datestamp"] = {'$gte': start_date, '$lte': end_date}
			elif start_date:
				criteria["datetsamp"] = {'$gte': start_date}
			elif end_date:
				criteria["datetsamp"] = {'$lte': end_date}

			if title:
				criteria["title"] = {'$regex': title}
			if body:
				criteria["body"] = {'$regex': body} if body else None
			if tags:
				tags = [tag.strip() for tag in tags.split(',')]
				criteria["tags"] = {'$elemMatch': {'$in': tags}}
			
			entries = Entry.get_by_criteria(criteria)
			print(criteria)
			print(entries)
		else:
			entries = Entry.get_all()

		# mongo db query

		# build dictionary of returned results, display

	return render_template("home.html", entries=entries)


# add new entry
@main_blueprint.route("/write", methods=["GET", "POST"])
def write():
	if request.method == "GET":
		return redirect("/", 302)
	
	d = request.form
	entry_id = d["entry-id"]
	if entry_id:
		existing_entry = Entry.to_object(Entry.get_by_id(entry_id))
		if existing_entry:
			existing_entry.update(entry_id)
	else:
		new_entry = Entry(title=d["entry-title"], body=d["entry-body"], tags=d["entry-tags"])
		entry_id = new_entry.save()

	if entry_id is None:
		print("didnt save")
		# flash

	return redirect("/", 302)