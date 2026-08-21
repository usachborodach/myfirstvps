from pymongo import MongoClient

ADDRESS = 'localhost'
PORT = 27017

client = MongoClient(ADDRESS, PORT)
databases = client.list_database_names()
for db_name in databases:
    print(db_name)