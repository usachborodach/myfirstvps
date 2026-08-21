import pymongo, time, json, os
base_path = os.path.dirname(__file__)
ids_path = os.path.join(base_path, 'ids.json')
ids = json.loads(open(ids_path, encoding='utf-8').read())
mongo_instance = pymongo.MongoClient("mongodb://192.168.0.103:27017/")
database = mongo_instance["wekan"]
cards_collection = database["cards"]
doned_swimlaneid = ids['swimlanes']['doned']
myquery = {"$and": [{"swimlaneId": doned_swimlaneid}, {"archived": False}]}
newvalues = { "$set": { "archived": True } }
cards_collection.update_many(myquery, newvalues)
print('wekan doned tasks is archived')
time.sleep(0.5)