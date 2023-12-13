from datetime import datetime
import os, requests

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
    search_title = input("Search Title: ")
    search_body = input("Search Body: ")
    search_tags = input("Search Tags: ").replace(" ", "").split(",")
    start_date = input("Date From (yyyy-mm-dd): ")
    end_date = input("Date To (yyyy-mm-dd): ")

    criteria = {}
    criteria["search-title"] = {'$regex': search_title}
    criteria["search-body"] = {'$regex': search_body}
    criteria["search-tags"] = {'$elemMatch': {'$in': search_tags}}
			
    if start_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
    if end_date:
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

    response = requests.post(url + '/search', data=data)
    clear()
    if response.status_code == 200:
        print("Entry Added!\n")
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