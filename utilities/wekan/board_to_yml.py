import yaml
import common

board_title = 'work'
lists_to_exclude = ['Дейлик']

def main():
    client, db = common.connect_to_mongo()
    board_id = common.get_board_id(db, board_title)
    lists_data = get_lists_data(db, board_id)
    cards_data = get_cards_data(db, board_id)
    structure = build_structure(lists_data, cards_data)
    structure = exclude(structure, lists_to_exclude)
    dump_to_yaml(structure)
    client.close()

def exclude(structure, lists_to_exclude):
    for list_title in lists_to_exclude:
        del structure[list_title]
    return structure

def dump_to_yaml(structure):
    file_name = f'{board_title}_board_export.yml'
    with open(file_name, 'w') as fp:
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
    cursor = collection.find(query, projection).sort({'sort': 1})
    docs = list(cursor)
    lists_dict = dict()
    for item in docs:
        lists_dict[item['_id']] = item['title']
    return lists_dict

if __name__ == '__main__':
    main()