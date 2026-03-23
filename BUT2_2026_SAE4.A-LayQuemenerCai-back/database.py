from pymongo import MongoClient

db_uri = 'mongodb://127.0.0.1:27017/'
database = MongoClient(db_uri)
db = database.table
