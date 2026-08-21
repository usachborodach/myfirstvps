archive_older_than = 2

import os
import re
import json
from datetime import datetime, timedelta
from pymongo import MongoClient

base_path = os.path.dirname(__file__)
ids_path = os.path.join(base_path, 'ids.json')
ids = json.loads(open(ids_path, encoding='utf-8').read())

def get_swimlanes_to_move():
    swimlanes_to_move = list()
    for document in swimlanes_collection.find():
        if document['boardId'] == ids['board_id']:
            swimlanes_to_move.append(document['title'])
    swimlanes_to_move = [item for item in swimlanes_to_move if bool(re.fullmatch(r'\d{2}\.\d{2}', item))]
    swimlanes_to_move = sorted(swimlanes_to_move, key=lambda x: datetime.strptime(x, '%d.%m'))
    current_date = datetime.now()
    filtered_list = list()
    for item in swimlanes_to_move:
        item_date = datetime.strptime(item, '%d.%m').replace(year=current_date.year)
        if (current_date - item_date) >= timedelta(days=archive_older_than):
            filtered_list.append(item)
    return filtered_list

def switch_board_id_in_swimlane(swimlane_title):
    print(swimlane_title)
    result = swimlanes_collection.update_many(
        {'title': swimlane_title}, 
        {'$set': {'boardId': ids['archive_board']}})
    print(result)
    
def switch_board_and_line_in_cards(swimlaneId):
    for list_name, list_id in ids['lists'].items():
        result = cards_collection.update_many({
            'swimlaneId': swimlaneId,
            'listId': list_id}, 
            {'$set': {
                'boardId': ids['archive_board'],
                'listId': ids['archive_lists'][list_name]}
            })
    print(result)
    
db = MongoClient('mongodb://172.29.1.9:27017/')['wekan']
swimlanes_collection = db['swimlanes']
cards_collection = db['cards']
swimlanes_to_move = get_swimlanes_to_move()
for swimlane_title in swimlanes_to_move:
    switch_board_id_in_swimlane(swimlane_title)
    for doc in swimlanes_collection.find():
        if doc['title'] == swimlane_title:
            swimlaneId = doc['_id']
            break
    switch_board_and_line_in_cards(swimlaneId)