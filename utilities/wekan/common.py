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

def post_card(task_text, board_name, token):
    board_ids = {'work': '6nEeTCXHcdq3GaqoT', 'home': 'eyZsGfRcPAysgBbB3'}
    list_ids = {'work': 'WwR4yf6LbzKgnhaLx', 'home': 'uj8XTX37dMJT7SByr'}
    swimlane_ids = {'work': 'xbct7XafyWxqGhhWq', 'home': 'Qh75JghWz3eyAhY9K'}
    post_the_card_url = (
        f'{WEKAN_URL}/api/'
        f'boards/{board_ids[board_name]}/'
        f'lists/{list_ids[board_name]}/cards'
    )
    headers = {
        'Authorization': f'Bearer {token}'
    }
    request_data = {
        'title': f'{task_text}',
        'description': '',
        'authorId': 'YHrRysNZnbE5eEfrh',
        'swimlaneId': f"{swimlane_ids[board_name]}"
    }
    requests.post(post_the_card_url, headers=headers, data=request_data)