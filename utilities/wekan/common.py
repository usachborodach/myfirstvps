from pymongo import MongoClient

def connect_to_mongo():
    client = MongoClient()
    db = client['wekan']
    return client, db

def get_board_id(db, board_title):
    collection = db['boards']
    query = {'title': board_title}
    projection = {'_id': 1}
    document = collection.find_one(query, projection)
    return document['_id']

def get_list_id(db, board_title, list_title):
    collection = db['lists']
    board_id = get_board_id(db, board_title)
    query = {'title': list_title, 'boardId': board_id}
    projection = {'_id': 1}
    document = collection.find_one(query, projection)
    return document['_id']