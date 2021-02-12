from pymongo import MongoClient
from secrets import URI, DB_NAME

client = MongoClient(URI)
db = client[DB_NAME]
