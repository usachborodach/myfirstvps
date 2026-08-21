import os
from datetime import datetime
import yaml
from pymongo import MongoClient

base_path = os.path.dirname(__file__)
os.chdir(base_path)

client = MongoClient()

for filename in os.listdir('exported_data'):
    file = open(f'exported_data/{filename}')
    docs = yaml.safe_load(file)
    for doc in docs:
        if 'date' in doc:
            doc['date'] = datetime.strptime(doc['date'], '%Y-%m-%dT%H:%M:%S')
    splitted_filename = filename.split('.')
    db_name, collection_name = splitted_filename[0], splitted_filename[1]
    db = client[db_name]
    collection = db[collection_name]
    collection.insert_many(docs)