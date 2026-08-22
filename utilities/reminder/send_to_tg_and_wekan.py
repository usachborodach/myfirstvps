import os
import sys
import csv
import logger

base_path = os.path.dirname(__file__)
wekan_path = f'{base_path}/../..'
sys.path.append(wekan_path)
import wekan

def send_to_tg_and_wekan(index):
    reminders = csv.load()
    reminder = reminders[index]
    text_with_newlines = reminder['text'].replace('\\n', '\n')
    token = wekan.common.get_token()
    wekan.common.post_card(f"⏰ {text_with_newlines}", reminder['board'], token)
    reminders[index]['sended'] = '1'
    logger.log_debug(f"send_to_wekan ({reminder['text']}) function doned successfully")
    csv.dump(reminders)
