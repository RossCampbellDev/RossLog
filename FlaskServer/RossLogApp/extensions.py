import os

from dotenv import load_dotenv
from pymongo import MongoCLient

load_dotenv()
MONGO_CONN_STRING = os.environ.get('MONGO_CONN_STRING')

client = MongoCLient(MONGO_CONN_STRING)
db = client["log-db"]