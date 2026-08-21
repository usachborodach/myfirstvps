import json
import requests

auth_url = f'http://172.29.1.9:2000/users/login'
auth_data = {'username': 'agorbov', 'password': 'Sven159357258'}
response = requests.post(auth_url, data=auth_data).text
wekan_token = json.loads(response)['token']

def post_card(task_text, board_name):
    board_ids = {'work': '6nEeTCXHcdq3GaqoT', 'home': 'eyZsGfRcPAysgBbB3'}
    list_ids = {'work': 'WwR4yf6LbzKgnhaLx', 'home': 'uj8XTX37dMJT7SByr'}
    swimlane_ids = {'work': 'xbct7XafyWxqGhhWq', 'home': 'Qh75JghWz3eyAhY9K'}
    post_the_card_url = (
        f'http://172.29.1.9:2000/api/'
        f'boards/{board_ids[board_name]}/'
        f'lists/{list_ids[board_name]}/cards')
    headers = {'Authorization': f'Bearer {wekan_token}'}
    request_data = {
        'title': f'{task_text}',
        'description': '',
        'authorId': 'YHrRysNZnbE5eEfrh',
        'swimlaneId': f"{swimlane_ids[board_name]}" }
    requests.post(post_the_card_url, headers=headers, data=request_data)