# from myfirstvps.utilities.api_client.crud import get_all_docs

# dbs = ['quote_gun', 'tracker']

# for db in dbs:
#     get_all_docs(db)


from pymongo import MongoClient

ADDRESS = 'localhost'
port = 29017

client = MongoClient(ADDRESS, port)

dbs = ['quote_gun', 'tracker']

for db_name in dbs:
    db = client[db_name]               # получаем объект базы данных
    collections = db.list_collection_names()   # список имён коллекций
    print(f"База '{db_name}':")
    for col in collections:
        print(f"  - {col}")