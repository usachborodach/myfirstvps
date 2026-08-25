import yaml
from common import connect_to_mongo

CHOSEN_BOARDS = ['work', 'home']

def main():
    client, db = connect_to_mongo()
    boards_data = get_boards_data(db) 
    lists_data = get_lists_data(db)
    structure = build_structure(boards_data, lists_data)
    structure = count_cards(db, structure)
    structure = restrict_structure(structure)
    structure = hide_some_data(structure)
    print_as_yaml(structure)
    client.close()
    input('Пауза')

def hide_some_data(structure):
    del structure['work']['Дейлик']
    return structure

def restrict_structure(structure):
    res = dict()
    for board, lists in structure.items():
       res[board] = dict()
       for list_data in lists:
           res[board][list_data['title']] = list_data['cards_count']
    return res

def count_cards(db, structure):
    collection = db['cards']
    query = {'archived': False}
    projection = {'listId': 1}
    cursor = collection.find(query, projection)
    docs = list(cursor)
    for board, lists in structure.items():
        for index, list_data in enumerate(lists):
            structure[board][index]['cards_count'] = 0
            for doc in docs:
                if doc['listId'] == structure[board][index]['_id']:
                    structure[board][index]['cards_count'] += 1
    return structure

def print_as_yaml(data):
    yaml_str = yaml.safe_dump(
        data, 
        allow_unicode=True, 
        sort_keys=False)
    print(yaml_str)

def build_structure(boards_data, lists_data):
    structure = dict()
    for board_title in CHOSEN_BOARDS:
        structure[board_title] = list()
        for list_data in lists_data:
            if list_data['boardId'] == get_board_id(boards_data, board_title):
                structure[board_title].append(list_data)
        structure[board_title] = sorted(structure[board_title], key=lambda x: x['sort'])
    return structure

def get_board_id(boards_data, board_title):
    for board in boards_data:
        if board['title'] == board_title:
            return board['_id']

def get_boards_data(db):
    collection = db['boards']
    query = {"archived": False}
    projection = {"title": 1}
    cursor = collection.find(query, projection)
    docs = list(cursor)
    return docs

def get_lists_data(db):
    collection = db['lists']
    query = {"archived": False}
    projection = {"title": 1, "boardId": 1, "sort": 1}
    cursor = collection.find(query, projection)
    docs = list(cursor)
    return docs

if __name__ == "__main__":
    main()