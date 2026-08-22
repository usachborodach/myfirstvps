import os
import sys
import csv
import logger

base_path = os.path.dirname(__file__)
wekan_path = f'{base_path}/../wekan'
sys.path.append(wekan_path)
from common import post_card

def send_to_tg_and_wekan(index):
    reminders = csv.load()
    reminder = reminders[index]
    text_with_newlines = reminder['text'].replace('\\n', '\n')
    post_card(f"⏰ {text_with_newlines}", reminder['board'])
    reminders[index]['sended'] = '1'
    logger.log_debug(f"send_to_wekan ({reminder['text']}) function doned successfully")
    csv.dump(reminders)
