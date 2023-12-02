import os

from dotenv import load_dotenv
from pymongo import MongoCLient

load_dotenv()
MONGO_CONN_STRING = os.environ.get('MONGO_CONN_STRING')
MONGO_USER = os.environ.get('DB_USER')
MONGO_PASS = os.environ.get('DB_PASS')
MONGO_CONN_STRING = MONGO_CONN_STRING.replace('<username>', MONGO_USER)
MONGO_CONN_STRING = MONGO_CONN_STRING.replace('<password>', MONGO_USER)

db_client = MongoCLient(MONGO_CONN_STRING)

client = MongoCLient(MONGO_CONN_STRING)
db = client["log-db"]