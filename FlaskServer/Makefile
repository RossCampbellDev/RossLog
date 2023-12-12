ifeq ($(OS), Windows_NT)
# install dependencies (requirements.txt)
install: requirements.txt
	pip install -r requirements.txt

# run tests
test: /RossLogApp/unit_tests/test_entries.py
	pytest /tests/test_entries.pytest --dotenv=/RossLogApp/.flaskenv

# run app
run:
	flask run --debug
else
# install dependencies (requirements.txt)
install: requirements.txt
	pip install -r requirements.txt

# run tests
test: /RossLogApp/tests/test_entries.py
	pytest /tests/test_entries.pytest

# run app
run:
	flask run --debug
endif