from pymongo import MongoClient
client = MongoClient('mongodb://172.29.1.9:27017/')
db = client['wekan']
collection = db['swimlanes']
for document in collection.find():
    print(f"{' ' * 8}\"{document['title']}\": \"{document['_id']}\",")
client.close()