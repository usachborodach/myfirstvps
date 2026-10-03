import yaml
import common
from datetime import datetime

now = datetime.now()
formatted_now = now.strftime("%Y-%m-%d-%H-%M")

BOARDS = ['work', 'home']
OUTPUT_FILE_PATH = f'/home/user/Downloads/wekan_export_{formatted_now}.yml'

def main():
    tunnel = common.open_tunnel()
    client, db = common.connect_to_mongo()
    res = dict()
    for board_title in BOARDS:
        board_id = common.get_board_id(board_title)
        lists_data = get_lists_data(db, board_id)
        cards_data = get_cards_data(db, board_id)
        structure = build_structure(lists_data, cards_data)
        res[board_title] = structure
    dump_to_yaml(res)
    client.close()
    common.close_tunnel(tunnel)

def dump_to_yaml(structure):
    with open(OUTPUT_FILE_PATH, 'w') as fp:
        yaml.safe_dump(structure, fp, allow_unicode=True, sort_keys=False, width=10000, default_style='"')

def build_structure(lists_data, cards_data):
    structure = dict()
    for list_title in lists_data.values():
        structure[list_title] = list()
    for card in cards_data:
        list_title = lists_data[card['listId']]
        structure[list_title].append(card['title'])
    return structure

def get_cards_data(db, board_id):
    collection = db['cards']
    query = {'archived': False, 'boardId': board_id}
    projection = {'title': 1, 'listId': 1}
    cursor = collection.find(query, projection).sort([('sort', 1)])
    docs = list(cursor)
    return docs

def get_lists_data(db, board_id):
    collection = db['lists']
    query = {'archived': False, 'boardId': board_id}
    projection = {'title': 1}
    cursor = collection.find(query, projection).sort('sort')
    docs = list(cursor)
    lists_dict = dict()
    for item in docs:
        lists_dict[item['_id']] = item['title']
    return lists_dict

if __name__ == '__main__':
    main()