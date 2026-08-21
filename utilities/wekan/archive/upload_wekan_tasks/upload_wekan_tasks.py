from pymongo import MongoClient
import yaml

MONGO_URL = 'mongodb://172.29.1.9:27017'
ALL_BOARDS = ['work', 'home']
CHOSEN_BOARD = 'work'
UNWANTED_LISTS = ['Дейлик', 'Архив']

def main():
    global client
    global db
    global lists_ids
    client, db = connect_to_mongo()
    board_id = get_board_id()
    lists_ids = get_lists_ids(board_id)
    cards = get_cards(board_id)
    cards = filter_unwanted_lists(cards)
    structure = build_structure(cards)
    dump_to_yaml(structure, 'structure')
    dump_to_yaml(list(structure.keys()), 'list_names')
    client.close()

def build_structure(cards):
    structure = dict()
    for card in cards:
        if get_list_title(card) not in structure.keys():
            structure[get_list_title(card)] = list()
        structure[get_list_title(card)].append(card['title'])
    return structure

def get_list_title(card):
    return lists_ids[card['listId']]

def get_lists_ids(board_id):
    collection = db['lists']
    query = {'boardId': board_id}
    projection = {'title': 1}
    docs = list(collection.find(query, projection))
    res = dict()
    for doc in docs:
        res[doc['_id']] = doc['title']
    return res

def get_unwanted_lists_ids():
    collection = db['lists']
    query = {'title': {'$in': UNWANTED_LISTS}}
    projection = {'_id': 1}
    docs = list(collection.find(query, projection))
    res = list()
    for doc in docs:
        res.append(doc['_id'])
    return res

def filter_unwanted_lists(cards):
    unwanted_lists_ids = get_unwanted_lists_ids()
    res = list()
    for card in cards:
        if card['listId'] not in unwanted_lists_ids:
            res.append(card)
    return res

def get_cards(board_id):
    collection = db['cards']
    query = {'boardId': board_id, 'archived': False}
    projection = {'_id': 0, 'title': 1, 'boardId': 1, 'listId': 1, 'sort': 1}
    return list(collection.find(query, projection).sort('sort', 1))

def dump_to_yaml(data, filename):
    with open(f'{filename}.yml', 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

def get_board_id():
    collection = db['boards']
    query = {'title': CHOSEN_BOARD}
    projection = {'_id': 1}
    docs = list(collection.find(query, projection))
    return docs[0]['_id']

def connect_to_mongo():
    client = MongoClient(MONGO_URL)
    db = client['wekan']
    return client, db

if __name__ == "__main__":
    main()