import requests
from common import WEKAN_URL

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