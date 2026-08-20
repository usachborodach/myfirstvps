from pymongo import MongoClient
from myfirstvps.utilities.api_client.crud import create_document

uri = f"mongodb://172.29.1.9:27017/"
client = MongoClient(uri)
db = client['wekan']
coll = db['cards']
query = {'archived': False}
cursor = coll.find(query)
for doc in cursor:
    create_document('wekan', 'cards', doc)