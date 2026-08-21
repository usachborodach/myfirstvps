import json
import requests
from pymongo import MongoClient

WEKAN_URL = 'http://84.54.57.22:2000'

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

def get_token():
    auth_url = f'{WEKAN_URL}/users/login'
    auth_data = {'username': 'agorbov', 'password': 'Sven159357258'}
    response = requests.post(auth_url, data=auth_data).text
    return json.loads(response)['token']