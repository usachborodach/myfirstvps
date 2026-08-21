import pymongo, os, json
base_path = os.path.dirname(__file__)
ids_path = os.path.join(base_path, 'ids.json')
ids = json.loads(open(ids_path, encoding='utf-8').read())
export_path = os.path.join(base_path, 'wekan_export.json')
export = json.loads(open(export_path, encoding='utf-8').read())

mongo_instance = pymongo.MongoClient('mongodb://172.31.255.32:27017/')
database = mongo_instance['wekan']
cards_collection = database['cards']

for swimlanename, cardtitles in export.items():
    swimlaneid = ids['swimlanes'][swimlanename]
    for cardtitle in cardtitles:
        myquery = {'title': cardtitle}
        newvalues = {'$set': {'swimlaneId': swimlaneid}}
        cards_collection.update_one(myquery, newvalues)
        print(f'Updated "{cardtitle}" to {swimlanename}')