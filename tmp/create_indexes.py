from pymongo import MongoClient, ASCENDING

client = MongoClient()
db = client['tracker']
db.days.create_index([("date", ASCENDING)], unique=True)