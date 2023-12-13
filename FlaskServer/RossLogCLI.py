import os
from datetime import datetime

import requests

url = 'http://127.0.0.1:5002'

def clear():
	os.system('cls' if os.name == 'nt' else 'clear')


def write():
	clear()
	print("--- NEW ENTRY ---")
	data = {}
	try:
		data["entry-title"] = input("Enter Title: ")
		data["entry-body"] = input("Enter Body: ")
		data["entry-tags"] = input("Enter Tags: ").replace(" ", "").split(",")
	except:
		clear()
		print("You're supposed to enter stuff")
		return

	response = requests.post(url + '/write', data=data)
	clear()
	if response.status_code == 200:
		print("Entry Added!\n")
	else:
		print(f'Uh-oh, didn\'t work! <HTTP {response.status_code}>')


def search():
	clear()
	print("--- SEARCH ENTRIES ---")

	criteria = {}
	criteria["search-title"] = input("Search Title: ")
	criteria["search-body"]  = input("Search Body: ")
	criteria["search-tags"]  = input("Search Tags: ").replace(" ", "").split(",")
	start_date = input("Date From (yyyy-mm-dd): ")
	end_date = input("Date To (yyyy-mm-dd): ")
			
	if start_date:
		criteria["start-date"] = datetime.strptime(start_date, '%Y-%m-%d')
	if end_date:
		criteria["end-date"] = datetime.strptime(end_date, '%Y-%m-%d')

	response = requests.post(url + '/search/json/', data=criteria)
	clear()
	if response.status_code == 200:
		result = response.json()
		for entry in result:
			print("-------------------------------------------------------------------")
			print(f'{entry["datestamp"]} - {entry["title"]} ({entry["tags"]})\n{entry["body"]}')
		print("") # make a bit of space before menu
	else:
		print(f'Uh-oh, didn\'t work! <HTTP {response.status_code}>')


if __name__ == "__main__":
	sentinel = False
	while not sentinel:
		print("1. Write New Entry")
		print("2. Search Entries")
		print("3. Exit")
		choice = input("")
		clear()
		
		match choice:
			case "1":
				write()
			case "2":
				search()
			case "3":
				sentinel = True
			case _:
				print("try again...")

	exit()