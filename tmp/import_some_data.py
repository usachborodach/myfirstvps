import os
import yaml
from pymongo import MongoClient

base_path = os.path.dirname(__file__)
os.chdir(base_path)

client = MongoClient()

for filename in os.listdir('exported_data'):
    file = open(f'exported_data/{filename}')
    docs = yaml.safe_load(file)
    splitted_filename = filename.split('.')
    db_name, collection_name = splitted_filename[0], splitted_filename[1]
    db = client[db_name]
    collection = db[collection_name]
    collection.insert_many(docs)