import json
import subprocess
import atexit
import time
import requests
from pymongo import MongoClient

WEKAN_URL = 'http://84.54.57.22:2000'

def open_tunnel():
    ssh_process = subprocess.Popen(
        ['ssh', '-L', '27017:localhost:27017', 'myfirstvps', '-N'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    atexit.register(lambda: ssh_process.terminate())
    time.sleep(2)
    return ssh_process

def close_tunnel(ssh_process):
    ssh_process.terminate()
    ssh_process.wait(timeout=5)

def connect_to_mongo():
    client = MongoClient()
    db = client['wekan']
    return client, db

def get_board_id(board_title):
    client, db = connect_to_mongo()
    collection = db['boards']
    query = {'title': board_title}
    projection = {'_id': 1}
    document = collection.find_one(query, projection)
    client.close()
    return document['_id']

def get_list_id(board_title, list_title):
    client, db = connect_to_mongo()
    collection = db['lists']
    board_id = get_board_id(board_title)
    query = {'title': list_title, 'boardId': board_id}
    projection = {'_id': 1}
    document = collection.find_one(query, projection)
    client.close()
    return document['_id']

def get_token():
    auth_url = f'{WEKAN_URL}/users/login'
    auth_data = {'username': 'agorbov', 'password': 'Sven159357258'}
    response = requests.post(auth_url, data=auth_data).text
    return json.loads(response)['token']

def post_card(title, board_name, list_name, token):
    board_id = get_board_id(board_name)
    list_id = get_list_id(board_name, list_name)
    swimlane_ids = {'work': 'xbct7XafyWxqGhhWq', 'home': 'Qh75JghWz3eyAhY9K'}
    post_the_card_url = (
        f'{WEKAN_URL}/api/'
        f'boards/{board_id}/'
        f'lists/{list_id}/cards'
    )
    headers = {
        'Authorization': f'Bearer {token}'
    }
    request_data = {
        'title': title,
        'description': '',
        'authorId': 'YHrRysNZnbE5eEfrh',
        'swimlaneId': f"{swimlane_ids[board_name]}"
    }
    response = requests.post(post_the_card_url, headers=headers, data=request_data)
    response = json.loads(response.text)
    return response['_id']