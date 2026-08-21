import pymongo, os, json
base_path = os.path.dirname(__file__)
ids_path = os.path.join(base_path, 'ids.json')
ids = json.loads(open(ids_path, encoding='utf-8').read())
mongo_instance = pymongo.MongoClient('mongodb://172.31.255.32:27017/')
database = mongo_instance['wekan']
cards_collection = database['cards']
cards = cards_collection.find()

def get_name_by_id(search_dict, id):
    for key, value in search_dict.items():
        if value == id:
            return key

output = dict()
for card in cards:
    if card['archived'] == True:
        continue
    if card['listId'] == ids['lists']['favorite']:
        swimlanename = get_name_by_id(ids['swimlanes'], card['swimlaneId'])
        if swimlanename not in output.keys():
            output[swimlanename] = list()
        output[swimlanename].append(card['title'])

output_path = os.path.join(base_path, 'wekan_export.json')
with open(output_path, 'w', encoding='utf-8') as file:
    json.dump(output, file, indent=4, ensure_ascii=False)