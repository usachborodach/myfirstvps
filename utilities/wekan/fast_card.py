import sys
import common

def main():
    check_arguments()
    ssh_process = common.open_tunnel()
    client, db = common.connect_to_mongo()
    card_id = post_card()
    min_sort_num = get_min_sort_num(db)
    set_first_id(db, card_id, min_sort_num)
    client.close()
    common.close_tunnel(ssh_process)

def set_first_id(db, card_id, min_sort_num):
    min_sort_num -= 1
    collection = db['cards']
    query = {'_id': card_id}
    operation = {'$set': {'sort': min_sort_num}}
    collection.update_one(query, operation)

def get_min_sort_num(db):
    collection = db['cards']
    list_id = common.ids['lists']['work']['Сегодня']
    query = {'listId': list_id}
    projection = {'_id': 0, 'sort': 1}
    documents = collection.find(query, projection)
    sorts = list()
    for document in documents:
        sorts.append(document['sort'])
    return min(sorts)

def check_arguments():
    if len(sys.argv) != 2:
        print(f'Wrong number of arguments ({len(sys.argv)}). Terminated')
        exit()

def post_card():
    card_text = sys.argv[1]
    token = common.get_token()
    card_id = common.post_card(card_text, 'work', 'Сегодня', token)
    print(f'Card posted: {card_text}')
    return card_id

if __name__ == '__main__':
    main()