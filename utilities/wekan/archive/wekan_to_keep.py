import sys
import os
from pymongo import MongoClient, ASCENDING
import pyperclip
import path_depended.utilities.wekan.get_id as get_id

board_title = sys.argv[1]
chosen_lists = {
    'home': ['Новые', 'Сейчас', 'Танечке', 'Завтра', 'На очереди'],
    'work': ['Новые', 'Завтра', 'Сегодня', 'Архив']}
db = MongoClient('mongodb://172.29.1.9:27017/')['wekan']
cards = db['cards']

res = list()
for list_name in chosen_lists[board_title]:
    res.append(list_name.upper() + ':')
    list_id = get_id.by_title_and_board('lists', list_name, board_title)
    query = {"listId": list_id, "archived": False}
    documents = cards.find(query, {"title": 1, "_id": 0}).sort("sort", ASCENDING)
    titles = [doc["title"] for doc in documents]
    res.extend(titles)
    res.append(str())

res = '\n'.join(res)
pyperclip.copy(res)
keep_ids = {
    'work': '1ra6xZ9Pj4AGSbwRq53u8Psp13hY4AjUonIfSHerxCUh-EfD2tmrV6ESt-iU97EPf',
    'home': '1K-GtPwkPXnBsfUFstsISdI_OoQK7AU-YxX3psgDzcCbPokGkN_VSqE55CUSVkehO9GhJgQ'}
os.system(f"google-chrome --new-window 'https://keep.google.com/#NOTE/{keep_ids[board_title]}'")