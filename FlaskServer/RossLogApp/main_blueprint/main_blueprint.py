import json
from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, session
from flask_login import current_user, login_required, login_user, logout_user

from ..log_factory import get_logger
from ..models.entry_model import Entry
from ..models.user_model import User

logger = get_logger(__name__)

main_blueprint = Blueprint("main_blueprint", __name__, static_folder="static", template_folder="templates")

# HOME
@main_blueprint.route("/", methods=["GET", "POST"])
@main_blueprint.route("/<entry_id>", methods=["GET", "POST"])
@login_required
def home(entry_id=None):    
	if request.path == '/favicon.ico':	# well this is dumb
		return '', 204
	if not current_user.is_authenticated:
		return redirect("/login", 302)
	
	read_entry = Entry.to_presentation_object(Entry.get_by_id(entry_id)) if entry_id is not None else None
	
	# entries = Entry.get_all()
	selected_month = None
	if request.method == "POST":
		selected_month = request.form.get("select-month")
	if selected_month is None:
		this_month = f'0{datetime.now().month}'
		selected_month = f'{datetime.now().year}-{this_month[-2:]}'

	entries = Entry.get_by_month(selected_month)
	for entry in entries:
		entry["datestamp"] = entry["datestamp"].strftime("%Y-%m-%d %H:%M")
		
	return render_template("home.html", entries=entries, read_entry=read_entry, selected_month=selected_month)


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
		flash_msg("INVALID LOGIN CREDENTIALS")
		return redirect("login", 302)
 
	if not User.check_pass(username, password):
		flash_msg("INVALID LOGIN CREDENTIALS")
		return redirect("login", 302)
	
	login_user(User.to_object(user))

	# return render_template("home.html", current_user=current_user)
	return redirect("/", 302)


# LOGOUT
@main_blueprint.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
	logout_user()
	flash_msg("Logout successful!")
	return redirect("/login", 302)


# Retrieve log(s)
@main_blueprint.route("/search/", methods=["GET", "POST"])
@login_required
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
			
			if start_date:
				start_date = datetime.strptime(start_date, '%Y-%m-%d')
			if end_date:
				end_date = datetime.strptime(end_date, '%Y-%m-%d')

			if start_date and end_date:
				criteria["datestamp"] = {'$gte': start_date, '$lte': end_date}
			elif start_date:
				criteria["datestamp"] = {'$gte': start_date}
			elif end_date:
				criteria["datestamp"] = {'$lte': end_date}

			if title:
				criteria["title"] = {'$regex': title}
			if body:
				criteria["body"] = {'$regex': body} if body else None
			if tags:
				tags = [tag.strip() for tag in tags.strip().split(',')]
				criteria["tags"] = {'$elemMatch': {'$in': tags}}

			entries = Entry.get_by_criteria(criteria)

		if not form_data or not entries:
			flash_msg('Search returned no results...')
			entries = Entry.get_all()

		for entry in entries:
			entry["datestamp"] = entry["datestamp"].strftime("%Y-%m-%d %H:%M")

	return render_template("home.html", entries=entries)


# for CLI API
@main_blueprint.route("/search/json/", methods=["GET", "POST"])
def search_json():
	if request.method == "GET":
		entries = Entry.get_all()
	else:
		form_data = request.form
		print(form_data)
		if form_data is not None:
			criteria = {}
			start_date = form_data.get("start-date")
			end_date = form_data.get("end-date")
			title = form_data.get("search-title")
			body = form_data.get("search-body")
			tags = form_data.get("search-tags")

			if title:
				criteria["title"] = {'$regex': title}
			if body:
				criteria["body"] = {'$regex': body} if body else None
			if tags:
				tags = [tag.strip() for tag in tags.strip().split(',')]
				criteria["tags"] = {'$elemMatch': {'$in': tags}}
			
			if start_date:
				start_date = datetime.strptime(start_date, '%Y-%m-%d')
			if end_date:
				end_date = datetime.strptime(end_date, '%Y-%m-%d')

			if start_date and end_date:
				criteria["datestamp"] = {'$gte': start_date, '$lte': end_date}
			elif start_date:
				criteria["datestamp"] = {'$gte': start_date}
			elif end_date:
				criteria["datestamp"] = {'$lte': end_date}

			entries = Entry.get_by_criteria(criteria)

		if not form_data or not entries:
			flash_msg('Search returned no results...')
			entries = Entry.get_all()

	for entry in entries:
		entry["_id"] = None	# dont send IDs to API users
		entry["datestamp"] = entry["datestamp"].strftime("%Y-%m-%d %H:%M")

	json_data = json.dumps(entries)

	return entries


# add new entry
@main_blueprint.route("/write", methods=["GET", "POST"])
def write():
	if request.method == "GET":
		return redirect("/", 302)
	
	errors = []
	d = request.form
	new_title = d.get("entry-title")
	new_body  = d.get("entry-body")
	new_tags  = d.get("entry-tags").replace("\r\n", ",").replace("\n", ",").replace(", ", ",").replace(",,", ",").split(",")
	entry_id  = d.get("entry-id")

	if not new_title:
		errors.append("missing title")
	if not new_body:
		errors.append("missing body text")

	if errors:
		flash_msg("Error writing entry: " + ", ".join(errors))
	
	if not errors:
		if entry_id:
			existing_entry = Entry.to_object(Entry.get_by_id(entry_id))
			if existing_entry:
				existing_entry.title = new_title
				existing_entry.body = new_body 
				existing_entry.tags = new_tags if new_tags else []
				existing_entry.update(entry_id)
				flash_msg("Entry updated!")
		else:		
			new_entry = Entry(
					title=new_title, body=new_body, tags=new_tags
				)
			entry_id = new_entry.save()
			flash_msg("Entry saved!")

	return redirect("/", 302)


@main_blueprint.route("/delete/<entry_id>", methods=["GET", "POST"])
@login_required
def delete(entry_id: str):
	to_delete_entry = Entry.to_object(Entry.get_by_id(entry_id))
	to_delete_entry.delete()
	flash_msg("Entry Deleted!")
	return redirect("/", 302)


def flash_msg(msg: str=""):
	# session['_flashes'].clear()
	flash(msg)