from pymongo import MongoClient

"""
ssh myfirstvps "python3 /root/myfirstvps/tmp/del_cards.py"
"""

MONGO_HOST = "localhost"
MONGO_PORT = 27017
DB_NAME = "wekan"
COLL_NAME = "cards"

uri = f"mongodb://{MONGO_HOST}:{MONGO_PORT}/"
client = MongoClient(uri, serverSelectionTimeoutMS=5000)
db = client[DB_NAME]
coll = db[COLL_NAME]
result = coll.delete_many({})